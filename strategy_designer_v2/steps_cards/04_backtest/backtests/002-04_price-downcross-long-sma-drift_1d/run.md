# Backtest of 002-04_price-downcross-long-sma-drift_1d

- Plan: `../../../03_test_plan/plans/002-04_price-downcross-long-sma-drift_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1d bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | -0.24828 | -31.795 |
| w2 | 49 | -0.098333 | 62.841 |
| w3 | 17 | -0.149124 | -9.52 |
| w4 | 2 | -0.066684 | -7.265 |
| w5 | 2 | -0.086924 | -1.414 |
| w6 | 5 | 0.005089 | -4.757 |

