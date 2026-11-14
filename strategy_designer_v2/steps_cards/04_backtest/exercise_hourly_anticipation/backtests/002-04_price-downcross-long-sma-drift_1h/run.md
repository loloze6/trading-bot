# Backtest of 002-04_price-downcross-long-sma-drift_1h

- Plan: `../../../03_test_plan/plans/002-04_price-downcross-long-sma-drift_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1h bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 305 | 0.013003 | 11.895 |
| w2 | 349 | 0.019039 | 48.639 |
| w3 | 301 | -0.015524 | -18.398 |
| w4 | 185 | 0.025438 | -8.831 |
| w5 | 416 | -0.010934 | -16.818 |
| w6 | 199 | -0.021488 | -29.142 |

