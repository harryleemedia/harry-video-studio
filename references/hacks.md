# 5 个技巧

成品之所以像工作室做的、而不像一句随手写的 prompt 生成的，靠的就是这五个习惯。
技能会替你把五个都做到。下面说明每个技巧是什么、出处在哪。

## 1. 先选定一种风格，然后坚持到底

写任何代码之前，先从 `styles/` 里选定**一种**风格（或根据用户给的参考新建一种）。
风格是一份简短的规范：hex 颜色、字体、缓动参数、动效规则和禁用清单。
作品里的每个镜头都用这同一份规范，不混搭。

原因：风格不定下来，每个模型都会退回同一个默认样子
（深色背景、发光、紫色渐变）。固定的规范能防止镜头之间风格漂移。

技能的做法：阶段 A 展示风格画廊，用户选一种风格。它的 STYLE.md 会粘贴进简报，
它的颜色会变成文件顶部的 CSS token。其他任何地方都不手写颜色。

出处：
- Motion Lab 主张一开始就禁掉默认的 AI 风格：https://github.com/NovusEdge/motion-lab
- 「锁定设计 token」，放在一个共享的地方：https://aiartimind.com/how-to-make-motion-graphics-with-claude-opus-5-5/

## 2. 真实参考胜过形容词

「做得简洁现代一点」毫无意义，一部真实影片里的一帧真实画面却信息量巨大。
向用户要 1 到 3 个参考，然后描述它们是**怎么**做出来的（遮罩文字、缓慢的镜头、
长时间停留），而不只是它们给人什么感觉。

去哪里找好参考：
- https://savee.com（设计与动效静帧的情绪板）
- https://godly.website（真实网站上最好的动效）
- https://mobbin.com（真实的 App 界面，很适合做产品演示）
- Linear、Apple 和 Cursor 的发布影片（搜索 "<company> launch video"）

出处：
- 逐帧拆解 Linear Agent 发布影片（遮罩揭示、长时间停留、快起步的缓动）：
  https://impractical.ai/launch-videos/linear-agent
- 「先找参考，再用文字描述它的制作方法」：
  https://aiartimind.com/how-to-make-motion-graphics-with-claude-opus-5-5/

## 3. 用数字写简报

开工前，把每个形容词都换成数字：
- 时长（秒）和画幅（1920 x 1080 或 1080 x 1920）
- 颜色用 hex
- 缓动写名称和秒数（expo.out，0.6 秒），绝不写「顺滑」
- 每个镜头一个主动作，写明开始时间
- 一份禁用清单

默认禁用清单（始终生效）：
- 不要变色相的渐变
- 不要发光、泛光或镜头光晕
- 眼睛追随的任何东西都不要用线性缓动
- 不要所有东西都居中的版式
- 强调色最多一种
- 任何东西都不从 0 开始放大（缩放起点用 0.6 到 0.9，配合透明度渐显）

出处：
- Motion Lab 的数字化简报：时间、hex 色板、缓动与弹簧参数、镜头列表、每个镜头一个主动作：
  https://github.com/NovusEdge/motion-lab
- 禁用变色渐变、发光和线性缓动：https://aiartimind.com/how-to-make-motion-graphics-with-claude-opus-5-5/

## 4. 循环：只用一个时钟，最后一帧 = 第一帧

只有结尾真的就是开头，循环才看起来无缝。所以：
- **所有**动效都由同一个时钟驱动（`templates/motion/studio.js` 里的 `STUDIO.play(render)`）。
  render(t) 只凭 t 画出整帧画面。
- 每个重复动作在整个时长内都要走完整数个周期（`STUDIO.wave(t, 2)`），
  每个一次性动作结束时都要回到起点。
- 要把不循环的作品改成循环：按 `references/loops.md` 里的清单逐项做。
- 证明它：`scripts/loop_check.py` 渲染 0 秒处和结尾处的帧，逐像素比对。
  只要有差异就判定失败。它还会检查从最后一帧跳回第一帧的变化
  不大于正常的一帧步进。

出处：
- 让首尾帧一致的循环相位辅助函数：https://github.com/NovusEdge/motion-lab
- HyperFrames 逐帧渲染一条暂停的时间轴，所以同一时间永远得到同一画面：
  https://hyperframes.heygen.com（或运行 `npx hyperframes docs gsap`）

## 5. 检查画面帧，而不是代码

看起来正确的代码，画面仍可能是错的。所以要在关键时刻看图：
1. 完整渲染前，截 3 到 4 张静帧，每张在镜头切换后约 0.6 秒、画面元素落定之后（`scripts/stills.sh`）。
   逐张查看，修好不对的地方，拿到用户点头。
2. 渲染完成后，运行节奏检查（`scripts/pacing_check.py`）：
   不能有超过 1 秒的空档，任何东西在画面上停留都不少于 0.3 秒。
3. 查看它生成的联系表（每秒一帧）。

出处：
- 「看完整视频之前，先检查切换处的帧」：https://aiartimind.com/how-to-make-motion-graphics-with-claude-opus-5-5/
- 镜头切换处的静帧、带编号的联系表、帧差比对：https://github.com/NovusEdge/motion-lab
- HyperFrames 的 `snapshot` 能从合成中截取精确的帧：https://hyperframes.heygen.com
