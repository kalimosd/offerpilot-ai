# OfferPilot AI

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=flat&logo=playwright&logoColor=white)](https://playwright.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

这是 **OfferPilot Skill Pack 分支**。

这个分支的主入口是 `skill-pack/`。它提供一套可移植的求职工作流文档、规则、模板和本地 helper scripts，给 Cursor、Claude Code、Codex 等 AI 编程工具使用。

如果你想运行 LangGraph Agent、CLI 或 Web UI，请切换到 `offerpilot-agent` 分支。

[English](./README_en.md)

## 适合谁使用

使用这个分支，如果你想：

- 让 AI 编程工具按照固定流程优化简历
- 做 JD 匹配分析和 10 维结构化评估
- 针对具体岗位改写简历
- 生成求职信、LinkedIn 外联消息
- 做模拟面试和产品研究准备
- 用本地脚本提取文本、渲染 PDF、校验输入输出

## 如何开始

1. 打开 `skill-pack/README.md`
2. 按 Start Order 阅读对应文档
3. 根据任务类型选择具体 workflow：
   - `JD_MATCHING.md`
   - `EVALUATION.md`
   - `MOCK_INTERVIEW.md`
   - `PRODUCT_RESEARCH.md`
   - `TRACKER.md`
   - `OUTREACH.md`
4. 需要脚本时查看 `skill-pack/scripts/README.md`
5. 如果你的 AI 工具支持 repo-local skill，查看 `skill-pack/adapters/`

## Skill Pack 包含什么

```text
skill-pack/
├── README.md              # Skill Pack 入口
├── WORKFLOW.md            # 通用任务流程
├── INPUTS.md              # 输入选择和隐私规则
├── OUTPUTS.md             # 输出格式和质量检查
├── PROMPTS.md             # 可复用提示词约束
├── DATASTORE.md           # profile_store.yaml 规范
├── JD_MATCHING.md         # JD 匹配分析
├── EVALUATION.md          # 10 维结构化岗位评估
├── MOCK_INTERVIEW.md      # 模拟面试
├── PRODUCT_RESEARCH.md    # 产品研究
├── TRACKER.md             # 申请状态追踪
├── OUTREACH.md            # LinkedIn 外联
├── templates/             # 本地模板
├── data/                  # 技能别名等辅助数据
├── examples/              # 示例
├── scripts/               # 本地辅助脚本
└── adapters/              # Cursor / Claude Code / Codex 适配器
```

## 本地脚本

这些脚本是可选辅助工具，不要求你运行完整 Agent。

```bash
python skill-pack/scripts/validate_inputs.py profile_store.yaml jds/example.md
python skill-pack/scripts/extract_text.py resume.pdf
python skill-pack/scripts/render_pdf.py outputs/resumes/resume.md outputs/resumes/resume.pdf
python skill-pack/scripts/validate_outputs.py outputs/resumes/resume.md
```

## 与 Agent 分支的关系

OfferPilot 有两种发行形态：

- `offerpilot-skill`：规则层 / workflow / portable skill pack
- `offerpilot-agent`：可运行 Agent / CLI / Web UI

建议把 `offerpilot-skill` 理解成 OfferPilot 的方法论和规则层；`offerpilot-agent` 是消费这套规则层的运行时产品。

本分支可能仍保留少量历史 runtime 文件，但它们不是这个分支的主入口。

## 写在最后

工作很重要。离开学校以后，它不声不响地占据了你醒着的大部分时间。

但工作又没那么重要。人不是为了优化 bullet point 而来到这个世界上的。

你做过真实的事。你解决过真实的问题。你加过班、赶过 deadline、替别人擦过屁股，但没人好好写下来，你自己也没有。

这个项目改变不了你的人生。但如果它能帮一个人不再低估自己，不再把同一份万能简历投进黑洞，真正拿到一个配得上的面试机会，那就够了。

去拿 offer 吧。然后合上电脑，好好生活。
