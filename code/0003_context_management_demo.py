"""
第 3 课 · 上下文管理演示（零依赖，无需 key）
================================================
把抽象问题变具体：第 2 课的「记忆 = messages」会随对话无限增长，
导致 ① token 成本爆炸 ② 最终撑爆上下文窗口。

本演示展示三种应对，并打印 token 估算的变化，让你直观看到「省了多少」。
运行：python3 code/0003_context_management_demo.py
"""


def est_tokens(messages) -> int:
    """粗略估算 token。英文约 4 字符/token，中文约 1.5 字符/token，
    这里取通用近似（÷3）仅用于演示【相对】变化；精确计费请用官方 tokenizer。"""
    chars = sum(len(m["content"]) for m in messages)
    return max(1, chars // 3)


def show(label, messages):
    print(f"  · {label:<22} {len(messages)} 条消息 ≈ {est_tokens(messages)} tokens")


def build_history():
    """模拟一段【已经较长】的会话历史。对话越长，下面的对比越明显。"""
    turns = [
        ("user", "用户：帮我查北京天气"),
        ("assistant", "助手：北京 5°C，西北风 6 级"),
        ("user", "用户：上海呢"),
        ("assistant", "助手：上海 22°C，多云"),
        ("user", "用户：广州"),
        ("assistant", "助手：广州 30°C，闷热"),
        ("user", "用户：成都"),
        ("assistant", "助手：成都 18°C，小雨"),
        ("user", "用户：哈尔滨"),
        ("assistant", "助手：哈尔滨 -8°C，大雪"),
        ("user", "用户：昆明"),
        ("assistant", "助手：昆明 20°C，晴"),
        ("user", "用户：综合看哪个城市最冷"),
        ("assistant", "助手：哈尔滨 -8°C 最冷"),
        ("user", "用户：那最暖的是"),
        ("assistant", "助手：广州 30°C 最暖"),
    ]
    return [{"role": r, "content": c} for r, c in turns]


# ── 策略 A：滑动窗口（只留最近 K 条，直接丢最旧的）──
def sliding_window(messages, keep_last=4):
    return messages[-keep_last:]


# ── 策略 B：摘要压缩（把旧消息合成一条摘要，保留要点）──
def summarize_old(messages, keep_last=4):
    old, recent = messages[:-keep_last], messages[-keep_last:]
    summary = ("【历史摘要】用户查询了北京/上海/广州/成都/哈尔滨/昆明天气"
               "（5°C大风·22°C多云·30°C闷热·18°C雨·-8°C雪·20°C晴）；"
               "最冷哈尔滨，最暖广州。")
    return [{"role": "system", "content": summary}] + recent


if __name__ == "__main__":
    msgs = build_history()

    print("=== 问题：messages 越攒越多 ===")
    show("完整历史（原始）", msgs)
    print("  ↑ 对话一长，这串会一直涨，直到撑爆上下文窗口。\n")

    print("=== 策略 A：滑动窗口（留最近 4 条，丢最旧的）===")
    a = sliding_window(msgs, keep_last=4)
    show("滑动窗口", a)
    print("  ✅ 最简单、最省。  ❌ 北京天气的原始信息被直接丢弃。\n")

    print("=== 策略 B：摘要压缩（旧消息 → 一条摘要）===")
    b = summarize_old(msgs, keep_last=4)
    show("摘要压缩", b)
    print("  ✅ 既省空间、又保住了关键事实。  ⚠️ 代价：摘要本身需要一次模型调用。\n")

    print("=== 三种方式 token 对比 ===")
    show("原始", msgs)
    show("滑动窗口", sliding_window(msgs))
    show("摘要压缩", summarize_old(msgs))

    print("\n=== 关键认知 ===")
    print("  · 第 2 课的「记忆 = messages」是【上下文内记忆】，受上下文窗口硬限制。")
    print("  · 窗口装不下时：压缩（滑动 / 摘要）或 把记忆搬到【外部】按需取回（RAG）。")
    print("  · 另一维度：prompt caching 不减少 token，但能把【稳定前缀】缓存起来，")
    print("    成本 ↓90%、延迟 ↓85% —— 这是上生产的必杀技。")
