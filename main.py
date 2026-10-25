"""
电商运营自动化 Agent
====================
用户用自然语言下达运营指令，Agent 自动判断该调用哪个工具完成任务。
对标企业级 RPA + LLM Agent 场景。
"""
import json
from openai import OpenAI
from tools.order_tools import query_order, refund_order, send_reminder

# ============ 配置 ============
# 建议把 key 存在环境变量里，不要硬编码在代码中（尤其上传GitHub前）
MY_API_KEY = "在这里填你的DeepSeek-Key"

client = OpenAI(api_key=MY_API_KEY, base_url="https://api.deepseek.com")
MODEL = "deepseek-chat"

# ============ 工具注册 ============
# 函数名 -> 实际函数 的映射
AVAILABLE_FUNCTIONS = {
    "query_order": query_order,
    "refund_order": refund_order,
    "send_reminder": send_reminder,
}

# 告诉大模型有哪些工具可用
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "query_order",
            "description": "根据订单号查询订单状态、物流和价格",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "订单号，比如1001、1002"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "refund_order",
            "description": "对指定订单发起退款申请",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "要退款的订单号"},
                    "reason": {"type": "string", "description": "退款原因"}
                },
                "required": ["order_id", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_reminder",
            "description": "给指定订单的买家发送一条提醒消息",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "订单号"},
                    "message": {"type": "string", "description": "要发送的消息内容"}
                },
                "required": ["order_id", "message"]
            }
        }
    }
]


def run_agent(user_question: str, max_loops: int = 5):
    """运行Agent主循环"""
    print(f"💬 用户: {user_question}\n" + "=" * 50)
    messages = [{"role": "user", "content": user_question}]

    for loop in range(max_loops):
        print(f"\n[--- 第 {loop+1} 轮思考 ---]")
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS
        )
        msg = resp.choices[0].message

        if msg.tool_calls:
            messages.append(msg)
            for call in msg.tool_calls:
                func_name = call.function.name
                args = json.loads(call.function.arguments)
                print(f"  → 调用工具: {func_name}")
                print(f"  → 参数: {args}")

                func = AVAILABLE_FUNCTIONS[func_name]
                result = func(**args)
                print(f"  → 结果: {result}\n")

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result)
                })
        else:
            print("=" * 50)
            print(f"🤖 Agent: {msg.content}")
            return

    print("[警告] 达到最大轮次仍未结束，已强制停止")


if __name__ == "__main__":
    # 在这里输入你的运营指令，自己试
    run_agent("帮我查一下订单1002的状态，如果还没发货，就给买家发个消息提醒仓库优先处理")
