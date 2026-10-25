# 海报爆破（Poster Pop）

id: poster-pop
适合：开头钩子、Shorts、大胆主张、倒计时、“3 件事”清单。
气质：一张响亮的演出海报。巨大的窄体字、平涂色、硬切。
参考作品：styles/poster-pop/index.html（12 s，循环）
画廊视频：gallery/videos/poster-pop.mp4

## 配色 (hex)
- 底色：#FFD400（黄）
- 墨色：#111111
- 纸白：#FFFFFF（用于卡片和镂空文字）
- 强调色：黄底上的 #111111 就是强调色。没有其他颜色。

## 字体
- 展示字：League Gothic，全大写，字距 0.01em，行高 0.85
- 主词：画面高度的 50% 到 90%
- 辅助字：Archivo Black，40 px 或更大
- 字体链接（粘贴到 <head>；所有字体均免费）：
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=League+Gothic&family=Archivo+Black&display=swap">
- 中文文字用 Noto Sans SC（无衬线），从 Google Fonts 引入，因为拉丁字体没有中文字形：`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@900&display=swap">`

## 缓动 (数值)
- 砸入：power4.out，0.2 s
- 缩放冲击：在拍上 1.0 到 1.06 再回 1.0。0.05 s 内放大，0.4 s 内回落（sine.inOut）。回得更快会看起来像闪光。
- 离场：power3.in，0.2 s
- 每 0.5 到 1.0 s 切一次

## 动效规则
- 每拍一个词或数字。在拍上切。
- 文字从画面外砸入，戛然停住。
- 用满整个画面。故意让字母被边缘裁掉。

## 标志动作
- 大到装不下海报的词：主词和数字占画面高度的 80% 到 150%，被两条边裁掉。
- 字母砸入：字母一个接一个到达，间隔 0.033 s，戛然停住。拉链版本让奇数位字母从上方来、偶数位字母从下方来。
- 底色翻转：一次硬切交换黄色底和墨色，让文字变成墨底黄字。
- 纸卡：一张白卡横砸过巨大的数字，2 帧后卡上的 Archivo Black 词从卡片边缘内升起。
- 落地震动：一个词砸中时整张海报下沉 18 px，0.15 s 内回稳。

## 网格
主词没有边距。辅助文字边距 64 px。

## 带素材
- 照片和片段放在纸卡或硬边矩形遮罩里。不要圆角。
- 调成高对比黑白，让黄色始终是唯一的颜色。
- 像切词一样在拍上切素材。绝不淡入。

## 禁用清单
- 渐变、阴影、辉光
- 小字
- 屏幕上超过 3 个词
- 柔和缓慢的淡化
