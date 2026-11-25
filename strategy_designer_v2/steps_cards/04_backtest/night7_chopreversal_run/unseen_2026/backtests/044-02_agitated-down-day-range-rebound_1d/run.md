# Backtest of 044-02_agitated-down-day-range-rebound_1d

- Plan: `../../../../../03_test_plan/night7_chopreversal_run/plans/044-02_agitated-down-day-range-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | 0.014533 | -17.819 |
| w2 | 20 | -0.036289 | -6.305 |
| w3 | 11 | 0.133933 | 5.12 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.003642 | -8.259 |
| w2 | 10 | 0.003795 | -0.561 |
| w3 | 8 | 0.242521 | 9.595 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.19256 | 9.45 |
| w2 | 0 | None | 0.0 |
| w3 | 26 | 0.131032 | 8.197 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | 0.001332 | -4.143 |
| w2 | 16 | -0.088277 | -5.882 |
| w3 | 6 | 0.218616 | 10.019 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.328488 | 21.543 |
| w2 | 5 | 0.002189 | -0.177 |
| w3 | 22 | 0.261887 | 13.296 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 50 | -0.162432 | -21.873 |
| w2 | 20 | -0.126029 | -6.0 |
| w3 | 14 | 0.21237 | 13.731 |

