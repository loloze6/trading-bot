# Backtest of 003-05_up-move-retrace-by-volume_1h

- Plan: `../../../03_test_plan/plans/003-05_up-move-retrace-by-volume_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1h bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1046 | -0.000938 | -78.215 |
| w2 | 1038 | -0.00699 | -81.531 |
| w3 | 1023 | -0.020377 | -81.581 |
| w4 | 1028 | 0.020877 | -68.658 |
| w5 | 985 | 0.027594 | -68.804 |
| w6 | 1065 | -0.016994 | -81.2 |

