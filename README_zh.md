# OfferPilot AI

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=flat&logo=playwright&logoColor=white)](https://playwright.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

OfferPilot 是一个本地优先的 AI 求职 Agent，用来做简历改写、JD 匹配、岗位扫描、批量评估和申请追踪。

它的底线很简单：**只使用你的真实经历，不编项目、不编数据、不编联系方式。**

[English](./README.md)

## 这个项目是什么

OfferPilot 有三种入口：

- **Agent CLI**：主入口。你用自然语言描述任务，LangGraph Agent 自动判断流程和调用工具。
- **Web UI**：本地聊天界面，包含 Chat、Tracker、Outputs。
- **Skill Pack**：给 Cursor、Claude Code、Codex 等 AI 编程工具使用的一套工作流文档和脚本。

现在 Agent 不是单纯的“LLM 自己想怎么调工具”。它会先做意图路由：

- 普通求职任务走通用 ReAct 工具循环。
- pipeline 任务走固定的扫描、排序、报告流程。
- 批量 JD 评估走专门的批处理流程，用低温度 LLM 保持评分稳定。

## 能做什么

- 优化通用简历：精炼表达，强化 bullet point，不编造经历。
- 针对 JD 改写简历：围绕目标岗位重排和重写内容。
- 做 JD 匹配分析：找匹配点、差距和修改优先级。
- 批量评估 JD：快速判断哪些岗位值得投。
- 扫描招聘网站：把最近新增岗位排序成推荐报告。
- 追踪申请状态：管理 `discovered`、`applied`、`interviewing`、`offer`、`rejected`、`ghosted`。
- 生成求职信、LinkedIn 外联、模拟面试题、产品研究材料。
- 把 Markdown 输出导出成 PDF。

## 环境要求

- Python 3.10+
- 如果要跑 Web UI，需要 Node.js 18+
- 至少一个 LLM API key，例如 DeepSeek、Claude、Gemini 或 OpenAI
- 推荐安装 Playwright Chromium，用于 PDF 渲染和部分网页扫描能力

## 安装

```bash
git clone https://github.com/kalimosd/offerpilot-ai.git
cd offerpilot-ai

python -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
python -m playwright install chromium
```

如果只跑 Agent，不跑测试，可以用：

```bash
pip install -e .
```

`.[dev]` 主要额外安装 `pytest`。

## 配置 LLM

在项目根目录创建 `.env`：

```bash
touch .env
```

然后按你使用的模型填写其中一种配置。

### DeepSeek

```bash
OFFERPILOT_MODEL=deepseek-chat
OFFERPILOT_API_KEY=your-deepseek-key
OFFERPILOT_BASE_URL=https://api.deepseek.com
```

### Claude

```bash
OFFERPILOT_MODEL=claude-sonnet-4-20250514
ANTHROPIC_API_KEY=your-anthropic-key
```

### Gemini

```bash
OFFERPILOT_MODEL=gemini-2.0-flash
GOOGLE_API_KEY=your-google-key
```

### OpenAI

```bash
OFFERPILOT_MODEL=gpt-4o-mini
OPENAI_API_KEY=your-openai-key
```

可选：覆盖默认温度。

```bash
OFFERPILOT_TEMPERATURE=0.3
```

代码里也有任务默认值：普通 Agent 任务 `0.3`，JD/简历评估类精确任务 `0.1`，创意写作类任务 `0.7`。

## 准备个人资料和 JD

先创建个人素材库：

```bash
cp skill-pack/templates/profile_store.yaml profile_store.yaml
```

然后编辑 `profile_store.yaml`。建议尽量写全，不要一开始就精简。Agent 会根据 JD 选择最相关的材料。

重点字段：

- `meta`：姓名、邮箱、电话、更新时间
- `experience`：工作经历，每段经历下面写多个 bullet
- `projects`：个人项目、开源项目、比赛、校园项目
- `skills`：技能、熟练度、使用证据
- `education`、`certifications`、`achievements`

把 JD 放到 `jds/`：

```bash
mkdir -p jds outputs/resumes outputs/pipeline outputs/interview outputs/research outputs/misc
```

示例结构：

```text
jds/
  anthropic-ai-agent-engineer.md
  meituan-algorithm-engineer.md
```

`profile_store.yaml`、`jds/`、`outputs/`、`data/` 都是本地私有数据，默认不应该提交到 git。

## 运行 Agent

单次模式：

```bash
python -m offerpilot.agent "分析 jds/anthropic-ai-agent-engineer.md 和 profile_store.yaml 的匹配度"
python -m offerpilot.agent "批量评估 jds/ 目录下所有 JD"
python -m offerpilot.agent "运行 pipeline，扫描最近 7 天的岗位，推荐 Top 10"
python -m offerpilot.agent "查看有哪些申请需要跟进"
```

多轮交互模式：

```bash
python -m offerpilot.agent
```

进入后可以输入：

```text
帮我优化 profile_store.yaml 里的简历素材
针对 jds/anthropic-ai-agent-engineer.md 做定向改写
把最新简历导出成 PDF
exit
```

也可以使用安装后的命令：

```bash
offerpilot-agent "批量评估 jds/ 目录下所有 JD"
```

## Web UI

Web UI 使用 FastAPI 后端和 Next.js 前端。

先安装 Web 依赖：

```bash
source .venv/bin/activate
pip install -r web/api/requirements.txt

cd web/frontend
npm install
cd ../..
```

一条命令启动：

```bash
./start.sh
```

打开：

```text
http://localhost:3000
```

手动启动方式：

```bash
# 终端 1
source .venv/bin/activate
uvicorn web.api.main:app --port 8000

# 终端 2
cd web/frontend
npm run dev -- --port 3000
```

## Skill Pack 模式

如果你不是直接跑 OfferPilot Agent，而是想让 Cursor、Claude Code、Codex 这类工具按照一套文档流程工作，就使用 `skill-pack/`。

建议阅读顺序：

1. `skill-pack/WORKFLOW.md`
2. `skill-pack/INPUTS.md`
3. 国内岗位匹配任务阅读 `skill-pack/JD_MATCHING.md`
4. `skill-pack/PROMPTS.md`
5. `skill-pack/OUTPUTS.md`
6. 需要本地脚本时阅读 `skill-pack/scripts/README.md`
7. 需要平台适配时阅读 `skill-pack/adapters/`

常用脚本：

```bash
python skill-pack/scripts/validate_inputs.py profile_store.yaml jds/example.md
python skill-pack/scripts/extract_text.py resume.pdf
python skill-pack/scripts/render_pdf.py outputs/resumes/resume.md outputs/resumes/resume.pdf
python skill-pack/scripts/validate_outputs.py outputs/resumes/resume.md
```

Agent 里也已经接入 `validate_inputs` 和 `validate_outputs`，可以在对话流程里自动调用。

## Pipeline 是什么

这里的 pipeline 指“岗位扫描和推荐流程”，不是泛泛的数据管道。

它做五件事：

1. 根据配置扫描招聘网站。
2. 从 `data/scan-history.tsv` 读取最近新增岗位。
3. 根据职位配置、个人 profile 标签、中英技能别名打分。
4. 去重并排序。
5. 写出 `outputs/pipeline/pipeline_recommendations.md`。

示例：

```bash
python -m offerpilot.agent "运行 pipeline，扫描最近 14 天，推荐前 20 个国内岗位"
```

## 开发和验证

运行测试：

```bash
source .venv/bin/activate
python -m pytest
```

检查 Agent 图是否能编译：

```bash
python - <<'PY'
from unittest.mock import Mock, patch
from offerpilot.graph import build_graph

with patch("offerpilot.graph.get_llm") as get_llm:
    llm = Mock()
    llm.bind_tools.return_value.invoke.return_value = "ok"
    get_llm.return_value = llm
    print(type(build_graph()).__name__)
PY
```

期望输出：

```text
CompiledStateGraph
```

## 项目结构

```text
.
├── offerpilot/
│   ├── agent.py            # CLI 入口
│   ├── graph.py            # LangGraph 路由和工作流
│   ├── intent.py           # 意图识别
│   ├── llm.py              # 多 provider LLM 初始化
│   ├── script_loader.py    # legacy script 加载器
│   ├── state.py            # 图状态
│   └── tools.py            # Agent tools
├── skill-pack/             # 工作流文档、适配器、脚本和数据
├── web/
│   ├── api/                # FastAPI 后端
│   └── frontend/           # Next.js 前端
├── tests/                  # 测试
├── outputs/                # 本地生成结果
├── jds/                    # 本地 JD
├── data/                   # tracker 和扫描历史
└── profile_store.yaml      # 本地个人素材库
```

## 写在最后

工作很重要。离开学校以后，它不声不响地占据了你醒着的大部分时间。

但工作又没那么重要。人不是为了优化 bullet point 而来到这个世界上的。

你做过真实的事。你解决过真实的问题。你加过班、赶过 deadline、替别人擦过屁股，但没人好好写下来，你自己也没有。

这个项目改变不了你的人生。但如果它能帮一个人不再低估自己，不再把同一份万能简历投进黑洞，真正拿到一个配得上的面试机会，那就够了。

去拿 offer 吧。然后合上电脑，好好生活。
