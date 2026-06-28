"""
第 4 课 · 工具设计演示（零依赖，无需 key）
================================================
演示两个进阶技能：
  A) 工具出错 → 返回【错误字符串】而非抛异常 → 模型据此自我纠正（不中断循环）
  B) 并行调用：模型一轮请求多个工具 → 你的代码全部执行、一起把结果喂回去

运行：python3 code/0004_tool_design_demo.py
"""


# ── 工具：注意出错时返回错误【字符串】，而不是 raise 异常 ──
def get_weather(city: str) -> str:
    table = {"北京": "5°C，西北风 6 级", "上海": "22°C，多云"}
    if city not in table:
        # 关键：错误也用字符串返回，并告诉模型「错在哪 / 可选项」，方便它纠正
        return f"ERROR: 没有城市「{city}」的数据。可选城市：{list(table)}"
    return table[city]


def get_time(timezone: str) -> str:
    return f"{timezone} 当前 14:30"


TOOLS = {"get_weather": get_weather, "get_time": get_time}


# ── 脚本：模拟模型在多轮里的决策（生产中由真实模型给出）──
#   第1轮：错误地查了「南京」  → 触发错误恢复
#   第2轮：纠正成「北京」，且【同时】要查时间 → 并行调用
#   第3轮：给出最终答案
_script = [
    [{"name": "get_weather", "input": {"city": "南京"}}],
    [{"name": "get_weather", "input": {"city": "北京"}},
     {"name": "get_time",   "input": {"timezone": "北京"}}],
]
_final = "北京现在 14:30，5°C 且大风，建议穿厚外套、注意防风保暖。"
_step = [0]


def llm(messages):
    """模拟模型一轮的决策：返回本轮要调用的工具列表；为空则给最终答案。"""
    if _step[0] >= len(_script):
        return {"final": _final}
    actions = _script[_step[0]]
    _step[0] += 1
    return {"tool_calls": actions}


def run_agent(task: str, max_turns: int = 5):
    messages = [{"role": "user", "content": task}]
    print(f"👤 任务: {task}\n")

    for turn in range(1, max_turns + 1):
        resp = llm(messages)

        if "final" in resp:                       # 模型不再要工具 → 最终答案
            print(f"✅ Final : {resp['final']}")
            return

        calls = resp["tool_calls"]
        n = len(calls)
        print(f"── 第 {turn} 轮：模型请求 {n} 个工具" + ("（并行）" if n > 1 else "") + " ──")

        had_error = False
        results = []
        for c in calls:
            name, args = c["name"], c["input"]
            out = TOOLS[name](**args)             # 即使错误，也正常返回（不抛异常）
            print(f"⚙️  Action  : {name}({args})")
            print(f"👁  Observe : {out}")
            if str(out).startswith("ERROR"):
                had_error = True
                print(f"🛠  处理   : 工具返回错误，但循环【不中断】——喂回模型，让它自己改。")
            results.append(f"{name}({args}) => {out}")

        # 把【所有】结果作为一条消息喂回（并行时多个结果合并到同一条）
        messages.append({"role": "user", "content": " | ".join(results)})
        print()

    print("⚠️ 达到最大轮数，停止。")               # 兜底


if __name__ == "__main__":
    run_agent("查一下北京现在几点、天气如何，给我穿搭建议。")
