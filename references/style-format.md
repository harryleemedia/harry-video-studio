# 风格怎么写

风格画廊里的每种风格都是 `styles/<id>/` 下的一个文件夹：

- `STYLE.md` 规范（必有）。格式见下。控制在大约 80 行以内。
- `index.html` 用这种风格做的完整作品（如果有）。复制它作为起点。
- `studio.js` 仅当该作品用到单一时钟辅助脚本时才有。

根据用户参考新建的风格也用同样的格式，保存为 `styles/<new-id>/STYLE.md`。

## STYLE.md 格式

```
# <中文名>（<English name>）

id: <id>
适合：<3 到 6 种视频>
气质：<一句话>
参考作品：styles/<id>/index.html（<时长> 秒，<循环或不循环>）   或   无，只有规范
画廊视频：gallery/videos/<id>.mp4

## 配色 (hex)
- 底色：#......
- 墨色：#......
- ……（每种颜色都要命名；标出唯一的强调色）

## 字体
- 标题：<字体> <字重>，字距 <em>，行高 <n>
- 标签：<字体> <字重>，<px>
- 中文：Noto Sans SC（无衬线）或 Noto Serif SC（衬线），按拉丁字体的风格选
- 字体链接（贴进 <head>；所有字体都免费）：
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=...&display=swap">

## 缓动 (数值)
- 落定：<ease>，<秒>
- 离开：<ease>，<秒>
- 移动：<ease>，<秒>
- 错开：<秒>

## 动效规则
- <4 到 8 条，让动效有这个风格的感觉>

## 标志动作
- <2 到 4 个让人一眼认出的动作>

## 构图
- <网格、边距、主体放哪、画面填多满>

## 带素材
- <真实照片或片段怎么放进这个风格：遮罩、调色、取景；人物默认用 assets/me/ 里 Harry 的素材>

## 禁用清单
- <会破坏这个风格的东西>
```

标题行和段落标题都用上面的中文写法，和 `styles/*/STYLE.md` 保持一致；H1 写中文名，后面括号里保留英文原名。

## 字体规则（所有风格）
- 只用免费字体：Google Fonts，或渲染时从 Fontshare 官方链接加载的 Fontshare 字体。
- 只要加了任何字体 `<link>`，就把作品用到的**每个**字体都链接上（这时 HyperFrames 会跳过它自己的字体加载）。
- 中文文字要链接 Noto Sans SC 或 Noto Serif SC（Switzer 和 Inter 没有中文字形）。
- 绝不附带字体文件。绝不用付费字体。
