# Backtest of 060-01.g1.d2.d1_own-range-close-height-fade_1d

- Plan: `../../../../../03_test_plan/night8_risingagitated_run/plans/060-01.g1.d2.d1_own-range-close-height-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.089652 | 10.351 |
| w2 | 4 | -0.071242 | -3.299 |
| w3 | 1 | 0.030894 | 1.16 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.080523 | 7.795 |
| w2 | 4 | -0.064797 | -4.205 |
| w3 | 1 | 0.020845 | 1.097 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.066665 | 3.878 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.075502 | 2.393 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.010946 | -0.798 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.085418 | 4.294 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.056521 | 2.412 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.029866 | 2.03 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

