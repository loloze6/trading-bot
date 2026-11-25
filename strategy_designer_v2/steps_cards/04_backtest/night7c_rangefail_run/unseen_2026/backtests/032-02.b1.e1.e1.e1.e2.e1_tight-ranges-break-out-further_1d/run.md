# Backtest of 032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further_1d

- Plan: `../../../../../03_test_plan/night7c_rangefail_run/plans/032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.025451 | -4.672 |
| w2 | 3 | 0.074984 | 0.514 |
| w3 | 2 | -0.077214 | 1.106 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.080123 | -5.597 |
| w2 | 0 | 0.157361 | 0.0 |
| w3 | 1 | 0.109353 | -0.707 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | -0.130065 | -8.993 |
| w3 | 2 | 0.06614 | 1.601 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.079591 | -3.011 |
| w2 | 3 | -0.051035 | 3.246 |
| w3 | 6 | -0.128537 | -17.926 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | 0.339623 | 0.0 |
| w3 | 0 | -0.031873 | 0.0 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.139083 | 0.0 |
| w2 | 2 | 0.156575 | 1.793 |
| w3 | 2 | 0.065618 | 0.496 |

