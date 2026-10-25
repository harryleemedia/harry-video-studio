#!/usr/bin/env bash
# stills.sh：第 5 招。在完整渲染之前，先在镜头切换点截几张静帧。
# 用法：bash scripts/stills.sh <project dir> [时间点，逗号分隔]   例如 0,3,6
# 不给时间点时，取 0、三分之一、三分之二和结尾。
set -e
HF="npx --yes hyperframes@${HF_VERSION:-0.8.181}"
DIR=$(cd "${1:?用法：stills.sh <dir> [t1,t2,t3]}" && pwd)
D=$(grep -oE 'data-duration="[0-9.]+"' "$DIR/index.html" | head -1 | grep -oE '[0-9.]+')
AT=${2:-$(python3 -c "d=$D; print(','.join(str(round(x,2)) for x in (0, d/3, 2*d/3, d-0.05)))")}
OUT="$DIR/stills"; rm -rf "$OUT"; mkdir -p "$OUT"
$HF snapshot "$DIR" --at "$AT" --no-end -o "$OUT" >/dev/null
# 生成小尺寸副本，方便查看
for f in "$OUT"/*.png; do ffmpeg -v error -y -i "$f" -vf scale=960:-2 -q:v 7 "${f%.png}.jpg"; done
# 再拼一张小的总览图（看图工具常常拒绝打开大文件）
[ -f "$OUT/contact-sheet.jpg" ] && ffmpeg -v error -y -i "$OUT/contact-sheet.jpg" -vf scale=1400:-2 -q:v 8 "$OUT/peek.jpg"
ls "$OUT"/*.jpg
echo "逐张看这些静帧，把不对的地方改好，然后再运行 render.sh。"
