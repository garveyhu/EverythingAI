#!/usr/bin/env python3
"""Rebuild AI Panorama with refined categories + verified blogger section."""
import re, os, json

HTML_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ai_panorama.html')

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    old_html = f.read()
icon_map = {}
for m in re.finditer(r'"title":\s*"([^"]+)"[^}]*?"icon":\s*"(data:image[^"]*)"', old_html):
    icon_map[m.group(1)] = m.group(2)

# ═══ CATEGORIES (通用篇 moved before 设计篇) ═══
TOOL_CATS = ["AI 控制台", "AI 社区", "提示词篇", "通用篇", "设计篇", "产品篇", "开发篇", "测试篇"]
BLOGGER_CATS = [
    "AI 硬核技术", "AI 前沿资讯", "深度访谈", "创业 & 创投", "效率 & 个人成长",
    "AI 创意艺术"
]

TOOLS = [
    # ─── AI 控制台 ───
    {"title": "Claude", "desc": "Anthropic 旗舰 AI 助手，超长上下文，指令遵循能力强", "url": "https://platform.claude.com/settings/keys", "cat": "AI 控制台"},
    {"title": "OpenAI", "desc": "ChatGPT 背后的平台，GPT 系列模型 API 管理", "url": "https://platform.openai.com/settings/proj_8vm3Av8jUd85UbDohNEgMkYA/api-keys", "cat": "AI 控制台"},
    {"title": "火山方舟", "desc": "字节跳动大模型平台，集成豆包等 AI 模型服务", "url": "https://console.volcengine.com/ark", "cat": "AI 控制台"},
    {"title": "阿里百炼", "desc": "阿里云大模型应用开发平台，通义系列模型入口", "url": "https://bailian.console.aliyun.com/?tab=model#/model-market", "cat": "AI 控制台"},
    {"title": "智谱 AI", "desc": "清华系 GLM 大模型平台，ChatGLM 系列 API 服务", "url": "https://bigmodel.cn/usercenter/glm-coding/usage", "cat": "AI 控制台"},
    {"title": "DeepSeek", "desc": "高性价比开源大模型，擅长代码与深度推理", "url": "https://platform.deepseek.com/usage", "cat": "AI 控制台"},
    {"title": "火山引擎体验中心", "desc": "火山引擎 AI 能力在线体验，语音、图像、NLP 等", "url": "https://exp.volcengine.com/", "cat": "AI 控制台"},

    # ─── AI 社区 (WaytoAGI first) ───
    {"title": "WaytoAGI", "desc": "通往 AGI 之路，AI 学习路线图与前沿资讯", "url": "https://www.waytoagi.com/zh", "cat": "AI 社区"},
    {"title": "AIHub", "desc": "中文 AI 工具导航，发现最新 AI 应用与资源", "url": "https://www.aihub.cn/", "cat": "AI 社区"},
    {"title": "魔搭社区", "desc": "阿里开源模型社区，海量模型下载与体验", "url": "https://modelscope.cn/home", "cat": "AI 社区"},
    {"title": "FlowGPT", "desc": "AI Prompt 与角色社区，分享创意对话与应用灵感", "url": "https://flowgpt.com/", "cat": "AI 社区"},

    # ─── 通用篇 (merged AI通识 + 原通用 + Coze/雾象) ───
    {"title": "Google AI Studio", "desc": "Google Gemini 模型体验平台，支持多模态对话、代码与创意生成", "url": "https://aistudio.google.com/", "cat": "通用篇"},
    {"title": "Coze (扣子)", "desc": "字节 AI Bot 构建平台，零代码创建智能体与自动化", "url": "https://space.coze.cn/", "cat": "通用篇"},
    {"title": "雾象", "desc": "动画智能体创作平台，AI 驱动的交互式虚拟角色", "url": "https://fogsight.ai/app", "cat": "通用篇"},
    {"title": "模型排行榜", "desc": "LMArena 大模型实时排名，基于人类偏好盲评 ELO", "url": "https://lmarena.ai/leaderboard", "cat": "通用篇"},
    {"title": "AI Ping", "desc": "国产模型 API 质量测评，对比延迟、价格与准确率", "url": "https://www.aiping.cn/modelList", "cat": "通用篇"},
    {"title": "Tokenizer", "desc": "OpenAI Token 计算器，精确统计文本消耗量", "url": "https://platform.openai.com/tokenizer", "cat": "通用篇"},
    {"title": "通义听悟", "desc": "阿里 AI 音视频总结，自动生成会议记录与摘要", "url": "https://tingwu.aliyun.com/home", "cat": "通用篇"},
    {"title": "Watermark Remover", "desc": "AI 智能去水印工具，一键清除图片水印保持画质", "url": "https://www.watermarkremover.io/zh", "cat": "通用篇"},
    {"title": "佐糖去水印", "desc": "国产 AI 图片水印去除，支持批量处理与高清修复", "url": "https://picwish.cn/remove-image-watermark", "cat": "通用篇"},
    {"title": "Notion AI", "desc": "Notion 内置 AI 助手，自动总结、写作、任务规划一站式", "url": "https://www.notion.com/product/ai", "cat": "通用篇"},

    # ─── 设计篇 ───
    {"title": "Midjourney", "desc": "顶级 AI 图像生成平台，艺术风格表现力最强", "url": "https://www.midjourney.com/home/?callbackUrl=%2Fapp%2F", "cat": "设计篇"},
    {"title": "即梦 Dreamina", "desc": "字节 AI 创作平台，搭载 Seedance 2.0 视频生成模型，支持文生视频与图生视频", "url": "https://jimeng.jianying.com/", "cat": "设计篇"},
    {"title": "Pencil", "desc": "AI 原生设计工具，自然语言驱动的 UI/UX 设计与原型生成", "url": "https://pencil.dev/", "cat": "设计篇"},
    {"title": "v0", "desc": "Vercel 出品的 AI UI 生成器，用文字描述快速生成 React 界面", "url": "https://v0.app/", "cat": "设计篇"},
    {"title": "Motiff", "desc": "AI 驱动的 UI 设计工具，支持 Figma 插件形式的智能设计辅助", "url": "https://motiff.com/", "cat": "设计篇"},
    {"title": "Google Stitch", "desc": "原 Galileo AI，Google 收购后重塑，文字/草图秒变专业多屏 UI", "url": "https://stitch.withgoogle.com/", "cat": "设计篇"},
    {"title": "Civitai", "desc": "全球最大 AI 图像模型社区，Stable Diffusion 模型分享", "url": "https://civitai.com/", "cat": "设计篇"},
    {"title": "Microsoft Designer", "desc": "微软 AI 设计工具，DALL·E 驱动的图像生成与编辑", "url": "https://designer.microsoft.com/", "cat": "设计篇"},
    {"title": "Stable Diffusion Online", "desc": "在线免费 AI 绘画，无需安装即可生成图像", "url": "https://stablediffusionweb.com/", "cat": "设计篇"},
    {"title": "Lexica", "desc": "AI 图像搜索引擎，浏览百万级 AI 生成图片库", "url": "https://lexica.art/", "cat": "设计篇"},
    {"title": "一帧秒创", "desc": "国产 AI 视频创作平台，文案、配音、视频一站式", "url": "https://aigc.yizhentv.com/", "cat": "设计篇"},
    {"title": "ImagePrompt", "desc": "AI 图片提示词反推，从图片逆向生成 Prompt", "url": "https://imageprompt.org/zh/image-to-prompt", "cat": "设计篇"},

    # ─── 产品篇 ───
    {"title": "Gamma", "desc": "AI 驱动的演示文稿与文档平台，输入主题一键生成精美 PPT", "url": "https://gamma.app/", "cat": "产品篇"},
    {"title": "Kraftful", "desc": "AI 产品洞察平台，整合 30+ 用户反馈源自动提取需求与趋势", "url": "https://www.kraftful.com/", "cat": "产品篇"},
    {"title": "Productboard", "desc": "AI 增强的产品管理平台，智能优先级排序与用户反馈分析", "url": "https://www.productboard.com/", "cat": "产品篇"},
    {"title": "Ponder", "desc": "AI 灵感激发工具，随机生成创意问题启发思维", "url": "https://ponder.ing/", "cat": "产品篇"},

    # ─── 提示词篇 ───
    {"title": "PromptPilot", "desc": "火山引擎 Prompt 工作台，可视化调试与优化提示词", "url": "https://promptpilot.volcengine.com/home", "cat": "提示词篇"},
    {"title": "扣子罗盘", "desc": "字节扣子 Prompt Playground，交互式测试提示效果", "url": "https://loop.coze.cn/console/enterprise/personal/space/7531320096816365587/pe/playground", "cat": "提示词篇"},
    {"title": "PromptPort", "desc": "Prompt 模板市场，按场景分类的高质量提示词库", "url": "https://app.promptport.ai/", "cat": "提示词篇"},
    {"title": "AiShort", "desc": "开源 AI 快捷指令集合，一键复制即用的 Prompt 库", "url": "https://www.aishort.top/", "cat": "提示词篇"},
    {"title": "PromptBase", "desc": "全球最大 Prompt 交易市场，买卖高质量提示词模板", "url": "https://promptbase.com/", "cat": "提示词篇"},
    {"title": "LearnPrompting", "desc": "系统化 Prompt 工程教程，从入门到高阶的提示词学习路径", "url": "https://learnprompting.org/", "cat": "提示词篇"},

    # ─── 开发篇 ───
    {"title": "Claude Code Docs", "desc": "Claude Code CLI 官方文档，AI 编程助手操作指南", "url": "https://code.claude.com/docs/zh-CN/cli-reference", "cat": "开发篇"},
    {"title": "Antigravity Docs", "desc": "Google Antigravity AI 编程助手技能与插件开发文档", "url": "https://antigravity.google/docs/skills", "cat": "开发篇"},
    {"title": "Gemini CLI", "desc": "Google Gemini CLI 工具参考文档，命令行 AI 利器", "url": "https://geminicli.com/docs/cli/cli-reference/", "cat": "开发篇"},
    {"title": "Context7", "desc": "MCP 协议实时文档服务，为 AI 编程助手提供最新 SDK 文档", "url": "https://context7.com/", "cat": "开发篇"},
    {"title": "Dify", "desc": "开源 LLM 应用开发框架，可视化编排 RAG 与 Agent 工作流", "url": "https://github.com/langgenius/dify", "cat": "开发篇"},
    {"title": "Awesome Dify Workflow", "desc": "Dify 精选工作流模板，开箱即用的 AI 应用最佳实践", "url": "https://github.com/svcvit/Awesome-Dify-Workflow/tree/main?tab=readme-ov-file", "cat": "开发篇"},
    {"title": "Dify 101", "desc": "Dify 新手入门教程，从零搭建 LLM 应用的系统指南", "url": "https://dify101.com/", "cat": "开发篇"},
    {"title": "Langflow", "desc": "开源可视化 AI 应用构建器，拖拽式 LangChain 工作流", "url": "https://github.com/langflow-ai/langflow", "cat": "开发篇"},
    {"title": "n8n", "desc": "开源工作流自动化平台，支持 AI 节点的低代码引擎", "url": "https://github.com/n8n-io/n8n", "cat": "开发篇"},
    {"title": "LangSmith", "desc": "LangChain 调试与监控平台，追踪 LLM 应用全链路性能", "url": "https://smith.langchain.com/", "cat": "开发篇"},
    {"title": "SkillsMP", "desc": "Agent Skills 市场，发现并分享 AI 智能体技能插件", "url": "https://skillsmp.com/zh", "cat": "开发篇"},
    {"title": "Skills.sh", "desc": "开源 AI Agent 技能仓库，可直接集成的函数式技能包", "url": "https://skills.sh/", "cat": "开发篇"},

    # ─── 测试篇 ───
    {"title": "Testsigma", "desc": "AI 驱动的无代码测试平台，自然语言编写测试用例，支持自愈", "url": "https://testsigma.com/", "cat": "测试篇"},
    {"title": "Applitools", "desc": "视觉 AI 测试先驱，用计算机视觉自动检测 UI 视觉回归", "url": "https://applitools.com/", "cat": "测试篇"},
    {"title": "Katalon", "desc": "一站式 AI 测试平台，覆盖 Web/移动/API 自动化，Gartner 推荐", "url": "https://katalon.com/", "cat": "测试篇"},
    {"title": "Mabl", "desc": "智能测试自动化平台，AI Agent 自主创建测试套件与根因分析", "url": "https://www.mabl.com/", "cat": "测试篇"},
]

# ═══ BLOGGERS (YouTube channels verified 2026-02-11 + X/Twitter accounts) ═══
BLOGGERS = [
    # ── AI 硬核技术 (YouTube) ──
    {"title": "Andrej Karpathy", "desc": "OpenAI 创始成员、特斯拉前 AI 总监，大模型领域顶级大佬，内容硬核通透", "yt": "https://www.youtube.com/@AndrejKarpathy", "x": "https://x.com/karpathy", "cat": "AI 硬核技术"},
    {"title": "OpenAI", "desc": "OpenAI 官方频道，GPT、Sora 等一手技术发布与研究进展", "yt": "https://www.youtube.com/@OpenAI", "x": "https://x.com/OpenAI", "cat": "AI 硬核技术"},
    {"title": "Google DeepMind", "desc": "谷歌顶级 AI 实验室，AlphaGo、AlphaFold、AGI 前沿研究", "yt": "https://www.youtube.com/@GoogleDeepMind", "x": "https://x.com/DeepMind", "cat": "AI 硬核技术"},
    {"title": "Two Minute Papers", "desc": "AI 顶会论文速读，可视化讲解，短小精悍高质量", "yt": "https://www.youtube.com/@TwoMinutePapers", "x": "https://x.com/TwoMinutePapers", "cat": "AI 硬核技术"},
    {"title": "3Blue1Brown", "desc": "数学与 AI 底层原理可视化，神经网络讲得极其直观", "yt": "https://www.youtube.com/@3blue1brown", "x": "https://x.com/3blue1brown", "cat": "AI 硬核技术"},
    {"title": "Umar Jamil", "desc": "大模型架构精讲，Transformer、LLaMA、MoE 论文逐段精读", "yt": "https://www.youtube.com/@umarjamilai", "x": "https://x.com/umarjamilai", "cat": "AI 硬核技术"},
    # ── AI 前沿资讯 (YouTube) ──
    {"title": "The AI Daily Brief", "desc": "每日 AI 新闻与行业动态，快速扫遍全球 AI 热点", "yt": "https://www.youtube.com/@AIDailyBrief", "x": "https://x.com/AIDailyBrief", "cat": "AI 前沿资讯"},
    {"title": "Riley Brown AI", "desc": "AI 工具实测与工作流教程，偏实战、效率、落地应用", "yt": "https://www.youtube.com/@rileybrownai", "x": "https://x.com/rileybrown_ai", "cat": "AI 前沿资讯"},
    {"title": "Jeff Su", "desc": "AI + 效率工具，用 GPT、Claude 做自动化与个人第二大脑", "yt": "https://www.youtube.com/@jeffsu", "x": "", "cat": "AI 前沿资讯"},
    # ── 深度访谈 (YouTube) ──
    {"title": "Lex Fridman", "desc": "全球顶流 AI 访谈，专访马斯克、Karpathy 等大佬聊 AGI", "yt": "https://www.youtube.com/@lexfridman", "x": "https://x.com/lexfridman", "cat": "深度访谈"},
    {"title": "Dwarkesh Patel", "desc": "新生代硬核长访谈，专聊 AGI、大模型、AI 安全深度拉满", "yt": "https://www.youtube.com/@dwarkeshpatel", "x": "https://x.com/dwarkesh_sp", "cat": "深度访谈"},
    {"title": "The Diary of a CEO", "desc": "顶级企业家深度访谈，讲决策、成长、商业底层逻辑", "yt": "https://www.youtube.com/@TheDiaryofaCEO", "x": "https://x.com/stevenbartlett", "cat": "深度访谈"},
    # ── 创业 & 创投 (YouTube + X) ──
    {"title": "Y Combinator", "desc": "世界最顶级创业孵化器，创业方法论、融资、产品全流程", "yt": "https://www.youtube.com/@ycombinator", "x": "https://x.com/ycombinator", "cat": "创业 & 创投"},
    {"title": "Google Ventures", "desc": "谷歌风投官方，科技赛道、AI 投资逻辟、行业趋势", "yt": "https://www.youtube.com/@GoogleVentures", "x": "", "cat": "创业 & 创投"},
    {"title": "@venturetwins", "desc": "a16z 合伙人，顶级风投视角看 AI 与科技创业", "yt": "", "x": "https://x.com/venturetwins", "cat": "创业 & 创投"},
    {"title": "@javilopen", "desc": "科技创始人，分享 AI 产品开发与创业实战经验", "yt": "", "x": "https://x.com/javilopen", "cat": "创业 & 创投"},
    {"title": "@mreflow", "desc": "FutureTools.io 创始人，AI 工具测评与行业洞察", "yt": "", "x": "https://x.com/mreflow", "cat": "创业 & 创投"},
    {"title": "@NathanLands", "desc": "Lore.com 创始人，AI 艺术商业化先驱", "yt": "", "x": "https://x.com/NathanLands", "cat": "创业 & 创投"},
    # ── 效率 & 个人成长 (YouTube) ──
    {"title": "Ali Abdaal", "desc": "牛津学霸 productivity 顶流，学习、时间管理、知识体系", "yt": "https://www.youtube.com/@AliAbdaal", "x": "https://x.com/aliabdaal", "cat": "效率 & 个人成长"},
    {"title": "Thomas Frank", "desc": "效率工具、第二大脑、学习方法，个人系统与知识管理", "yt": "https://www.youtube.com/@ThomasFrank", "x": "https://x.com/tomfrankly", "cat": "效率 & 个人成长"},
    # ── AI 创意艺术 (X/Twitter) ──
    {"title": "@icreatelife", "desc": "AI 艺术家，探索 AI 生成艺术的无限可能", "yt": "", "x": "https://x.com/icreatelife", "cat": "AI 创意艺术"},
    {"title": "@ClaireSilver12", "desc": "AI 艺术领域先锋，用 AI 创造惊艳视觉作品", "yt": "", "x": "https://x.com/ClaireSilver12", "cat": "AI 创意艺术"},
    {"title": "@dvorahfr", "desc": "AI 艺术家，数字艺术与 AI 创作融合实践者", "yt": "", "x": "https://x.com/dvorahfr", "cat": "AI 创意艺术"},
    {"title": "@8co28", "desc": "日本 AI 艺术家，近期活跃于 Suno 音乐创作", "yt": "", "x": "https://x.com/8co28", "cat": "AI 创意艺术"},
    {"title": "@hollyherndon", "desc": "AI 艺术家与音乐人，AI 与创意表达的跨界探索者", "yt": "", "x": "https://x.com/hollyherndon", "cat": "AI 创意艺术"},
    {"title": "@iamneubert", "desc": "电子艺术家，AI 生成艺术创世纪系列作者", "yt": "", "x": "https://x.com/iamneubert", "cat": "AI 创意艺术"},
    {"title": "@liberxx0", "desc": "日本 AI 艺术家，千与千寻风格 AI 创作者", "yt": "", "x": "https://x.com/liberxx0", "cat": "AI 创意艺术"},
    {"title": "@Riabovitchev", "desc": "电影概念艺术家，AI 辅助视觉开发与概念设计", "yt": "", "x": "https://x.com/Riabovitchev", "cat": "AI 创意艺术"},
    {"title": "@nickfloats", "desc": "创意总监，Midjourney 社区活跃创作者", "yt": "", "x": "https://x.com/nickfloats", "cat": "AI 创意艺术"},
    {"title": "@ActionMovieKid", "desc": "动画工作室 / VFX 视觉特效创作者", "yt": "", "x": "https://x.com/ActionMovieKid", "cat": "AI 创意艺术"},
    {"title": "@ammaar", "desc": "ElevenLabs 设计主管，AI 产品设计实践", "yt": "", "x": "https://x.com/ammaar", "cat": "AI 创意艺术"},
    {"title": "@commonstyle", "desc": "Adobe 社区布道者，设计工具与 AI 创意结合", "yt": "", "x": "https://x.com/commonstyle", "cat": "AI 创意艺术"},
    {"title": "@daniel_eckler", "desc": "技术 × 设计 × 营销，曾服务 Meta / Spotify / Nike", "yt": "", "x": "https://x.com/daniel_eckler", "cat": "AI 创意艺术"},
    {"title": "@itspetergabriel", "desc": "音乐创作者，AI 辅助音乐创作探索者", "yt": "", "x": "https://x.com/itspetergabriel", "cat": "AI 创意艺术"},
    # ── AI 布道者 → merged into AI 前沿资讯 ──
    {"title": "@op7418", "desc": "AI 布道者「归藏」，中文圈知名 AI 资讯博主", "yt": "", "x": "https://x.com/op7418", "cat": "AI 前沿资讯"},
    {"title": "@_akhaliq", "desc": "论文布道者，第一时间分享 AI 前沿论文与研究", "yt": "", "x": "https://x.com/_akhaliq", "cat": "AI 前沿资讯"},
    {"title": "@chatgptair", "desc": "AI 新闻布道者（日本），日语圈 AI 资讯先锋", "yt": "", "x": "https://x.com/chatgptair", "cat": "AI 前沿资讯"},
    {"title": "@heyBarsee", "desc": "AI 新闻布道者，日常分享 AI 工具与行业动态", "yt": "", "x": "https://x.com/heyBarsee", "cat": "AI 前沿资讯"},
    {"title": "@LinusEkenstam", "desc": "AI 新闻布道者，AI 趋势与工具深度解读", "yt": "", "x": "https://x.com/LinusEkenstam", "cat": "AI 前沿资讯"},
    {"title": "@AiBreakfast", "desc": "AI 新闻布道者，每日 AI 早报播客", "yt": "", "x": "https://x.com/AiBreakfast", "cat": "AI 前沿资讯"},
    {"title": "@rpnickson", "desc": "AI 新闻布道者，视频内容形式分享 AI 资讯", "yt": "", "x": "https://x.com/rpnickson", "cat": "AI 前沿资讯"},
    {"title": "@mrgreen", "desc": "AI 新闻布道者，AI 行业动态与工具推荐", "yt": "", "x": "https://x.com/mrgreen", "cat": "AI 前沿资讯"},
    {"title": "@chaseleantj", "desc": "AI 布道者，知名画图 GPTs 创始人", "yt": "", "x": "https://x.com/chaseleantj", "cat": "AI 前沿资讯"},
    {"title": "@thatroblennon", "desc": "AI 教育布道者，系统化的 AI 学习与应用教程", "yt": "", "x": "https://x.com/thatroblennon", "cat": "AI 前沿资讯"},
    {"title": "@dr_cintas", "desc": "AI 布道者，AI 技术与应用趋势分析", "yt": "", "x": "https://x.com/dr_cintas", "cat": "AI 前沿资讯"},
    {"title": "@HBCoop_", "desc": "人工智能教育家和顾问，AI 培训与咨询", "yt": "", "x": "https://x.com/HBCoop_", "cat": "AI 前沿资讯"},
    {"title": "@TheJackForge", "desc": "开发者 + 艺术爱好者，AI 开发与创意跨界", "yt": "", "x": "https://x.com/TheJackForge", "cat": "AI 前沿资讯"},
    # ── AI 工具官方 → merged into AI 前沿资讯 ──
    {"title": "@runwayml", "desc": "Runway 官方，Gen-2/Gen-3 AI 视频生成工具", "yt": "", "x": "https://x.com/runwayml", "cat": "AI 前沿资讯"},
    {"title": "@pika_labs", "desc": "Pika 官方，AI 视频生成与编辑平台", "yt": "", "x": "https://x.com/pika_labs", "cat": "AI 前沿资讯"},
    {"title": "@Magnific_AI", "desc": "Magnific AI 官方，AI 图片超分辨率放大工具", "yt": "", "x": "https://x.com/Magnific_AI", "cat": "AI 前沿资讯"},
    {"title": "@StabilityAI_JP", "desc": "Stability AI 日本官方，Stable Diffusion 日本社区", "yt": "", "x": "https://x.com/StabilityAI_JP", "cat": "AI 前沿资讯"},
    # ── 技术 & 学术 → merged into AI 硬核技术 ──
    {"title": "@emollick", "desc": "沃顿商学院教授，AI 对企业与教育影响的研究权威", "yt": "", "x": "https://x.com/emollick", "cat": "AI 硬核技术"},
    {"title": "@tunguz", "desc": "英伟达机器学习工程师，AI 芯片与模型训练洞察", "yt": "", "x": "https://x.com/tunguz", "cat": "AI 硬核技术"},
    {"title": "@dylan522p", "desc": "人工智能与半导体研究员，AI 算力与芯片趋势分析", "yt": "", "x": "https://x.com/dylan522p", "cat": "AI 硬核技术"},
    {"title": "@bilawalsidhu", "desc": "前 Google Maps & AR/VR 工程师，AI 与空间计算技术", "yt": "", "x": "https://x.com/bilawalsidhu", "cat": "AI 硬核技术"},
]

# Inject icons for tools
for tool in TOOLS:
    if tool['title'] in icon_map:
        tool['icon'] = icon_map[tool['title']]
    else:
        for old_title, icon in icon_map.items():
            if old_title in tool['title'] or tool['title'] in old_title:
                tool['icon'] = icon
                break
        if 'icon' not in tool:
            tool['icon'] = ''

# Build JS
def js_str(s):
    return s.replace('\\','\\\\').replace('"','\\"')

tools_lines = []
for t in TOOLS:
    ic = js_str(t['icon']) if t['icon'] else ''
    tools_lines.append(f'  {{"title":"{t["title"]}","desc":"{t["desc"]}","url":"{t["url"]}","cat":"{t["cat"]}","icon":"{ic}"}}')
tools_js = 'const RESOURCES = [\n' + ',\n'.join(tools_lines) + '\n];'

bloggers_lines = []
for b in BLOGGERS:
    bloggers_lines.append(f'  {{"title":"{b["title"]}","desc":"{b["desc"]}","yt":"{b["yt"]}","x":"{b["x"]}","cat":"{b["cat"]}"}}')
bloggers_js = 'const BLOGGERS = [\n' + ',\n'.join(bloggers_lines) + '\n];'

tool_cats_js = 'const TOOL_CATS = ' + json.dumps(TOOL_CATS, ensure_ascii=False) + ';'
blogger_cats_js = 'const BLOGGER_CATS = ' + json.dumps(BLOGGER_CATS, ensure_ascii=False) + ';'

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 全景视界 — EverythingAI 资源导航</title>
<meta name="description" content="汇聚全球顶尖 AI 资源、工具与推荐频道，按角色分类的一站式导航">
<style>
:root {{
  --bg:#f2fcf5;--card-bg:#fff;--text:#0f392b;--text2:#047857;
  --accent:#059669;--accent-hover:#047857;--glow:rgba(5,150,105,.2);
  --border:rgba(5,150,105,.12);--shadow-sm:0 1px 3px rgba(0,0,0,.06);
  --shadow-md:0 8px 24px rgba(5,150,105,.1);--grad1:#10b981;--grad2:#047857;
  --nav-bg:rgba(255,255,255,.75);--tag-bg:rgba(5,150,105,.08);--tag-c:#059669;
}}
[data-theme="blue"] {{
  --bg:#f0f7ff;--card-bg:#fff;--text:#1e3a8a;--text2:#2563eb;
  --accent:#2563eb;--accent-hover:#1d4ed8;--glow:rgba(37,99,235,.2);
  --border:rgba(37,99,235,.12);--shadow-sm:0 1px 3px rgba(0,0,0,.06);
  --shadow-md:0 8px 24px rgba(37,99,235,.1);--grad1:#3b82f6;--grad2:#1d4ed8;
  --nav-bg:rgba(255,255,255,.8);--tag-bg:rgba(37,99,235,.08);--tag-c:#2563eb;
}}
[data-theme="dark"] {{
  --bg:#0f172a;--card-bg:rgba(30,41,59,.7);--text:#f1f5f9;--text2:#94a3b8;
  --accent:#38bdf8;--accent-hover:#0ea5e9;--glow:rgba(56,189,248,.15);
  --border:rgba(255,255,255,.08);--shadow-sm:0 1px 3px rgba(0,0,0,.2);
  --shadow-md:0 8px 24px rgba(0,0,0,.3);--grad1:#38bdf8;--grad2:#0284c7;
  --nav-bg:rgba(30,41,59,.85);--tag-bg:rgba(56,189,248,.1);--tag-c:#38bdf8;
}}
*{{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"PingFang SC","Microsoft YaHei",sans-serif}}
body{{background:var(--bg);color:var(--text);min-height:100vh;transition:all .3s;padding-bottom:3rem}}
/* Theme switcher */
.tw{{position:fixed;top:16px;right:16px;z-index:200}}
.tw-btn{{width:36px;height:36px;border-radius:50%;background:var(--card-bg);border:1px solid var(--border);cursor:pointer;box-shadow:var(--shadow-md);backdrop-filter:blur(12px);display:flex;align-items:center;justify-content:center;font-size:16px;transition:all .25s;-webkit-user-select:none;user-select:none}}
.tw-btn:hover{{transform:scale(1.08);box-shadow:0 4px 16px var(--glow)}}
.tw-pop{{position:absolute;top:44px;right:0;background:var(--card-bg);border:1px solid var(--border);padding:10px;border-radius:14px;display:flex;flex-direction:column;gap:8px;box-shadow:var(--shadow-md);backdrop-filter:blur(16px);opacity:0;transform:translateY(-8px) scale(.95);pointer-events:none;transition:all .25s cubic-bezier(.25,.8,.25,1)}}
.tw.open .tw-pop{{opacity:1;transform:translateY(0) scale(1);pointer-events:auto}}
.tw-item{{display:flex;align-items:center;gap:8px;padding:6px 12px;border-radius:10px;cursor:pointer;white-space:nowrap;font-size:.82rem;color:var(--text2);transition:all .2s}}
.tw-item:hover{{background:var(--tag-bg)}}
.tw-dot{{width:16px;height:16px;border-radius:50%;flex-shrink:0;border:2px solid transparent;transition:all .2s}}
.tw-item.active .tw-dot{{border-color:var(--accent);box-shadow:0 0 0 2px var(--glow)}}
.tw-dot.green{{background:linear-gradient(135deg,#10b981,#059669)}}.tw-dot.blue{{background:linear-gradient(135deg,#3b82f6,#1d4ed8)}}.tw-dot.dark{{background:linear-gradient(135deg,#334155,#1e293b)}}
.hdr{{padding:2.5rem 2rem 1rem;max-width:1400px;margin:0 auto}}
.top{{display:flex;flex-direction:column;align-items:center;margin-bottom:1.5rem}}
h1{{font-size:2.4rem;font-weight:800;margin-bottom:.4rem;background:linear-gradient(135deg,var(--grad1),var(--grad2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-.5px}}
.sub{{color:var(--text2);font-size:.95rem;opacity:.8;margin-bottom:1.2rem}}
.sc{{width:100%;max-width:480px}}.si{{width:100%;padding:10px 18px;border-radius:100px;border:2px solid transparent;background:var(--card-bg);box-shadow:var(--shadow-sm);font-size:.95rem;color:var(--text);transition:all .3s;outline:none}}
.si:focus{{border-color:var(--accent);box-shadow:0 0 0 3px var(--glow)}}
[data-theme="dark"] .si:focus{{background:rgba(30,41,59,.9)}}
.sec-tabs{{display:flex;justify-content:center;gap:0;margin-bottom:.5rem}}
.sec-btn{{padding:10px 28px;border:none;background:transparent;color:var(--text2);font-size:1rem;font-weight:600;cursor:pointer;border-bottom:3px solid transparent;transition:all .2s}}
.sec-btn:hover{{color:var(--accent)}}
.sec-btn.active{{color:var(--accent);border-bottom-color:var(--accent)}}
.nc{{position:sticky;top:0;z-index:50;padding:8px 0;margin-bottom:1.5rem;transition:background .3s}}
.nc.stuck{{background:var(--nav-bg);backdrop-filter:blur(10px);border-bottom:1px solid var(--border);box-shadow:var(--shadow-sm)}}
.nt{{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;max-width:1200px;margin:0 auto;padding:0 1rem}}
.nb{{padding:6px 16px;border-radius:16px;border:1px solid transparent;background:transparent;color:var(--text2);font-size:.9rem;font-weight:500;cursor:pointer;transition:all .2s}}
.nb:hover{{background:rgba(0,0,0,.03);color:var(--accent-hover)}}
.nb.active{{background:var(--accent);color:#fff;box-shadow:0 2px 6px var(--glow)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.25rem;padding:0 2rem;max-width:1400px;margin:0 auto}}
.card{{background:var(--card-bg);border-radius:14px;padding:1.1rem 1.2rem;border:1px solid var(--border);box-shadow:var(--shadow-sm);transition:all .25s cubic-bezier(.25,.8,.25,1);display:flex;flex-direction:column;text-decoration:none;color:var(--text);cursor:pointer;position:relative;overflow:hidden}}
.card:hover{{transform:translateY(-3px);box-shadow:var(--shadow-md);border-color:var(--accent)}}
.card-head{{display:flex;align-items:center;gap:12px;margin-bottom:.6rem}}
.card-icon{{width:32px;height:32px;border-radius:8px;object-fit:contain;flex-shrink:0;background:var(--tag-bg);padding:2px}}
.card-icon-ph{{width:32px;height:32px;border-radius:8px;background:linear-gradient(135deg,var(--grad1),var(--grad2));display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:14px;flex-shrink:0}}
.card-title{{font-size:1rem;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.card-desc{{font-size:.82rem;color:var(--text2);line-height:1.45;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;flex:1;margin-bottom:.6rem}}
.card-foot{{display:flex;align-items:center;justify-content:space-between}}
.card-tag{{display:inline-block;font-size:.72rem;padding:2px 8px;border-radius:10px;background:var(--tag-bg);color:var(--tag-c);font-weight:500}}
.card-links{{display:flex;gap:6px}}
.card-links a{{font-size:.72rem;padding:3px 10px;border-radius:8px;background:var(--tag-bg);color:var(--tag-c);text-decoration:none;font-weight:500;transition:all .2s;white-space:nowrap}}
.card-links a:hover{{background:var(--accent);color:#fff}}
.cnt{{text-align:center;padding:1rem;color:var(--text2);font-size:.85rem;opacity:.6}}
@media(max-width:768px){{.grid{{grid-template-columns:1fr;padding:0 1rem}}.hdr{{padding:1.5rem 1rem .5rem}}h1{{font-size:1.8rem}}.tw{{top:10px;right:10px}}}}
</style>
</head>
<body>
<div class="tw" id="tw">
  <div class="tw-btn" id="tw-btn">🎨</div>
  <div class="tw-pop">
    <div class="tw-item active" data-theme="green"><div class="tw-dot green"></div>清新绿</div>
    <div class="tw-item" data-theme="blue"><div class="tw-dot blue"></div>商务蓝</div>
    <div class="tw-item" data-theme="dark"><div class="tw-dot dark"></div>暗夜黑</div>
  </div>
</div>
<div class="hdr">
  <div class="top">
    <h1>AI 全景视界</h1>
    <div class="sub">汇聚全球顶尖 AI 资源与工具生态</div>
    <div class="sc"><input type="text" id="si" class="si" placeholder="搜索工具、博主或描述..."></div>
  </div>
</div>
<div class="sec-tabs">
  <button class="sec-btn active" data-sec="tools">🛠️ 工具资源</button>
  <button class="sec-btn" data-sec="bloggers">🎬 推荐频道</button>
</div>
<div class="nc" id="nc"><div class="nt" id="nt"></div></div>
<div class="grid" id="grid"></div>
<div class="cnt" id="cnt"></div>
<script>
{tools_js}
{bloggers_js}
{tool_cats_js}
{blogger_cats_js}
document.addEventListener('DOMContentLoaded',()=>{{
  const si=document.getElementById('si'),nt=document.getElementById('nt'),
        grid=document.getElementById('grid'),nc=document.getElementById('nc'),
        cnt=document.getElementById('cnt'),tw=document.getElementById('tw'),
        twBtn=document.getElementById('tw-btn');
  let filter='all', section='tools';

  // Theme switcher
  twBtn.onclick=e=>{{e.stopPropagation();tw.classList.toggle('open')}};
  document.addEventListener('click',e=>{{if(!tw.contains(e.target))tw.classList.remove('open')}});
  document.querySelectorAll('.tw-item').forEach(item=>item.onclick=()=>{{
    document.querySelectorAll('.tw-item').forEach(x=>x.classList.remove('active'));
    item.classList.add('active');
    const t=item.dataset.theme;
    t==='green'?document.body.removeAttribute('data-theme'):document.body.setAttribute('data-theme',t);
    tw.classList.remove('open');
  }});
  window.onscroll=()=>nc.classList.toggle('stuck',scrollY>80);

  // Section tabs
  document.querySelectorAll('.sec-btn').forEach(b=>b.onclick=()=>{{
    document.querySelectorAll('.sec-btn').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');
    section=b.dataset.sec;filter='all';buildTabs();render();
  }});

  function buildTabs(){{
    const cats=section==='tools'?TOOL_CATS:BLOGGER_CATS;
    let h='<button class="nb active" data-f="all">全部</button>';
    cats.forEach(c=>h+=`<button class="nb" data-f="${{c}}">${{c}}</button>`);
    nt.innerHTML=h;
    nt.querySelectorAll('.nb').forEach(b=>b.onclick=()=>{{
      nt.querySelectorAll('.nb').forEach(x=>x.classList.remove('active'));
      b.classList.add('active');filter=b.dataset.f;render();
    }});
  }}

  function render(){{
    const term=si.value.toLowerCase();let html='',count=0;
    if(section==='tools'){{
      RESOURCES.forEach(t=>{{
        if((filter!=='all'&&t.cat!==filter)||term&&!t.title.toLowerCase().includes(term)&&!t.desc.toLowerCase().includes(term))return;
        count++;
        const ic=t.icon?`<img src="${{t.icon}}" class="card-icon" onerror="this.outerHTML='<div class=card-icon-ph>${{t.title[0]}}</div>'">`:`<div class="card-icon-ph">${{t.title[0]}}</div>`;
        html+=`<a href="${{t.url}}" class="card" target="_blank" rel="noopener"><div class="card-head">${{ic}}<div class="card-title">${{t.title}}</div></div><div class="card-desc">${{t.desc}}</div><div class="card-foot"><span class="card-tag">${{t.cat}}</span></div></a>`;
      }});
    }}else{{
      BLOGGERS.forEach(b=>{{
        if((filter!=='all'&&b.cat!==filter)||term&&!b.title.toLowerCase().includes(term)&&!b.desc.toLowerCase().includes(term))return;
        count++;
        let links='';
        if(b.yt) links+=`<a href="${{b.yt}}" target="_blank" rel="noopener">▶ YouTube</a>`;
        if(b.x) links+=`<a href="${{b.x}}" target="_blank" rel="noopener">𝕏 Twitter</a>`;
        html+=`<div class="card"><div class="card-head"><div class="card-icon-ph">${{b.title[0]}}</div><div class="card-title">${{b.title}}</div></div><div class="card-desc">${{b.desc}}</div><div class="card-foot"><span class="card-tag">${{b.cat}}</span><div class="card-links">${{links}}</div></div></div>`;
      }});
    }}
    grid.innerHTML=html||'<div style="grid-column:1/-1;text-align:center;color:var(--text2);padding:3rem">未找到匹配内容</div>';
    cnt.textContent=section==='tools'?`共 ${{count}} 个工具`:`共 ${{count}} 位推荐`;
  }}
  si.oninput=render;buildTabs();render();
}});
</script>
</body>
</html>'''

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

cat_counts = {}
for t in TOOLS:
    cat_counts[t['cat']] = cat_counts.get(t['cat'], 0) + 1
print(f"✅ Dashboard rebuilt: {len(TOOLS)} tools + {len(BLOGGERS)} bloggers")
for c in TOOL_CATS:
    print(f"   {c}: {cat_counts.get(c, 0)} tools")
bcats = {}
for b in BLOGGERS:
    bcats[b['cat']] = bcats.get(b['cat'], 0) + 1
for c in BLOGGER_CATS:
    print(f"   {c}: {bcats.get(c, 0)} bloggers")
