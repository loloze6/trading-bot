# Backtest of 002-02_sma-downcross-downward-drift_1d

- Plan: `../../../03_test_plan/plans/002-02_sma-downcross-downward-drift_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1d bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.108713 | 7.871 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 11 | 0.080007 | -25.526 |
| w5 | 9 | 0.008243 | 4.463 |
| w6 | 14 | 0.044291 | -27.058 |

