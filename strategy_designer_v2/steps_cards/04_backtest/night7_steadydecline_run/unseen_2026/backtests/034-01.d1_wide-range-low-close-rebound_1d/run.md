# Backtest of 034-01.d1_wide-range-low-close-rebound_1d

- Plan: `../../../../../03_test_plan/night7_steadydecline_run/plans/034-01.d1_wide-range-low-close-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 71 | 0.025861 | -18.588 |
| w2 | 35 | -0.053814 | -10.291 |
| w3 | 25 | 0.065819 | -1.615 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.078987 | -20.051 |
| w2 | 22 | -0.032132 | -4.102 |
| w3 | 19 | 0.173285 | 8.242 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | 0.11712 | 5.16 |
| w2 | 0 | None | 0.0 |
| w3 | 51 | 0.066716 | 1.047 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | -0.147866 | -22.286 |
| w2 | 31 | -0.112716 | -8.7 |
| w3 | 12 | 0.062761 | 3.513 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.18181 | 16.063 |
| w2 | 11 | 0.168573 | 19.321 |
| w3 | 37 | 0.067902 | -4.411 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 80 | -0.106752 | -22.559 |
| w2 | 39 | -0.107138 | -3.603 |
| w3 | 27 | 0.099546 | 14.214 |

