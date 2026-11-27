# Backtest of 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d

- Plan: `../../../../../03_test_plan/step7ab_b_run/plans/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | -0.124207 | -23.189 |
| w2 | 44 | -0.010909 | -11.825 |
| w3 | 47 | -0.10641 | 6.031 |
| w4 | 36 | -0.109171 | -24.773 |
| w5 | 38 | 0.063875 | 49.153 |
| w6 | 35 | -0.146323 | -13.148 |
| w7 | 46 | 0.066868 | 11.49 |
| w8 | 50 | -0.033141 | -6.162 |
| w9 | 49 | 0.08515 | 20.017 |
| w10 | 38 | 0.112164 | 17.374 |
| w11 | 43 | -0.003426 | 11.304 |
| w12 | 43 | 4.1e-05 | 1.176 |
| w13 | 45 | 0.105475 | 34.396 |
| w14 | 40 | 0.074346 | 30.984 |
| w15 | 40 | -0.042669 | -2.519 |
| w16 | 40 | 0.031687 | 17.965 |
| w17 | 45 | 0.123249 | 27.279 |
| w18 | 47 | -0.108876 | -21.993 |
| w19 | 40 | -0.146464 | -24.544 |
| w20 | 48 | 0.017084 | 6.209 |
| w21 | 40 | -0.089067 | -18.017 |
| w22 | 50 | -0.097792 | -4.603 |
| w23 | 44 | 0.118015 | 15.947 |
| w24 | 43 | 0.084829 | 25.445 |
| w25 | 42 | 0.015874 | 5.748 |
| w26 | 50 | -0.014625 | -9.28 |
| w27 | 45 | -0.01685 | 9.269 |
| w28 | 39 | 0.057858 | 2.022 |
| w29 | 41 | -0.083597 | -9.764 |
| w30 | 45 | -0.066948 | -12.248 |
| w31 | 43 | -0.004266 | -7.295 |
| w32 | 35 | -0.055917 | -12.647 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 47 | 0.167186 | 34.802 |
| w2 | 42 | -0.090113 | -21.436 |
| w3 | 34 | -0.078188 | -21.744 |
| w4 | 37 | -0.013409 | -30.347 |
| w5 | 47 | -0.045514 | 17.282 |
| w6 | 45 | 0.04014 | 21.387 |
| w7 | 45 | -0.00398 | 0.685 |
| w8 | 44 | 0.029145 | 10.785 |
| w9 | 43 | -0.000278 | 3.261 |
| w10 | 47 | -0.000103 | 14.777 |
| w11 | 47 | 0.051868 | 4.717 |
| w12 | 45 | 0.032581 | 5.197 |
| w13 | 45 | 0.090795 | 17.508 |
| w14 | 45 | 0.19749 | 59.714 |
| w15 | 46 | 0.046505 | 10.208 |
| w16 | 44 | -0.11148 | -12.58 |
| w17 | 43 | 0.140343 | 42.056 |
| w18 | 46 | -0.077249 | -21.002 |
| w19 | 46 | -0.069645 | -14.556 |
| w20 | 55 | 0.162709 | 35.735 |
| w21 | 51 | -0.1682 | -36.128 |
| w22 | 47 | -0.008159 | -3.449 |
| w23 | 45 | -0.113177 | -30.354 |
| w24 | 44 | -0.071715 | -19.425 |
| w25 | 41 | 0.065769 | -3.367 |
| w26 | 50 | 0.014887 | 0.983 |
| w27 | 39 | -0.039099 | -8.367 |
| w28 | 46 | -0.105561 | -16.615 |
| w29 | 49 | 0.000569 | -3.615 |
| w30 | 41 | -0.069339 | -8.774 |
| w31 | 40 | -0.066475 | -12.361 |
| w32 | 46 | -0.003867 | -8.801 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 48 | -0.06545 | -13.421 |
| w7 | 41 | -0.065772 | -3.506 |
| w8 | 45 | -0.033707 | -0.262 |
| w9 | 38 | -0.038669 | -6.013 |
| w10 | 34 | 0.079632 | 8.598 |
| w11 | 41 | 0.01179 | -3.675 |
| w12 | 47 | 0.04135 | 3.442 |
| w13 | 42 | 0.027251 | -1.921 |
| w14 | 43 | 0.080839 | 25.384 |
| w15 | 46 | 0.041322 | 6.874 |
| w16 | 43 | -0.117583 | -14.117 |
| w17 | 46 | 0.172023 | 33.925 |
| w18 | 49 | -0.017352 | -6.803 |
| w19 | 42 | -0.080095 | -17.904 |
| w20 | 25 | 0.067822 | 10.33 |
| w21 | 47 | 0.099053 | 26.44 |
| w22 | 43 | 0.118216 | 36.043 |
| w23 | 44 | -0.00624 | 5.615 |
| w24 | 38 | -0.018502 | -5.958 |
| w25 | 46 | 0.120922 | 26.157 |
| w26 | 47 | -0.087108 | -19.275 |
| w27 | 46 | -0.022334 | -3.075 |
| w28 | 34 | -0.073454 | -18.075 |
| w29 | 51 | 0.013672 | -1.398 |
| w30 | 45 | 0.004753 | 3.572 |
| w31 | 47 | -0.064332 | -14.323 |
| w32 | 44 | -0.020831 | -8.661 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 46 | 0.036407 | 0.891 |
| w8 | 45 | -0.046648 | -9.32 |
| w9 | 38 | -0.31313 | -52.514 |
| w10 | 44 | 0.032315 | 9.499 |
| w11 | 44 | 0.235292 | 36.431 |
| w12 | 45 | -0.024903 | -13.297 |
| w13 | 43 | 0.088781 | 17.24 |
| w14 | 42 | 0.138348 | 15.169 |
| w15 | 42 | 0.016473 | -4.865 |
| w16 | 40 | 0.049995 | 16.813 |
| w17 | 48 | 0.216063 | 61.282 |
| w18 | 46 | -0.113309 | -23.807 |
| w19 | 43 | -0.122544 | -24.657 |
| w20 | 49 | 0.048194 | 8.098 |
| w21 | 41 | -0.009862 | -9.051 |
| w22 | 36 | -0.059945 | -22.266 |
| w23 | 51 | 0.106535 | 9.965 |
| w24 | 44 | -0.060266 | -18.605 |
| w25 | 43 | 0.047776 | 6.852 |
| w26 | 43 | 0.037097 | 3.226 |
| w27 | 47 | -0.088534 | -25.068 |
| w28 | 48 | 0.099701 | 14.192 |
| w29 | 52 | 0.078951 | 16.709 |
| w30 | 42 | 0.108152 | 9.737 |
| w31 | 40 | 0.025985 | -4.989 |
| w32 | 39 | -0.070411 | -13.269 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | -0.005076 | 18.388 |
| w2 | 30 | -0.141592 | -22.453 |
| w3 | 37 | -0.020346 | -5.863 |
| w4 | 45 | -0.054519 | 16.819 |
| w5 | 36 | -0.03021 | 7.299 |
| w6 | 44 | 0.028085 | 12.084 |
| w7 | 42 | -0.089373 | -8.398 |
| w8 | 45 | -0.023355 | 1.798 |
| w9 | 43 | -0.008109 | 6.317 |
| w10 | 43 | 0.108314 | 19.289 |
| w11 | 40 | 0.107343 | 25.255 |
| w12 | 42 | -0.083268 | -19.489 |
| w13 | 48 | 0.00257 | 1.235 |
| w14 | 48 | 0.07883 | 35.801 |
| w15 | 44 | -0.027444 | -3.687 |
| w16 | 34 | 0.081325 | 40.667 |
| w17 | 47 | 0.142543 | 41.608 |
| w18 | 48 | -0.035928 | -11.285 |
| w19 | 41 | -0.025746 | -5.606 |
| w20 | 43 | 0.056162 | 18.885 |
| w21 | 44 | 0.020594 | 2.069 |
| w22 | 50 | 0.033748 | 17.406 |
| w23 | 45 | 0.066402 | 4.584 |
| w24 | 47 | 0.143033 | 28.881 |
| w25 | 47 | 0.04328 | 7.676 |
| w26 | 47 | 0.029281 | 3.919 |
| w27 | 45 | -0.0725 | -15.167 |
| w28 | 46 | 0.229369 | 47.6 |
| w29 | 41 | -0.024008 | 16.178 |
| w30 | 44 | -0.081609 | -11.809 |
| w31 | 46 | -0.02572 | -12.662 |
| w32 | 45 | 0.02676 | 2.208 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 47 | 0.08295 | 21.049 |
| w11 | 39 | 0.000359 | -7.03 |
| w12 | 50 | -0.092442 | -17.662 |
| w13 | 46 | 0.102083 | 26.276 |
| w14 | 53 | 0.205102 | 67.069 |
| w15 | 49 | 0.027877 | -1.572 |
| w16 | 43 | 0.032481 | 32.373 |
| w17 | 46 | 0.17329 | 54.564 |
| w18 | 48 | 0.022924 | 5.721 |
| w19 | 43 | -0.010377 | -5.783 |
| w20 | 51 | 0.071024 | 5.352 |
| w21 | 39 | -0.045798 | -5.147 |
| w22 | 39 | 0.049732 | 9.045 |
| w23 | 46 | -0.039998 | -7.741 |
| w24 | 46 | 0.011489 | -5.219 |
| w25 | 41 | 0.000574 | -5.96 |
| w26 | 42 | -0.02055 | -5.435 |
| w27 | 42 | -0.13552 | -28.34 |
| w28 | 46 | -0.175957 | -43.2 |
| w29 | 48 | -0.023907 | -12.294 |
| w30 | 36 | -0.063434 | -7.026 |
| w31 | 39 | -0.054774 | -8.324 |
| w32 | 45 | -0.11051 | -26.287 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 47 | -0.17631 | -34.076 |
| w13 | 47 | -0.018374 | -15.071 |
| w14 | 44 | 0.087688 | 37.927 |
| w15 | 40 | -0.121883 | -18.566 |
| w16 | 46 | 0.012833 | 15.253 |
| w17 | 45 | 0.077992 | 16.384 |
| w18 | 43 | 0.075058 | 9.56 |
| w19 | 39 | -0.047607 | -11.769 |
| w20 | 47 | 0.12452 | 21.667 |
| w21 | 54 | 0.002509 | -7.177 |
| w22 | 47 | 0.204982 | 35.161 |
| w23 | 44 | 0.079618 | 11.308 |
| w24 | 44 | 0.054364 | -8.548 |
| w25 | 45 | -0.019762 | -12.578 |
| w26 | 46 | -0.000861 | 2.465 |
| w27 | 45 | -0.088036 | -23.627 |
| w28 | 43 | 0.006844 | -3.289 |
| w29 | 44 | -0.140871 | -32.824 |
| w30 | 37 | 0.025238 | 8.302 |
| w31 | 46 | -0.032306 | -18.451 |
| w32 | 42 | 0.073392 | 4.489 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 48 | -0.021953 | -9.676 |
| w16 | 51 | -0.03171 | 8.672 |
| w17 | 47 | 0.145488 | 27.095 |
| w18 | 54 | 0.022596 | 3.554 |
| w19 | 48 | 0.016842 | 2.203 |
| w20 | 51 | 0.058165 | 3.252 |
| w21 | 42 | 0.025164 | -4.304 |
| w22 | 42 | 0.010762 | -6.53 |
| w23 | 46 | 0.054292 | 9.209 |
| w24 | 43 | 0.070521 | 11.059 |
| w25 | 48 | 0.034277 | -3.498 |
| w26 | 47 | -0.061402 | -17.215 |
| w27 | 45 | 0.000799 | -7.866 |
| w28 | 46 | -0.018666 | -1.61 |
| w29 | 45 | -0.062748 | -19.036 |
| w30 | 44 | -0.020546 | 2.124 |
| w31 | 45 | -0.084985 | -25.068 |
| w32 | 43 | -0.085362 | -27.241 |

- w14 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ALGOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- TRXUSD: 18 of 18 windows run. w1 to w14 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 43 | -0.077332 | -15.872 |
| w16 | 50 | -0.076174 | 8.312 |
| w17 | 52 | 0.178748 | 34.976 |
| w18 | 36 | 0.025988 | 0.362 |
| w19 | 47 | -0.108169 | -21.705 |
| w20 | 52 | 0.161602 | 33.354 |
| w21 | 42 | -0.043293 | -15.971 |
| w22 | 39 | -0.041424 | -7.852 |
| w23 | 48 | 0.055727 | 9.43 |
| w24 | 34 | -0.049834 | -2.281 |
| w25 | 50 | 0.003104 | -5.593 |
| w26 | 53 | -0.139928 | -33.63 |
| w27 | 49 | -0.072855 | -13.546 |
| w28 | 37 | -0.000191 | -4.706 |
| w29 | 45 | -0.002498 | 8.215 |
| w30 | 49 | -0.0226 | -8.189 |
| w31 | 50 | 0.091345 | 5.815 |
| w32 | 39 | -0.16593 | -24.253 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 42 | -0.017894 | 5.849 |
| w17 | 50 | 0.11102 | 21.246 |
| w18 | 47 | 0.002354 | -6.342 |
| w19 | 49 | -0.078602 | -17.575 |
| w20 | 48 | 0.087107 | 13.392 |
| w21 | 43 | 0.075569 | 8.574 |
| w22 | 48 | 0.051283 | 1.104 |
| w23 | 47 | 0.057087 | -5.275 |
| w24 | 45 | 0.06869 | -3.81 |
| w25 | 42 | 0.118834 | 11.715 |
| w26 | 42 | -0.073043 | -10.209 |
| w27 | 46 | -0.156571 | -39.506 |
| w28 | 47 | 0.041755 | 3.647 |
| w29 | 46 | -0.109186 | -29.562 |
| w30 | 37 | -0.098918 | -25.912 |
| w31 | 43 | -0.097497 | -18.424 |
| w32 | 45 | -0.112502 | -28.116 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 47 | 0.074263 | 19.217 |
| w21 | 42 | 0.077664 | 9.747 |
| w22 | 40 | -0.025006 | -8.72 |
| w23 | 49 | 0.082937 | 13.302 |
| w24 | 35 | 0.035895 | 11.606 |
| w25 | 45 | 0.163564 | 35.496 |
| w26 | 41 | -0.106638 | -17.64 |
| w27 | 48 | -0.097391 | -18.759 |
| w28 | 46 | 0.066803 | 14.555 |
| w29 | 40 | -0.153629 | -31.447 |
| w30 | 39 | -0.098018 | -16.626 |
| w31 | 35 | -0.055432 | -10.968 |
| w32 | 44 | 0.047519 | 3.728 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 53 | 0.059056 | 6.59 |
| w23 | 45 | -0.021206 | -4.872 |
| w24 | 44 | 0.118486 | 15.963 |
| w25 | 52 | 0.046631 | 19.344 |
| w26 | 50 | 0.026128 | -5.806 |
| w27 | 43 | -0.037775 | -12.231 |
| w28 | 48 | 0.048317 | 10.916 |
| w29 | 43 | -0.160119 | -29.544 |
| w30 | 45 | -0.211324 | -40.759 |
| w31 | 42 | -0.050132 | -11.308 |
| w32 | 54 | 0.004647 | -9.289 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 54 | 0.196382 | 48.712 |
| w25 | 42 | 0.02163 | 4.481 |
| w26 | 40 | -0.112814 | -18.177 |
| w27 | 49 | 0.086515 | 54.95 |
| w28 | 43 | 0.101887 | 18.164 |
| w29 | 52 | -0.114213 | -23.221 |
| w30 | 40 | -0.073179 | -7.012 |
| w31 | 34 | -0.078279 | -11.338 |
| w32 | 44 | -0.030688 | -8.327 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 36 | 0.027485 | 15.914 |
| w6 | 40 | 0.058009 | 20.598 |
| w7 | 44 | -0.022435 | -0.575 |
| w8 | 49 | -0.011084 | -8.106 |
| w9 | 42 | -0.108622 | -24.87 |
| w10 | 45 | 0.095162 | 8.982 |
| w11 | 48 | 0.06464 | 5.467 |
| w12 | 40 | -0.011014 | -0.931 |
| w13 | 45 | 0.021675 | 2.573 |
| w14 | 48 | 0.054693 | 26.527 |
| w15 | 43 | -0.066491 | -15.779 |
| w16 | 43 | -0.091415 | -2.318 |
| w17 | 50 | 0.166569 | 45.578 |
| w18 | 50 | -0.008993 | -6.679 |
| w19 | 46 | -0.048928 | -18.49 |
| w20 | 44 | -0.002751 | -7.631 |
| w21 | 49 | -0.075543 | -6.125 |
| w22 | 44 | 0.061533 | 5.988 |
| w23 | 56 | -0.073353 | -12.538 |
| w24 | 45 | 0.046844 | 0.964 |
| w25 | 45 | -0.051768 | -15.463 |
| w26 | 43 | -0.100304 | -20.836 |
| w27 | 48 | -0.050979 | -7.936 |
| w28 | 51 | -0.138576 | -24.063 |
| w29 | 39 | -0.071488 | -19.865 |
| w30 | 45 | -0.02745 | 19.883 |
| w31 | 39 | -0.150256 | -26.244 |
| w32 | 45 | 0.029864 | 10.642 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 41 | 0.01547 | 22.072 |
| w6 | 48 | 0.153317 | 41.105 |
| w7 | 47 | 0.102432 | 22.941 |
| w8 | 48 | 0.005816 | -0.81 |
| w9 | 43 | 0.098634 | 18.296 |
| w10 | 44 | 0.216641 | 43.411 |
| w11 | 45 | -0.016081 | -4.745 |
| w12 | 38 | -0.00394 | -1.911 |
| w13 | 47 | 0.060765 | 15.42 |
| w14 | 43 | 0.299778 | 91.513 |
| w15 | 42 | 0.024948 | 2.064 |
| w16 | 40 | -0.01334 | 11.733 |
| w17 | 51 | 0.11769 | 30.386 |
| w18 | 44 | -0.159335 | -26.416 |
| w19 | 53 | 0.009641 | -9.627 |
| w20 | 50 | 0.068769 | 5.679 |
| w21 | 42 | 0.043947 | -1.367 |
| w22 | 44 | 0.030837 | -3.985 |
| w23 | 57 | 0.042339 | -9.985 |
| w24 | 49 | 0.050285 | -3.075 |
| w25 | 40 | -0.025039 | -6.682 |
| w26 | 42 | 0.164839 | 22.2 |
| w27 | 43 | -0.024777 | -17.988 |
| w28 | 33 | -0.01397 | -6.187 |
| w29 | 41 | -0.171807 | -38.24 |
| w30 | 45 | -0.134847 | -15.885 |
| w31 | 43 | -0.034969 | -11.04 |
| w32 | 39 | 0.063431 | 19.2 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 47 | -0.013888 | -8.413 |
| w18 | 52 | -0.015154 | 3.305 |
| w19 | 46 | -0.197359 | -31.797 |
| w20 | 52 | 0.017496 | -1.381 |
| w21 | 45 | 0.008182 | -1.897 |
| w22 | 47 | 0.117005 | 19.345 |
| w23 | 43 | -0.005441 | -5.049 |
| w24 | 50 | 0.09697 | 13.957 |
| w25 | 48 | 0.125914 | 18.536 |
| w26 | 46 | 0.013243 | -3.528 |
| w27 | 47 | 0.078498 | 20.565 |
| w28 | 49 | 0.025543 | 2.473 |
| w29 | 52 | -0.078233 | -22.97 |
| w30 | 41 | 0.039017 | 8.406 |
| w31 | 43 | -0.055273 | -13.337 |
| w32 | 43 | -0.035008 | -19.585 |

- w16 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_CRVUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- AAVEUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 46 | 0.099076 | 28.388 |
| w18 | 48 | -0.121331 | -21.897 |
| w19 | 39 | 0.00617 | -2.722 |
| w20 | 50 | 0.091925 | 14.398 |
| w21 | 44 | 0.072897 | 9.9 |
| w22 | 42 | 0.126821 | 22.272 |
| w23 | 49 | 0.027339 | 3.133 |
| w24 | 55 | -0.063798 | -9.56 |
| w25 | 41 | 0.165195 | 32.892 |
| w26 | 44 | -0.072987 | -19.417 |
| w27 | 47 | -0.108434 | -22.605 |
| w28 | 46 | 0.074672 | 11.163 |
| w29 | 46 | 0.009467 | 6.181 |
| w30 | 45 | 0.053105 | 12.548 |
| w31 | 41 | -0.067428 | -9.019 |
| w32 | 47 | -0.03131 | -9.808 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 35 | -0.045841 | -9.231 |
| w20 | 46 | 0.10534 | 22.167 |
| w21 | 39 | 0.010733 | -3.908 |
| w22 | 46 | -0.057628 | 11.938 |
| w23 | 44 | -0.029349 | -11.126 |
| w24 | 45 | 0.055168 | 21.985 |
| w25 | 46 | 0.051615 | -3.868 |
| w26 | 39 | -0.029877 | -13.47 |
| w27 | 41 | -0.041371 | -21.913 |
| w28 | 48 | 0.06206 | 10.255 |
| w29 | 35 | -0.235166 | -42.37 |
| w30 | 40 | -0.029727 | -1.235 |
| w31 | 44 | -0.112373 | -21.237 |
| w32 | 51 | 0.045234 | 7.898 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 43 | 0.167364 | 36.877 |
| w23 | 39 | -0.071443 | -15.263 |
| w24 | 47 | 0.220485 | 37.458 |
| w25 | 39 | -0.079869 | -24.174 |
| w26 | 43 | 0.036101 | 0.596 |
| w27 | 49 | -0.138381 | -36.113 |
| w28 | 37 | -0.087586 | -15.089 |
| w29 | 48 | -0.180124 | -36.3 |
| w30 | 39 | -0.085963 | -11.142 |
| w31 | 47 | 0.040116 | 4.192 |
| w32 | 46 | -0.072433 | -24.506 |

- w21 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_LDOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ONDOUSD: 6 of 6 windows run. w1 to w26 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w27 | 47 | 0.022462 | 8.011 |
| w28 | 45 | 0.088824 | 13.544 |
| w29 | 45 | -0.100306 | -22.469 |
| w30 | 45 | -0.089605 | -10.178 |
| w31 | 38 | -0.121544 | -17.017 |
| w32 | 39 | -0.064018 | -12.616 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 45 | 0.141511 | 30.961 |
| w18 | 47 | -0.038022 | -7.06 |
| w19 | 47 | -0.046084 | -11.507 |
| w20 | 51 | 0.018939 | -1.852 |
| w21 | 43 | 0.025502 | -1.03 |
| w22 | 47 | 0.040924 | 8.932 |
| w23 | 55 | 0.088988 | 10.742 |
| w24 | 43 | 0.01203 | -11.71 |
| w25 | 47 | 0.027319 | -6.034 |
| w26 | 43 | 0.096386 | 12.392 |
| w27 | 46 | -0.110173 | -28.944 |
| w28 | 45 | 0.043588 | 6.677 |
| w29 | 40 | -0.099043 | -24.566 |
| w30 | 43 | -0.314358 | -58.716 |
| w31 | 38 | -0.066642 | -14.789 |
| w32 | 43 | -0.047141 | -17.693 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 41 | 0.121954 | 24.442 |
| w18 | 44 | 0.032006 | -2.328 |
| w19 | 38 | -0.055703 | -10.898 |
| w20 | 49 | -0.016795 | -10.548 |
| w21 | 39 | -0.106999 | -15.885 |
| w22 | 48 | -0.008879 | 8.821 |
| w23 | 46 | 0.029488 | -1.694 |
| w24 | 50 | 0.082921 | 9.286 |
| w25 | 47 | 0.013732 | -2.306 |
| w26 | 43 | 0.045161 | 2.87 |
| w27 | 42 | -0.10177 | -24.738 |
| w28 | 42 | 0.09914 | 17.182 |
| w29 | 47 | -0.170702 | -34.259 |
| w30 | 41 | -0.016206 | -0.743 |
| w31 | 38 | -0.040558 | -5.438 |
| w32 | 36 | -0.038604 | -29.737 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 43 | -0.051878 | -12.355 |
| w29 | 42 | -0.075739 | -18.007 |
| w30 | 38 | -0.062082 | -11.305 |
| w31 | 51 | -0.098561 | -24.96 |
| w32 | 38 | 0.076111 | 13.803 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 46 | 0.0079 | 15.862 |
| w15 | 45 | 0.056785 | 5.762 |
| w16 | 53 | 0.17397 | 189.115 |
| w17 | 45 | 0.006087 | -2.721 |
| w18 | 45 | 0.013098 | 0.305 |
| w19 | 44 | -0.050823 | -12.576 |
| w20 | 43 | 0.141158 | 21.888 |
| w21 | 50 | -0.058375 | -13.611 |
| w22 | 41 | 0.001895 | -1.302 |
| w23 | 50 | 0.117358 | 19.389 |
| w24 | 45 | 0.089785 | 16.381 |
| w25 | 42 | -0.029736 | -5.821 |
| w26 | 50 | -0.010464 | -5.122 |
| w27 | 39 | -0.122891 | -11.869 |
| w28 | 42 | -0.048493 | -6.121 |
| w29 | 50 | -0.152323 | -30.764 |
| w30 | 40 | -0.080072 | -13.54 |
| w31 | 40 | -0.104357 | -19.545 |
| w32 | 41 | -0.028207 | -11.541 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 42 | 0.055901 | 13.937 |
| w26 | 47 | 0.043515 | 2.549 |
| w27 | 49 | -0.109219 | -20.353 |
| w28 | 42 | 0.137561 | 22.753 |
| w29 | 53 | -0.194606 | -37.422 |
| w30 | 53 | -0.073028 | -9.639 |
| w31 | 44 | -0.002302 | -7.576 |
| w32 | 48 | -0.059838 | -26.045 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

