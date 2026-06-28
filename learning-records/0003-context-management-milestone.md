# 第 3 课里程碑：记忆、上下文管理与「上生产」分水岭

2026-06-29。课程到达「Agent 能否上生产」的认知分水岭。

## 已建立的核心框架（决策级，后续课程据此展开）
1. **两种记忆**：上下文内（in-context，受窗口限制、贵）vs 外部（external，无限、需检索）。第 2 课的「记忆 = messages」被正确定为「上下文内记忆」。
2. **应对上下文膨胀的三策略**：滑动窗口（最省/丢信息）→ 摘要压缩（省空间+保要点）→ RAG（容量无限/复杂）。三者可组合。
3. **2026 心智升级**：从 prompt engineering 到 **context engineering**——优化「填进窗口的信息环境」而非只优化问题。
4. **Prompt caching**：另一维度，不减 token 但成本↓90%/延迟↓85%，靠稳定前缀前缀匹配。上生产必杀技。
5. **RAG vs 长上下文决策表**（实测：单文档深推理长上下文 +34%；跨文档综合 RAG +67% 且省 8 倍；共识=混合）。

## 验证资产
- `code/0003_context_management_demo.py` —— 零依赖、无需 key，**已亲自运行验证**。诚实数字：原始 55 / 滑动窗口 15 / 摘要压缩 43 tokens。
  - 修正记录：初版对话历史太短，导致「摘要压缩」反比原始更费 token，与教学论点矛盾；已加长历史修复，使对比诚实可信。

## 一手主源（已联网核实）
- [Effective Context Engineering for AI Agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)（头号主源）
- Prompt caching 数据：Anthropic 官方（cache_control / 4 断点 / 前缀匹配）
- RAG vs 长上下文数字：Redis、LlamaIndex、arXiv:2501.01880 等多家 2026 对比

## Implications（对后续课程的指引）
- 用户已具备「上下文是稀缺资源」的直觉，第 4 课（工具设计）可自然引出「工具结果也是上下文开销，要精简返回」。
- 用户求职线强烈，决策表与生产数据（caching 90% 降本）是高频面试点，后续课程继续穿插「面试常问」标注。
- 混合架构（RAG + 长上下文）是未来项目课的天然选题。

_术语 in-context/external memory、滑动窗口、摘要压缩、RAG、context engineering、prompt caching 已收入 [[GLOSSARY.md]]。_
