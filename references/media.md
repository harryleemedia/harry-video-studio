# 素材模式：图形 + 真实照片、视频片段和 AI 片段

素材模式就是放进了真实画面的动效模式。图形依然是主角，素材嵌在图形里面。

## 三类素材（从便宜到贵）
1. 用户自己的照片。免费。代码可以让照片活起来：缓慢推近、抠图与背景之间的
   视差、光线扫过、遮罩揭示。
2. 用户自己的视频片段（录屏、产品镜头、口播）。免费。
3. Higgsfield 生成的 AI 片段。消耗 credit（积分）。最适合把**一张**静态照片变成 4 到 8 秒的
   运动镜头（图生视频），或者生成没人拍过的 B-roll（文生视频）。

## 默认人物素材
当作品需要出现人物、而用户没有提供其他素材时，使用 Harry 本人在 `assets/me/` 里的素材：
- `p1.png`–`p5.png`：已去背景，1333x2000。
- `photo1.jpg`–`photo5.jpg`：原图，炭灰色影棚背景，黑色西装、白衬衫。
- `webcam.mp4`：864x1080 的口播片段，27 秒，带他本人的声音。
绝不把文字压在他的脸上。

## Higgsfield 计费顺序
Higgsfield 有两种付费方式：订阅 credit（每月发放，不用就作废）和 API credit（按量付费）。
1. 先查订阅余额：调用 Higgsfield MCP 的 `balance` 工具。
2. 订阅 credit 够这一单 → 通过 MCP 生成（`generate_video` / `generate_image`）。生成前先用
   `get_cost: true` 参数调用一次来报价（只返回 credit 花费，不提交任务）。MCP 的模型 id 与下表的 API
   端点名不同，用 `models_explore` 查。
3. 只有订阅 credit 不够这一单时，才改用 `scripts/higgsfield.py`（走 API，key 在 `.env`）。
   改走 API 之前，先告诉用户原因。
付费视频一律先展示价格，等用户明确说「好」再生成。

## Key（绝不出现在聊天里）
- 用户在 shell 里设置 `HIGGSFIELD_API_KEY=key_id:key_secret`，或者写进项目文件夹里的
  `.env` 文件。Key 在 https://console.higgsfield.ai 获取。
- `python3 scripts/higgsfield.py check` 只回答有或没有，绝不打印 key。
- 绝不让用户粘贴 key。绝不回显、记录或提交 key。`.env` 已在 `.gitignore` 里。

## API（脚本做了什么）
- Base：`https://platform.higgsfield.ai`（设置 `HIGGSFIELD_API_BASE` 可修改；文档里写的是 `https://api.higgsfield.ai`）。
- 请求头：`Authorization: Key <key_id>:<key_secret>`。
- 上传照片：`POST /files/generate-upload-url`，body 为 `{"content_type": "image/jpeg"}`，然后带上返回的请求头，
  把文件 PUT 到 `upload_url`。把 `public_url` 作为 `image_url` 使用。
- 查价，免费：`POST /estimate/<endpoint>`，body 相同。返回 `credits`。
- 提交：`POST /<endpoint>`，带 `Idempotency-Key` 请求头。返回 `status_url`。
- 轮询 `status_url`（间隔从 2 秒逐渐增加到 10 秒），直到状态为 `completed`、`failed`、`nsfw` 或 `canceled`。
  片段在 `video.url`。要下载下来；链接大约 7 天有效。失败的任务不扣费。
- 文档：https://docs.higgsfield.ai

| 本技能里的名称 | 端点 | 适合 | 时长 |
|---|---|---|---|
| seedance-2.0（默认） | `bytedance/seedance-2.0/image-to-video` 和 `/text-to-video` | 照片转片段、任何较复杂的运动、起始帧 + 结束帧 | 4 到 15 秒 |
| seedance-2.5 | `bytedance/seedance-2.5/image-to-video` 和 `/text-to-video` | 更长的单镜头 | 4 到 30 秒 |
| kling-3-turbo | `kling-video/v3.0-turbo/image-to-video` | 便宜的简单运动 | 3 到 15 秒 |

脚本会关闭生成的声音（`generate_audio: false`）。声音在剪辑里处理。

## 分镜表关卡（始终执行）
花任何钱之前：
1. 写 `storyboard.json`（参见 `examples/storyboard.json`）：每个镜头、它的时间、图形
   做什么，以及用哪种素材：`code`、`user_photo`、`user_clip` 或 `generate`（附模型、prompt、
   时长、分辨率）。
2. 运行 `python3 scripts/storyboard.py storyboard.json`。它会打印表格和 credit 估算。
3. 把这张表给用户看。等用户明确说「好」。有任何改动：更新后再给用户看一遍。
4. 这之后才运行 `scripts/higgsfield.py generate ... --yes`，一次生成一个镜头，每个片段用之前
   都要检查（截 3 帧）。

## 照片转片段的有效 prompt
- 描述**镜头运动**和**一个**动作："slow push in, she looks up from the laptop and smiles, soft window light"。
- 构图尽量贴近原照片。构图变化太大会让模型在片段中途切镜。
- 做循环时，把同一张照片也作为结束图传入（seedance），让片段结束在开始的地方。
- 绝不要求片段里出现文字。文字永远用代码叠加在上面。
- prompt 用英文写，因为它会发给英文视频模型。

## 把素材放进合成
- 把文件复制到项目的 `media/` 文件夹。
- 片段写成 `<video class="clip" muted playsinline data-start=".." data-duration=".." data-media-start="..">`。
- 把素材放进图形**里面**（遮罩、卡片、形状），让它读起来是一个整体设计，而不是幻灯片。
- 绝不在人脸上叠画任何东西。不说明就绝不把 16:9 片段裁成奇怪的形状。
- 统一颜色：从片段取色，把风格的底色往它靠一点；或者用 CSS filter 给片段调色，让两者像同一个世界。
