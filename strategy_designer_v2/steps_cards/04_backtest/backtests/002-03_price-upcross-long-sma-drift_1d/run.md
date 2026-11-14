# Backtest of 002-03_price-upcross-long-sma-drift_1d

- Plan: `../../../03_test_plan/plans/002-03_price-upcross-long-sma-drift_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1d bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 20 | -0.189079 | 14.769 |
| w5 | 14 | -0.021614 | -6.444 |
| w6 | 13 | -0.03225 | 48.756 |

