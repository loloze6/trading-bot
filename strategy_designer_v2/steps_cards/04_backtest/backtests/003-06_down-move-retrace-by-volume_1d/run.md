# Backtest of 003-06_down-move-retrace-by-volume_1d

- Plan: `../../../03_test_plan/plans/003-06_down-move-retrace-by-volume_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1d bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 59 | -0.020064 | -15.355 |
| w2 | 71 | 0.129713 | 37.68 |
| w3 | 68 | -0.013671 | -15.313 |
| w4 | 59 | -0.102078 | -29.947 |
| w5 | 67 | -0.021744 | -10.704 |
| w6 | 57 | -0.106796 | -25.665 |

