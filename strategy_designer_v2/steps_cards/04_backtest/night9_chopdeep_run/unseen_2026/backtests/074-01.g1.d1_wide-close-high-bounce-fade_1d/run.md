# Backtest of 074-01.g1.d1_wide-close-high-bounce-fade_1d

- Plan: `../../../../../03_test_plan/night9_chopdeep_run/plans/074-01.g1.d1_wide-close-high-bounce-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.135649 | 13.029 |
| w2 | 3 | -0.086827 | -5.795 |
| w3 | 1 | 0.030894 | 0.8 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.081758 | 6.642 |
| w2 | 4 | -0.098405 | -6.135 |
| w3 | 1 | 0.020845 | 0.322 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.034341 | 1.768 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | 0.075502 | 0.0 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.025687 | -0.305 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.099353 | 4.324 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.056521 | 1.004 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.120954 | -11.89 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

