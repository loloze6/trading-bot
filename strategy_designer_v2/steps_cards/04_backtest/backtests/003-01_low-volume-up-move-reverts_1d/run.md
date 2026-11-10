# Backtest of 003-01_low-volume-up-move-reverts_1d

- Plan: `../../../03_test_plan/plans/003-01_low-volume-up-move-reverts_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1d bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.132218 | -19.86 |
| w2 | 26 | 0.03801 | 13.009 |
| w3 | 21 | -0.040915 | -3.796 |
| w4 | 21 | -0.009425 | -15.162 |
| w5 | 24 | 0.119424 | 5.601 |
| w6 | 21 | 0.024351 | -8.232 |

