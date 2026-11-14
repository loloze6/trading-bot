# Backtest of 003-03_high-volume-up-move-continues_1h

- Plan: `../../../03_test_plan/plans/003-03_high-volume-up-move-continues_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1h bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 431 | 0.002923 | -51.511 |
| w2 | 441 | 0.015317 | -47.761 |
| w3 | 444 | -0.025667 | -61.941 |
| w4 | 448 | 0.023992 | -32.304 |
| w5 | 417 | 0.014577 | -46.677 |
| w6 | 462 | -0.018059 | -52.9 |

