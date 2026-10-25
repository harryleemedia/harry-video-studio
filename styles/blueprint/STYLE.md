# 蓝图（Blueprint）

id: blueprint
参考作品：styles/blueprint/index.html（12 s，循环）
画廊视频：gallery/videos/blueprint.mp4
适合：工作原理、产品部件、工程、分步讲解。
气质：一张自己逐线绘制出来的技术图纸。

## 配色 (hex)
- 底色：#0E3A66
- 线条：#CFE3F7（2 px 描边）
- 淡网格：#1C4D80
- 文字：#EAF3FC
- 强调色：#FFD23F（唯一的高亮：最关键的那个部件）

## 字体
- 标签：IBM Plex Mono 500，26 到 32 px，全大写，字距 0.06em
- 大数字：IBM Plex Mono 700
- 字体链接：
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;700&display=swap">
- 中文文字用 Noto Sans SC（无衬线），从 Google Fonts 引入，因为拉丁字体没有中文字形：`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@500;700&display=swap">`

## 缓动 (数值)
- 描一笔：power1.inOut，0.6 到 1.2 s（stroke-dashoffset）
- 尺寸箭头：expo.out，0.5 s
- 镜头：power2.inOut，1.0 s 平移

## 动效规则
- 一切先以描边画出，之后（如果需要）再填充。
- 标签出现时带一条引线，从部件画向标签。
- 只有强调部件填充黄色。

## 标志动作
- 辅助线先横扫整张图纸，真正的线条沿着它们描出，然后辅助线淡出。
- 爆炸视图：部件沿一条轴滑开，带小幅错开和阻尼回稳。内部部件滞后。
- 隐藏线：被包在另一个部件里的部件画成虚线，一旦露出立刻变成实线。
- 尺寸线从数字处向外生长，箭头骑在线端。
- 关键部件自下而上擦入黄色填充，它的标签变黄，镜头推近它。

## 网格
细网格 24 px，粗网格 120 px。边距 96 px。
向内 48 px 处有一道细图框，带角标、比例尺和一个空白标题栏。
网格以镜头 30% 的速度移动，形成视差。

## 带素材
- 照片不要放进图纸本身。
- 照片可以放在图纸旁边，用同样 2 px 的线画出直角边框，调成冷蓝双色调。
- 或者从照片里描出物体，然后在一笔描线上从照片切到图纸。

## 禁用清单
- 图纸内部出现照片
- 柔和阴影、辉光
- 圆润可爱的字体
- 同时出现多于一个高亮
