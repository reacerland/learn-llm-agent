# AI Agent 开发与前沿研究 — Resources

> 高可信度资源库。所有课程内容优先从此处取材，而非凭记忆。
> 每条都标注：**覆盖什么 / 何时查阅**。
> 最后更新：2026-06-28

## Knowledge（知识 · 一手权威）

### 基础心智模型（入门必读）

- [Building Effective AI Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)
  Anthropic 工程团队的经验总结。**何时查**：建立「workflow vs agent」的核心区分；判断什么时候该用 agent、什么时候不该。配套演讲：[How We Build Effective Agents (YouTube)](https://www.youtube.com/watch?v=D7_ipDqhtwk)。

- [LLM Powered Autonomous Agents — Lilian Weng (Lil'Log)](https://lilianweng.github.io/posts/2023-06-23-agent/)
  业界公认的 Agent 综述级长文。**何时查**：理解经典公式 `Agent = LLM + 规划(Planning) + 记忆(Memory) + 工具使用(Tool Use)`，以及每部分的拆解。（[中文翻译参考](https://zhuanlan.zhihu.com/p/641322714)）

### 经典论文（研究线）

- [ReAct: Synergizing Reasoning and Acting in Language Models — arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
  Yao et al., ICLR 2023。**何时查**：几乎所有现代 Agent 循环的思想源头。读懂它=拿到 Agent 的「底层语法」。[代码仓库](https://github.com/ysymyth/ReAct) · [Google Research 解读](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/)

### 工程落地（求职线）

- [A Practical Guide to Building Agents — OpenAI](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) · [PDF](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
  ~34 页实战手册。**何时查**：模型选型、工具设计、guardrails、多 agent 编排——面试常问的工程问题。

- [Anthropic 官方文档 · Build with Claude（Agents / Tool use）](https://docs.anthropic.com/en/docs/build-with-claude/agent-tool-use)
  **何时查**：动手写代码时的 API 参考（tool use、prompt caching、thinking 等）。

### 待补充（Gaps）
- _（随着课程推进，会逐步补充：evaluation/evals、memory/向量检索、planning、multi-agent、MCP 等专题的一手资源）_

## Wisdom（智慧 · 社区）

- [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) — 高信号社区，开源模型与 agent 实践的前沿讨论。
- [Hugging Face Daily Papers](https://huggingface.co/papers) — 每日新论文跟踪，研究线必备。
- [LangChain / LlamaIndex 官方文档](https://python.langchain.com/) — 仅作「框架对比」参考；课程主线先用最小依赖讲清原理，再对比框架。

---
_资源会持续校准：错的、浅的、偏离 mission 的会被删掉，宁可少而精。_
