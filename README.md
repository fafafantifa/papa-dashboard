# Energy & FX Dashboard

A lightweight dashboard that shows:

- Brent crude price
- Gas (natural gas futures) price
- ETS (EU carbon futures) price
- EUR/USD exchange rate
- Up/down trend indicator for each instrument

## Requirements

- Python 3.10+ (works on Ubuntu 24.04 and macOS)
- Internet access (for live Yahoo Finance data)

## Run

```bash
python3 app.py
```

Then open <http://localhost:8000>.

## Notes

- Data source: Yahoo Finance quote endpoint.
- Refresh interval: every 30 seconds.
- If market data cannot be fetched, the UI shows `n/a` with an error status message.
