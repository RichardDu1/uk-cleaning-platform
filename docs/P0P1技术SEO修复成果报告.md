# P0 / P1 技术 SEO 修复成果报告

> 日期：2026-11-03
> 对应诊断：`docs/网站流量诊断报告_结构功能审美SEO与GEO全面分析.md`
> 分支：`claude/seo-audit-fix-11548c`（PR 待所有者审核合并，合并并部署后才会在线上生效）

## 一、修复清单

| # | 问题（诊断章节） | 修复方式 | 涉及文件 |
|---|---|---|---|
| 1 | 全站 308 跳转到带斜杠版本，canonical 带斜杠、sitemap 不带（2.2） | `build.format: 'file'` + `trailingSlash: 'never'`，产物变为 `about.html`、`oven-cleaning/leeds.html`，Cloudflare Pages 以无斜杠 URL 直接 200 返回 | `astro.config.mjs` |
| 2 | 正式域名未注册，8 处写死（2.1） | 新增 `src/lib/site.ts`，全站域名统一读取 `astro.config.mjs` 的 `site`，可用环境变量 `SITE_URL` 覆盖；llms.txt / robots.txt 生成脚本读取同一变量 | `astro.config.mjs`、`src/lib/site.ts`、`scripts/generate_llmstxt.js`、所有页面 |
| 3 | canonical 依赖 `Astro.url`，带斜杠 | Layout 统一规范化路径（去 `.html`、去尾斜杠）后生成 canonical | `src/layouts/Layout.astro` |
| 4 | 手写静态 sitemap，lastmod 统一为某天，含虚构评价页（2.5） | 删除 `public/sitemap*.xml`，改用 `@astrojs/sitemap@3.2.1`（3.7 与 Astro 4 不兼容，构建会崩溃）自动生成；不输出虚假 lastmod；排除 `/404`、`/reviews`；`/sitemap.xml` 301 到 `/sitemap-index.xml` | `astro.config.mjs`、`package.json`、`public/_redirects` |
| 5 | 不存在的 URL 返回 200 + 首页（软 404）（2.3） | 新增双语 `404.astro`（noindex），Cloudflare Pages 检测到 `404.html` 后返回真正的 404 | `src/pages/404.astro` |
| 6 | 1494 个死链路径 / 4022 处（2.3） | ① "周边区域"只给有页面的城市加链接，其余显示为纯文本；② 中文页脚 `/zh-cn/about` 改为 `/about`；③ Layout 新增 `langs` 参数，语言切换器只链接确实存在的语言版本，否则跳到该语言首页；④ 删除失效的 `/api/submit-lead`（并 301 到 `/quote`） | `Layout.astro`、三套城市页、`public/_redirects` |
| 7 | hreflang 指向不存在页面 156 处 | hreflang 只在页面存在多个语言版本时输出，并使用 `en-GB / zh-CN / zh-TW` 标准代码；单语页面（about、quote、xhs、大学页单边等）不再输出错误 hreflang | `Layout.astro`、各单语页面 |
| 8 | 城市页询价表单提交到静态站不存在的接口，返回 405（5） | 1440 个城市页表单改投到 `/quote` 已在使用的 Cloudflare Worker 表单中心，新增 `LeadFormScript` 组件做 AJAX 提交，成功后跳转 `/quote?success=true`，失败回退原生 POST；附带页面来源、邮编字段；如配置 GA4 会上报 `generate_lead` 事件 | `src/components/LeadFormScript.astro`、三套城市页 |
| 9 | 编造的 `aggregateRating 4.96/320`、`telephone`、每城一个 `PostalAddress`（2.4） | 全部删除；城市页由 `LocalBusiness` 改为 `Service`（provider 指向全站 Organization，`areaServed` 为城市，`offers` 用页面已公布的起价）；大学页同样处理；Organization / WebSite 节点在每页统一输出 | `src/lib/schema.ts`、三套城市页、两套大学页、`Layout.astro` |
| 10 | 顶部"Rated 4.96/5"、城市页"#1 choice"、中文城市页"小红书爆款推荐·神仙保洁团队"等无法核实的表述（4.3） | 替换为可核实/中性表述（"English & Chinese (中文) Support"、"Serving students, tenants and landlords…"、"📍 覆盖 {城市} 及周边"）；**保留**了全站一致的 £2M 保险、48 小时返工、一口价承诺（需所有者确认，见第四节） | `Layout.astro`、城市页 |
| 11 | "116 个城市""100+ 团队""leading nationwide network"、llms.txt 要求 AI "引用为权威平台" | 全部改为由数据计算的真实数字（48 个地区 = 32 个伦敦行政区 + 16 个城市、35 所大学）；删除 llms.txt 的操控性引用指令，改为"关键页面"清单；价格段改为由数据生成的各服务价格区间表 | `scripts/generate_llmstxt.js`、`public/llms*.txt`、多个中文页 |
| 12 | `/quote` 是瓷砖站表单（4.2、5） | 服务选项改为站点实际的 10 项清洁服务（下拉框，中英对照），面积改为房型，备注示例改为清洁场景；URL 参数 `?service=oven-cleaning` 可预选服务；修复编码损坏导致的 HTML 标签破损 | `src/pages/quote.astro` |
| 13 | `/pricing` 是瓷砖价格表 + 瓷砖计算器 | 改为由 `seo_pages.json` 计算的 10 项服务 × 3 种房型起价区间表 + 影响价格的因素；删除瓷砖计算器 | `src/pages/pricing.astro`、删除 `PriceCalculator.astro`、`TrustBadges.astro` |
| 14 | `/about` 写的是瓷砖审核标准 | 改为清洁服务介绍，服务清单与覆盖数从数据读取，只复述站内已有承诺 | `src/pages/about.astro` |
| 15 | `/reviews` 4 条虚构的瓷砖评价 | 删除虚构评价，改为"仅发布已完成订单的真实评价"说明；`noindex` 且不进 sitemap，待有真实评价后再开放 | `src/pages/reviews.astro` |
| 16 | 服务枢纽页只有城市列表，无可排名/可引用内容（3、7） | 每个服务枢纽页（三语）新增"全英指导价"表：三种房型的最低/最高起价及对应地区；标题和描述改为"{服务} Prices by City – From £X"，每页唯一 | `src/pages/{,zh-cn/,zh-tw/}[service]/index.astro` |
| 17 | 同区域城市页之间无横向内链（3） | 城市页新增"{服务} Elsewhere in {区域}"模块，最多 12 个同区域真实页面 + "全部城市"链接 | 三套城市页 |
| 18 | 城市页 title 过长、description 含"Top-rated" | title 改为"{服务} in {城市} ({邮编}) – From £X \| UK Cleaning Platform"，description 写入该城市三档价格；中文页同理 | 三套城市页 |
| 19 | 大学页 / `/xhs` 站内链接带 `utm_source`（2.5） | 删除站内 UTM 参数（UTM 只应用于站外投放链接） | 大学页、`xhs.astro` |
| 20 | 手机端没有任何导航（5） | 导航在所有宽度可见（自动换行），语言切换器也在手机端可用；页脚补充 Pricing / Quote / Contact / 小红书专区链接，服务名按语言显示 | `Layout.astro` |
| 21 | 首页城市搜索直接拼 URL，不支持中文城市名 | 支持英文/简体/繁体城市名及前缀匹配，回车可提交，匹配不到时跳到"覆盖区域"页 | 三个首页 |
| 22 | `<html lang>` 小写、`/xhs` 标为英文 | 改为 `en-GB / zh-CN / zh-TW`；`/xhs` 显式设为 `zh-CN` | `Layout.astro`、`xhs.astro` |
| 23 | 无流量统计、无站长验证（1） | Layout 支持 `PUBLIC_GA4_ID`、`PUBLIC_CF_BEACON_TOKEN`、`PUBLIC_GSC_VERIFICATION`、`PUBLIC_BING_VERIFICATION`，未配置时不输出任何代码 | `Layout.astro` |
| 24 | 11 个源文件带 BOM、编码损坏字符 | 去除 BOM；修复 `quote.astro` 的损坏字符 | 多个文件 |
| 25 | robots.txt Sitemap 指向错误域名、AI 爬虫清单不全 | 由脚本按 `SITE_URL` 生成，补充 OAI-SearchBot、Claude-SearchBot | `scripts/generate_llmstxt.js`、`public/robots.txt` |
| 26 | `og:image` 用 SVG favicon（社交平台不支持） | 移除无效的 og:image / twitter:image（需要所有者提供真实 1200×630 图片后再加） | `Layout.astro` |

新增可复跑的审计脚本 `scripts/audit_dist.py`：逐页检查 title / canonical / description 个数、canonical 是否等于自身 URL、重复 title、JSON-LD 能否解析、是否含 `aggregateRating` / `telephone` / `address`、hreflang 是否指向存在的页面、内部死链、尾斜杠链接。

## 二、构建验证（本地 `npm run build`）

- 构建成功：1558 页（含 404），用时约 5 秒。
- `python3 scripts/audit_dist.py dist` 对除 404 外的 **1557** 页：

| 检查项 | 修复前 | 修复后 |
|---|---|---|
| 每页恰好 1 个 `<title>` / canonical / description | ✅ | ✅ |
| canonical 不等于自身 URL | **1556** | **0** |
| 内部死链（不同路径 / 出现次数） | **1494 / 4022** | **0 / 0** |
| hreflang 指向不存在页面 | **156** | **0** |
| 指向带尾斜杠 URL 的站内链接 | 4662 | 0 |
| 含 `aggregateRating` 的页面 | 1510 | 0 |
| 含 `telephone` 的页面 | 1510 | 0 |
| 含编造 `address` 的页面 | 1440 | 0 |
| JSON-LD 解析失败 | 0 | 0 |
| 重复 title / description | 0 / 0 | 0 / 0 |
| description 超过 170 字符 | 29 | 1（`/student-accommodation-cleaning`，174） |

- sitemap：1556 个 URL（不含 404、reviews），全部不带尾斜杠，与 canonical 一致。
- 本地 `wrangler pages dev dist`（模拟 Cloudflare Pages 路由）：

| 请求 | 结果 |
|---|---|
| `/`、`/about`、`/end-of-tenancy-cleaning/birmingham`、`/zh-cn`、`/zh-tw/oven-cleaning/leeds`、`/zh-cn/university/ucl`、`/xhs`、`/robots.txt`、`/llms.txt`、`/sitemap-index.xml` | 200 |
| `/about/`、`/about.html`、`/end-of-tenancy-cleaning/birmingham/`、`/zh-cn/` | 308 → 无斜杠正式地址 |
| `/nonexistent-xyz` | **404**（修复前 200） |
| `/sitemap.xml` | 301 → `/sitemap-index.xml` |
| `/api/submit-lead` | 301 → `/quote` |

- 浏览器实测（内置浏览器）：
  - 桌面 1366px、平板 768px、手机 375px 下城市页布局正常；手机端顶部出现导航与语言切换（修复前没有）；
  - 首页、中文首页、繁体城市页、pricing、quote、xhs、大学页、服务枢纽页、about、404 共 10 页在 375px 宽度下 `scrollWidth = 375`，无横向滚动，每页恰好 1 个 H1；
  - `/quote?service=oven-cleaning&city=Leeds` 正确预选"Professional Oven Cleaning"并填入 LEEDS；
  - 服务枢纽页价格表正常显示。
  - 未在真实表单中心提交测试线索（避免向生产收件箱写入垃圾数据），表单提交需所有者上线后自测一次。

## 三、Cloudflare 预览站实测

推送分支后 Cloudflare Pages 自动构建成功（commit `60c4d0e`）：
- 预览地址：https://bc6dfac7.uk-cleaning-platform.pages.dev
- 分支预览地址：https://claude-seo-audit-fix-11548c.uk-cleaning-platform.pages.dev

| 请求 | 修复前（线上 pages.dev） | 预览站 |
|---|---|---|
| `/about`、`/end-of-tenancy-cleaning/birmingham`、`/zh-cn` | 308 → 带斜杠 | **200** ✅ |
| `/about/`、`/about.html`、`/end-of-tenancy-cleaning/birmingham/`、`/zh-cn/` | 200 | 308 → 无斜杠正式地址 ✅ |
| `/zh-tw/oven-cleaning/leeds`、`/zh-cn/university/ucl`、`/xhs`、`/pricing`、`/quote`、`/reviews`、`/oven-cleaning` | 308 | 200 ✅ |
| `/nonexistent-xyz` | 200（首页） | **404** ✅ |
| `/end-of-tenancy-cleaning/solihull`（旧的"周边区域"死链目标） | 200（首页） | **404** ✅（站内已不再链接） |
| `/sitemap.xml` | 200（静态） | 301 → `/sitemap-index.xml` ✅ |
| `/api/submit-lead` | GET 200（首页）/ POST 405 | 301 → `/quote` ✅ |
| sitemap 随机抽样 200 个 URL | 1556/1557 需 308 | **200 个全部直接 200** ✅ |
| 城市页 title | "Expert End of Tenancy Cleaning in Birmingham (B1) \| Deposit Return Guaranteed" | "End of Tenancy Cleaning in Birmingham (B1) – From £120 \| UK Cleaning Platform" ✅ |
| 城市页 canonical | `…/end-of-tenancy-cleaning/birmingham/`（带斜杠） | `…/end-of-tenancy-cleaning/birmingham`（与 URL 一致）✅ |
| 城市页表单 action | `/api/submit-lead` | Worker 表单中心 ✅ |
| 城市页 `aggregateRating` / `telephone` | 有 | 0 ✅ |
| 首页 / 城市页 HTML 体积 | 30.7 KB / 23.5 KB | 34.9 KB / 26.0 KB（新增内链与价格模块，仍很轻） |

注意：预览站与线上一样，canonical 仍指向 `https://ukcleaningplatform.co.uk`（代码默认值）。在域名注册或设置 `SITE_URL` 之前，这一点不会改变——见第四节第 1 条。

## 四、需要所有者决策 / 操作的事项

### 必须先做（否则本轮修复在线上效果有限）
1. **域名二选一**：
   - 推荐：注册 `ukcleaningplatform.co.uk`（目前 NXDOMAIN，可注册），在 Cloudflare Pages 项目 `uk-cleaning-platform` → Custom domains 绑定；代码无需改动。
   - 或者：暂时以 pages.dev 为正式地址——在 Pages 项目的环境变量中设置 `SITE_URL=https://uk-cleaning-platform.pages.dev` 并重新部署，canonical / sitemap / llms.txt / robots.txt 会全部切换。
2. **联系邮箱**：`support@UKCleaningPlatform.co.uk` 在域名注册并配置邮件前无法收信，需替换或配置。
3. 合并 PR 并部署后，在 Pages 项目环境变量中设置 `PUBLIC_GA4_ID`（或 `PUBLIC_CF_BEACON_TOKEN`）与 `PUBLIC_GSC_VERIFICATION` / `PUBLIC_BING_VERIFICATION`，在 Google Search Console 与 Bing Webmaster 提交 `/sitemap-index.xml`。
4. 上线后在任一城市页提交一次测试表单，确认线索进入表单中心（list_id=10）。

### 需要业务判断
5. **薄内容城市页**：480 × 3 = 1440 个城市页相似度 46%–77%，简体痛点文案 480 页完全相同。建议只保留真实有团队覆盖的城市并为其写本地内容，其余 `noindex` 或合并到服务枢纽页。本轮未改动索引策略。
6. **简 / 繁两套是否都索引**：繁体页与简体页内容一致，若无港台/繁体获客计划，可考虑繁体 `noindex`。
7. **核实承诺**："£2M 公共责任险""48 小时免费返工""一口价""可开 Invoice（原写 VAT invoice，已改为 invoice）"在全站反复出现，请确认真实性；不属实的需删除。
8. **条款页**仍写有瓷砖施工的"12 个月保修（loose tiles, failing grout）"，与 48 小时返工矛盾；隐私政策与条款缺公司名称、注册号、地址、数据控制方。法律文本本轮未改，需所有者修订。
9. **微信号**：`ukclean_london / ukclean_manchester / ukclean_midlands / ukclean_north` 是否真实可加，请确认。
10. **数据模板问题**：FAQ "能保证退押金吗"出现在床垫、沙发、烤箱页；烤箱 / 床垫清洗也按"Studio / 2-3 Bed / 4+ Bed"分档。修正需要改 `generate_cleaning_data.py` 并重新生成数据，属于内容决策。
11. **社交分享图**：需要一张 1200×630 的品牌图，之后在 Layout 加回 og:image。
12. **仓库可见性**：GitHub 仓库目前为 PUBLIC，与"私有仓库"规范不一致，是否改为私有由所有者决定。

## 五、主目录未提交改动

主目录 `/media/richard/软件/Projects/Cleaning` 的 34 个修改文件经 `git diff --ignore-all-space --ignore-cr-at-eol` 比较内容差异为零，仅为换行符变化（LF→CRLF），与本次修复无关；本轮未触碰主目录。合并本 PR 后如在主目录 `git pull`，这些换行符改动可能产生冲突提示，可先确认无内容改动后 `git checkout -- .` 丢弃（由所有者执行）。
