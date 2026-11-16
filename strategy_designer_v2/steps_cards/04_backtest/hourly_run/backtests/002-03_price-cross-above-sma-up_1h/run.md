# Backtest of 002-03_price-cross-above-sma-up_1h

- Plan: `../../../../03_test_plan/hourly_run/plans/002-03_price-cross-above-sma-up_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1h bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 174 | 0.013583 | 3.982 |
| w2 | 193 | -0.000418 | -23.198 |
| w3 | 221 | 0.001242 | -10.119 |
| w4 | 237 | 0.025036 | 68.243 |
| w5 | 178 | 0.000726 | -8.122 |
| w6 | 324 | 0.009516 | 40.028 |

