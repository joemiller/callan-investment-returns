#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "yfinance",
#     "pandas",
# ]
# ///
"""Fetch ETF historical data and write to JSON for GitHub Pages."""

import json
from datetime import datetime, timedelta
from pathlib import Path

import yfinance as yf

ETFS = {
    "SPY": "Large Cap",
    "IWM": "Small Cap",
    "EFA": "Dev ex-US",
    "EEM": "Emerging Mkt",
    "REET": "Real Estate",
    "AGG": "US Fixed Inc",
    "BNDX": "Intl Fixed Inc",
    "HYG": "High Yield",
    "BIL": "Cash",
}

COLORS = {
    "Large Cap": "#1f77b4",
    "Small Cap": "#ff7f0e",
    "Dev ex-US": "#2ca02c",
    "Emerging Mkt": "#d62728",
    "Real Estate": "#9467bd",
    "US Fixed Inc": "#8c564b",
    "Intl Fixed Inc": "#e377c2",
    "High Yield": "#7f7f7f",
    "Cash": "#bcbd22",
}


def main():
    # Fetch 6 years of data (covers 5 full calendar years + current YTD)
    end_date = datetime.now()
    start_date = datetime(end_date.year - 5, 1, 1)

    print(f"Fetching data from {start_date.date()} to {end_date.date()}")

    symbols = list(ETFS.keys())
    data = yf.download(symbols, start=start_date, end=end_date, progress=False)

    if data.empty:
        print("ERROR: No data returned from yfinance")
        return 1

    # Extract adjusted close prices
    closes = data["Adj Close"] if "Adj Close" in data.columns.get_level_values(0) else data["Close"]

    # Build date-indexed price data
    prices = {}
    for date_idx in closes.index:
        date_str = date_idx.strftime("%Y-%m-%d")
        prices[date_str] = {}
        for symbol in symbols:
            price = closes[symbol].loc[date_idx]
            if not (price is None or (hasattr(price, "__len__") and len(price) == 0) or price != price):  # nan check
                prices[date_str][ETFS[symbol]] = round(float(price), 4)

    # Sort by date
    sorted_dates = sorted(prices.keys())
    sorted_prices = [{"date": d, **prices[d]} for d in sorted_dates]

    output = {
        "updated_at": datetime.now().isoformat(),
        "asset_classes": [
            {"name": name, "symbol": symbol, "color": COLORS[name]}
            for symbol, name in ETFS.items()
        ],
        "prices": sorted_prices,
    }

    output_path = Path(__file__).parent / "data.json"
    with open(output_path, "w") as f:
        json.dump(output, f, separators=(",", ":"))

    print(f"Wrote {len(sorted_prices)} days of data to {output_path}")
    print(f"Date range: {sorted_dates[0]} to {sorted_dates[-1]}")
    return 0


if __name__ == "__main__":
    exit(main())
