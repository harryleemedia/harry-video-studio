# Harry 的视频工作室 1.0（基于 Claude Video 的中文版）

一个免费的 Claude Code 技能，做出来的动态图形像专业工作室出品。

- **选一个风格**：风格画廊里有 21 种风格，每一种都以真实视频播放。
- **回答 5 个简短问题。**
- **拿到你的视频。** Claude 用代码搭建，先给你 3 张静帧确认，再渲染成 MP4，
  并从真实画面帧检查自己的成果。

可以是纯图形，也可以放进你自己的照片和视频片段，或者用 Higgsfield 生成的 AI 片段（它会先给你看
方案和 credit（积分）花费，等你说「好」才动手）。普通 Claude Pro 套餐即可使用。

## 3 步安装

1. 下载到技能文件夹（文件夹名必须是 `claude-video-studio`）：
   `git clone https://github.com/harryleemedia/harry-video-studio.git ~/.claude/skills/claude-video-studio`
   确保存在 `~/.claude/skills/claude-video-studio/SKILL.md`。
2. 仅在需要 AI 片段时：到 https://console.higgsfield.ai 申请 key，在项目文件夹里一个叫 `.env` 的文件中
   加一行：`HIGGSFIELD_API_KEY=your_key_id:your_key_secret`。千万不要把 key 贴进聊天。
3. 打开 Claude Code，说：**make me a motion graphic**（帮我做个动态图形）

另外需要 Node 22 或更新版本（https://nodejs.org）和 ffmpeg（`brew install ffmpeg`）。
Claude 会替你检查，缺什么就告诉你一条命令补上。

## 工作流程

**A. 选风格。** 浏览器里会打开风格画廊，每个格子都是真实视频。把工作室作品切换到
「带素材」，就能看到同一设计里放进真实素材的效果。点 **「用这个风格」**，把名字
粘贴到 Claude Code。也可以粘贴你自己的参考链接或图片。

**B. 五个问题**，放在一条消息里，每题都有默认值：

1. 用在哪里？（YouTube 片头、Shorts 短视频、产品发布、讲解、广告）多长？【12 秒，16:9】
2. 画面上要出现哪些文字？【我根据你的主题来写】
3. 需要循环播放吗？【不需要】
4. 你的品牌：颜色、字体、logo？【用风格自带的】
5. 用真实素材吗？你自己的照片或视频片段、Higgsfield 生成的 AI 片段，还是不用（纯图形）？【不用】

问题写在 `questions.md` 里，你可以自己改。

**C. 制作。** 先出分镜表（镜头、时间、素材，有 AI 片段时还有 credit 花费），
再出 3 张静帧给你确认，然后渲染，最后做节奏检查；如果是循环作品，还要做像素级循环检查。

## 21 种风格

工作室作品：`paper-world`、`ink-line`、`weather-widget`、`data-story`、`swiss-kinetic`、
`particle-field`、`growing-city`、`explainer-diagram`、`time-travel`、`editor-ui`、`motion-app-ui`、
`design-app-ui`、`audio-app-ui`。

代码风格：`swiss-grid`、`editorial-paper`、`midnight-grid`、`paper-cut`、`risograph`、`blueprint`、
`graphite-ui`、`poster-pop`。

每种风格都是 `styles/` 里的一个文件夹，里面有一个 `STYLE.md`（颜色、字体、缓动参数、动效规则、禁用清单），
大多数还附带一个可以直接起步的完整作品。随时打开风格画廊：
`python3 ~/.claude/skills/claude-video-studio/scripts/gallery.py`

## 为什么好看：5 个技巧

1. 先选定一种风格，然后坚持到底。
2. 真实参考胜过形容词。
3. 用数字写简报。
4. 循环：只用一个时钟，最后一帧必须等于第一帧。
5. 检查画面帧，而不是代码。

`references/hacks.md` 逐条解释每个技巧及其出处。

## 里面有什么

- `SKILL.md` Claude 遵循的步骤
- `gallery/` 风格画廊及其视频
- `styles/` 21 种风格
- `questions.md` 提问清单（随意修改）和 `config.json`（可选，一个 Claude 在最后提到的链接）
- `references/` 5 个技巧、动效参数、引擎规则、素材模式、如何编写风格
- `templates/` 起步页面和单一时钟辅助脚本
- `scripts/` 风格画廊、渲染、静帧、节奏检查、循环检查、分镜表、Higgsfield
- `examples/` 一份简短的简报和一份分镜表
- `assets/me/` Harry 的默认素材（照片、去背景人像、口播视频、两段 AI 片段），个人素材保留所有权利

基于 [HyperFrames](https://hyperframes.heygen.com) 和 [GSAP](https://gsap.com) 制作。所有字体都免费
（Google Fonts，以及渲染时从 Fontshare 加载的 Switzer）。

## 授权

- **代码和文档**：MIT 许可证（见 `LICENSE`），版权同时属于 Harry Lee 和原版 Claude Video 的作者。
- **Harry 本人的素材**（`assets/me/`、画廊里出现 Harry 的 8 支样片等）：**保留所有权利**，不适用 MIT，详见 `ASSETS-LICENSE.md`。
  想做你自己的版本，把 `assets/me/` 换成你的照片和视频即可。
