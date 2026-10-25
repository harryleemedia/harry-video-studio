# Harry 的视频工作室 1.0（基于 Claude Video 的中文版，免费技能）

用 Claude Code 做出工作室水准的动态图形。从真实视频组成的风格画廊里选一个风格，
回答 5 个问题，就能拿到你的 MP4。免费，普通 Claude Pro 套餐即可。

**下载：** [REPO LINK GOES HERE]

---

## 它是什么

技能（skill）是 Claude Code 会读取的一个文件夹，里面装着说明和工具。这个技能把 Claude 变成一个
小型动效工作室。你用大白话跟它说，它用代码写出视频，渲染成 MP4，
再通过查看画面帧来检查自己的成果。

它能做两件事：

**纯代码动态图形。** 标题、数据、图解、logo 片头、循环动画。不需要任何素材。

**带真实素材的图形。** 同样的设计，里面放进你自己的照片和视频片段。它还能用 Higgsfield AI
把一张照片变成一段会动的短片。在花掉任何一个 credit（积分）之前，它会先给你看
分镜表和花费，等你说「好」。

---

## 工作流程

**A. 选风格。** 浏览器里会打开风格画廊，共 21 种风格，每种都以真实视频播放。
把格子切换到「带素材」，就能看到放进真实素材的效果。点 **「用这个风格」**，把名字粘贴到
Claude Code。也可以粘贴 1 到 3 个你自己的参考链接或图片。

**B. 回答 5 个问题**（一条消息，每题都有默认值）：

1. 用在哪里？（YouTube 片头、Shorts 短视频、产品发布、讲解、广告）多长？【12 秒，16:9】
2. 画面上要出现哪些文字？【我根据你的主题来写】
3. 需要循环播放吗？【不需要】
4. 你的品牌：颜色、字体、logo？【用风格自带的】
5. 用真实素材吗？你自己的照片或视频片段、Higgsfield 生成的 AI 片段，还是不用（纯图形）？【不用】

**C. 制作。** 先出分镜表（每个镜头、它的时间和用到的素材），再出 3 张静帧给你确认，然后渲染，
最后做两项自动检查：节奏检查（不能有超过 1 秒的空档，任何东西在画面上停留都不少于 0.3 秒），
以及循环作品的像素检查，确认最后一帧等于第一帧。

---

## 5 个技巧

**1. 先选定一种风格，然后坚持到底。**
风格不定下来，任何 AI 都会滑向同一个默认样子（深色背景、发光、紫色渐变）。
一份风格规范会把整支作品的颜色、字体、缓动和禁用清单都固定下来。
出处：https://github.com/NovusEdge/motion-lab

**2. 真实参考胜过形容词。**
「简洁现代」毫无意义，一帧真实画面却信息量巨大。然后说清它是怎么做出来的（遮罩文字、
缓慢的镜头、长时间停留），而不只是它给人什么感觉。
去这些地方找参考：https://savee.com 、https://godly.website 、https://mobbin.com ，以及 Linear、
Apple 和 Cursor 的发布影片。
出处：https://impractical.ai/launch-videos/linear-agent

**3. 用数字写简报。**
时长用秒，颜色用 hex，缓动用数字（例如 expo.out，0.6 秒）。每个镜头只有一个主动作。
再加一份禁用清单：不要变色相的渐变，不要发光、泛光或镜头光晕，眼睛追随的东西不要用线性缓动，
不要所有东西都居中。
出处：https://aiartimind.com/how-to-make-motion-graphics-with-claude-opus-5-5/

**4. 循环：只用一个时钟，最后一帧 = 第一帧。**
所有动作都由同一个时钟驱动，这样视频的结尾就恰好是开头。然后证明它：
渲染第一帧和最后一帧，逐像素比较。只要有差异，就判定失败。
出处：https://github.com/NovusEdge/motion-lab 和 https://hyperframes.heygen.com

**5. 检查画面帧，而不是代码。**
完整渲染前，看 3 张镜头切换处的静帧。渲染完成后，做节奏检查。
出处：https://aiartimind.com/how-to-make-motion-graphics-with-claude-opus-5-5/ 和 https://github.com/NovusEdge/motion-lab

---

## 3 步安装

1. 下载文件夹，复制到 `~/.claude/skills/`
   （确保文件 `~/.claude/skills/claude-video-studio/SKILL.md` 存在）。
2. 仅在需要 AI 片段时：到 https://console.higgsfield.ai 申请 key，在项目文件夹里一个叫
   `.env` 的文件中加上这一行：
   `HIGGSFIELD_API_KEY=your_key_id:your_key_secret`
   千万不要把 key 贴进聊天。
3. 打开 Claude Code，说：**make me a motion graphic**（帮我做个动态图形）

**另外需要：** Node 22 或更新版本（https://nodejs.org）和 ffmpeg（`brew install ffmpeg`）。
不确定？Claude 会替你检查，并给你一条要运行的命令。

---

基于 HyperFrames（https://hyperframes.heygen.com）和 GSAP（https://gsap.com）构建。所有字体都免费。MIT 许可证。
