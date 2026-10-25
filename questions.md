# 提问清单（阶段 B / Stage B）

用户选好风格后，Claude 把下面这段作为**一条**消息原样发出。
要改问题就改这个文件。保持编号、每题一行、默认值放在【】里。
用户已经回答过的题目，Claude 跳过，其余照问。

---

1. 用在哪里？（YouTube 片头、Shorts 短视频、产品发布、讲解、广告）多长？【12 秒，16:9】
2. 画面上要出现哪些文字？【我根据你的主题来写】
3. 需要循环播放吗？【不需要】
4. 你的品牌：颜色、字体、logo？【用风格自带的】
5. 用真实素材吗？你自己的照片或视频片段、Higgsfield 生成的 AI 片段，还是不用（纯图形）？【不用】

只回复你想改的题号就行，比如「1：Shorts，8 秒。5：用我的照片」。或者直接回复「开始」（或 "go"），全部用默认值。

---

## 追问（仅在需要时）

- 如果第 5 题选「我的照片或片段」：「把文件拖进来，或者告诉我文件夹路径。不给的话，我就用你的默认素材（assets/me 里的 5 张定妆照、口播片段和两段 AI 片段）。」
- 如果第 5 题选「AI 片段」：先按 `references/media.md` 里的「Higgsfield 计费顺序」，用 Higgsfield MCP 的 `balance` 工具查订阅 credit（积分）。只有订阅 credit 不够、需要改走 API 时，才运行 `python3 scripts/higgsfield.py check`。如果没有 key，就说：
  「把你的 Higgsfield key 写进这个文件夹里一个叫 .env 的文件，只需一行：
  HIGGSFIELD_API_KEY=your_key_id:your_key_secret（在 https://console.higgsfield.ai 获取）。千万不要贴到聊天里。弄好了告诉我。」
