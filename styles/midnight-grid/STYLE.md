# 午夜网格（Midnight Grid）

id: midnight-grid
适合：科技讲解、AI 和软件话题、图表、流程。
气质：深藏青、安静的点阵网格，由一抹干净的蓝来说话。
参考作品：styles/midnight-grid/index.html（12 s，循环）
画廊视频：gallery/videos/midnight-grid.mp4

## 配色 (hex)
- 底色：#0B1220
- 圆点：#1E2A44（40 px 网格上的 2 px 圆点）
- 面板：#111A2E，2 px 边框 #22304D（连线 3 px）
- 文字：#E8EDF7
- 弱化文字：#8C98B3
- 强调色：#3D8BFF（唯一的蓝，只用在当前激活的东西上）

## 字体
- 展示字：Inter 700，字距 -0.03em
- 标签：Inter 500，28 px
- 代码或数字：JetBrains Mono 500
- 字体链接（粘贴到 <head>；所有字体均免费）：
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500&display=swap">
  （参考作品只用 Inter，所以只链接了 Inter）
- 中文文字用 Noto Sans SC（无衬线），从 Google Fonts 引入，因为拉丁字体没有中文字形：`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@500;700&display=swap">`

## 缓动 (数值)
- 落定：power3.out，0.5 s（15 帧）
- 移动：power3.inOut，0.8 s
- 连一条线：power2.inOut，0.6 s
- 离场：power2.in，0.3 s
- 错开：0.05 s

## 动效规则
- 图表逐个节点搭建。画一条线，然后下一个节点落下。
- 当前激活的节点拿到蓝色。旧节点回到弱化色。
- 镜头像平稳的幻灯片一样在网格上平移，绝不甩镜。

## 标志动作
- 每条连线描画时，一个蓝色脉冲骑在线端，然后把蓝色交给它抵达的节点。
- 节点从输入一侧擦入并短距离滑动落下；标签在 0.1 s 后透过遮罩升起。
- 镜头一次停留一个节点间距；平移途中点阵网格稍微滞后，然后落回网格对齐。
- 结尾流程倒放：节点倒序离场，连线缩回它们的源头。

## 网格
点阵网格 40 px。每个方框都吸附到网格上。安全边距 96 px。

## 带素材
- 把截图或片段放进节点面板：同样的 #111A2E 填充、1 px #22304D 边框、16 px 圆角，吸附到网格。
- 让素材保持平静、略暗，让蓝色强调色依然胜出。不要加偏紫或偏青的调色。
- 当前激活的素材面板拿到蓝色边框。其他保持弱化。
- 用与节点相同的擦入方式显露素材。绝不放进漂浮的玻璃卡片。

## 禁用清单
- 辉光、泛光、镜头光晕、霓虹边
- 紫到蓝的渐变
- 带模糊的玻璃卡片
- 假的 HUD 圆环、假时间码、角落标签
