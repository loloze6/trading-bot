# Backtest of 003-03_high-volume-up-move-continues_1d

- Plan: `../../../03_test_plan/plans/003-03_high-volume-up-move-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1d bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.080335 | -20.241 |
| w2 | 17 | -0.038716 | -23.271 |
| w3 | 22 | -0.046956 | -15.639 |
| w4 | 29 | 0.127186 | 50.944 |
| w5 | 17 | -0.023944 | -8.524 |
| w6 | 32 | -0.020071 | 12.583 |

