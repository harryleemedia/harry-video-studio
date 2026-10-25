#!/usr/bin/env bash
# new_project.sh：新建一个 HyperFrames 项目。
# 用法：bash scripts/new_project.sh <dir> [16x9|9x16] [seconds] [style id]
# 如果给的风格 id 带参考作品（styles/<id>/index.html），项目会从这份作品的副本开始，
# 你只需改文字、颜色和节奏，不必从零做起。
set -e
HERE=$(cd "$(dirname "$0")/.." && pwd)
DIR=${1:?用法：new_project.sh <dir> [16x9|9x16] [seconds] [style id]}
FMT=${2:-16x9}; SEC=${3:-9}; STYLE=${4:-}
if [ -e "$DIR/index.html" ]; then echo "$DIR 里已经有 index.html。请换一个新文件夹。"; exit 1; fi
mkdir -p "$DIR/media"
cp "$HERE/templates/motion/"{index.html,studio.js,hyperframes.json,meta.json} "$DIR/"
if [ -n "$STYLE" ]; then
  [ -f "$HERE/styles/$STYLE/STYLE.md" ] || { echo "没有叫 $STYLE 的风格。请在 $HERE/styles/ 里查看。"; exit 1; }
  cp "$HERE/styles/$STYLE/STYLE.md" "$DIR/STYLE.md"
  if [ -f "$HERE/styles/$STYLE/index.html" ]; then
    cp "$HERE/styles/$STYLE/index.html" "$DIR/index.html"
    if [ -f "$HERE/styles/$STYLE/studio.js" ]; then cp "$HERE/styles/$STYLE/studio.js" "$DIR/studio.js"
    elif ! grep -q 'studio.js' "$DIR/index.html"; then rm -f "$DIR/studio.js"; fi
    PW=$(grep -oE 'data-width="[0-9]+"' "$DIR/index.html" | head -1 | grep -oE '[0-9]+')
    PH=$(grep -oE 'data-height="[0-9]+"' "$DIR/index.html" | head -1 | grep -oE '[0-9]+')
    PD=$(grep -oE 'data-duration="[0-9.]+"' "$DIR/index.html" | head -1 | grep -oE '[0-9.]+')
    if [ "$FMT" = 9x16 ]; then WW=1080; WH=1920; else WW=1920; WH=1080; fi
    echo "新项目：${DIR}，从 $STYLE 的参考作品开始（${PW} x ${PH}，${PD} 秒）。"
    if [ "$PW" != "$WW" ] || [ "$PH" != "$WH" ]; then
      echo "警告：你要的是 $WW x ${WH}，但这份作品是 $PW x ${PH}。请按 $WW x $WH 重新排版画面"
      echo "      （改 data-width/data-height、viewport 和页面尺寸，再把所有元素重新摆放）。绝不能直接裁切。"
    fi
    if [ "$PD" != "$SEC" ] && [ "$PD" != "$SEC.0" ]; then
      echo "警告：你要的是 $SEC 秒，但这份作品是 $PD 秒。请修改 data-duration，并重新安排各个节拍的时间。"
    fi
    exit 0
  fi
fi
if [ "$FMT" = 9x16 ]; then W=1080; H=1920; else W=1920; H=1080; fi
# 在模板里设置尺寸和时长
sed -i.bak -e "s/width=1920, height=1080/width=$W, height=$H/" \
  -e "s/width: 1920px; height: 1080px/width: ${W}px; height: ${H}px/g" \
  -e "s/data-duration=\"9\"/data-duration=\"$SEC\"/" \
  -e "s/data-width=\"1920\" data-height=\"1080\"/data-width=\"$W\" data-height=\"$H\"/" "$DIR/index.html"
rm -f "$DIR/index.html.bak"
echo "新项目：${DIR}（$W x ${H}，$SEC 秒）。编辑 $DIR/index.html，然后运行：bash $HERE/scripts/stills.sh $DIR"
