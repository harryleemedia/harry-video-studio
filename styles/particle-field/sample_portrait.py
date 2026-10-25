# 粒子人像取样器（index-media.html 用的就是它的输出）。用法：python3 sample_portrait.py <去背景人像.png> <输出.json>
# 下面的 HX/HY（头部中心 x、头顶 y）和 Y0/Y1（裁切范围）是按 assets/me/p4.png 调的；换别的人像要改这几个数。需要 Pillow。
# Offline sampler: p4.png -> 9500 portrait targets + 500 rim points (world coords), deterministic.
import sys, json, math, random, bisect, colorsys
from PIL import Image
src, outp = sys.argv[1], sys.argv[2]
S, HX, HY, TOPW = 1.42, 643, 210, -400.0   # world = ((sx-HX)*S, (sy-HY)*S + TOPW)
NT, NR = 9500, 500
im = Image.open(src).convert('RGBA')
W0, H0 = im.size
Y0, Y1 = 196, 870
STEP = 2
half = im.resize((W0 // STEP, H0 // STEP), Image.LANCZOS)
px = half.load()
def smooth(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def world(sx, sy):
    return (sx - HX) * S, (sy - HY) * S + TOPW
def feather(X, Y):
    return (1 - smooth((Y - 395) / 130)) * (1 - smooth((abs(X) - 440) / 150))
cells, cum = [], []
tot = 0.0
for y in range(Y0 // STEP, Y1 // STEP):
    for x in range(W0 // STEP):
        r, g, b, a = px[x, y]
        if a < 40: continue
        lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
        X, Y = world(x * STEP + 1, y * STEP + 1)
        w = (a / 255) * (0.13 + lum ** 1.35) * feather(X, Y)
        if w <= 0: continue
        tot += w; cells.append((x, y)); cum.append(tot)
rng = random.Random(4471)
pts = []
for k in range(NT):
    u = (k + rng.random()) / NT * tot
    j = min(bisect.bisect_left(cum, u), len(cells) - 1)
    cx, cy = cells[j]
    sx, sy = (cx + rng.random()) * STEP, (cy + rng.random()) * STEP
    r, g, b, a = px[cx, cy]
    # saturation lift 1.45x, dark pixels lifted to a dim cool grey so the suit still reads
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    r2, g2, b2 = colorsys.hls_to_rgb(h, l, min(1, s * 1.45))
    lum = 0.2126 * r2 + 0.7152 * g2 + 0.0722 * b2
    lift = 0.30 * (1 - lum) ** 2
    r3 = min(1, r2 * 1.12 + lift * 0.62); g3 = min(1, g2 * 1.12 + lift * 0.70); b3 = min(1, b2 * 1.12 + lift * 0.90)
    X, Y = world(sx, sy)
    pts.append((round(X, 1), round(Y, 1), int(r3 * 255), int(g3 * 255), int(b3 * 255)))
pts.sort(key=lambda p: (p[0], p[1]))
# rim: boundary pixels of the full-res alpha, upper part (head + shoulder tops)
A = im.split()[3].load()
edge = []
for y in range(Y0, 790):
    for x in range(1, W0 - 1):
        if A[x, y] > 128 and (A[x - 1, y] <= 128 or A[x + 1, y] <= 128 or A[x, y - 1] <= 128 or A[x, y + 1] <= 128):
            edge.append((x, y))
# keep only the outer silhouette: per angle around the neck, outermost point
CX, CY = 643, 800
best = {}
for x, y in edge:
    ang = math.atan2(y - CY, x - CX)
    if ang > -0.06 or ang < -math.pi + 0.06: continue
    key = round(ang * 1400)
    d = math.hypot(x - CX, y - CY)
    if key not in best or d > best[key][0]: best[key] = (d, x, y)
outer = [best[k] for k in sorted(best)]  # from left (-pi) to right (0)
chain = [(x, y) for d, x, y in outer]
# arc-length resample along continuous runs only
seg, L = [], 0.0
for a, b in zip(chain, chain[1:]):
    d = math.hypot(b[0] - a[0], b[1] - a[1])
    if d < 14: seg.append((a, b, L, d)); L += d
rim = []
for k in range(NR):
    u = (k + 0.5) / NR * L
    for a, b, l0, d in seg:
        if l0 + d >= u:
            f = (u - l0) / d if d else 0
            sx, sy = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
            X, Y = world(sx, sy)
            rim.append((round(X, 1), round(Y, 1))); break
print('targets', len(pts), 'rim', len(rim), 'rim length px', round(L), 'cells', len(cells))
flatT = [v for p in pts for v in p]
flatR = [v for p in rim for v in p]
with open(outp, 'w') as f:
    f.write('const PT = ' + json.dumps(flatT, separators=(',', ':')) + ';\n')
    f.write('const RIM = ' + json.dumps(flatR, separators=(',', ':')) + ';\n')
# preview
pv = Image.new('RGB', (1920, 1080), (10, 15, 28))
pp = pv.load()
for X, Y, r, g, b in pts:
    x, y = int(960 + X), int(540 + Y)
    if 0 <= x < 1920 and 0 <= y < 1080: pp[x, y] = (r, g, b)
for X, Y in rim:
    x, y = int(960 + X), int(540 + Y)
    if 0 <= x < 1920 and 0 <= y < 1080: pp[x, y] = (111, 211, 232)
pv.save(outp + '.png')
