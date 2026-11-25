# Backtest of 041-02_wide-down-day-next-day-rebound_1d

- Plan: `../../../../../03_test_plan/night7_panic_run/plans/041-02_wide-down-day-next-day-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 50 | -0.024114 | -25.116 |
| w2 | 50 | -0.172578 | -26.849 |
| w3 | 35 | 0.032481 | -9.858 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 52 | -0.02662 | -20.644 |
| w2 | 48 | -0.158874 | -26.934 |
| w3 | 33 | 0.053255 | -10.01 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 51 | -0.012239 | -24.851 |
| w2 | 56 | -0.067663 | -27.068 |
| w3 | 28 | 0.154648 | 13.159 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 50 | 0.128266 | 17.827 |
| w2 | 46 | 0.131437 | 38.898 |
| w3 | 30 | 0.093305 | 3.776 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 58 | -0.102776 | -32.969 |
| w2 | 51 | -0.113235 | -20.984 |
| w3 | 39 | 0.089246 | -4.531 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 56 | -0.140968 | -20.96 |
| w2 | 45 | 0.018343 | 18.688 |
| w3 | 34 | 0.089148 | 10.987 |

