# Backtest of 002-02_sma-downcross-downward-drift_1h

- Plan: `../../../03_test_plan/plans/002-02_sma-downcross-downward-drift_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1h bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 125 | 0.011253 | 18.81 |
| w2 | 188 | 0.021723 | 63.234 |
| w3 | 125 | -0.016052 | -10.947 |
| w4 | 96 | 0.013585 | -18.516 |
| w5 | 157 | -0.004153 | 0.461 |
| w6 | 72 | -0.006078 | -17.569 |

