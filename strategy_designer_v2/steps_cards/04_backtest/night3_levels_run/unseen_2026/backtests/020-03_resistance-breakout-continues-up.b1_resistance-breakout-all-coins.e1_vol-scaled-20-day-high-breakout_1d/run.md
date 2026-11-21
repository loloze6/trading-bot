# Backtest of 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d

- Plan: `../../../../../03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.043796 | -1.182 |
| w2 | 6 | 0.254703 | 18.173 |
| w3 | 3 | -0.032796 | -3.898 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.070686 | -2.225 |
| w2 | 4 | 0.073419 | 11.593 |
| w3 | 4 | 0.03104 | 1.765 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.010171 | -1.153 |
| w2 | 9 | 0.003889 | -17.93 |
| w3 | 5 | 0.056903 | 10.145 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.195066 | -8.955 |
| w2 | 11 | 0.027871 | 22.771 |
| w3 | 8 | -0.138398 | -19.983 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.079565 | -6.556 |
| w2 | 4 | 0.353129 | 0.496 |
| w3 | 2 | 0.032931 | -0.587 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.019257 | -4.247 |
| w2 | 12 | 0.129125 | 32.447 |
| w3 | 6 | -0.027912 | 7.762 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.017488 | -4.252 |
| w2 | 6 | -0.019876 | -13.929 |
| w3 | 4 | 0.004484 | -3.564 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.047148 | -2.912 |
| w2 | 6 | 0.266224 | 5.725 |
| w3 | 2 | 0.014807 | -2.73 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.011022 | -6.285 |
| w2 | 11 | -0.030451 | 13.419 |
| w3 | 4 | -0.14059 | -21.384 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.135398 | 1.633 |
| w2 | 13 | 0.049946 | -10.48 |
| w3 | 5 | -0.359233 | -18.168 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.102971 | -1.177 |
| w2 | 12 | -0.004154 | -1.643 |
| w3 | 6 | -0.045924 | 4.835 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.007596 | -4.239 |
| w2 | 8 | 0.162894 | 7.03 |
| w3 | 3 | -0.010698 | -2.814 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.038497 | -2.253 |
| w2 | 7 | 0.108429 | -3.844 |
| w3 | 5 | 0.291653 | 12.318 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.001452 | -4.375 |
| w2 | 9 | 0.133315 | 27.667 |
| w3 | 2 | -0.032471 | 2.685 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.034281 | -1.394 |
| w2 | 9 | 0.016237 | 5.97 |
| w3 | 7 | 0.007257 | -4.017 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.108172 | 0.087 |
| w2 | 9 | 0.051899 | 16.628 |
| w3 | 10 | 0.008718 | 32.023 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.042056 | -10.327 |
| w2 | 9 | 0.227109 | -5.737 |
| w3 | 4 | 0.024006 | 6.662 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.164435 | 5.06 |
| w2 | 6 | -0.041167 | -1.41 |
| w3 | 3 | -0.042561 | -6.441 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.023668 | -0.97 |
| w2 | 7 | 0.138008 | 19.319 |
| w3 | 5 | 0.029226 | 0.139 |

