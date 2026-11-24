# Backtest of 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h

- Plan: `../../../../../03_test_plan/night4_volumehour_run/plans/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 147 | 0.011764 | 16.317 |
| w2 | 139 | -0.007714 | -6.156 |
| w3 | 60 | 0.028752 | -10.155 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 182 | 0.01314 | -7.729 |
| w2 | 139 | 0.024107 | 0.934 |
| w3 | 43 | -0.014586 | -7.953 |

