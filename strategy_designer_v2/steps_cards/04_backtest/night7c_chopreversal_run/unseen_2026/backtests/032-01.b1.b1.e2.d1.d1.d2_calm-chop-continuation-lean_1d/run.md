# Backtest of 032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d

- Plan: `../../../../../03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | 0.040326 | 14.395 |
| w2 | 27 | 0.207345 | -19.096 |
| w3 | 16 | 0.120696 | 38.519 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.025175 | 15.676 |
| w2 | 27 | 0.075126 | 82.281 |
| w3 | 12 | -0.033516 | 20.107 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | 0.01961 | 16.378 |
| w2 | 42 | 0.070807 | -22.459 |
| w3 | 12 | 0.330209 | 56.216 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | 0.045672 | 25.565 |
| w2 | 32 | -0.074228 | 18.021 |
| w3 | 25 | 0.006405 | -17.322 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | -0.019603 | 3.139 |
| w2 | 43 | 0.080221 | -29.604 |
| w3 | 14 | -0.001605 | 6.926 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.028332 | 2.881 |
| w2 | 31 | 0.014402 | -35.543 |
| w3 | 12 | -0.006593 | -1.803 |

