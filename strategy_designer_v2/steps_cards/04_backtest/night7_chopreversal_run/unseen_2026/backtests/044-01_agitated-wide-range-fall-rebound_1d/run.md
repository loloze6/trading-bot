# Backtest of 044-01_agitated-wide-range-fall-rebound_1d

- Plan: `../../../../../03_test_plan/night7_chopreversal_run/plans/044-01_agitated-wide-range-fall-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.018046 | -22.008 |
| w2 | 18 | -0.025272 | -4.391 |
| w3 | 15 | 0.099826 | 3.788 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.086442 | -18.24 |
| w2 | 8 | 0.016293 | 0.109 |
| w3 | 11 | 0.225634 | 11.624 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.203824 | 7.785 |
| w2 | 0 | None | 0.0 |
| w3 | 26 | 0.078942 | 4.726 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.046317 | 2.194 |
| w2 | 15 | -0.05763 | -4.525 |
| w3 | 8 | 0.151845 | 9.322 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.398028 | 20.748 |
| w2 | 4 | -0.012099 | -1.397 |
| w3 | 23 | 0.167218 | 8.876 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 56 | -0.172331 | -31.563 |
| w2 | 20 | -0.045056 | -0.327 |
| w3 | 15 | 0.190879 | 23.023 |

