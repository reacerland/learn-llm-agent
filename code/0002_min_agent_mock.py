"""
第 2 课 · 最小可运行的 ReAct Agent —— 零依赖、无需 API key
============================================================
学习目标：看清 Agent 的「循环」到底长什么样。

关键认知（务必记住）：
  - 模型只负责「决定下一步要调用什么工具」；
  - 真正「执行」工具函数的，是【你自己的代码】；
  - 把执行结果喂回给模型，它才能据此决定再下一步。

运行：  python3 0002_min_agent_mock.py
（本文件不依赖任何第三方库，任何装了 Python 的机器都能跑。）
"""

from typing import Callable

# ──────────────────────────────────────────────
# 1) 工具：真正「做事」的 Python 函数（你的代码）
# ──────────────────────────────────────────────
def get_weather(city: str) -> str:
    # 真实场景：这里会去调某个天气 API。这里用假数据，方便演示。
    table = {"北京": "5°C，西北风 6 级", "上海": "22°C，多云"}
    return table.get(city, f"{city}：暂无数据")


def search_web(query: str) -> str:
    return f"搜索结果：关于「{query}」的 3 条链接（略）"


# 工具注册表：工具名 -> 函数。模型通过名字请求，我们通过名字找到函数。
TOOLS: dict[str, Callable] = {
    "get_weather": get_weather,
    "search_web": search_web,
}


# ──────────────────────────────────────────────
# 2) 一个「假的 LLM」：模拟模型决定下一步
#    —— 它不联网、不要 key，按脚本依次「请求」调用工具。
#    生产中你把整个 llm() 换成对 Anthropic / OpenAI 的真实调用，
#    下面的 run_agent() 循环【一行都不用改】。
# ──────────────────────────────────────────────
_script = [
    {"kind": "tool_use", "name": "get_weather", "input": {"city": "北京"}},
    {"kind": "text", "text": "今天北京 5°C 且大风，建议穿厚外套、围巾，注意防风保暖。"},
]
_step = [0]  # 用列表包一下，好在闭包里自增


def llm(messages):
    """模拟一次模型调用。真实模型会根据 messages 自行决定；这里按脚本走。"""
    action = _script[_step[0]]
    _step[0] += 1
    return action


# ──────────────────────────────────────────────
# 3) ★ Agent 的灵魂：这个 while 循环 ★
# ──────────────────────────────────────────────
def run_agent(user_task: str, max_steps: int = 5):
    messages = [{"role": "user", "content": user_task}]
    print(f"👤 任务: {user_task}\n")

    for step in range(max_steps):            # ← 循环
        response = llm(messages)             # ① 让模型决定下一步

        if response["kind"] == "tool_use":   # ② 模型【请求】调用工具
            name, args = response["name"], response["input"]
            print(f"🧠 Thought : 我需要调用 {name}({args})")
            print(f"⚙️  Action  : {name}(**{args})")
            result = TOOLS[name](**args)     # ③ 【你的代码】真正执行工具
            print(f"👁  Observe : {result}\n")
            # ④ 把结果喂回去，下一轮模型就能「看见」它
            messages.append({"role": "assistant", "content": f"request {name}({args})"})
            messages.append({"role": "user", "content": f"{name} => {result}"})
        else:                                # ②' 模型不再请求工具 → 给出最终答案
            print(f"✅ Final   : {response['text']}")
            return response["text"]

    print("⚠️ 达到最大步数，强制停止。")     # 保护：防止模型陷入死循环


if __name__ == "__main__":
    run_agent("今天北京适合穿什么？")
