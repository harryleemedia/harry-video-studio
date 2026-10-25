# HyperFrames：要紧的规则

HyperFrames 把一个带有暂停 GSAP 时间轴的 HTML 页面逐帧转成 MP4。
文档：https://hyperframes.heygen.com ，或在终端运行：`npx hyperframes docs gsap`、
`npx hyperframes docs compositions`、`npx hyperframes docs data-attributes`。
脚本锁定版本 0.8.181（用 `HF_VERSION` 修改）。需要 Node 22+ 和 ffmpeg。

## 约定
- 只有一个根元素：`<div id="root" data-composition-id="main" data-start="0" data-duration="9" data-width="1920" data-height="1080">`。
- 只有一条暂停的时间轴，注册为 `window.__timelines["main"] = tl`。`STUDIO.play()` 会替你完成。
- 有时间段的媒体加上 `class="clip"` 以及 `data-start` 和 `data-duration`。
  视频：`<video class="clip" src="media/x.mp4" muted playsinline data-start="2" data-duration="4" data-media-start="0.5">`。
- 渲染：`npx hyperframes render <dir> -o out.mp4 -q draft`（快速草稿）或 `-q high`（最终版）。
- 静帧：`npx hyperframes snapshot <dir> --at 0,3,6 --no-end -o stills/`。
- 检查代码：`npx hyperframes lint <dir>`。

## 必须遵守的规则（否则渲染会闪烁或每次不一样）
- 同一时间输入，同一画面输出。不用 `Math.random`（改用 `STUDIO.rng(seed)`），不用 `Date.now`，不用定时器，不用 `requestAnimationFrame` 循环。
- 随时间变化的文字，要在 render 函数或补间的 onUpdate 里改，绝不用 gsap.set 改 innerHTML。
- Canvas：在 render(t) 里根据 t 画出整帧。
- 从项目文件夹（`media/`）加载媒体。文件名保持简单。

## 字体
- 只用免费字体：Google Fonts，或渲染时从 Fontshare 官方链接加载的 Fontshare 字体
  （例如 Switzer：`https://api.fontshare.com/v2/css?f[]=switzer@400,500,600,700,800&display=swap`）。
  绝不把字体文件复制进项目。绝不用付费字体。
- 每个字体都在 `<head>` 里用 `<link>` 加载。只要加了**任何**字体链接，就要把页面用到的**每个**字体都链接上：
  这时 HyperFrames 会跳过它自己的字体加载，没链接的字体会退回成 Times。
- 中文文字需要 CJK 字体，因为 Switzer 和 Inter 没有中文字形。用 Google Fonts 的 Noto Sans SC 或 Noto Serif SC
  （`https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@700;900&display=swap`），和其他字体一样用 `<link>` 链接。
- 系统字体名会被 HyperFrames 替换："Helvetica Neue"、"Avenir"、"SF Pro" 会变成 Inter，
  "Futura" 会变成 Montserrat。请主动选一款 Google Font（Inter、Jost、Bodoni Moda、Playfair Display……）。
- 在代码里测量的文字（canvas、offsetWidth）必须在字体加载后重新测量
  （`document.fonts.ready.then(redraw)`）。`studio.js` 会替你完成。
- 渲染需要联网，因为 GSAP 和字体都从公共 CDN 加载。

## 画幅
- 16:9 是 1920 x 1080，9:16 是 1080 x 1920。每种画幅都重新排版，绝不直接裁切。
- 给剪辑软件用的透明叠加层：`--format mov` 并使用透明背景。
