# 电商运营自动化 Agent

基于 LLM Function Calling 的多工具智能体，模拟企业级电商运营自动化场景。

## 它能干什么

用自然语言下达运营指令，Agent 自动拆解任务、选择工具、执行并汇总结果。例如：

> 用户说："帮我查一下订单1002的状态，如果还没发货，就给买家发个消息提醒仓库优先处理"

Agent 会自动：
1. 调用 `query_order` 查询订单1002 → 发现是"待发货"
2. 调用 `send_reminder` 给买家发提醒消息
3. 把整个过程用人话总结给用户

## 技术栈

- **大模型**：DeepSeek-Chat（OpenAI 兼容 API）
- **核心能力**：Function Calling（工具调用）
- **语言**：Python 3.11
- **依赖**：openai SDK

## 项目结构

```
ecommerce-agent/
├── main.py              # 主程序入口，Agent循环在这里
├── tools/
│   └── order_tools.py   # 业务工具函数（查订单/退款/发提醒）
├── requirements.txt     # Python依赖
└── README.md
```

## 如何运行

1. 安装依赖：`pip install -r requirements.txt`
2. 在 `main.py` 里填入你的 DeepSeek API Key
3. 运行：`python main.py`

## 设计思路

- **大模型负责"想"**：判断用户意图、决定调用哪个工具、提取参数
- **代码负责"干"**：真实执行查订单、退款、发消息等动作
- **防死循环**：最多5轮工具调用，避免大模型陷入循环
- **可扩展**：新增工具只需在 `order_tools.py` 写函数 + 在 `TOOLS` 注册 + 在 `AVAILABLE_FUNCTIONS` 映射

## 当前局限

- 数据是模拟的（FAKE_ORDER_DB），真实场景会接电商开放平台API
- 没有做 RAG（知识库问答），后续可以接入店铺规则文档
- 没有对话记忆，每次运行都是独立会话

## 后续计划

- [ ] 接入真实电商API（如抖店/淘宝开放平台）
- [ ] 加入RAG，让Agent基于店铺规则回答
- [ ] 加Web界面，非技术人员也能用
