# 15 秒穿越 30,000 年（30,000 years in 15 seconds）

id: time-travel
适合：一个想法的历史、“过去 vs 现在”、演化故事、时间线、起源故事。
气质：史诗而温暖；一台镜头沿一条无尽的时间线穿越每个时代，每个时代都用它自己的时代风格绘制。
参考作品：styles/time-travel/index.html（17 s，不循环）
画廊视频：gallery/videos/time-travel.mp4

## 配色 (hex)
- 底色：墨色 #15120F
- 文字和时间线：象牙白 #F3EEE4（唯一永不改变的东西；它把所有时代串在一起）
- 洞穴：赭石 #C86E3C，配暖色岩石
- 陶瓶：赤陶 #B95F35，高光 #D88B5C，黑釉 #17110E
- 西洋镜（zoetrope）：黄铜 #C9A15A，配奶油色纸
- 胶片：银 #C8C8C4
- 电视：胡桃木 #4A2B18，荧光 #78C8F0
- 8 位像素：夜 #0E0B24、#2A1D5C，草 #5BBF5A，砖 #B4532A，金 #F2C14E
- 每个时代有自己的配色；象牙白是所有时代唯一共享的颜色

## 字体
- 年份标签：每个用它所在时代的字体，38 到 44 px，字距 2 到 6 px
  - 30,000 BC：Libre Baskerville · 500 BC：Tenor Sans · 1834：Bodoni Moda
  - 1895：Playfair Display 斜体 · 1951：Jost 500 · 1980：用代码画的像素字体 · 2026：JetBrains Mono
- 代码行：JetBrains Mono 400，58 px
- 屏幕上最多两个词：年份，以及最后一个时代里的代码行。
- 字体链接（粘贴到 <head>；所有字体均免费）：
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:wght@400&family=JetBrains+Mono:wght@400&family=Jost:wght@500&family=Libre+Baskerville&family=Playfair+Display:ital,wght@1,400&family=Tenor+Sans&display=swap">
- 中文文字按时代选：衬线时代（30,000 BC、1834、1895）用 Noto Serif SC（衬线），无衬线时代（500 BC、1951、2026）用 Noto Sans SC（无衬线），从 Google Fonts 引入，因为拉丁字体没有中文字形：`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400&family=Noto+Sans+SC:wght@400;500&display=swap">`

## 缓动 (数值)
- 时代穿越：power4.inOut，每次切换 0.5 s（拍前 0.24 s 到拍后 0.26 s）
- 切换前推进：power3.in，约 0.55 s
- 揭示和转向：power3.inOut，0.3 到 0.45 s
- 排队落定：expo.out，0.4 s，错开 0.035 s
- 跑步循环：每秒 1.5 步，所有时代共用一个时钟
- 每次切换的曝光冲击：0.35 s 淡出，7% 暖白

## 动效规则
- 一个跑者是每个时代的主角：同一副骨架，同一个相位时钟。只有画法改变。
- 每个时代在运动中变成下一个，按形状匹配（陶瓶变鼓，缝隙变齿孔，屏幕变电视）。
- 每次切换落在 0.5 s 的拍上。
- 年份标签骑在时间线上，镜头快速移动时带着残影拖尾。
- 处处有质感：颗粒、暗角、火光闪烁、光束里的灰尘。
- 镜头从不停下；它推进一个细节，然后顺着这个运动切换。

## 标志动作
- 匹配剪辑链：洞穴野牛到陶瓶到西洋镜到胶片到电视到像素到代码。
- 打出 `draw(frame + 1)`，然后代码把跑者画成一条象牙白线。
- 终章：七个跑者在一条倾斜的时间线上排成一排，步调一致地奔跑。

## 构图
- 全画面，一次一个时代，主角居中。
- 象牙白时间线低低地横在 y 996，每 24 px 一个刻度；年份在它上方靠左。
- 终章时间线向右上倾斜；过去小而远，现在大而近。

## 带素材
- 渲染器里 canvas 无法绘制视频帧，所以要分层：底层背景 canvas，然后每帧用 CSS（position、transform、clip-path、filter）摆放的 video 元素，再上面是一层叠加 canvas，用于颗粒、划痕、扫描线、标签和时间线。
- 把每个片段调成它所在时代的样子。1895 胶片：grayscale、sepia 0.28、contrast 1.38、blur 0.6 px、闪烁、片门晃动、划痕、灰尘。1951 电视：grayscale、sepia 0.32、hue-rotate 168 deg、saturate 0.55、contrast 1.3、弯曲扫描线、圆角、玻璃高光。
- 现代可以是一个真人全屏奔跑，然后缩成一张圆角卡片，作为第七个跑者。绝不在人脸上画图形。
- 人物默认用 Harry 本人的素材：`assets/me/p1.png`–`p5.png`（已去背景）、`assets/me/photo1.jpg`–`photo5.jpg`（原图）、`assets/me/webcam.mp4`（口播片段）、`assets/me/ai-walk.mp4`（AI 走路片段）、`assets/me/ai-turn.mp4`（AI 转身片段）。文字绝不压在他脸上。

## 禁用清单
- 所有时代用同一种字体
- 没有质感的干净扁平矢量风格
- 没有按形状或运动匹配的硬切
- 屏幕上超过两个词
- 破坏时代感的颜色（洞穴里不要霓虹，8 位像素里不要棕褐色）
