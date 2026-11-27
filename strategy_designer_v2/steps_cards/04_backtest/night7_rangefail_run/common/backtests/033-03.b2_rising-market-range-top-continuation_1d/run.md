# Backtest of 033-03.b2_rising-market-range-top-continuation_1d

- Plan: `../../../../../03_test_plan/night7_rangefail_run/plans/033-03.b2_rising-market-range-top-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.172754 | -4.414 |
| w2 | 35 | 0.184935 | 82.146 |
| w3 | 44 | -0.034827 | 45.725 |
| w4 | 43 | 0.056859 | -14.214 |
| w5 | 59 | 0.0518 | 80.507 |
| w6 | 49 | 0.077738 | 90.971 |
| w7 | 11 | -0.032378 | -5.581 |
| w8 | 8 | -0.028912 | -0.389 |
| w9 | 1 | -0.060777 | -9.129 |
| w10 | 21 | 0.09461 | 27.941 |
| w11 | 58 | 0.040699 | 29.913 |
| w12 | 1 | -0.008497 | -0.522 |
| w13 | 19 | 0.008642 | -1.89 |
| w14 | 50 | -0.168534 | 6.793 |
| w15 | 42 | 0.140817 | 54.687 |
| w16 | 59 | -0.055117 | 4.609 |
| w17 | 21 | 0.047208 | 4.976 |
| w18 | 36 | 0.047388 | 11.722 |
| w19 | 6 | 0.082852 | 4.351 |
| w20 | 2 | 0.050728 | -9.634 |
| w21 | 4 | -0.018756 | -27.969 |
| w22 | 45 | -0.009401 | 16.999 |
| w23 | 29 | -0.045878 | 10.753 |
| w24 | 29 | -0.030715 | 43.874 |
| w25 | 49 | -0.003299 | 18.001 |
| w26 | 0 | None | 0.0 |
| w27 | 35 | 0.05085 | 23.367 |
| w28 | 11 | -0.115263 | -12.148 |
| w29 | 53 | -0.034633 | -7.292 |
| w30 | 0 | None | 0.0 |
| w31 | 11 | -0.020262 | 3.662 |
| w32 | 18 | 0.120037 | 18.913 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.004549 | -5.357 |
| w2 | 33 | 0.105219 | 28.9 |
| w3 | 6 | -0.130973 | -10.99 |
| w4 | 25 | -0.023977 | -16.675 |
| w5 | 60 | -0.014803 | 44.392 |
| w6 | 48 | 0.054626 | 56.653 |
| w7 | 18 | -0.065341 | -2.046 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 43 | -0.015551 | 29.322 |
| w11 | 36 | 0.093629 | 22.557 |
| w12 | 0 | None | 0.0 |
| w13 | 26 | 0.076071 | 30.509 |
| w14 | 40 | -0.09593 | -1.299 |
| w15 | 35 | 0.044954 | 9.409 |
| w16 | 62 | -0.024631 | 3.863 |
| w17 | 14 | 0.045386 | -4.933 |
| w18 | 39 | 0.092848 | 35.457 |
| w19 | 8 | 0.002745 | -8.069 |
| w20 | 4 | 0.019745 | -3.788 |
| w21 | 30 | -0.04516 | -15.575 |
| w22 | 33 | 0.036725 | 8.043 |
| w23 | 11 | -0.074981 | -1.709 |
| w24 | 24 | -0.074811 | -10.562 |
| w25 | 29 | -0.10689 | -17.988 |
| w26 | 0 | None | 0.0 |
| w27 | 42 | 0.018851 | 13.067 |
| w28 | 26 | -0.208538 | -25.038 |
| w29 | 31 | -0.10457 | -11.345 |
| w30 | 12 | -0.096715 | -6.154 |
| w31 | 2 | -0.019916 | -3.953 |
| w32 | 11 | -0.169498 | -18.541 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 36 | 0.194054 | 105.982 |
| w7 | 24 | -0.001127 | -1.288 |
| w8 | 5 | -0.05865 | -6.386 |
| w9 | 24 | -0.059814 | -0.209 |
| w10 | 8 | -0.140269 | -7.531 |
| w11 | 31 | -0.033279 | 0.903 |
| w12 | 12 | -0.096512 | -9.469 |
| w13 | 12 | 0.123421 | 55.333 |
| w14 | 33 | 0.058304 | 29.523 |
| w15 | 28 | 0.261093 | 114.38 |
| w16 | 40 | 0.028659 | 15.857 |
| w17 | 21 | -0.1675 | -17.366 |
| w18 | 32 | 0.03085 | -2.685 |
| w19 | 8 | -0.007425 | -5.608 |
| w20 | 3 | 0.115759 | -2.707 |
| w21 | 35 | -0.006982 | 10.564 |
| w22 | 28 | -0.099682 | -3.129 |
| w23 | 32 | -0.012904 | -33.569 |
| w24 | 31 | 0.020679 | 13.424 |
| w25 | 18 | -0.189982 | -16.119 |
| w26 | 18 | -0.093505 | -7.033 |
| w27 | 28 | 0.315402 | 181.043 |
| w28 | 19 | -0.06346 | -6.926 |
| w29 | 29 | -0.041462 | -0.046 |
| w30 | 5 | -0.110942 | -3.744 |
| w31 | 0 | None | 0.0 |
| w32 | 3 | 0.128032 | 11.973 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 19 | -0.030915 | 9.853 |
| w8 | 22 | 0.068705 | 9.16 |
| w9 | 3 | -0.052584 | -5.888 |
| w10 | 34 | 0.131652 | 38.603 |
| w11 | 33 | -0.006176 | 0.257 |
| w12 | 0 | None | 0.0 |
| w13 | 20 | 0.039063 | 23.164 |
| w14 | 35 | -0.105069 | -14.238 |
| w15 | 29 | 0.009854 | -1.793 |
| w16 | 60 | 0.072128 | 42.972 |
| w17 | 23 | -0.090755 | -9.174 |
| w18 | 21 | -0.031001 | -2.547 |
| w19 | 7 | -0.030056 | -6.131 |
| w20 | 7 | 0.048252 | 3.603 |
| w21 | 8 | -0.20442 | -23.769 |
| w22 | 30 | 0.043229 | 12.086 |
| w23 | 25 | 0.220503 | 84.144 |
| w24 | 25 | -0.073228 | -9.568 |
| w25 | 38 | 0.087093 | 14.15 |
| w26 | 6 | 0.051429 | 2.988 |
| w27 | 30 | 0.081819 | -6.886 |
| w28 | 7 | -0.124156 | -7.976 |
| w29 | 63 | -0.208568 | -14.84 |
| w30 | 23 | -0.088355 | -10.284 |
| w31 | 15 | 0.07563 | 5.711 |
| w32 | 4 | 0.222787 | 23.23 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 57 | 0.208986 | 174.277 |
| w2 | 32 | -0.007191 | 0.748 |
| w3 | 12 | 0.010259 | 3.547 |
| w4 | 40 | 0.029175 | 154.779 |
| w5 | 37 | 0.172523 | 102.053 |
| w6 | 40 | 0.058494 | 54.616 |
| w7 | 27 | 0.002537 | 21.498 |
| w8 | 16 | -0.015687 | 7.948 |
| w9 | 2 | -0.034428 | -8.345 |
| w10 | 35 | -0.071014 | -5.859 |
| w11 | 38 | 0.130986 | 31.568 |
| w12 | 3 | -0.048029 | -4.103 |
| w13 | 17 | 0.147224 | 50.925 |
| w14 | 58 | -0.008573 | 37.725 |
| w15 | 45 | 0.037048 | -1.173 |
| w16 | 53 | -0.052438 | 41.316 |
| w17 | 34 | -0.028986 | 6.404 |
| w18 | 61 | -0.105992 | -13.022 |
| w19 | 8 | 0.093385 | 12.763 |
| w20 | 10 | -0.032792 | -3.197 |
| w21 | 9 | -0.069214 | -7.057 |
| w22 | 45 | -0.069348 | -2.783 |
| w23 | 11 | -0.128713 | 1.252 |
| w24 | 29 | -0.099947 | 20.306 |
| w25 | 51 | 0.059014 | -1.904 |
| w26 | 15 | -0.035139 | 6.398 |
| w27 | 30 | 0.075942 | 22.115 |
| w28 | 6 | -0.188097 | -13.398 |
| w29 | 37 | -0.040407 | 35.52 |
| w30 | 21 | -0.003912 | -12.111 |
| w31 | 14 | -0.037407 | -1.88 |
| w32 | 18 | 0.176607 | 39.611 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 40 | 0.072093 | 39.46 |
| w11 | 31 | -0.052161 | -0.456 |
| w12 | 0 | None | 0.0 |
| w13 | 24 | 0.113302 | 60.957 |
| w14 | 58 | 0.026039 | 53.903 |
| w15 | 27 | -0.067137 | 11.437 |
| w16 | 54 | 0.050495 | 53.545 |
| w17 | 38 | 0.020453 | 20.608 |
| w18 | 23 | -0.107521 | -8.649 |
| w19 | 5 | 0.021322 | -8.315 |
| w20 | 6 | 0.039543 | -8.755 |
| w21 | 1 | -0.055794 | -3.194 |
| w22 | 31 | 0.021493 | 4.494 |
| w23 | 9 | 0.053815 | 12.637 |
| w24 | 30 | 0.117627 | 82.99 |
| w25 | 45 | -0.061234 | -6.503 |
| w26 | 0 | None | 0.0 |
| w27 | 24 | 0.313869 | 138.699 |
| w28 | 15 | -0.19237 | -22.488 |
| w29 | 28 | -0.060702 | -13.859 |
| w30 | 16 | -0.134995 | -17.552 |
| w31 | 0 | None | 0.0 |
| w32 | 12 | 0.022507 | 0.807 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 33 | -0.143987 | -6.0 |
| w13 | 17 | -0.047707 | -33.541 |
| w14 | 53 | 0.004034 | 27.127 |
| w15 | 29 | 0.082104 | 27.638 |
| w16 | 59 | -0.001834 | 38.539 |
| w17 | 16 | 0.044685 | 17.021 |
| w18 | 35 | -0.106915 | -0.893 |
| w19 | 26 | -0.112147 | -11.641 |
| w20 | 18 | -0.030088 | -15.705 |
| w21 | 20 | -0.00079 | -22.823 |
| w22 | 38 | -0.017844 | -0.399 |
| w23 | 0 | None | 0.0 |
| w24 | 31 | -0.16013 | 5.011 |
| w25 | 31 | 0.085583 | 19.927 |
| w26 | 0 | None | 0.0 |
| w27 | 26 | 0.183994 | 31.077 |
| w28 | 7 | -0.224585 | -7.803 |
| w29 | 12 | -0.062328 | -0.783 |
| w30 | 2 | -0.03535 | -0.807 |
| w31 | 5 | -0.030986 | -2.518 |
| w32 | 19 | 0.046408 | 13.982 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 13 | 0.047879 | -17.94 |
| w16 | 61 | 0.029535 | 7.643 |
| w17 | 13 | -0.126187 | -16.334 |
| w18 | 38 | -0.117766 | -4.739 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | 0.011842 | -10.591 |
| w21 | 9 | 0.002857 | -18.753 |
| w22 | 15 | 0.018743 | -1.208 |
| w23 | 0 | None | 0.0 |
| w24 | 25 | 0.036172 | 41.04 |
| w25 | 34 | 0.025641 | 5.123 |
| w26 | 0 | None | 0.0 |
| w27 | 27 | 0.186702 | 81.305 |
| w28 | 13 | -0.131356 | -7.911 |
| w29 | 37 | -0.072294 | -4.33 |
| w30 | 5 | -0.071563 | -2.009 |
| w31 | 16 | -0.155827 | -20.666 |
| w32 | 24 | -0.062417 | -24.662 |

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
| w15 | 35 | -0.104863 | -25.14 |
| w16 | 64 | -0.011113 | 47.119 |
| w17 | 27 | -0.006085 | 4.28 |
| w18 | 34 | -0.104112 | -23.612 |
| w19 | 6 | 0.063069 | 3.951 |
| w20 | 28 | -0.01995 | 3.499 |
| w21 | 0 | None | 0.0 |
| w22 | 37 | 0.02407 | 19.002 |
| w23 | 32 | -0.070027 | -22.339 |
| w24 | 52 | -0.196362 | -10.741 |
| w25 | 25 | 0.180405 | 47.995 |
| w26 | 24 | 0.226854 | 6.823 |
| w27 | 55 | 0.097909 | 143.931 |
| w28 | 12 | -0.157311 | -6.539 |
| w29 | 62 | -0.042498 | 11.18 |
| w30 | 15 | 0.040327 | -3.909 |
| w31 | 20 | -0.102956 | -10.45 |
| w32 | 7 | 0.148763 | 23.496 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 53 | -0.010274 | 16.877 |
| w17 | 12 | -0.035573 | -27.052 |
| w18 | 49 | -0.02752 | 1.501 |
| w19 | 10 | 0.056437 | 2.32 |
| w20 | 3 | -0.029993 | -7.324 |
| w21 | 1 | -0.083734 | -4.767 |
| w22 | 31 | -0.110508 | -18.299 |
| w23 | 4 | 0.060383 | 13.003 |
| w24 | 31 | 0.027246 | 30.861 |
| w25 | 47 | -0.004071 | 0.399 |
| w26 | 0 | None | 0.0 |
| w27 | 19 | 0.169195 | 42.619 |
| w28 | 8 | -0.190396 | -13.441 |
| w29 | 17 | -0.068044 | 4.471 |
| w30 | 11 | -0.176158 | -28.842 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 11 | 0.046102 | 8.18 |
| w21 | 4 | 0.034008 | 3.024 |
| w22 | 35 | -0.010957 | -16.893 |
| w23 | 0 | None | 0.0 |
| w24 | 20 | 0.2178 | 113.062 |
| w25 | 42 | 0.062799 | 39.745 |
| w26 | 0 | None | 0.0 |
| w27 | 47 | 0.078808 | -13.818 |
| w28 | 13 | -0.194378 | -16.34 |
| w29 | 30 | -0.141656 | -18.853 |
| w30 | 30 | 0.184615 | 27.436 |
| w31 | 2 | 0.015755 | -0.622 |
| w32 | 6 | 0.007356 | -1.435 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 35 | -0.076037 | -12.345 |
| w23 | 5 | 0.039374 | 7.294 |
| w24 | 28 | 0.095777 | 67.659 |
| w25 | 54 | 0.015365 | 5.037 |
| w26 | 10 | -0.016287 | 3.006 |
| w27 | 37 | 0.139381 | 33.339 |
| w28 | 6 | -0.154588 | -11.149 |
| w29 | 25 | -0.036605 | -0.516 |
| w30 | 11 | -0.091077 | -28.242 |
| w31 | 15 | 0.018077 | -3.638 |
| w32 | 39 | 0.021946 | 16.038 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 28 | -0.133416 | -8.082 |
| w25 | 46 | 0.021532 | 47.682 |
| w26 | 1 | -0.102908 | -8.05 |
| w27 | 58 | -0.069541 | -4.563 |
| w28 | 17 | 0.019728 | -0.076 |
| w29 | 39 | -0.013502 | -2.583 |
| w30 | 6 | -0.078078 | -2.723 |
| w31 | 2 | 0.012529 | -3.252 |
| w32 | 13 | 0.114782 | 17.077 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 41 | 0.18271 | 2.705 |
| w6 | 32 | 0.087 | -14.415 |
| w7 | 19 | 0.008337 | -0.174 |
| w8 | 11 | 0.053522 | 8.587 |
| w9 | 4 | -0.056234 | -12.615 |
| w10 | 19 | 0.162311 | 28.65 |
| w11 | 43 | 0.065203 | 13.385 |
| w12 | 0 | None | 0.0 |
| w13 | 28 | 0.179325 | 44.137 |
| w14 | 60 | -0.114775 | -0.899 |
| w15 | 14 | -0.044998 | -11.144 |
| w16 | 60 | 0.031517 | 12.463 |
| w17 | 19 | 0.06496 | -11.373 |
| w18 | 43 | -0.016521 | -13.329 |
| w19 | 21 | 0.051119 | 12.573 |
| w20 | 8 | 0.050571 | 2.27 |
| w21 | 4 | -0.029418 | -2.462 |
| w22 | 15 | 0.045857 | 1.642 |
| w23 | 6 | 0.056141 | 13.283 |
| w24 | 32 | -0.08953 | -3.485 |
| w25 | 21 | 0.133776 | 1.401 |
| w26 | 26 | 0.095354 | -3.034 |
| w27 | 36 | -0.043245 | 0.514 |
| w28 | 12 | -0.034501 | -8.122 |
| w29 | 33 | 0.093509 | 2.709 |
| w30 | 47 | 0.118654 | 190.188 |
| w31 | 13 | 0.138328 | 15.121 |
| w32 | 46 | 0.072942 | 81.907 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 52 | 0.137544 | 88.756 |
| w6 | 43 | 0.096305 | 53.048 |
| w7 | 14 | -0.056953 | -0.644 |
| w8 | 0 | None | 0.0 |
| w9 | 6 | 0.001517 | 5.401 |
| w10 | 34 | -0.001779 | 8.816 |
| w11 | 40 | -0.023024 | 13.542 |
| w12 | 0 | None | 0.0 |
| w13 | 28 | 0.052613 | 18.695 |
| w14 | 47 | -0.160291 | 1.863 |
| w15 | 64 | -0.086211 | 7.209 |
| w16 | 64 | 0.011589 | 17.625 |
| w17 | 20 | 0.114405 | 6.017 |
| w18 | 18 | -0.058127 | -13.188 |
| w19 | 24 | 0.054648 | 12.175 |
| w20 | 13 | -0.033047 | 2.504 |
| w21 | 10 | -0.198438 | -11.076 |
| w22 | 26 | 0.103722 | 14.916 |
| w23 | 13 | 0.117533 | 7.711 |
| w24 | 34 | -0.111374 | -10.824 |
| w25 | 0 | -0.083277 | 0.0 |
| w26 | 35 | -0.04486 | -3.296 |
| w27 | 25 | -0.071337 | -1.908 |
| w28 | 31 | -0.154923 | -2.824 |
| w29 | 26 | 0.123436 | 37.033 |
| w30 | 55 | -0.192904 | -32.08 |
| w31 | 24 | 0.109047 | -15.12 |
| w32 | 35 | 0.030924 | 39.456 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 14 | -0.253209 | -23.232 |
| w18 | 64 | -0.172392 | -16.883 |
| w19 | 13 | -0.095761 | -9.125 |
| w20 | 18 | -0.095598 | -13.682 |
| w21 | 6 | -0.016774 | -3.838 |
| w22 | 37 | -0.046419 | 11.595 |
| w23 | 0 | None | 0.0 |
| w24 | 28 | -0.111095 | -0.153 |
| w25 | 24 | 0.053579 | 19.879 |
| w26 | 1 | -0.075027 | -4.039 |
| w27 | 35 | 0.100329 | 72.284 |
| w28 | 21 | -0.021376 | -3.283 |
| w29 | 46 | -0.093562 | -8.926 |
| w30 | 7 | -0.10252 | -5.16 |
| w31 | 0 | None | 0.0 |
| w32 | 21 | 0.102845 | 7.61 |

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
| w17 | 20 | -0.086062 | -23.052 |
| w18 | 9 | -0.112749 | -21.095 |
| w19 | 13 | 0.062635 | 15.276 |
| w20 | 15 | 0.000957 | 3.483 |
| w21 | 12 | -0.151601 | -29.529 |
| w22 | 34 | 0.016292 | 16.327 |
| w23 | 20 | 0.153068 | 12.499 |
| w24 | 45 | -0.146327 | -46.742 |
| w25 | 21 | -0.000964 | -29.418 |
| w26 | 20 | -0.032663 | -17.076 |
| w27 | 51 | -0.072099 | -20.345 |
| w28 | 19 | -0.072315 | -1.214 |
| w29 | 51 | -0.039976 | 3.278 |
| w30 | 3 | -0.127444 | -2.016 |
| w31 | 0 | None | 0.0 |
| w32 | 15 | 0.066235 | -22.517 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 17 | 0.000896 | -4.139 |
| w20 | 8 | -0.108224 | -7.859 |
| w21 | 32 | -0.068741 | -21.139 |
| w22 | 48 | 0.012901 | 89.75 |
| w23 | 41 | -0.054658 | -17.398 |
| w24 | 28 | 0.124116 | 177.834 |
| w25 | 30 | -0.137503 | -10.474 |
| w26 | 3 | -0.080855 | -27.03 |
| w27 | 45 | 0.112886 | 8.988 |
| w28 | 6 | -0.166026 | -15.44 |
| w29 | 43 | -0.036969 | -6.886 |
| w30 | 10 | -0.040391 | -5.022 |
| w31 | 4 | -0.005138 | -4.056 |
| w32 | 40 | 0.059237 | 26.837 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 41 | -0.065734 | 8.698 |
| w23 | 4 | -0.029335 | -10.934 |
| w24 | 41 | -0.124697 | 11.85 |
| w25 | 44 | -0.001143 | -17.473 |
| w26 | 8 | -0.110878 | -10.353 |
| w27 | 26 | -0.024248 | 2.794 |
| w28 | 19 | -0.18503 | -23.468 |
| w29 | 31 | -0.052889 | -39.892 |
| w30 | 16 | -0.220651 | -13.049 |
| w31 | 4 | -0.230859 | -20.08 |
| w32 | 27 | 0.090233 | -4.629 |

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
| w27 | 32 | 0.162362 | 55.26 |
| w28 | 14 | -0.052984 | -1.937 |
| w29 | 31 | -0.088719 | -14.697 |
| w30 | 7 | -0.026532 | -10.599 |
| w31 | 2 | -0.128754 | -0.154 |
| w32 | 40 | -0.030387 | 14.324 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 14 | 0.159353 | 20.499 |
| w18 | 18 | 0.055968 | 15.738 |
| w19 | 6 | 0.000182 | -4.173 |
| w20 | 10 | 0.024304 | 2.383 |
| w21 | 7 | -0.097227 | -24.992 |
| w22 | 34 | -0.091884 | -16.099 |
| w23 | 6 | 0.058955 | 10.201 |
| w24 | 36 | -0.063313 | 6.533 |
| w25 | 48 | 0.094956 | 25.409 |
| w26 | 0 | None | 0.0 |
| w27 | 27 | 0.144884 | 33.465 |
| w28 | 13 | -0.24959 | -15.023 |
| w29 | 10 | -0.106129 | -5.477 |
| w30 | 1 | -0.151457 | -8.713 |
| w31 | 0 | None | 0.0 |
| w32 | 13 | 0.098626 | 13.092 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 12 | 0.063429 | 6.241 |
| w18 | 39 | -0.041508 | -8.218 |
| w19 | 3 | -0.007875 | -2.639 |
| w20 | 8 | 0.041443 | -0.549 |
| w21 | 6 | -0.00747 | 2.295 |
| w22 | 44 | 0.073431 | 57.891 |
| w23 | 1 | -0.132311 | -2.33 |
| w24 | 33 | -0.102701 | 26.472 |
| w25 | 41 | 0.131659 | 34.239 |
| w26 | 1 | 0.130783 | 6.344 |
| w27 | 34 | 0.121423 | 16.93 |
| w28 | 10 | -0.228746 | -18.066 |
| w29 | 30 | 0.053265 | 15.858 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | -0.055668 | -8.839 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 6 | -0.031241 | -4.924 |
| w29 | 27 | -0.026003 | 1.624 |
| w30 | 16 | -0.046684 | -12.07 |
| w31 | 20 | -0.004354 | -5.134 |
| w32 | 16 | 0.012003 | -7.137 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 48 | -0.016212 | 5.396 |
| w15 | 22 | 0.146662 | 57.97 |
| w16 | 58 | -0.110861 | -93.219 |
| w17 | 34 | -0.040204 | -7.929 |
| w18 | 18 | 0.054633 | 1.674 |
| w19 | 2 | -0.365992 | -20.197 |
| w20 | 5 | 0.038065 | 4.909 |
| w21 | 29 | 0.116757 | 54.648 |
| w22 | 14 | 0.030334 | 7.607 |
| w23 | 12 | 0.020203 | 7.266 |
| w24 | 26 | -0.024429 | -0.88 |
| w25 | 40 | 0.108644 | 37.92 |
| w26 | 4 | -0.06781 | 1.603 |
| w27 | 37 | 0.241152 | 122.44 |
| w28 | 9 | -0.184041 | -18.548 |
| w29 | 45 | 0.001564 | 0.735 |
| w30 | 17 | -0.007196 | -20.606 |
| w31 | 1 | 0.0561 | 2.872 |
| w32 | 23 | 0.032821 | 8.463 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 41 | 0.165337 | 85.469 |
| w26 | 33 | 0.057877 | 10.955 |
| w27 | 42 | 0.094374 | 34.917 |
| w28 | 9 | -0.071885 | -4.548 |
| w29 | 41 | 0.060069 | 10.597 |
| w30 | 0 | None | 0.0 |
| w31 | 10 | -0.037864 | -9.619 |
| w32 | 13 | 0.121983 | 16.43 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

