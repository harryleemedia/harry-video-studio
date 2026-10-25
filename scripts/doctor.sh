#!/usr/bin/env bash
# doctor.sh：检查本 skill 需要的工具。每缺一个工具，打印一条修复命令。
# 用法：bash scripts/doctor.sh [motion|media]
MODE=${1:-motion}
ok=1
say() { printf '%-10s %s\n' "$1" "$2"; }

if command -v node >/dev/null; then
  v=$(node -p 'process.versions.node.split(".")[0]')
  if [ "$v" -ge 22 ]; then say node "正常 ($(node -v))"; else say node "版本太旧 ($(node -v))。修复：从 https://nodejs.org 安装 Node 22 或更新版本"; ok=0; fi
else say node "缺失。修复：从 https://nodejs.org 安装 Node 22 或更新版本"; ok=0; fi

for t in ffmpeg ffprobe; do
  if command -v $t >/dev/null; then say $t 正常; else say $t "缺失。修复：brew install ffmpeg"; ok=0; fi
done

if command -v python3 >/dev/null; then say python3 "正常"; else say python3 "缺失。修复：brew install python"; ok=0; fi

if [ "$MODE" = media ]; then
  if [ -n "$HIGGSFIELD_API_KEY" ] || [ -n "$HF_API_KEY_ID" ] || grep -qs '^HIGGSFIELD_API_KEY=' .env; then
    say higgsfield "已找到密钥（不显示）"
  else
    say higgsfield "没有密钥。在这个文件夹里建一个名为 .env 的文件，只写一行：HIGGSFIELD_API_KEY=your_key_id:your_key_secret（在 https://console.higgsfield.ai 获取）。千万不要把它贴到聊天里。"
  fi
fi

[ $ok = 1 ] && echo "就绪" || { echo "请先修好上面几行，再运行一次"; exit 1; }
