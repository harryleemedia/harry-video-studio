"""storyboard.py：在花任何钱之前，展示素材模式的计划和费用。

用法：python3 scripts/storyboard.py <storyboard.json>

storyboard.json（由 Claude 编写；参见 examples/storyboard.json）：
  {"title": "...", "format": "16:9", "seconds": 12,
   "shots": [{"time": "0.0-3.0", "graphic": "画面做什么",
              "asset": {"kind": "code"}},                                   # 纯代码，免费
             {"time": "3.0-8.0", "graphic": "...",
              "asset": {"kind": "user_photo", "path": "media/me.jpg"}},     # 对方的照片，免费
             {"time": "...", "graphic": "...",
              "asset": {"kind": "user_clip", "path": "media/demo.mp4"}},    # 对方的视频片段，免费
             {"time": "...", "graphic": "...",
              "asset": {"kind": "generate", "from": "media/me.jpg", "model": "seedance-2.0",
                        "prompt": "...", "duration": 5, "resolution": "720p"}}]}   # 花费 credit
打印一张表、每个 'generate' 镜头的 credit 估价和总计，并写出 storyboard.md。
它从不生成任何东西。"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sb = json.load(open(sys.argv[1], encoding='utf-8'))
root = os.path.dirname(os.path.abspath(sys.argv[1]))
rows, total, unknown, sources, missing = [], 0.0, 0, set(), []
for n, s in enumerate(sb['shots'], 1):
    a = s.get('asset', {'kind': 'code'})
    kind = a.get('kind', 'code')
    cost = '0'
    if kind in ('user_photo', 'user_clip'):
        p = a.get('path', '')
        if not os.path.exists(os.path.join(root, p)) and not os.path.exists(p):
            missing.append(p)
        what = f"你的{'照片' if kind == 'user_photo' else '视频片段'}：{os.path.basename(p)}"
    elif kind == 'generate':
        frm = a.get('from')
        what = (f"Higgsfield {a.get('model', 'seedance-2.0')} 片段，"
                + (f"由 {os.path.basename(frm)} 生成" if frm else '由文字生成') + f"，{a.get('duration', 5)} 秒，"
                f"{a.get('resolution', '720p')}。提示词：\"{a.get('prompt', '')}\"")
        cmd = [sys.executable, os.path.join(HERE, 'higgsfield.py'), 'estimate', '--model', a.get('model', 'seedance-2.0'),
               '--duration', str(a.get('duration', 5)), '--resolution', a.get('resolution', '720p'),
               '--prompt', a.get('prompt', '')]
        if not frm:
            cmd.append('--text')
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=root)
        try:
            est = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            est = {'credits': None, 'source': (r.stderr or r.stdout)[-200:]}
        sources.add(est['source'])
        if est['credits'] is None:
            cost, unknown = '?', unknown + 1
        else:
            cost = f"{est['credits']:g}"
            total += est['credits']
    else:
        what = '纯代码（无素材）'
    rows.append((n, s.get('time', ''), s.get('graphic', ''), what, cost))

gen = sum(1 for s in sb['shots'] if s.get('asset', {}).get('kind') == 'generate')
lines = [f"# 分镜：{sb.get('title', '未命名')}", '',
         f"{sb.get('format', '16:9')}，{sb.get('seconds', '?')} 秒。还没有生成任何东西，也没有花任何 credit。", '',
         '| 镜头 | 时间（秒） | 画面做什么 | 素材 | Credit |', '|---|---|---|---|---|']
lines += [f'| {n} | {t} | {g} | {w} | {c} |' for n, t, g, w, c in rows]
lines.append('')
if gen:
    tot = f'{total:g}' + (f' + {unknown} 个未知' if unknown else '')
    lines.append(f"生成 {gen} 个片段，总计约 {tot} credit"
                 f"（{'；'.join(sorted(sources))}）。失败的任务不收费。")
    lines.append('')
    lines.append('回复 "yes" 就开始生成。回复其他内容，我会先修改计划。')
else:
    lines.append('这个计划里没有 AI 片段，所以花费 0 credit。')
if missing:
    lines.append('')
    lines.append('缺少文件：' + '、'.join(missing))
md = '\n'.join(lines)
open(os.path.join(root, 'storyboard.md'), 'w', encoding='utf-8').write(md + '\n')
print(md)
