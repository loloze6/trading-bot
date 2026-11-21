# Backtest of 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d

- Plan: `../../../../../03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.06844 | -6.076 |
| w2 | 20 | 0.036517 | 30.274 |
| w3 | 9 | -0.094396 | -9.814 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.023033 | -22.127 |
| w2 | 19 | 0.071208 | 23.439 |
| w3 | 8 | -0.012899 | -8.819 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.001812 | -17.739 |
| w2 | 19 | 0.103436 | 17.741 |
| w3 | 7 | 0.135443 | 10.524 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.067505 | 33.899 |
| w2 | 26 | -0.022181 | 50.136 |
| w3 | 16 | 0.008876 | -13.752 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.005333 | -28.983 |
| w2 | 14 | 0.307437 | 27.356 |
| w3 | 3 | 0.126321 | -3.173 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.063199 | -0.445 |
| w2 | 14 | -0.023083 | 47.88 |
| w3 | 9 | -0.087108 | 3.861 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.045186 | -18.15 |
| w2 | 19 | 0.228293 | 19.791 |
| w3 | 11 | 0.029939 | -8.082 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.029113 | -7.132 |
| w2 | 10 | 0.217041 | 12.024 |
| w3 | 8 | 0.0406 | -13.159 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | -0.014747 | -20.929 |
| w2 | 20 | -0.022939 | 16.374 |
| w3 | 7 | 0.245251 | -3.074 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | -0.046611 | 23.279 |
| w2 | 25 | 0.097187 | -2.885 |
| w3 | 11 | -0.230436 | -24.961 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.027078 | -14.679 |
| w2 | 26 | 0.028433 | 13.321 |
| w3 | 5 | 0.264008 | 14.185 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.097076 | -29.47 |
| w2 | 16 | -0.037829 | 0.46 |
| w3 | 7 | 0.024347 | 13.018 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.016341 | -22.779 |
| w2 | 17 | 0.174172 | 6.96 |
| w3 | 7 | 0.223731 | 32.165 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.031745 | -21.627 |
| w2 | 14 | 0.114621 | 40.094 |
| w3 | 9 | -0.073022 | -5.107 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.009116 | -16.862 |
| w2 | 18 | -0.038684 | 29.555 |
| w3 | 13 | 0.13475 | 17.774 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.104042 | -12.167 |
| w2 | 12 | -0.121242 | 55.509 |
| w3 | 5 | 0.016726 | 102.462 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.006131 | -18.21 |
| w2 | 21 | 0.301212 | 21.467 |
| w3 | 10 | 0.092299 | -0.008 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.202691 | 30.48 |
| w2 | 12 | 0.000902 | 2.243 |
| w3 | 7 | -0.056404 | 2.161 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.072536 | -28.711 |
| w2 | 14 | -0.072846 | 19.31 |
| w3 | 10 | 0.092373 | 5.477 |

