# Backtest of 003-06_down-move-retrace-by-volume_1d

- Plan: `../../../03_test_plan/plans/003-06_down-move-retrace-by-volume_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1d bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 44 | -0.023892 | -17.335 |
| w2 | 51 | 0.135322 | 40.847 |
| w3 | 45 | -0.018882 | -15.641 |
| w4 | 36 | -0.113038 | -34.153 |
| w5 | 39 | -0.003965 | -8.698 |
| w6 | 35 | -0.097149 | -27.309 |

