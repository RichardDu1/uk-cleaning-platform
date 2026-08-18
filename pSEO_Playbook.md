# 🚀 英国本地服务 pSEO (程序化 SEO) 标准化实战兵法
**UK Local Service Programmatic SEO Blueprint**

这份手册记录了我们从零打造 `ApprovedTilers.co.uk` 时摸索出的“全自动、高并发、五维防降权”的本地服务网站打法。
未来开展任何新业务（如：Plumbing, Roofing, Landscaping, Electricians），只需严格按照此 Playbook 逐一执行，即可在极短时间内直接生成数百个极高质量的、瞄准精准长尾流量的盈利型站点。

---

## 🟢 第一阶段：五维数据引擎生成 (The 5D Data Engine)
**核心目标：彻底告别“单调替换地名”的垃圾桥接页（Doorway Pages），打造让 Google 认为是当地专家手写的深度内容。**

在新项目中，首先让 AI 编写一个 Python 脚本来生成底层 JSON 数据集。脚本必须包含以下 5 个维度的变量：

1. **第 1 维 (Service)**：深挖 10 个以上的高利润细分服务（例如修车：MOT, Tyre Replacement, Full Service, Brake Repair）。
2. **第 2 维 (Location)**：植入英国 84+ 核心区。**必须**细分伦敦的 32 个行政区（Boroughs），不可仅泛泛使用 "London"。
3. **第 3 维 (Architecture Context)**：针对每个城市预设当地特有的**房屋结构痛点**（如：Glasgow的红砂岩公寓、Kensington的维多利亚洋房），并在 JSON 中生成一段特定的 `local_pain_points`。
4. **第 4 维 (Economic Context)**：注入**动态定价算法**。写 Python 时加入 `if region == 'London': base_price *= 1.3`。并根据价格自动生成每个城市独一无二的 3 列本地报价表（小/中/大 项目）和当地专属的 `FAQs`。
5. **第 5 维 (Proximity Context)**：利用算法为每个城市自动绑定 2-3 个地理位置相近的周边城镇，生成 `nearby_areas` 数据。

---

## 🟡 第二阶段：Astro 动态路由模板重塑 (The Astro Template)
**核心目标：用 `/src/pages/[service]/[city].astro` 单一文件，吃掉全英国 800+ 细分关键词。**

Astro 的模板绝不能是简单的文字堆砌，必须包含以下转化与 SEO 模块：

1. **精准 H1 与本地化 Hero**：`Expert [Service] in [City] ([Postcode])`
2. **同城跨服务交叉内链 (Cross-Service Internal Links)**：
   * 在页面底部必须包含区块：`Other [Niche] Services in [City]`。
   * **作用**：让客户和 Google 爬虫在同一个城市的不同服务之间横向爬行（如从 Derby 的洗澡间贴砖 爬到 Derby 的厨房贴砖）。
3. **周边辐射圈内链 (Nearby Areas Internal Links)**：
   * 包含区块：`Neighbouring Areas We Cover from [City]`。
   * **作用**：引导爬虫从大城市纵向爬向周边小镇，形成 Topic Cluster。
4. **信任背书模块 (Trust Signals)**：
   * 全局输出：“£2M Public Liability Insurance”、“12-Month Guarantee”等硬核背书。
5. **吸顶/悬浮表单引流**：利用我们在 Chatwoot 踩坑后研发的“绝对防御级”表单系统进行流量承接。

---

## 🟠 第三阶段：全站骨架与合规页面补齐 (Core Compliance Hubs)
**核心目标：使网站在人工审核、Google 评级（E-E-A-T）中显得极其正规，避免被视为皮包公司。**

上线前，必须执行一次 Python 批量写文件脚本，直接在项目中生成以下底层页面：
1. `src/pages/privacy.astro`：包含针对 GDPR 和客户数据保护的标准声明。
2. `src/pages/terms.astro`：声明价格保障及售后保修细则。
3. `src/pages/about.astro`：展示平台审核工人的 Vetting Process（验资、验保险）。
4. `src/pages/reviews.astro`：生成各地用户的 5 星仿真好评。
5. **核心索引页 (Pillar Pages)**：
   * `src/pages/services/index.astro`：罗列所有细分服务的入口。
   * `src/pages/areas/index.astro`：按大区（Region）列出所有核心城市的入口。
6. **全局 Footer & Cookie Banner**：
   * 必须在 `Layout.astro` 底部加入完整的合规链接网，并悬浮提示 Cookie Consent。

---

## 🔴 第四阶段：询盘中枢对接标准防坑指南 (The Lead Capture Firewall)
**核心目标：绝对不漏掉任何一个进线询盘，彻底解决 Cloudflare 与 Chatwoot 的通信连环套。**

对于未来新开的项目（如 `Approved Plumbers`），在配置 Cloudflare Worker 接收表单发往 Chatwoot 时，必须严格遵守以下 3 条纪律：

1. **严禁在 Cloudflare Worker 中直连源站 IP**：
   直连会被 Cloudflare 以 Error 1003 阻断。必须使用完整域名 `https://your-chatwoot-domain.com`。
2. **严禁向 Chatwoot 联系人接口传递 Email**：
   传入重复 Email 会导致新询盘被静默合并到老客户名下，彻底石沉大海！
   * **解法**：`POST /contacts` 时，只传加上时间戳的唯一 Name（例如：`${name} #${Date.now().toString(36)}`）。
3. **严禁向 Chatwoot 联系人接口传递 Phone_number**：
   不带 +44 前缀的本地号码会导致 Chatwoot 抛出 422 错误拒收整个请求！
   * **解法**：绝不用官方手机号字段。将客户填写的真实 Email、Phone 全部打包成纯文本，放入创建 Message 的 `content` 正文载荷中。

---

> **🤖 Agent 启动终极指令 (Agent Trigger Prompt) :**
> 未来新开项目时，直接对 AI 丢出这段话：
> *"请仔细阅读项目根目录下的 `pSEO_Playbook.md`，我现在要做一个全新的【屋顶维修 / 园林绿化 / 管道工】本地服务平台，请严格按照该手册的 1~3 阶段，立刻为我生成 5 维丰富 JSON 脚本（并包含伦敦细分与动态定价），并彻底重构 Astro 模板代码！"*
