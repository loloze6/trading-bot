# Backtest of 002-05_sma-up-regime-positive-drift_1h

- Plan: `../../../03_test_plan/plans/002-05_sma-up-regime-positive-drift_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1h bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 80 | 0.0017 | -6.938 |
| w2 | 96 | 0.004937 | -15.22 |
| w3 | 125 | -0.024726 | -32.485 |
| w4 | 103 | 0.019786 | 81.777 |
| w5 | 95 | -0.010174 | -12.462 |
| w6 | 151 | 0.012041 | 61.007 |

