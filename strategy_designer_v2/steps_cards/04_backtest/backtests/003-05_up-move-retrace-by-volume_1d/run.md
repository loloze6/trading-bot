# Backtest of 003-05_up-move-retrace-by-volume_1d

- Plan: `../../../03_test_plan/plans/003-05_up-move-retrace-by-volume_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1d bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 47 | -0.110929 | -33.319 |
| w2 | 36 | 0.001432 | -13.123 |
| w3 | 34 | -0.079806 | -24.274 |
| w4 | 48 | 0.065008 | 18.45 |
| w5 | 29 | 0.042472 | -1.619 |
| w6 | 47 | 0.006386 | 6.498 |

