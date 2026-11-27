# Backtest of 074-01.b1.d3.d1_deep-run-break-fade-falling_1d

- Plan: `../../../../../03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d3.d1_deep-run-break-fade-falling_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.031481 | 5.072 |
| w2 | 4 | -0.01776 | -1.281 |
| w3 | 1 | 0.030894 | 1.316 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.053335 | 5.181 |
| w2 | 2 | 0.001712 | 0.055 |
| w3 | 1 | 0.020845 | 1.097 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.032774 | 3.958 |
| w2 | 4 | 0.034402 | 2.468 |
| w3 | 1 | 0.075502 | 2.393 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.009052 | 0.044 |
| w2 | 1 | 0.016757 | -0.021 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.064345 | 5.729 |
| w2 | 6 | -0.001096 | -1.131 |
| w3 | 1 | 0.056521 | 2.412 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.166132 | -13.892 |
| w2 | 1 | 0.004956 | -0.169 |
| w3 | 1 | 0.029527 | 0.874 |

