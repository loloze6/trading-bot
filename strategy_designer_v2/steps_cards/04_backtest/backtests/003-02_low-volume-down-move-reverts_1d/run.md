# Backtest of 003-02_low-volume-down-move-reverts_1d

- Plan: `../../../03_test_plan/plans/003-02_low-volume-down-move-reverts_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1d bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.011374 | -2.861 |
| w2 | 30 | 0.154218 | 19.973 |
| w3 | 27 | -0.024101 | -7.979 |
| w4 | 14 | -0.132498 | -8.833 |
| w5 | 13 | -0.03966 | -5.337 |
| w6 | 14 | 0.029423 | 6.03 |

