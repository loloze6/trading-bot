# Backtest of 002-02_sma-downcross-downward-drift_1d

- Plan: `../../../03_test_plan/plans/002-02_sma-downcross-downward-drift_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1d bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.127464 | -11.709 |
| w2 | 34 | -0.149865 | 35.112 |
| w3 | 8 | -0.033565 | 5.712 |
| w4 | 4 | -0.150572 | -19.529 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.072409 | -8.428 |

