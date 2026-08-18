# 04. 核心护城河：AI 实时中英双向翻译与派单中台

本系统的核心竞争力在于：**彻底消除华人师傅的英语沟通障碍，将英国本土主流高客单客户无缝对接给华人师傅**。

## 1. 业务流程架构

```
【英国本地客户】                             【AI 翻译与调度中枢】                        【华人师傅】
      │                                                │                                      │
1. 在线提交英文表单/拨打虚拟电话                                   │                                      │
   "Need full bathroom tiled.                          │                                      │
   15 sqm, subway tiles, RG1 2AB"                      │                                      │
      │                                                │                                      │
      ▼                                                ▼                                      │
2. Webhook 触发 ──────────────────────────────► AI 清洗提取并转为标准中文工单                   │
                                                 - 项目: 卫浴贴砖 (约 15 平米)                 │
                                                 - 类型: 地铁砖 (Subway Tiles)                │
                                                 - 建议报价: £550 - £750                      │
                                                 - 区域: Reading RG1                          │
                                                       │                                      │
                                                       ▼                                      ▼
                                                推送到师傅微信群/Telegram ──────────────► 3. 师傅看到纯中文工单
                                                                                         点击【接单】，输入中文：
                                                                                         "下周二可开工，
                                                                                         工期3天，人工£600"
                                                       ▲                                      │
                                                       │                                      │
4. 客户收到纯正英式地道英文短信/WhatsApp ◄──────────────┴ AI 自动转译润色 ◄────────────────────────┘
   "Hi Sarah, our senior tiler can start                                                      
   next Tuesday. Estimated duration 3 days.                                                   
   Fixed labour quote is £600. Reply YES to book."                                            
```

---

## 2. 系统技术实现方案

1. **前端线索捕获**：
   * Webhook 实时触发（Next.js API Routes / Astro Endpoints）。
   * 收集字段：姓名、电话（英国手机号 07xxx）、完整 Postcode、房屋类型、时间要求、现场照片上传。
2. **AI 解析与结构化中转（LLM Engine）**：
   * 采用 Claude 3.5 Sonnet / DeepSeek-V3 提示词工程，提取关键工况、材料需求与报价建议。
3. **分发通路**：
   * 师傅端：企业微信 Webhook / Telegram Bot / 微信小程序通知。
   * 客户回传通道：Twilio Programmable SMS 或 WhatsApp Business API。
4. **商业变现扣费（Monetization Engine）**：
   * 师傅在系统中预充值（或绑定 Stripe），每次点击【查看客户电话/抢单】扣除 £25 ~ £50。