"""loop_check.py：第 4 招。证明循环是无缝的。

用法：python3 scripts/loop_check.py <video.mp4> [--project <dir>]

测试 A（带 --project 时）：用 HyperFrames 渲染 t = 0 和 t = 结尾 两帧，
  逐像素比较。两帧必须是同一张画面。
测试 B（总是做）：比较视频最后一帧和第一帧。这一跳不能比两帧之间的正常变化大，
  这样视频重复播放时就看不出接缝。
退出码 0 = 通过，1 = 不通过。"""
import argparse, os, re, shutil, subprocess, sys, tempfile, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _media import probe, gray_frames, diff_stats

ap = argparse.ArgumentParser(description='证明循环是无缝的')
ap.add_argument('video', help='要检查的 mp4')
ap.add_argument('--project', help='项目文件夹；给了就同时做测试 A')
a = ap.parse_args()
ok = True

if a.project:
    html = open(os.path.join(a.project, 'index.html')).read()
    D = float(re.search(r'data-duration="([\d.]+)"', html).group(1))
    tmp = tempfile.mkdtemp()
    # 用一份关掉时钟回绕的副本来测，这样结尾那帧真的是在 t = 结尾 时画出来的
    proj = os.path.join(tmp, 'proj')
    shutil.copytree(a.project, proj, ignore=shutil.ignore_patterns('*.mp4', 'stills', '.hyperframes', 'out'))
    page = open(os.path.join(proj, 'index.html')).read()
    page = page.replace('<head>', '<head>\n<script>window.STUDIO_NO_WRAP = true;</script>', 1)
    open(os.path.join(proj, 'index.html'), 'w').write(page)
    hf = ['npx', '--yes', 'hyperframes@' + os.environ.get('HF_VERSION', '0.8.181')]
    subprocess.run(hf + ['snapshot', proj, '--at', f'0,{D}', '--no-end', '-o', tmp],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pngs = sorted(f for f in os.listdir(tmp) if f.startswith('frame') and f.endswith('.png'))
    if len(pngs) < 2:
        print('FAIL 没能截到首尾两帧：', pngs); sys.exit(1)
    first, last = os.path.join(tmp, pngs[0]), os.path.join(tmp, pngs[-1])
    fa, w, h = gray_frames(first, None, 640)
    fb, _, _ = gray_frames(last, None, 640)
    mean, moved = diff_stats(fa[0], fb[0], 8)
    same = moved < 0.0005
    ok &= same
    print(f"A. 0 秒的帧 对比 {D} 秒的帧：{moved * 100:.3f}% 的像素不同"
          f"（平均 {mean:.2f} 级）-> {'PASS，同一张画面' if same else 'FAIL，循环没有闭合'}")

info = probe(a.video)
frames, w, h = gray_frames(a.video, None, 320)
steps = [diff_stats(frames[i - 1], frames[i])[0] for i in range(1, len(frames))]
seam = diff_stats(frames[-1], frames[0])[0]
typical = statistics.median(steps) if steps else 0
p90 = sorted(steps)[int(0.9 * (len(steps) - 1))] if steps else 0
limit = max(2.5 * typical, p90, 0.6)
seam_ok = seam <= limit
ok &= seam_ok
print(f"B. 接缝跳变（最后一帧到第一帧）{seam:.2f} 级；正常步长 {typical:.2f}，"
      f"上限 {limit:.2f} -> {'PASS，无缝' if seam_ok else 'FAIL，重复播放时会看到跳动'}")
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
