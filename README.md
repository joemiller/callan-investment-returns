# Callan-Style Daily Returns Chart

A browser-based visualization of asset class returns, inspired by the Callan Periodic Table of Investment Returns.

## Features

- **Multiple time views**: YTD, Last 12 Months, and individual years (5 year history)
- **Daily updates**: GitHub Actions fetches fresh data after market close
- **No API keys needed**: Viewers just need to load the page
- **Zero cost**: Runs entirely on GitHub (Actions + Pages)

## Quick Setup

1. **Create a new GitHub repository**

2. **Upload these files** to the root:
   ```
   index.html
   fetch_data.py
   data.json
   .github/workflows/update-data.yml
   ```

3. **Enable GitHub Pages**:
   - Go to Settings → Pages
   - Source: "Deploy from a branch"
   - Branch: `main`, folder: `/ (root)`
   - Save

4. **Run the workflow manually** (first time):
   - Go to Actions → "Update ETF Data"
   - Click "Run workflow"

5. **View your chart** at `https://<username>.github.io/<repo-name>/`

## How It Works

- `fetch_data.py` uses `yfinance` to download 5+ years of ETF price history
- GitHub Actions runs this daily at 6 PM Pacific (after market close)
- Results are committed to `data.json`
- `index.html` loads `data.json` and renders the chart client-side

## ETF Proxies

| Asset Class | ETF |
|-------------|-----|
| Large Cap Equity | SPY |
| Small Cap Equity | IWM |
| Developed ex-US | EFA |
| Emerging Markets | EEM |
| Real Estate | VNQ |
| US Fixed Income | AGG |
| Intl Fixed Income | BNDX |
| High Yield | HYG |
| Cash Equivalent | BIL |

## Local Development

```bash
# Fetch data (uv auto-installs dependencies from inline metadata)
uv run fetch_data.py

# Or with pip
pip install yfinance pandas
python3 fetch_data.py

# Serve locally (Python 3)
python -m http.server 8000
# Open http://localhost:8000
```

## Customization

Edit `fetch_data.py` to:
- Add/remove ETFs
- Change date range
- Modify colors

Then push changes and the workflow will use the new configuration.
