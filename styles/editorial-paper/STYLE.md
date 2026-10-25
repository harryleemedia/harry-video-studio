# 社论纸面（Editorial Paper）

id: editorial-paper
适合：数据、图表、讲解、“数字在说什么”。
气质：一张活过来的报纸图表。暖色纸张、黑色墨水、一抹蓝。
参考作品：styles/editorial-paper/index.html（10 s，循环）
画廊视频：gallery/videos/editorial-paper.mp4

## 配色 (hex)
- 底色：#FFF1E5（鲑鱼色纸）
- 墨色：#1A1A1A
- 分隔线和网格线：#E3D3C3
- 弱化文字：#6B5E55
- 强调色：#0F5499（最关键的那条线、那根柱或那个数字）

## 字体
- 标题：Playfair Display 700，字距 -0.02em
- 数字：Playfair Display 900，等宽数字
- 标签：Inter 500，26 到 32 px
- 字体链接（粘贴到 <head>；所有字体均免费）：
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700;900&display=swap">
- 中文文字：标题和数字用 Noto Serif SC（衬线），标签用 Noto Sans SC（无衬线），从 Google Fonts 引入，因为拉丁字体没有中文字形：`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&family=Noto+Sans+SC:wght@500&display=swap">`

## 缓动 (数值)
- 落定：power3.out，0.7 s（21 帧）
- 画线：power2.inOut，1.2 到 2.0 s
- 数字计数：power2.out，时长与它同步的那条线相同
- 离场：power2.in，0.4 s

## 动效规则
- 线条从左到右画出。数字同步向上计数。
- 镜头可以缩放图表（改变坐标轴），绝不晃动。
- 可以有细腻的纸张颗粒。保持静止或非常缓慢。

## 标志动作
- 一根柱子变蓝，然后长过其余柱子。它的数字同步计数。
- 坐标轴拉远以容纳领先者。网格线滑动，新的一条进入。
- 平滑的重新排名：蓝色那一行攀升，其他行紧随其后依次下移。
- 聚焦：其他柱子淡成分隔线的颜色，让蓝色那根独自突出。
- 标题在一条短墨条下透过遮罩逐词替换。

## 网格
12 栏，边距 120 px，栏间距 32 px。图表立在清晰的基线上。

## 带素材
- 照片放在网格上的硬边矩形里，不要圆角，不要阴影。
- 把照片调成偏暖、略平的色调，让它融入纸面。绝不出现纯黑。
- 上方一条细墨线，下方一行 Inter 500 弱化色的说明文字。
- 图表或数字始终是主角。照片只是辅助，最多占半个画面。

## 禁用清单
- 3D 图表、超过 3 块的饼图
- 霓虹、辉光、柱子上的渐变
- 屏幕上的来源行或小号脚注
- 多于一种强调色
