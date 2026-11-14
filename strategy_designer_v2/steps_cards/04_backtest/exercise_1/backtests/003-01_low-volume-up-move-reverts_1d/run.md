# Backtest of 003-01_low-volume-up-move-reverts_1d

- Plan: `../../plans/003-01_low-volume-up-move-reverts_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1d bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.099356 | -16.626 |
| w2 | 18 | 0.052327 | 16.272 |
| w3 | 13 | -0.057982 | -8.508 |
| w4 | 19 | -0.062328 | -22.401 |
| w5 | 12 | 0.137395 | 7.236 |
| w6 | 16 | 0.048832 | -5.009 |

