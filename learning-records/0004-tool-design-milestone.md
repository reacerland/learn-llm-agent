# 第 4 课里程碑：工具设计进阶

2026-06-29。课程从「工具的机制」推进到「工具的设计」。

## 已建立的核心原则（决策级）
1. **描述为王**：工具发现是按「名字 + 描述」匹配；描述是影响调用准确率最大的因素（官方要求 extremely detailed descriptions）。
2. **好工具四原则**：动词+名词的名字（含命名空间化前缀）/ 描述答三问（何时用·做什么·返回什么）/ 参数自解释+enum+required / 少而精。
3. **错误当数据返回**：工具失败不抛异常，格式化为错误字符串喂回模型 → 自我纠正；配最大重试防死循环。属 tool-grounded（可验证）纠错。
4. **并行工具调用**：一轮多工具需全部执行、结果合并为一条喂回；有依赖时串行；能减轮数、提性能（生产常见 5–10 并发）。

## 验证资产
- `code/0004_tool_design_demo.py` —— 零依赖、无需 key，**已亲自运行验证**。真实输出清晰演示：① 错误自愈（南京→ERROR→纠正成北京）；② 并行调用（一轮 2 工具，结果一起返回）。

## 一手主源（已联网核实）
- [Writing effective tools for AI agents — Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Define tools 官方文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
- [Parallel tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use)
- 错误处理共识：多来源（Towards AI、LangChain forum、arXiv:2509.18847）

## Implications（对后续课程的指引）
- 容错范式（错误当数据 + 最大重试）将在第 5 课 Planning、后续 Multi-agent、个人项目中反复复用——已是基线认知。
- 用户求职线：本课的「错误处理 + 并行」是高频面试点，已标注。
- 研究线：self-correction 的 epistemic vs tool-grounded 区分是热点，可供用户深挖。
- 工具数「少而精 + 命名空间化」为后续「工具路由 / 动态工具发现」埋下伏笔。

_术语 命名空间化、并行工具调用、错误当数据返回 已收入 [[GLOSSARY.md]]。_
