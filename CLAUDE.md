# CLAUDE.md

## Project Overview

Browser-based visualization of asset class returns inspired by the Callan Periodic Table of Investment Returns. Displays cumulative daily returns for 9 ETF proxies representing major asset classes.

**Goals:**
- Daily updated chart showing YTD and historical year performance
- Zero viewer friction (no API keys, no backend for users)
- Minimal maintenance (GitHub Actions + Pages, no servers)

## Architecture

```
GitHub Actions (daily cron)
    │
    ▼
fetch_data.py (yfinance) ──► data.json (committed to repo)
                                  │
                                  ▼
                            index.html (static, loads JSON)
                                  │
                                  ▼
                            GitHub Pages (serves to users)
```

**Data flow:** Python script fetches 5+ years of ETF prices from Yahoo Finance, writes to `data.json`. Static HTML loads this JSON and renders charts client-side with Recharts.

## Files

| File | Purpose |
|------|---------|
| `fetch_data.py` | Fetches ETF data via yfinance, outputs `data.json`. Uses PEP 723 inline deps. |
| `data.json` | Price history for all ETFs. Committed by GitHub Actions. |
| `index.html` | Single-file React app. Loads JSON, renders charts. No build step. |
| `.github/workflows/update-data.yml` | Daily cron (6 PM Pacific) to refresh data. |

## ETF Mappings

| Asset Class | ETF | Color |
|-------------|-----|-------|
| Large Cap | SPY | #1f77b4 |
| Small Cap | IWM | #ff7f0e |
| Dev ex-US | EFA | #2ca02c |
| Emerging Mkt | EEM | #d62728 |
| Real Estate | REET | #9467bd |
| US Fixed Inc | AGG | #8c564b |
| Intl Fixed Inc | BNDX | #e377c2 |
| High Yield | HYG | #7f7f7f |
| Cash | BIL | #bcbd22 |

### Real Estate (REET)

Callan uses the **FTSE EPRA Nareit Developed REIT Index**.

**Selected:** REET (iShares Global REIT ETF) - tracks FTSE EPRA Nareit Global REITs Index

**Why REET:**
- Same FTSE EPRA Nareit index family that Callan uses
- VNQ (common alternative) tracks MSCI US Real Estate 25/50 Index (different family, US-only)

**Tradeoffs:**
- REET tracks "Global" (developed + emerging) vs Callan's "Developed" only
- Emerging markets ~5-10% of REET; over 70% is US-based
- No US-listed ETF tracks the exact "Developed" variant (HSBC H4ZL is European-listed only)

### Global ex-US Fixed Income (BNDX) ⚠️

Callan uses the **Bloomberg Global Aggregate ex-US Bond Index (unhedged)**.

**Selected:** BNDX (Vanguard Total International Bond ETF) - USD-hedged

**Known limitation:** BNDX is currency-hedged, while Callan's index is unhedged. This causes significant return differences when the USD moves. For example, in 2025 when the USD weakened, Callan showed ~8.85% while BNDX showed ~2.78%.

**Why we kept BNDX despite the mismatch:**
- No US-listed ETF tracks the unhedged Bloomberg Global Aggregate ex-USD
- Unhedged alternatives (IGOV, BWX) only hold treasuries, not the full aggregate (which includes corporates)
- BNDX has low expense ratio (0.07%) and high liquidity

**Alternatives considered:**
- IGOV: Unhedged, developed markets, but treasury-only (no corporates)
- BWX: Unhedged, dev + emerging, but treasury-only (no corporates)

## Development

```bash
# Fetch fresh data locally
uv run fetch_data.py

# Serve locally
python3 -m http.server 8000
# Open http://localhost:8000
```

## Tech Stack

- **Python:** yfinance for data, inline script deps (PEP 723)
- **Frontend:** React 18 + Recharts via ESM imports (esm.sh), Tailwind CSS via CDN
- **Hosting:** GitHub Pages (static)
- **CI:** GitHub Actions with `astral-sh/setup-uv@v5`

## Key Implementation Details

- `index.html` uses `React.createElement()` calls, not JSX (no build/transpile step)
- Chart views recalculate returns from each period's start date as 0%
- `data.json` stores raw prices; return calculations happen client-side
- Workflow runs at 2 AM UTC (6 PM Pacific) to capture full trading day

## View Options

- **YTD:** Current year, Jan 1 = 0%
- **Last 12 Months:** Rolling window
- **Historical years:** 2024, 2023, 2022, 2021 (each year's Jan 1 = 0%)

## Potential Improvements

- Add tooltips showing exact date on hover (currently shows m/d format)
- Mobile responsiveness tweaks
- Option to compare specific ETFs side-by-side
- Download CSV/PNG export
- Add benchmark comparison line (e.g., 60/40 portfolio)
