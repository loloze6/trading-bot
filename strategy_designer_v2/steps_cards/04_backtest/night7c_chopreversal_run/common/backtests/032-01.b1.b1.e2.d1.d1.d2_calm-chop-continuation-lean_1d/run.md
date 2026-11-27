# Backtest of 032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d

- Plan: `../../../../../03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | -0.0015 | 0.742 |
| w2 | 20 | 0.185758 | 37.884 |
| w3 | 36 | -0.130603 | 31.391 |
| w4 | 16 | -0.10981 | -8.716 |
| w5 | 17 | -0.069861 | -4.865 |
| w6 | 17 | 0.054565 | 15.112 |
| w7 | 31 | -0.046762 | -6.463 |
| w8 | 27 | 0.026389 | 2.339 |
| w9 | 21 | -0.176889 | -23.791 |
| w10 | 31 | 0.018523 | 44.556 |
| w11 | 29 | 0.091631 | 54.246 |
| w12 | 27 | 0.031445 | -5.68 |
| w13 | 26 | 0.135443 | 39.318 |
| w14 | 24 | 0.143137 | 27.125 |
| w15 | 29 | 0.027061 | 13.656 |
| w16 | 35 | -0.006582 | 18.497 |
| w17 | 27 | 0.133759 | 12.899 |
| w18 | 44 | -0.119296 | -25.849 |
| w19 | 35 | -0.044067 | 19.449 |
| w20 | 33 | 0.175992 | 37.258 |
| w21 | 32 | -0.006418 | 2.215 |
| w22 | 32 | 0.095303 | 28.633 |
| w23 | 38 | 0.125092 | 20.575 |
| w24 | 24 | 0.0883 | 56.948 |
| w25 | 28 | -0.086595 | 2.499 |
| w26 | 37 | -0.0553 | 0.056 |
| w27 | 31 | -0.095327 | 0.32 |
| w28 | 41 | -0.140855 | -2.284 |
| w29 | 34 | -0.042223 | 7.705 |
| w30 | 42 | 0.062584 | -8.939 |
| w31 | 31 | 0.040326 | 14.395 |
| w32 | 27 | 0.207345 | -19.096 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | -0.078256 | 17.5 |
| w2 | 32 | 0.034024 | 10.472 |
| w3 | 45 | -0.169097 | -23.285 |
| w4 | 33 | 0.065598 | 95.553 |
| w5 | 25 | -0.069774 | 15.359 |
| w6 | 22 | -0.081468 | 5.502 |
| w7 | 21 | 0.035138 | -0.181 |
| w8 | 29 | 0.153542 | 37.624 |
| w9 | 29 | -0.036936 | -15.56 |
| w10 | 27 | -0.003283 | 27.779 |
| w11 | 33 | 0.130992 | 22.761 |
| w12 | 28 | -0.043732 | -39.684 |
| w13 | 18 | 0.151566 | 43.748 |
| w14 | 35 | -0.063243 | 9.65 |
| w15 | 35 | -0.058927 | -16.793 |
| w16 | 31 | 0.078028 | 10.585 |
| w17 | 32 | 0.098988 | 11.103 |
| w18 | 28 | 0.044364 | 22.141 |
| w19 | 32 | -0.07302 | -30.998 |
| w20 | 38 | 0.036198 | 0.332 |
| w21 | 36 | -0.004096 | -15.575 |
| w22 | 28 | -0.008763 | -13.332 |
| w23 | 33 | -0.089329 | -8.583 |
| w24 | 38 | -0.108531 | -26.398 |
| w25 | 31 | -0.003002 | 19.678 |
| w26 | 36 | -0.140407 | -13.158 |
| w27 | 38 | -0.075122 | 46.499 |
| w28 | 44 | -0.096869 | -21.947 |
| w29 | 24 | -0.072166 | 15.202 |
| w30 | 36 | -0.07246 | -20.705 |
| w31 | 35 | 0.01961 | 15.874 |
| w32 | 42 | 0.070807 | -22.459 |

- XRPUSD: 26 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 20 | 0.038652 | 26.051 |
| w8 | 35 | 0.073551 | 26.911 |
| w9 | 23 | 0.225433 | 32.077 |
| w10 | 33 | -0.127049 | -25.703 |
| w11 | 37 | 0.040219 | 9.744 |
| w12 | 28 | 0.038401 | 9.954 |
| w13 | 25 | 0.089035 | 23.882 |
| w14 | 30 | -0.040821 | 27.336 |
| w15 | 33 | -0.04053 | 26.542 |
| w16 | 25 | -0.00313 | 26.068 |
| w17 | 34 | -0.031185 | 22.951 |
| w18 | 24 | -0.085594 | 14.18 |
| w19 | 26 | -0.045146 | 29.762 |
| w20 | 0 | 0.02764 | 0.0 |
| w21 | 36 | 0.043918 | 3.941 |
| w22 | 33 | -0.022517 | -14.658 |
| w23 | 19 | -0.004302 | -25.705 |
| w24 | 29 | -0.02226 | -13.429 |
| w25 | 36 | 0.035274 | 2.885 |
| w26 | 44 | 0.062015 | -16.211 |
| w27 | 31 | 0.034384 | -25.138 |
| w28 | 31 | 0.044775 | -9.292 |
| w29 | 29 | 0.067459 | 28.82 |
| w30 | 35 | -0.023529 | -17.842 |
| w31 | 28 | -0.019603 | 3.012 |
| w32 | 43 | 0.080221 | -29.604 |

- w6 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 106 warm-up bars -- required_bars=114. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- BCHUSD: 25 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 26 | 0.053267 | 10.085 |
| w9 | 24 | 0.11846 | 16.654 |
| w10 | 18 | -0.045378 | -2.944 |
| w11 | 33 | -0.056219 | 10.691 |
| w12 | 25 | 0.021113 | -3.801 |
| w13 | 18 | 0.044635 | 30.968 |
| w14 | 41 | -0.1079 | 2.48 |
| w15 | 39 | -0.114689 | -46.423 |
| w16 | 36 | 0.144505 | 46.696 |
| w17 | 31 | 0.07664 | 20.716 |
| w18 | 36 | -0.036923 | -2.836 |
| w19 | 42 | 0.057626 | -11.699 |
| w20 | 27 | 0.177614 | 35.272 |
| w21 | 38 | -0.12104 | -32.185 |
| w22 | 45 | 0.109551 | -15.868 |
| w23 | 32 | 0.22671 | 58.105 |
| w24 | 39 | -0.081514 | -32.94 |
| w25 | 17 | -0.077881 | -13.707 |
| w26 | 28 | -0.124745 | -27.835 |
| w27 | 44 | -0.079731 | 4.592 |
| w28 | 33 | -0.11891 | 7.166 |
| w29 | 42 | -0.223224 | -12.516 |
| w30 | 49 | -0.076929 | -39.383 |
| w31 | 28 | -0.036398 | 13.844 |
| w32 | 22 | -0.000564 | -73.242 |

- w7 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_BCHUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.133781 | 55.343 |
| w2 | 29 | -0.064352 | 14.409 |
| w3 | 29 | 0.04798 | 18.68 |
| w4 | 16 | 0.105761 | 61.649 |
| w5 | 13 | -0.019243 | 6.419 |
| w6 | 26 | -0.045753 | 26.901 |
| w7 | 17 | 0.036151 | 7.153 |
| w8 | 33 | 0.052253 | 19.749 |
| w9 | 19 | 0.004346 | 14.321 |
| w10 | 34 | 0.21083 | 17.678 |
| w11 | 34 | 0.115099 | 58.952 |
| w12 | 28 | 0.003236 | -2.091 |
| w13 | 13 | 0.034277 | 7.211 |
| w14 | 24 | -0.009565 | 27.222 |
| w15 | 39 | -0.068951 | -6.321 |
| w16 | 34 | 0.130223 | 86.329 |
| w17 | 26 | 0.08996 | 27.342 |
| w18 | 29 | -0.222604 | -16.434 |
| w19 | 23 | -0.006074 | 14.094 |
| w20 | 25 | 0.163622 | 58.92 |
| w21 | 33 | -0.015343 | 0.369 |
| w22 | 33 | 0.026726 | -3.939 |
| w23 | 35 | -0.033544 | -2.914 |
| w24 | 31 | 0.002371 | 25.628 |
| w25 | 22 | -0.05843 | 3.849 |
| w26 | 37 | 0.10106 | -3.97 |
| w27 | 39 | -0.192461 | -53.92 |
| w28 | 36 | -0.070135 | 27.795 |
| w29 | 17 | 0.036963 | 4.601 |
| w30 | 30 | 0.030538 | 8.232 |
| w31 | 27 | -0.025175 | 15.322 |
| w32 | 27 | 0.075126 | 82.281 |

- ADAUSD: 22 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 33 | -0.033981 | 15.2 |
| w12 | 43 | -0.127312 | -44.588 |
| w13 | 22 | 0.06317 | 74.593 |
| w14 | 18 | 0.18127 | 66.584 |
| w15 | 37 | 0.04227 | -14.227 |
| w16 | 28 | -0.011708 | 46.96 |
| w17 | 29 | 0.04585 | 53.115 |
| w18 | 30 | -0.120254 | 15.076 |
| w19 | 36 | 0.049902 | 13.388 |
| w20 | 31 | -0.110956 | -20.27 |
| w21 | 21 | 0.019465 | 26.613 |
| w22 | 23 | 0.032521 | 4.396 |
| w23 | 31 | 0.174531 | 45.339 |
| w24 | 36 | 0.042797 | 39.229 |
| w25 | 30 | -0.023784 | -11.463 |
| w26 | 34 | -0.08386 | -2.764 |
| w27 | 36 | -0.097338 | -60.789 |
| w28 | 28 | -0.112684 | -13.637 |
| w29 | 29 | 0.048608 | 15.746 |
| w30 | 38 | 0.061702 | 11.705 |
| w31 | 32 | -0.183386 | -5.79 |
| w32 | 34 | 0.084807 | 16.657 |

- w10 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 95 warm-up bars -- required_bars=114. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ATOMUSD: 20 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 38 | 0.052885 | 0.239 |
| w14 | 24 | 0.100211 | 70.177 |
| w15 | 40 | -0.109905 | -35.835 |
| w16 | 33 | -0.132811 | 14.988 |
| w17 | 26 | -0.057976 | 1.429 |
| w18 | 24 | -0.092808 | 0.104 |
| w19 | 37 | -2.8e-05 | -15.617 |
| w20 | 29 | 0.041462 | -4.826 |
| w21 | 37 | -0.010382 | 2.498 |
| w22 | 30 | 0.043719 | -8.777 |
| w23 | 27 | -0.016503 | 18.3 |
| w24 | 30 | -0.039074 | 28.543 |
| w25 | 30 | -0.025958 | 9.116 |
| w26 | 29 | 0.031929 | 21.855 |
| w27 | 45 | 0.03579 | -26.314 |
| w28 | 36 | -0.131497 | -19.892 |
| w29 | 43 | -0.083919 | -46.38 |
| w30 | 33 | 0.075025 | 28.113 |
| w31 | 33 | 0.148582 | 5.545 |
| w32 | 23 | 0.000711 | -13.102 |

- w12 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ATOMUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ALGOUSD: 17 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 32 | -0.034108 | -10.722 |
| w17 | 41 | -0.088315 | 27.273 |
| w18 | 36 | -0.005172 | 32.353 |
| w19 | 35 | -0.029241 | 17.439 |
| w20 | 43 | 0.023274 | -16.401 |
| w21 | 28 | 0.042931 | -41.507 |
| w22 | 28 | 0.021209 | -5.484 |
| w23 | 26 | -0.117609 | -13.835 |
| w24 | 33 | 0.032947 | 58.814 |
| w25 | 28 | -0.104042 | 0.446 |
| w26 | 38 | 0.021837 | -6.513 |
| w27 | 28 | 0.036651 | -12.009 |
| w28 | 40 | -0.041944 | -2.127 |
| w29 | 30 | 0.089754 | -18.991 |
| w30 | 36 | 0.084844 | -17.971 |
| w31 | 32 | -0.001795 | -37.715 |
| w32 | 51 | -0.104556 | -56.278 |

- w14 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ALGOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w15 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ALGOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- TRXUSD: 18 of 18 windows run. w1 to w14 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 35 | -0.064686 | -25.555 |
| w16 | 33 | 0.009378 | 47.472 |
| w17 | 33 | 0.020416 | 19.228 |
| w18 | 30 | -0.091637 | -10.342 |
| w19 | 31 | -0.060226 | 0.599 |
| w20 | 34 | -0.074933 | -33.712 |
| w21 | 33 | 0.128531 | 20.052 |
| w22 | 32 | -0.035018 | -9.671 |
| w23 | 28 | -0.061927 | -6.864 |
| w24 | 36 | -0.040257 | 22.317 |
| w25 | 37 | 0.078554 | 13.7 |
| w26 | 30 | 0.218902 | 12.69 |
| w27 | 20 | 0.00857 | 57.249 |
| w28 | 47 | -0.137896 | -27.817 |
| w29 | 33 | -0.02674 | 34.053 |
| w30 | 44 | -0.032987 | -33.612 |
| w31 | 39 | 0.120106 | 31.864 |
| w32 | 33 | 0.043475 | 13.268 |

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 24 | 0.004263 | 11.243 |
| w18 | 18 | -0.138341 | -2.888 |
| w19 | 48 | -0.029722 | -13.8 |
| w20 | 33 | -0.053414 | -13.999 |
| w21 | 48 | -0.09145 | 0.907 |
| w22 | 31 | -0.035824 | -9.506 |
| w23 | 37 | 0.104521 | 28.651 |
| w24 | 31 | 0.15949 | 55.918 |
| w25 | 18 | -0.020373 | -14.408 |
| w26 | 36 | 0.015329 | 16.939 |
| w27 | 35 | 0.022844 | -26.368 |
| w28 | 44 | -0.131808 | -2.49 |
| w29 | 32 | -0.075121 | -37.314 |
| w30 | 38 | 0.017221 | -24.046 |
| w31 | 26 | 0.029816 | 4.994 |
| w32 | 35 | 0.016278 | 7.554 |

- w16 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_DOTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 28 | 0.070239 | 6.21 |
| w21 | 39 | -0.040245 | -4.214 |
| w22 | 29 | 0.042875 | -20.029 |
| w23 | 32 | 0.115075 | 13.269 |
| w24 | 25 | 0.037645 | 1.741 |
| w25 | 32 | 0.096887 | 6.742 |
| w26 | 43 | 0.023589 | 0.293 |
| w27 | 42 | -0.007354 | -30.355 |
| w28 | 41 | -0.097015 | 7.021 |
| w29 | 32 | 0.027591 | -0.005 |
| w30 | 31 | 0.06154 | 25.617 |
| w31 | 32 | -0.068352 | 6.665 |
| w32 | 35 | 0.030763 | 7.834 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 37 | 0.123762 | 8.601 |
| w23 | 33 | 0.188854 | 54.133 |
| w24 | 31 | 0.210893 | 99.324 |
| w25 | 26 | -0.003892 | 19.56 |
| w26 | 36 | 0.028751 | -4.628 |
| w27 | 33 | -0.042981 | 1.413 |
| w28 | 42 | -0.037276 | -4.454 |
| w29 | 33 | -0.000458 | -16.712 |
| w30 | 34 | -0.091268 | -23.621 |
| w31 | 31 | 0.023909 | -2.032 |
| w32 | 28 | -0.041659 | 20.83 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 46 | 0.089242 | 19.156 |
| w25 | 30 | -0.077641 | 0.07 |
| w26 | 41 | -0.043499 | -26.957 |
| w27 | 15 | 0.080799 | 91.783 |
| w28 | 41 | 0.002076 | 8.921 |
| w29 | 28 | 0.038458 | 13.89 |
| w30 | 29 | 0.005593 | -16.873 |
| w31 | 31 | 0.078315 | 19.043 |
| w32 | 25 | 0.05379 | -17.804 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 16 | 0.010269 | 26.425 |
| w6 | 30 | 0.073394 | 15.253 |
| w7 | 27 | 0.02801 | 34.073 |
| w8 | 34 | -0.025739 | -19.154 |
| w9 | 38 | 0.003002 | -3.075 |
| w10 | 25 | 0.008395 | 25.838 |
| w11 | 20 | 0.100522 | 17.124 |
| w12 | 37 | 0.113191 | 30.382 |
| w13 | 18 | 0.140783 | 55.735 |
| w14 | 30 | -0.088729 | 15.608 |
| w15 | 36 | -0.147669 | -17.536 |
| w16 | 38 | 0.301535 | 45.397 |
| w17 | 34 | 0.022269 | 26.307 |
| w18 | 30 | 0.041202 | -17.096 |
| w19 | 29 | 0.032713 | 42.064 |
| w20 | 30 | -0.047884 | -1.461 |
| w21 | 32 | -0.120553 | 8.073 |
| w22 | 39 | -0.120175 | -18.022 |
| w23 | 27 | 0.159453 | 17.458 |
| w24 | 41 | -0.062018 | -30.002 |
| w25 | 40 | -0.007265 | -15.768 |
| w26 | 21 | 0.19828 | 48.362 |
| w27 | 33 | 0.002487 | 9.093 |
| w28 | 33 | -0.130787 | 9.097 |
| w29 | 33 | -0.041175 | -23.402 |
| w30 | 20 | -0.076929 | 78.378 |
| w31 | 27 | -0.028332 | 4.431 |
| w32 | 31 | 0.014402 | -35.618 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 33 | 0.071043 | 84.79 |
| w6 | 20 | 0.002454 | -25.097 |
| w7 | 36 | -0.009874 | -13.472 |
| w8 | 28 | -0.012029 | 7.173 |
| w9 | 21 | -0.069575 | 6.317 |
| w10 | 38 | -0.046746 | 13.512 |
| w11 | 31 | -0.023804 | -22.172 |
| w12 | 28 | 0.053426 | 16.359 |
| w13 | 18 | -0.000155 | 22.791 |
| w14 | 35 | -0.159467 | 3.838 |
| w15 | 33 | -0.123006 | 1.175 |
| w16 | 32 | 0.142214 | 24.406 |
| w17 | 28 | -0.02121 | -26.989 |
| w18 | 41 | -0.195824 | -24.466 |
| w19 | 33 | -0.08998 | -46.619 |
| w20 | 28 | -0.037788 | 17.715 |
| w21 | 37 | -0.074124 | -20.578 |
| w22 | 31 | 0.073877 | 16.267 |
| w23 | 38 | 0.105875 | 29.352 |
| w24 | 47 | 0.03771 | 8.049 |
| w25 | 31 | -0.138429 | -32.252 |
| w26 | 25 | -0.116882 | -20.139 |
| w27 | 36 | 0.10101 | -44.082 |
| w28 | 39 | -0.162321 | -0.456 |
| w29 | 21 | 0.04625 | 23.663 |
| w30 | 36 | -0.060582 | -15.03 |
| w31 | 31 | 0.045672 | 26.715 |
| w32 | 32 | -0.074228 | 18.021 |

- CRVUSD: 15 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 37 | 0.002264 | 11.979 |
| w19 | 32 | 0.058559 | -39.932 |
| w20 | 32 | 0.001153 | -10.919 |
| w21 | 44 | -0.188562 | 7.154 |
| w22 | 27 | 0.058654 | 7.452 |
| w23 | 27 | 0.161577 | 22.518 |
| w24 | 33 | 0.013737 | 8.092 |
| w25 | 26 | -0.039832 | 21.075 |
| w26 | 37 | -0.016717 | -10.912 |
| w27 | 37 | 0.054128 | -12.31 |
| w28 | 39 | -0.107701 | -15.523 |
| w29 | 38 | 0.049357 | 30.401 |
| w30 | 40 | -0.066952 | -35.461 |
| w31 | 33 | -0.070078 | 14.924 |
| w32 | 34 | 0.070199 | 1.154 |

- w16 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_CRVUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w17 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_CRVUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- AAVEUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 32 | -0.020819 | -19.665 |
| w18 | 35 | -0.140499 | -13.905 |
| w19 | 34 | 0.072861 | -1.436 |
| w20 | 34 | 0.188123 | 30.668 |
| w21 | 35 | -0.032481 | -24.263 |
| w22 | 26 | 0.098785 | 2.146 |
| w23 | 37 | -0.002215 | 12.759 |
| w24 | 38 | 0.02364 | 7.442 |
| w25 | 29 | -0.057673 | -15.717 |
| w26 | 41 | -0.015916 | -45.484 |
| w27 | 38 | -0.13268 | -41.306 |
| w28 | 33 | -0.068338 | -8.011 |
| w29 | 30 | -0.085134 | -31.085 |
| w30 | 30 | -0.051413 | 10.73 |
| w31 | 39 | -0.11582 | 21.764 |
| w32 | 32 | 0.111331 | -4.51 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 34 | 0.008616 | 31.968 |
| w20 | 25 | 0.033326 | 4.406 |
| w21 | 36 | -0.157656 | -14.952 |
| w22 | 26 | -0.049394 | 2.9 |
| w23 | 32 | -0.075395 | -28.34 |
| w24 | 28 | 0.051436 | 111.656 |
| w25 | 33 | -0.151414 | -42.818 |
| w26 | 36 | -0.044684 | -31.252 |
| w27 | 52 | -0.086514 | -48.75 |
| w28 | 39 | -0.101281 | 7.329 |
| w29 | 37 | -0.058259 | -11.477 |
| w30 | 33 | 0.043954 | -10.802 |
| w31 | 33 | -0.056165 | 43.583 |
| w32 | 24 | -0.105153 | -24.855 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 26 | -0.051415 | 11.365 |
| w23 | 33 | -0.088505 | -23.078 |
| w24 | 36 | -0.177078 | -11.343 |
| w25 | 44 | -0.008149 | -46.214 |
| w26 | 37 | 0.059141 | 11.983 |
| w27 | 35 | -0.128822 | -14.495 |
| w28 | 39 | -0.09969 | -9.977 |
| w29 | 24 | 0.171559 | 28.496 |
| w30 | 35 | -0.033397 | 2.946 |
| w31 | 26 | 0.030277 | 19.635 |
| w32 | 24 | 0.182095 | 33.202 |

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
| w27 | 28 | -0.050554 | -15.473 |
| w28 | 51 | -0.127516 | 1.941 |
| w29 | 35 | 0.069782 | 10.778 |
| w30 | 37 | 0.169516 | 19.462 |
| w31 | 35 | -0.116456 | 0.034 |
| w32 | 29 | 0.052435 | 36.47 |

- FILUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 32 | 0.003785 | 13.584 |
| w19 | 28 | 0.091665 | 77.216 |
| w20 | 26 | 0.201283 | -39.53 |
| w21 | 33 | -0.036573 | 17.87 |
| w22 | 23 | 0.069091 | -6.681 |
| w23 | 26 | 0.125401 | 38.591 |
| w24 | 28 | -0.045008 | 35.918 |
| w25 | 26 | 0.091474 | 17.771 |
| w26 | 33 | -0.066032 | 1.777 |
| w27 | 38 | -0.149434 | -35.337 |
| w28 | 40 | -0.076927 | 9.209 |
| w29 | 38 | -0.002347 | -33.468 |
| w30 | 23 | -0.126308 | -49.182 |
| w31 | 23 | -0.015959 | 3.535 |
| w32 | 39 | -0.030805 | -26.446 |

- w17 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_FILUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- GRTUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 41 | -0.097538 | -4.019 |
| w19 | 32 | 0.006966 | -0.345 |
| w20 | 27 | -0.023176 | -16.429 |
| w21 | 29 | 0.005046 | -3.615 |
| w22 | 25 | 0.018455 | -8.315 |
| w23 | 33 | -0.076275 | -2.575 |
| w24 | 31 | 0.028886 | 20.395 |
| w25 | 18 | 0.032242 | 14.317 |
| w26 | 34 | 0.093748 | 14.945 |
| w27 | 35 | -0.071952 | 2.849 |
| w28 | 33 | -0.032407 | 16.676 |
| w29 | 30 | -0.029126 | -0.23 |
| w30 | 28 | 0.001927 | -3.088 |
| w31 | 30 | -0.123154 | 9.7 |
| w32 | 34 | 0.116007 | -6.907 |

- w17 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_GRTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 43 | -0.015907 | 4.14 |
| w29 | 29 | -0.056069 | -10.487 |
| w30 | 37 | 0.019573 | 28.516 |
| w31 | 20 | 0.008022 | 22.499 |
| w32 | 35 | 0.102458 | 12.729 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 35 | 0.158723 | -76.616 |
| w15 | 39 | 0.095673 | 28.351 |
| w16 | 19 | 0.000598 | 274.999 |
| w17 | 19 | -0.026995 | -7.046 |
| w18 | 35 | -0.106189 | -6.842 |
| w19 | 40 | 0.009253 | -0.274 |
| w20 | 36 | 0.16813 | 16.479 |
| w21 | 28 | 0.090172 | 179.035 |
| w22 | 29 | -0.193954 | -16.237 |
| w23 | 28 | 0.035219 | 5.52 |
| w24 | 36 | 0.163484 | 35.605 |
| w25 | 28 | -0.002789 | 65.318 |
| w26 | 34 | -0.055157 | 8.629 |
| w27 | 29 | 0.038342 | 32.199 |
| w28 | 30 | -0.090444 | -19.099 |
| w29 | 25 | -0.037254 | -3.703 |
| w30 | 37 | 0.076772 | 22.063 |
| w31 | 33 | -0.058512 | 25.259 |
| w32 | 20 | 0.288904 | -8.502 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 30 | 0.047085 | 68.296 |
| w26 | 33 | 0.034953 | -4.704 |
| w27 | 38 | -0.016032 | -6.118 |
| w28 | 39 | 0.011221 | -2.284 |
| w29 | 24 | 0.021988 | -5.324 |
| w30 | 29 | -0.02358 | -6.75 |
| w31 | 32 | 0.067272 | 28.32 |
| w32 | 32 | 0.137933 | -31.648 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

