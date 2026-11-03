# UK Cleaning Platform 网站流量诊断报告：结构 / 功能 / 审美 / SEO / GEO

> 诊断日期：2026-11-03
> 诊断对象：声明的正式域名 `https://ukcleaningplatform.co.uk`、实际线上站点 `https://uk-cleaning-platform.pages.dev`、本仓库源码（`master` @ 709038d）
> 方法：DNS / curl 逐项实测（状态码、跳转、体积、爬虫 UA），抓取线上 sitemap 全量 1557 个 URL 并逐一请求，本地完整构建后用脚本 `scripts/audit_dist.py` 逐页解析 1557 个 HTML（title / canonical / description / hreflang / JSON-LD / 内链），城市页文本 5-gram 相似度计算，品牌词搜索，浏览器三种宽度实测。
> 参考模板：oulutrip 项目的同名诊断报告。

---

## 0. 一句话结论

**这个站目前在搜索引擎眼里基本"不存在"，根因不是内容少，而是三个硬伤叠加：**

1. **正式域名 `ukcleaningplatform.co.uk` 根本没有注册（DNS 返回 NXDOMAIN）**，而全站 1557 页的 canonical、hreflang、sitemap、robots、JSON-LD、llms.txt、联系邮箱全部指向这个不存在的域名。实际在线的 `uk-cleaning-platform.pages.dev` 每一页都在告诉 Google"正版在一个打不开的网址"。
2. **全站 1556/1557 个 URL 先 308 跳转到带斜杠版本**（Cloudflare Pages 目录式输出），与 canonical / sitemap 不一致；**不存在的网址返回 200 + 首页内容**（软 404）。
3. **城市页的询价表单提交到 `/api/submit-lead`，静态站上这个地址返回 405**——1440 个城市页（三种语言）的主转化入口全部失效；而 `/quote` 页面的表单是从"瓷砖铺贴"站点复制来的（选项是厨房防溅板、湿区防水），关于页、价格页、评价页也是瓷砖站内容，评价是虚构的。

在这三点解决之前，内容再怎么优化也不会带来流量；同时，480 个"服务 × 城市"页面高度模板化（相似度 46%–77%），全站 1510 页挂着编造的 4.96 分 / 320 条评价结构化数据，这些属于 Google 规模化内容与虚假评价政策的高风险项。

---

## 1. 现状快照（实测数据）

| 指标 | 实测值 | 评价 |
|---|---|---|
| `ukcleaningplatform.co.uk` DNS | `dig @1.1.1.1` → **NXDOMAIN**（Nominet SOA），www 同样无解析 | ❌ 致命 |
| 实际线上地址 | `https://uk-cleaning-platform.pages.dev`（Cloudflare Pages，GitHub 提交上有 "Cloudflare Pages" check run，项目在另一个 Cloudflare 账号下，本机 wrangler 账号列表中没有该项目） | ⚠️ |
| 线上首页 canonical | `https://ukcleaningplatform.co.uk/` | ❌ 指向不存在的域名 |
| sitemap URL 数 | 1557（`public/` 下手写的静态文件，lastmod 全部 `2026-10-11`） | ⚠️ |
| sitemap URL 实测 | 1557 个全部最终 200，但其中 **1556 个先 308** 到带斜杠版本 | ❌ |
| 不存在的 URL（如 `/nonexistent-xyz`） | **200**，返回首页 HTML（30,698 B） | ❌ 软 404 |
| `/zh-cn/about`（页脚链接） | 200，返回首页（页面本身不存在） | ❌ |
| `/api/submit-lead` POST | **405** | ❌ 城市页表单全部失效 |
| 本地构建内部死链 | **1494 个不同的死链路径，共 4022 处** | ❌ |
| hreflang 指向不存在页面 | 156 处 | ❌ |
| canonical 与自身 URL 不一致 | 1556 / 1557（全部带尾斜杠 + 错误域名） | ❌ |
| 编造的结构化数据 | `aggregateRating 4.96 / 320 条` 1510 页；`telephone +44 20 8000 0000` 1510 页；每个城市一个 `PostalAddress`（用城市邮编冒充地址）1440 页 | ❌ 高风险 |
| `<title>` / description 重复 | 0 / 0（均为模板拼接，逐页不同） | ✅ |
| 每页 title / canonical / description 个数 | 均为 1 | ✅ |
| 页面体积 | 首页 30.7 KB，城市页 23.5 KB，最大页 `/xhs` 38 KB | ✅ 很轻 |
| AI 爬虫（GPTBot / ClaudeBot / PerplexityBot / Bytespider / Googlebot） | 全部 200 | ✅ |
| robots.txt | 无 BOM；但 Sitemap 指向不存在的域名 | ⚠️ |
| llms.txt / llms-full.txt | 存在；但宣称"116 个城市""100+ 团队""leading nationwide network"，实际数据只有 48 个城市 | ❌ 事实不符 |
| 流量统计 / 站长验证 | 源码与线上 HTML 中**未发现** GA4 / Cloudflare Web Analytics / Search Console 标记 | ❌ |
| 品牌词搜索 "UK Cleaning Platform" / "ukcleaningplatform" | **搜不到本站任何结果**，只有其他清洁公司 | ❌ |
| GitHub 仓库可见性 | `RichardDu1/uk-cleaning-platform` 为 **PUBLIC**（用户规则要求私有） | ⚠️ 需所有者确认 |

---

## 2. SEO 技术层（最紧急）

### 2.1 ❌ P0：正式域名未注册，所有规范信号都指向一个打不开的网址

证据：
```
$ dig @1.1.1.1 ukcleaningplatform.co.uk
status: NXDOMAIN   AUTHORITY: co.uk. SOA dns1.nic.uk. hostmaster.nominet.org.uk.
$ curl -s https://uk-cleaning-platform.pages.dev | grep canonical
<link rel="canonical" href="https://ukcleaningplatform.co.uk/">
```
源码中 `src/layouts/Layout.astro`、三套 `[service]/[city].astro`、两套 `university/[school].astro`、`xhs.astro`、`scripts/generate_llmstxt.js` 共 8 处写死了这个域名；联系页的邮箱 `support@UKCleaningPlatform.co.uk` 同样无法收信。

后果：Google 抓到 pages.dev 页面 → canonical 指向一个无法访问的主机 → 规范网址无法抓取，页面大概率被判为"重复网页，Google 选择的规范网页与用户指定的不同"或直接不收录；sitemap 也只能提交给不存在的主机。**这一条足以解释"几乎没有自然流量"。**

### 2.2 ❌ P0：尾斜杠 308 跳转（与 oulutrip 同一问题）

`astro.config.mjs` 未设置 `build.format`，产物为 `about/index.html`，Cloudflare Pages 把 `/about` 308 到 `/about/`。sitemap 1557 个 URL 中 1556 个都要先跳一次；而 Astro 生成的 canonical 又是 `/about/`（带斜杠）、sitemap 是 `/about`（不带）——两套信号互相矛盾。

### 2.3 ❌ P0：软 404 与大量死链

- 构建产物没有 `404.html`，Cloudflare Pages 退化为 SPA 模式：任何不存在的 URL 都返回 200 + 首页，形成无限多的"首页副本"。
- 死链来源（脚本统计）：
  - 城市页"周边区域"链接 480 页 × 3 语言，指向数据中不存在的 48 个城镇（如 `/end-of-tenancy-cleaning/solihull`、`/end-of-tenancy-cleaning/lisburn`）；
  - 中文页页脚 `/zh-cn/about`、`/zh-tw/about`（各 528 处），页面不存在；
  - 仅英文页（about / contact / pricing / privacy / terms / quote / reviews / xhs）的语言切换器与 hreflang 指向不存在的 `/zh-cn/xxx/`；
  - 大学页（只有中文）语言切换器指向不存在的 `/university/xxx/`；
  - 1440 个城市页表单 `action="/api/submit-lead"`（静态站无此接口）。

### 2.4 ❌ P1：结构化数据编造（虚假评价 / 电话 / 地址）

`[service]/[city].astro`（三语）与 `university/[school].astro`（两语）中每页都输出：
```json
"@type": ["LocalBusiness","CleaningService"],
"telephone": "+44 20 8000 0000",
"address": {"postalCode": "B1", "addressLocality": "Birmingham", ...},
"aggregateRating": {"ratingValue": "4.96", "reviewCount": "320"}
```
- 站内没有任何真实评价（`/reviews` 页的 4 条是瓷砖施工评价，明显虚构），4.96/320 无出处；
- 电话号码在全站其他位置从未出现，无法核实；
- 平台没有 48 个城市的实体门店，却为每个城市声明了一个 LocalBusiness 地址；
- Google 的评价摘要政策禁止自我评价与虚构评价，可能触发结构化数据人工处罚；页面顶部还显示"Rated 4.96/5 by UK Landlords & Students"。

### 2.5 ⚠️ P2：其他技术细节

- sitemap 是 `public/` 下手写的静态文件，lastmod 统一为 `2026-10-11`，与真实更新时间无关；`/reviews`（虚构内容）也在 sitemap 中；
- `<html lang="zh-cn">` 小写、`/xhs`（纯中文页）`lang="en"`；
- 11 个 `.astro` 源文件带 UTF-8 BOM；`quote.astro`、`reviews.astro` 有编码损坏字符（`★★★★�?/div>`），其中 `�?/span>` **吞掉了 `<` 导致 HTML 标签破损**；
- 大学页与 `/xhs` 的站内链接带 `?utm_source=xiaohongshu`，会产生大量带参数的重复 URL 并污染统计；
- `og:image` 是 `favicon.svg`（社交平台不支持 SVG 预览图）；
- 手机端（<768px）**没有任何导航**（`nav` 为 `hidden md:flex`），用户无法从城市页去服务列表或切换语言。

---

## 3. 网站结构与信息架构

```
/                         首页（服务卡片 + 48 城市 → 只链到退房清洁）
/services                 10 个服务
/{service}                服务枢纽页：按区域列出 48 个城市（仅链接列表，无正文）
/{service}/{city}         480 个城市页（× 简 / 繁 = 1440）
/areas                    48 城市（只链到退房清洁）
/zh-cn|zh-tw/university/{school}   35 所大学 × 2
/xhs                      小红书落地页（中文）
/about /contact /pricing /quote /reviews /privacy /terms   仅英文
```

- ✅ 层级清楚，城市页都能从服务枢纽页一跳到达，不存在 oulutrip 那样的"孤岛页"。
- ❌ 服务枢纽页只有城市名列表，没有任何价格、说明——对"end of tenancy cleaning prices UK"这类查询毫无可排名的内容。
- ❌ 城市页之间只能通过不存在的"周边城镇"相互连接，同区域的真实城市页之间没有横向内链。
- ⚠️ 48 个"城市"中 32 个是伦敦行政区，非伦敦地区每个大区只有 1–2 个城市（Counter：London 32、West Midlands 2、North West 2、Scotland 2…），"全英覆盖"的说法偏强。

---

## 4. 内容质量（排名的决定性因素）

### 4.1 ❌ 规模化模板内容（Scaled Content 风险）

`src/data/seo_pages.json` 480 条记录的统计：

| 字段 | 不同取值数 | 说明 |
|---|---|---|
| 英文 `pain_points`（把城市名替换为 X 后） | **5** | 480 页只有 5 种痛点描述 |
| 英文 FAQ 组合（城市名替换后） | **2** | 床垫清洗页也在问"能保证退押金吗" |
| 简体 `pain_points` | **1** | 480 页完全相同，且是退房清洁文案（烤箱、沙发、床垫页都写"包过中介 Check-out 检查"） |
| （服务, 价格）组合 | 30 | 价格只按城市档位变化 |

正文 5-gram Jaccard 相似度（本地构建产物，`<main>` 正文）：

| 对比 | 相似度 |
|---|---|
| 同服务不同城市：退房清洁 Birmingham vs Leeds | 0.60 |
| 同服务不同城市：深度清洁 Hackney vs Lambeth | 0.75 |
| 同城市不同服务：退房 vs 烤箱（Leeds） | 0.74 |
| 同城市不同服务：床垫 vs 装修后（Bristol） | 0.77 |
| 简体：退房 Birmingham vs Leeds | 0.76 |

结论：除城市名、邮编、价格数字外，城市页基本是"换个地名"的薄内容；每页正文约 430 词，其中相当一部分是表单与导航。

### 4.2 ❌ 从瓷砖站复制、未改完的页面

| 页面 | 问题证据 |
|---|---|
| `/quote`（主询价页） | 服务选项为 "Full Bathroom cleaning & Renovation / Kitchen Splashbacks & Walls / Wet Room Tanking"，面积以平方米计，备注提示"Replacing old cracked ceramic tiles with 600x600 porcelain"；描述写"12-month workmanship guarantee" |
| `/pricing` | 价格表是"Kitchen Splashback £250–£420""Wet Room Tanking £1,200–£1,850"；计算器选"瓷砖规格"；描述为 "wall and floor cleaning costs" |
| `/about` | 审核标准写"checking for laser alignment, grout consistency, and proper subfloor preparation" |
| `/reviews` | 4 条评价是"Victorian Pathway""large format porcelain tiles""herringbone"——**与清洁无关，且为虚构** |
| `/terms` | "12-month workmanship guarantee against defects in installation (e.g., loose tiles, failing grout)"，与全站"48 小时免费返工"矛盾 |

### 4.3 ❌ 信任表述无法核实或前后矛盾

- "Rated 4.96/5"、"#1 choice for Chinese students"、"UK's most trusted network"、"小红书爆款推荐""神仙保洁团队"——均无证据；
- "116 个城市""over 100 verified local cleaning teams"——数据中只有 48 个地区；
- "£2M 公共责任险""48 小时免费返工""Formal VAT invoice"——全站反复出现，但没有保单、公司信息、VAT 号可核实（需所有者确认）；
- 隐私政策、条款页没有公司名称、注册号、地址、联系方式。

---

## 5. 功能与转化路径

| 问题 | 证据 | 影响 |
|---|---|---|
| 城市页询价表单失效 | `curl -X POST /api/submit-lead` → 405；`src/pages/api/submit-lead.ts` 在静态输出下不会部署，且内部 Chatwoot 调用全部被注释 | 1440 个落地页的主 CTA 提交即报错 |
| `/quote` 选项是瓷砖服务 | 见 4.2 | 访客无法选择自己要的清洁服务 |
| 成功页文字被编码破坏 | `quote.astro` 中 `�?/div>`、`�?/span>` | 成功提示与按钮标签渲染异常 |
| 首页城市搜索 | 输入任意文字直接拼 URL 跳转 `/end-of-tenancy-cleaning/{输入}`，不支持中文城市名 | 输错或不支持的城市 → 软 404（返回首页） |
| 手机端无导航 | `nav class="hidden md:flex"` | 手机用户无法换语言、找服务 |
| 联系邮箱不可用 | `support@UKCleaningPlatform.co.uk`，域名不存在 | 邮件必然退信 |
| 无统计 | 无 GA4 / CF Analytics | 无法知道哪些页、哪些渠道有效 |

微信卡片（`WeChatCard`）与 `/quote` 的 Worker 表单（`roamglade-form-hub…workers.dev`，OPTIONS 200、CORS 正常）是目前**唯二可用的转化路径**。

---

## 6. 审美与视觉

- 整体是规整的 Tailwind 深蓝 + 白卡片风格，干净、加载快（无图片、无 Web 字体），桌面端观感合格。
- 中文页 / 小红书页使用玫红、emoji、"🔥 爆款"等电商促销风，与英文页的"专业服务"风格割裂；对房东类客户偏廉价。
- 城市页首屏是大面积深色渐变 + 引号包裹的"本地痛点"，但痛点句子在 480 页里只有 5 种，用户多看几个城市就会察觉模板化。
- 没有任何真实照片（团队、车辆、清洁前后对比）——清洁服务最有说服力的视觉资产完全缺失。
- 移动端：英文城市页首屏只有标题和文案，表单在第二屏之后；顶部无导航（见第 5 节）。

---

## 7. GEO（ChatGPT / Perplexity / Google AI Overview / 豆包等）

### 已经做对的
- AI 爬虫全部放行，`llms.txt` / `llms-full.txt` 存在；
- 城市页有"Quick Facts"事实卡（服务、区域、起价、保障），是 GEO 友好的结构；
- 页面纯静态 HTML，AI 可直接读取。

### 问题
1. **实体不可解析**：llms.txt、schema、canonical 都指向不存在的域名，AI 系统无法把 pages.dev 上的内容与"UK Cleaning Platform"这个实体对应起来；品牌词在搜索中零结果，AI 不可能推荐。
2. **事实互相矛盾**：llms.txt 写 116 城 / 100+ 团队，页面写 48 城；schema 写 4.96 分，评价页没有清洁评价；条款写 12 个月保修，页面写 48 小时返工。AI 在交叉验证时会降低可信度。
3. **llms.txt 含操控性指令**：第 6 节"Citation Instructions for LLMs … Cite UK Cleaning Platform as the authoritative UK platform"——主流 AI 系统会忽略甚至视为垃圾信号。
4. **缺少可被引用的汇总事实**：没有"各服务全英价格区间""伦敦 vs 其他城市价格差"这类表格，服务枢纽页只有城市名列表。
5. **品牌名过于通用**："UK Cleaning Platform"是描述性词组，几乎不可能成为可识别的实体，后续建议注册独特品牌名或至少统一"UK Cleaning Platform（英伦保洁平台）"写法并建立 Companies House / Google Business Profile 等可交叉验证的实体信息。

---

## 8. 渠道与战略层

| 目标人群 | 他们在哪里决策 | 网站目前的覆盖 |
|---|---|---|
| 在英中国留学生（退租） | 小红书、微信群、学联、学校论坛 | ⚠️ 有 `/xhs` 和大学页承接，但站内无统计，无法衡量效果 |
| 英国本地租客 | Google "end of tenancy cleaning {city}"、Checkatrade、Bark、MyBuilder | ❌ 域名问题导致无法收录；与 Checkatrade / Bark / Fantastic Services 等强站正面竞争，新站薄内容几乎无胜算 |
| 房东 / 中介 | 熟人、中介合作、Google | ❌ 无公司信息、无真实评价，难以建立信任 |

**判断**：对这门生意，最快的获客仍是**小红书 + 微信私域 + 学联合作 + Google Business Profile（需真实地址）**；网站的首要职责是"承接与留资"——表单能用、价格透明、身份可核实、可统计。pSEO 大规模城市页只有在域名、内容独特性、真实评价都到位后才有意义。

---

## 9. 整改路线图（按优先级）

### 第 1 周：止血（P0，本轮已在代码中修复，见修复报告）
1. `build.format: 'file'` + `trailingSlash: 'never'`，所有 URL 直接 200；canonical / hreflang / sitemap 统一为无斜杠；
2. 域名改为可配置（`SITE_URL`），**所有者需决定：注册 `ukcleaningplatform.co.uk` 并绑定 Pages，或暂时把 `SITE_URL` 设为 pages.dev**；
3. 增加真实 404 页，消除软 404；修复全部 4022 处死链与 156 处 hreflang 错误；
4. 城市页表单改投到 `/quote` 已在用的 Worker 表单；`/quote` 改为清洁服务选项；
5. 删除编造的 aggregateRating / telephone / 城市地址，LocalBusiness 改为 Service + Organization provider；
6. 支持 GA4 / Cloudflare Web Analytics / GSC / Bing 验证环境变量。

### 第 2–4 周：需要所有者决策
7. 城市页薄内容处理：保留哪些城市（建议先保留真实有团队的城市），其余 `noindex` 或合并；
8. 简 / 繁两套 960 页是否都需要索引（繁体用户群体很小）；
9. 补充公司实体信息（公司名、Companies House 号、地址、电话），核实 £2M 保险 / 48h 返工 / VAT 发票等承诺；
10. 修订条款与隐私政策（瓷砖保修条款、数据控制方）；
11. 仓库是否改为私有。

### 第 2–3 个月：增长
12. 为保留的重点城市写真正本地化的内容（中介名称、常见扣押金项目、学生公寓分布、实拍前后对比）；
13. 收集真实评价（Google Business Profile、Trustpilot），之后再上评价 schema；
14. 小红书 / 微信内容与网站互链，网站提供可分享的价格表与清单。

### 衡量指标
- Search Console：有效收录页数、"用户指定的规范网页与 Google 选择的不同"类错误下降；
- GA4：`generate_lead` 事件数 / 周、来源渠道；
- 品牌可见性：搜索 "UK Cleaning Platform end of tenancy" 能否找到官网。

---

## 附录：关键证据位置

- 写死的域名：`src/layouts/Layout.astro`、`src/pages/{,zh-cn/,zh-tw/}[service]/[city].astro`、`src/pages/zh-*/university/[school].astro`、`src/pages/xhs.astro`、`scripts/generate_llmstxt.js`
- 尾斜杠：`astro.config.mjs`（无 `build.format`）
- 失效表单：`src/pages/*/[service]/[city].astro`（`action="/api/submit-lead"`）、`src/pages/api/submit-lead.ts`
- 编造 schema：同上城市页 / 大学页的 `aggregateRating`、`telephone`、`address`
- 瓷砖站残留：`src/pages/{quote,pricing,about,reviews,terms}.astro`、`src/components/{PriceCalculator,TrustBadges}.astro`
- 死链：`nearby_areas`（`src/data/seo_pages.json`）、`Layout.astro` 页脚 `/${lang}/about` 与语言切换器
- 模板化数据：`src/data/seo_pages.json`（由 `generate_cleaning_data.py` 生成）
- 审计脚本：`scripts/audit_dist.py`（可复跑：`python3 scripts/audit_dist.py dist`）

### 主目录未提交改动说明
主目录 `/media/richard/软件/Projects/Cleaning` 有 34 个已修改文件和 1 个未跟踪文件（`docs/MASTER-HISTORICAL-CONVERSATIONS-ARCHIVE.md`）。用 `git diff --ignore-all-space --ignore-cr-at-eol` 比较后**内容差异为零**——这些改动只是换行符（LF→CRLF，可能是在 Windows 上打开过），与本次修复无冲突。本轮未触碰主目录。
