# Backtest of 058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d

- Plan: `../../../../../03_test_plan/night8_choppycalm_run/plans/058-02.b1.b2.b1.b2.b1.b1_convex-range-edge-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.066506 | -5.213 |
| w2 | 10 | 0.135943 | 51.593 |
| w3 | 9 | 0.059138 | 0.384 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.060031 | -1.421 |
| w2 | 12 | 0.383472 | -4.012 |
| w3 | 12 | 0.014248 | -2.977 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.019916 | -4.395 |
| w2 | 8 | -0.153321 | -32.858 |
| w3 | 5 | -0.035661 | 7.226 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.044127 | -33.785 |
| w2 | 16 | 0.066856 | 58.011 |
| w3 | 22 | 0.008168 | -25.257 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.015368 | 2.59 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.027721 | -1.298 |
| w2 | 10 | 0.142423 | 22.157 |
| w3 | 10 | 0.112662 | 10.321 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 7 | 0.105506 | -8.304 |
| w3 | 8 | 0.10495 | 7.99 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.0561 | 0.66 |
| w2 | 9 | 0.050447 | 0.822 |
| w3 | 0 | 0.478745 | 0.0 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.117244 | -4.668 |
| w2 | 10 | 0.17112 | 13.584 |
| w3 | 0 | None | 0.0 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.117027 | -10.072 |
| w2 | 9 | 0.126023 | 12.369 |
| w3 | 0 | None | 0.0 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.0382 | -4.178 |
| w2 | 9 | 0.116626 | -8.715 |
| w3 | 0 | -0.207561 | 0.0 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 10 | 0.047075 | -27.145 |
| w3 | 8 | 0.031649 | 22.749 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.016136 | -0.489 |
| w2 | 2 | 0.030687 | -2.683 |
| w3 | 9 | 0.188735 | -19.395 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.018936 | -20.422 |
| w2 | 6 | 0.18401 | 33.91 |
| w3 | 21 | -0.011439 | -14.45 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.100181 | -4.612 |
| w2 | 10 | 0.101041 | 18.192 |
| w3 | 4 | -0.258467 | 0.503 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.003221 | -10.257 |
| w2 | 12 | 0.145267 | 39.416 |
| w3 | 1 | 0.166069 | 6.764 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.013805 | -2.283 |
| w2 | 8 | 0.236926 | -6.932 |
| w3 | 5 | 0.09651 | 11.351 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.23722 | 3.777 |
| w2 | 3 | -0.13938 | -14.415 |
| w3 | 4 | 0.056578 | -10.643 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.128754 | -4.714 |
| w2 | 3 | 0.216121 | 30.501 |
| w3 | 7 | -0.058954 | 15.539 |

