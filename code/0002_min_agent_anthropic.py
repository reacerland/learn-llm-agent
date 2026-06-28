"""
第 2 课 · 最小 Agent（真实版）—— 使用 Anthropic Claude API
============================================================
⚠️ 这版需要 API key：  export ANTHROPIC_API_KEY="sk-ant-..."
   还需安装 SDK：       pip install anthropic

把它和 0002_min_agent_mock.py 放一起对比看：
  - TOOLS 注册表、run_agent() 循环【结构完全一样】；
  - 唯一的区别：llm() 从「脚本假模型」换成对 Claude 的真实调用。
  这正说明：Agent 的本质是「你的循环」，模型只是循环里的一步。

本文件未经运行（需要你的 key）。API 形态依据
https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview （2026-06 核实）。
"""

import os
import anthropic  # pip install anthropic

client = anthropic.Anthropic()  # 自动读取 ANTHROPIC_API_KEY 环境变量
MODEL = "claude-opus-4-8"       # 复杂工具/多步任务用 Opus；简单任务可换 Sonnet/Haiku 省钱

# ──────────────────────────────────────────────
# 1) 工具：和 mock 版一模一样
# ──────────────────────────────────────────────
def get_weather(city: str) -> str:
    # 真实场景：这里去调天气 API
    return f"{city}：5°C，西北风 6 级"  # 占位


def search_web(query: str) -> str:
    return f"搜索结果：关于「{query}」的 3 条链接（略）"


# 2a) 运行时：工具名 -> 函数
TOOLS = {"get_weather": get_weather, "search_web": search_web}

# 2b) 给模型看的「工具说明书」（JSON Schema）。模型靠它判断何时、怎么调。
TOOL_SPECS = [
    {
        "name": "get_weather",
        "description": "获取指定城市的实时天气。",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "城市名，如 北京"}},
            "required": ["city"],
        },
    },
    {
        "name": "search_web",
        "description": "在网页上搜索一个查询词。",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "搜索词"}},
            "required": ["query"],
        },
    },
]


# ──────────────────────────────────────────────
# 3) 真实的 llm()：把 messages 交给 Claude，拿回它的决定
# ──────────────────────────────────────────────
def llm(messages):
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        tools=TOOL_SPECS,
        messages=messages,
    )
    return resp  # 返回原始 response，循环里再解析


# ──────────────────────────────────────────────
# 4) ★ 循环：和 mock 版几乎一字不差 ★
# ──────────────────────────────────────────────
def run_agent(user_task: str, max_steps: int = 5):
    messages = [{"role": "user", "content": user_task}]
    print(f"👤 任务: {user_task}\n")

    for step in range(max_steps):
        resp = llm(messages)

        # 找出本轮模型请求调用的工具（可能多个）
        tool_uses = [b for b in resp.content if b.type == "tool_use"]

        if not tool_uses:                       # 模型不再请求工具 → 给最终答案
            text = "".join(b.text for b in resp.content if b.type == "text")
            print(f"✅ Final : {text}")
            return text

        # ① 先把模型的请求原样记进对话（必须保留 assistant 这条）
        messages.append({"role": "assistant", "content": resp.content})

        # ② 逐个执行工具，收集 tool_result
        results = []
        for tu in tool_uses:
            print(f"⚙️  Action : {tu.name}({tu.input})")
            result = TOOLS[tu.name](**tu.input)  # 【你的代码】真正执行
            print(f"👁  Observe: {result}\n")
            results.append({
                "type": "tool_result",
                "tool_use_id": tu.id,
                "content": str(result),
            })

        # ③ 把所有结果作为一条 user 消息喂回去
        messages.append({"role": "user", "content": results})

    print("⚠️ 达到最大步数，强制停止。")


if __name__ == "__main__":
    run_agent("今天北京适合穿什么？")
