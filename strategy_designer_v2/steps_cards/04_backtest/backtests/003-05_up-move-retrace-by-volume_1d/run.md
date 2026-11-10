# Backtest of 003-05_up-move-retrace-by-volume_1d

- Plan: `../../../03_test_plan/plans/003-05_up-move-retrace-by-volume_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1d bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 52 | -0.165517 | -41.988 |
| w2 | 49 | -0.045282 | -23.129 |
| w3 | 51 | -0.020079 | -11.951 |
| w4 | 47 | 0.137382 | 39.581 |
| w5 | 49 | 0.007699 | -7.469 |
| w6 | 48 | 0.039525 | 11.523 |

