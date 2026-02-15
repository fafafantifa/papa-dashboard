#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8000"))

# Yahoo Finance symbols for requested markets.
MARKETS = [
    {
        "key": "brent",
        "label": "Brent Crude",
        "symbol": "BZ=F",
        "unit": "USD/barrel",
    },
    {
        "key": "gas",
        "label": "Natural Gas",
        "symbol": "NG=F",
        "unit": "USD/MMBtu",
    },
    {
        "key": "ets",
        "label": "ETS (EU Carbon Futures)",
        "symbol": "CO2=F",
        "unit": "EUR/tonne",
    },
    {
        "key": "eurusd",
        "label": "EUR/USD",
        "symbol": "EURUSD=X",
        "unit": "FX rate",
    },
]

HTML = """<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Energy & FX Dashboard</title>
  <style>
    :root {
      color-scheme: light dark;
      --bg: #0b1220;
      --panel: #162033;
      --text: #edf2f7;
      --muted: #9fb0c7;
      --up: #2ecc71;
      --down: #e74c3c;
      --flat: #f1c40f;
    }
    body {
      margin: 0;
      font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      background: linear-gradient(120deg, #0f172a, #111827 45%, #1f2937);
      color: var(--text);
      min-height: 100vh;
    }
    .wrap {
      max-width: 1100px;
      margin: 0 auto;
      padding: 2rem 1rem 3rem;
    }
    h1 { margin: 0; font-size: 1.9rem; }
    .sub { color: var(--muted); margin: .5rem 0 1.5rem; }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1rem;
    }
    .card {
      background: rgba(22, 32, 51, 0.9);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 1rem;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
    }
    .name { font-size: .95rem; color: var(--muted); }
    .value { font-size: 2rem; font-weight: 700; margin-top: .45rem; }
    .meta {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: .75rem;
      font-size: .95rem;
    }
    .trend { font-weight: 700; }
    .trend.up { color: var(--up); }
    .trend.down { color: var(--down); }
    .trend.flat { color: var(--flat); }
    .status { margin-top: 1rem; color: var(--muted); font-size: .9rem; }
  </style>
</head>
<body>
  <div class=\"wrap\">
    <h1>Energy & FX Dashboard</h1>
    <p class=\"sub\">Brent crude, gas, ETS and EUR/USD with live trend indicators.</p>
    <section class=\"grid\" id=\"grid\"></section>
    <p class=\"status\" id=\"status\">Loading…</p>
  </div>

  <script>
    function trendClass(change) {
      if (change > 0) return 'up';
      if (change < 0) return 'down';
      return 'flat';
    }

    function trendText(change) {
      if (change > 0) return '▲ Up';
      if (change < 0) return '▼ Down';
      return '■ Flat';
    }

    function render(data) {
      const grid = document.getElementById('grid');
      const status = document.getElementById('status');
      grid.innerHTML = data.items.map((item) => {
        const cls = trendClass(item.change);
        const pct = item.change_percent == null ? 'n/a' : `${item.change_percent.toFixed(2)}%`;
        const value = item.price == null ? 'n/a' : item.price.toFixed(item.key === 'eurusd' ? 4 : 2);
        return `
          <article class=\"card\">
            <div class=\"name\">${item.label}</div>
            <div class=\"value\">${value}</div>
            <div class=\"meta\">
              <span>${item.unit}</span>
              <span class=\"trend ${cls}\">${trendText(item.change)}</span>
            </div>
            <div class=\"meta\">
              <span>Change</span>
              <span>${pct}</span>
            </div>
          </article>
        `;
      }).join('');

      const when = new Date(data.updated_at).toLocaleString();
      status.textContent = `Last update: ${when}`;
    }

    async function refresh() {
      const status = document.getElementById('status');
      try {
        const res = await fetch('/api/prices');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        render(data);
      } catch (err) {
        status.textContent = `Could not fetch market data: ${err.message}`;
      }
    }

    refresh();
    setInterval(refresh, 30000);
  </script>
</body>
</html>
"""


def fetch_market_data() -> list[dict]:
    symbols = ",".join(m["symbol"] for m in MARKETS)
    url = "https://query1.finance.yahoo.com/v7/finance/quote?" + urllib.parse.urlencode({"symbols": symbols})

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) EnergyDashboard/1.0",
            "Accept": "application/json",
        },
    )

    with urllib.request.urlopen(req, timeout=10) as response:
        payload = json.load(response)

    by_symbol = {row.get("symbol"): row for row in payload.get("quoteResponse", {}).get("result", [])}

    items = []
    for market in MARKETS:
        quote = by_symbol.get(market["symbol"], {})
        items.append(
            {
                "key": market["key"],
                "label": market["label"],
                "symbol": market["symbol"],
                "unit": market["unit"],
                "price": quote.get("regularMarketPrice"),
                "change": quote.get("regularMarketChange") or 0,
                "change_percent": quote.get("regularMarketChangePercent"),
            }
        )

    return items


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/":
            body = HTML.encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/api/prices":
            try:
                items = fetch_market_data()
                payload = {
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                    "items": items,
                }
                code = HTTPStatus.OK
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as err:
                payload = {
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                    "items": [
                        {
                            "key": m["key"],
                            "label": m["label"],
                            "symbol": m["symbol"],
                            "unit": m["unit"],
                            "price": None,
                            "change": 0,
                            "change_percent": None,
                            "error": str(err),
                        }
                        for m in MARKETS
                    ],
                    "error": "Failed to fetch live market prices",
                }
                code = HTTPStatus.BAD_GATEWAY

            raw = json.dumps(payload).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

    def log_message(self, fmt: str, *args) -> None:
        print("[dashboard]", fmt % args)


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), DashboardHandler)
    print(f"Dashboard running on http://{HOST}:{PORT}")
    server.serve_forever()
