# Backtest of 039-02.d1_wide-range-low-close-next-day-rebound_1d

- Plan: `../../../../../03_test_plan/night7_chopreversal_run/plans/039-02.d1_wide-range-low-close-next-day-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 68 | 0.031362 | -15.491 |
| w2 | 34 | -0.06992 | -12.714 |
| w3 | 24 | 0.023976 | -3.787 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.067913 | -19.314 |
| w2 | 22 | -0.062068 | -8.772 |
| w3 | 19 | 0.134451 | 5.354 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.099989 | 4.092 |
| w2 | 0 | None | 0.0 |
| w3 | 50 | 0.07231 | 1.748 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | -0.095427 | -15.202 |
| w2 | 31 | -0.076805 | -4.365 |
| w3 | 12 | 0.082685 | 4.725 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.200325 | 16.556 |
| w2 | 11 | 0.18609 | 20.945 |
| w3 | 40 | 0.042639 | -4.789 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 77 | -0.156995 | -31.71 |
| w2 | 38 | -0.065785 | 4.377 |
| w3 | 29 | 0.102694 | 13.353 |

