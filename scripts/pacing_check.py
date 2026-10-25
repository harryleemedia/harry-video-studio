"""pacing_check.py：第 5 招的第二部分。从渲染好的视频像素里测量节奏。

用法：python3 scripts/pacing_check.py <video.mp4> [--loop] [--max-gap 1.0] [--min-hold 0.3] [--end-hold 0]

检查项：
  1. 没有死寂空档：至少每 --max-gap 秒就有肉眼可见的变化。
     一次"变化"指：0.1 秒的一步里，超过 0.4% 的像素变化超过 14 级。
  2. 没有闪烁：两个硬切之间没有短于 --min-hold 秒的镜头，
     也没有在 --min-hold 秒内冒出来又消失的元素。
写出 <video>-contact.jpg（从 0 秒起每秒一帧，从左到右）和 <video>-pacing.json。
什么算变化：大的东西在动。小标签滑动或缓慢的颜色渐变可能不算，
所以在循环接缝附近，每秒都要保持一个大动作。快于约每秒 3 次的闪动会被看成闪烁。
退出码 0 = 通过，1 = 不通过。"""
import argparse, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _media import probe, gray_frames, diff_stats

ap = argparse.ArgumentParser(description='从视频像素测量节奏')
ap.add_argument('video', help='要检查的 mp4')
ap.add_argument('--max-gap', type=float, default=1.0, help='允许的最长无变化时间（秒）')
ap.add_argument('--min-hold', type=float, default=0.3, help='镜头或元素最短停留时间（秒）')
ap.add_argument('--end-hold', type=float, default=0.0, help='允许结尾静止这么久（秒）')
ap.add_argument('--loop', action='store_true', help='循环视频：同时测量跨越循环点的空档')
a = ap.parse_args()
info = probe(a.video)
dur = info['dur']

# 1. 死寂空档，每秒 10 步
f10, w, h = gray_frames(a.video, 10, 240)
events = []
for i in range(1, len(f10)):
    _, moved = diff_stats(f10[i - 1], f10[i])
    if moved > 0.004:
        events.append(round(i / 10, 2))
pts = [0.0] + events + [round(dur, 2)]
gaps = [(pts[i], pts[i + 1], round(pts[i + 1] - pts[i], 2)) for i in range(len(pts) - 1)]
if a.loop and len(pts) > 2:   # 结尾的静止时间会直接接上开头的静止时间
    wrap = round((pts[-1] - pts[-2]) + (pts[1] - pts[0]), 2)
    gaps.append((pts[-2], pts[1], wrap))
dead = [g for g in gaps if g[2] > a.max_gap + 0.05]
if a.end_hold:
    dead = [g for g in dead if not (g[1] >= dur - 0.05 and g[2] <= a.end_hold + 0.05)]

# 2. 闪烁，每秒 30 步
f30, _, _ = gray_frames(a.video, 30, 160)
k = max(1, int(round(a.min_hold / 2 * 30)))   # 向前后各看这么多帧
cuts, flashes = [], []
for i in range(1, len(f30)):
    _, moved = diff_stats(f30[i - 1], f30[i], 30)
    if moved > 0.35:
        cuts.append(i / 30)
for i in range(k, len(f30) - k, 2):
    _, ac = diff_stats(f30[i - k], f30[i], 30)
    _, ab = diff_stats(f30[i - k], f30[i + k], 30)
    if ac > 0.01 and ab < 0.25 * ac:
        flashes.append(round(i / 30, 2))
shots = [0.0] + cuts + [dur]
short_shots = [(round(shots[i], 2), round(shots[i + 1], 2)) for i in range(len(shots) - 1)
               if shots[i + 1] - shots[i] < a.min_hold - 0.01]
# 合并相邻的闪烁帧
merged = []
for t in flashes:
    if merged and t - merged[-1][1] <= 0.1:
        merged[-1][1] = t
    else:
        merged.append([t, t])

# 总览图，每秒一帧
base = os.path.splitext(a.video)[0]
cols = 6 if info['w'] >= info['h'] else 8
rows = max(1, int((dur + cols - 1) // cols))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a.video, '-vf',
                f'fps=1:round=down,scale={320 if info["w"] >= info["h"] else 180}:-2,tile={cols}x{rows}:padding=8:margin=8:color=white',
                '-frames:v', '1', '-q:v', '4', base + '-contact.jpg'], check=False)

rep = {'video': a.video, 'duration': round(dur, 2), 'change_steps': len(events),
       'longest_gap_s': max(g[2] for g in gaps), 'dead_gaps': dead,
       'hard_cuts': [round(c, 2) for c in cuts], 'too_short_shots': short_shots,
       'flashes': [m for m in merged], 'pass': not dead and not short_shots and not merged}
json.dump(rep, open(base + '-pacing.json', 'w'), indent=1)
print(f"节奏：最长空档 {rep['longest_gap_s']} 秒（上限 {a.max_gap}），{len(events)} 个变化步，"
      f"{len(cuts)} 个硬切")
for g in dead:
    print(f"  FAIL 死寂空档 {g[0]} 到 {g[1]} 秒（{g[2]} 秒内什么都没动）")
for s in short_shots:
    print(f"  FAIL 镜头 {s[0]} 到 {s[1]} 秒，短于 {a.min_hold} 秒")
for m in merged:
    print(f"  FAIL 大约 {m[0]} 到 {m[1]} 秒有东西冒出来又消失（停留不到 {a.min_hold} 秒）")
print('PASS' if rep['pass'] else 'FAIL', '| 总览图：', base + '-contact.jpg')
sys.exit(0 if rep['pass'] else 1)
