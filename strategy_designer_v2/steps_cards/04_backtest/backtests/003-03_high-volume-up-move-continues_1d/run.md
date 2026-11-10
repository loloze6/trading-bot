# Backtest of 003-03_high-volume-up-move-continues_1d

- Plan: `../../../03_test_plan/plans/003-03_high-volume-up-move-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1d bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.071202 | -20.162 |
| w2 | 15 | -0.03493 | -25.041 |
| w3 | 19 | -0.062634 | -19.218 |
| w4 | 26 | 0.118507 | 52.72 |
| w5 | 15 | -0.01283 | -7.976 |
| w6 | 27 | -0.018461 | 11.652 |

