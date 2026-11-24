# Backtest of 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h

- Plan: `../../../../../03_test_plan/retest_settlement_run/plans/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.012213 | 18.211 |
| w2 | 10 | -0.001123 | -26.897 |
| w3 | 12 | 0.013982 | 43.65 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.028052 | 25.578 |
| w2 | 24 | 0.008497 | -56.101 |
| w3 | 13 | -0.018556 | 57.388 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.012313 | 44.766 |
| w2 | 12 | 0.043657 | 20.852 |
| w3 | 19 | 0.029603 | -31.165 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.019022 | -7.47 |
| w2 | 6 | 0.042779 | -41.646 |
| w3 | 8 | 0.033738 | -1.648 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.021799 | 18.378 |
| w2 | 23 | 0.006735 | -60.719 |
| w3 | 17 | 0.011342 | 37.85 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.02786 | -13.002 |
| w2 | 15 | -0.003282 | 105.083 |
| w3 | 18 | -0.039279 | -36.31 |

