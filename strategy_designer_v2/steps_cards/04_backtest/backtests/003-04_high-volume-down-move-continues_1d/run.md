# Backtest of 003-04_high-volume-down-move-continues_1d

- Plan: `../../../03_test_plan/plans/003-04_high-volume-down-move-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1d bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.015588 | -8.952 |
| w2 | 22 | 0.061886 | 21.135 |
| w3 | 20 | -0.005513 | -7.933 |
| w4 | 20 | -0.042524 | -22.936 |
| w5 | 23 | -0.019584 | -7.15 |
| w6 | 20 | -0.139865 | -29.957 |

