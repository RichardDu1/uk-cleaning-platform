# UK Local Service Platform & Programmatic SEO Lead-Gen Engine

An automated, high-converting programmatic SEO (pSEO) platform and AI lead-dispatch engine tailored for the UK local trades & home improvement market (e.g., Wall & Floor Tiling, Bathroom Renovations, Emergency Locksmiths, Mobile Auto Services).

Built to bridge verified, skilled craftsmen with UK local homeowners through high-trust landing pages, localized pricing calculators, and multi-step quote funnels.

---

## 📁 Project Structure

```text
├── docs/                        # Complete research, competitor teardown & architecture docs
│   ├── 01_servicing_stop_teardown.md
│   ├── 02_niche_market_research.md
│   ├── 03_automated_pseo_pipeline.md
│   ├── 04_ai_lead_dispatch_system.md
│   ├── 05_strategic_comparison_and_roadmap.md
│   └── 06_competitor_trust_and_conversion_playbook.md
├── data/                        # UK Geography dataset & PSEO generator
│   ├── uk_towns.json            # 34+ UK major cities/towns with coordinates & housing contexts
│   ├── services_config.json     # Sub-services, base rates, and checklists
│   └── tiling_pseo_dataset.json # 136 compiled programmatic local datasets
├── site/                        # Astro SSG Static Website (Deploy to Cloudflare Pages)
│   ├── src/pages/[service]/[city].astro  # Dynamic programmatic local landing pages
│   ├── src/components/PriceCalculator.astro # Interactive regional cost estimator
│   ├── src/components/TrustBadges.astro     # £2M insurance, 12-mo guarantee badges
│   └── src/pages/quote.astro    # 4-step progressive disclosure quote funnel
└── dispatch-engine/             # AI Middleman Translation & Dispatch Webhook
    ├── webhook_server.py        # Converts English homeowner leads into structured Chinese dispatch cards
    └── test_lead_sim.py         # End-to-end simulation test script
```

---

## ⚡ Cloudflare Pages Deployment Guide

### Option 1: Deploy via Cloudflare Dashboard (Recommended)
1. Go to **Cloudflare Dashboard** > **Workers & Pages** > **Create application** > **Pages** > **Connect to Git**.
2. Select this GitHub repository.
3. Configure the **Build settings**:
   * **Framework preset**: `Astro`
   * **Build command**: `npm run build`
   * **Build output directory**: `dist`
   * **Root directory**: `site`
4. Click **Save and Deploy**. Your site with 139+ programmatic landing pages will be live globally on Cloudflare's Edge CDN in under 1 minute!

---

## 🛠️ Local Development

### 1. Run the Astro Static Site:
```bash
cd site
npm install
npm run dev
```
Visit `http://localhost:4321` to preview the homepage, dynamic city landing pages (e.g. `/bathroom-tiling/reading`), and the interactive pricing calculator.

### 2. Run the AI Lead Dispatch Server:
```bash
cd dispatch-engine
python webhook_server.py
```
Test lead intake simulation:
```bash
python test_lead_sim.py
```

---

## 📜 License
MIT License.
