# Backtest of 002-05_sma-up-regime-positive-drift_1d

- Plan: `../../plans/002-05_sma-up-regime-positive-drift_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1d bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.108713 | -8.145 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 8 | -0.080007 | 25.073 |
| w5 | 9 | -0.008243 | -9.038 |
| w6 | 10 | -0.044291 | 26.16 |

