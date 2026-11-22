# Backtest of 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d

- Plan: `../../../../../03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 20 | 0.073787 | 17.94 |
| w3 | 35 | 0.104976 | 24.107 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 21 | 0.133204 | 57.833 |
| w3 | 25 | 0.136173 | 24.449 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 9 | 0.044721 | 6.417 |
| w3 | 34 | 0.15774 | 43.811 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.292113 | 61.914 |
| w2 | 27 | -0.005979 | 32.084 |
| w3 | 46 | 0.020076 | -0.515 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 12 | -0.102457 | -14.597 |
| w3 | 32 | 0.063191 | 23.756 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.010923 | -7.2 |
| w2 | 54 | -0.017769 | 6.738 |
| w3 | 40 | 0.084826 | 5.722 |

