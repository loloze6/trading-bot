# Backtest of 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d

- Plan: `../../../../../03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.076134 | -1.717 |
| w2 | 26 | 0.123291 | 59.361 |
| w3 | 46 | 0.058466 | 54.487 |
| w4 | 29 | -0.2607 | -30.969 |
| w5 | 44 | 0.026904 | 78.627 |
| w6 | 53 | 0.086178 | 82.634 |
| w7 | 10 | -0.119255 | -17.643 |
| w8 | 23 | 0.049777 | -1.314 |
| w9 | 2 | 0.044691 | 5.039 |
| w10 | 41 | -0.038903 | -2.067 |
| w11 | 44 | -0.021653 | 29.512 |
| w12 | 9 | 0.150411 | 6.095 |
| w13 | 30 | -0.061409 | 2.465 |
| w14 | 42 | 0.051179 | 11.759 |
| w15 | 54 | -0.028376 | 57.857 |
| w16 | 27 | -0.032844 | 2.414 |
| w17 | 20 | 0.121436 | 13.897 |
| w18 | 21 | -0.090529 | -11.681 |
| w19 | 20 | 0.128883 | -4.48 |
| w20 | 9 | 0.105732 | 0.415 |
| w21 | 10 | -0.009724 | -10.032 |
| w22 | 48 | 0.11507 | 58.094 |
| w23 | 13 | 0.068818 | 9.439 |
| w24 | 41 | 0.052645 | 50.889 |
| w25 | 38 | 0.017717 | 27.737 |
| w26 | 25 | -0.14018 | -29.549 |
| w27 | 50 | 0.122609 | 66.543 |
| w28 | 13 | -0.074598 | -5.802 |
| w29 | 45 | 0.016634 | 7.17 |
| w30 | 10 | -0.024073 | 1.165 |
| w31 | 23 | -0.043165 | -5.133 |
| w32 | 27 | 0.156344 | 21.667 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.117308 | 40.16 |
| w2 | 28 | -0.146101 | -29.89 |
| w3 | 29 | -0.121013 | -19.086 |
| w4 | 37 | -0.048276 | 1.784 |
| w5 | 52 | 0.023939 | 31.192 |
| w6 | 41 | 0.216896 | 102.817 |
| w7 | 10 | -0.080926 | -5.541 |
| w8 | 11 | -0.058628 | -11.155 |
| w9 | 7 | -0.060353 | -14.564 |
| w10 | 32 | -0.024103 | 15.873 |
| w11 | 21 | -0.094041 | -4.794 |
| w12 | 14 | 0.037854 | -7.389 |
| w13 | 43 | -0.088631 | -1.683 |
| w14 | 28 | 0.096066 | 27.444 |
| w15 | 50 | 0.098747 | 62.93 |
| w16 | 40 | -0.166852 | -9.311 |
| w17 | 28 | 0.157682 | 14.915 |
| w18 | 30 | 0.032371 | 0.244 |
| w19 | 13 | -0.044688 | -10.526 |
| w20 | 13 | 0.072506 | -4.72 |
| w21 | 27 | -0.08337 | -14.821 |
| w22 | 35 | -0.084928 | 3.189 |
| w23 | 16 | -0.020684 | -10.527 |
| w24 | 36 | -0.01326 | -15.181 |
| w25 | 23 | 0.055268 | 12.546 |
| w26 | 7 | -0.124057 | -12.103 |
| w27 | 46 | -0.028771 | 55.24 |
| w28 | 16 | -0.170673 | -23.532 |
| w29 | 37 | 0.180902 | 19.815 |
| w30 | 6 | -0.266534 | -31.503 |
| w31 | 12 | -0.058316 | -8.353 |
| w32 | 23 | 0.033981 | -4.154 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 37 | 0.071519 | 76.158 |
| w7 | 20 | -0.034766 | -11.018 |
| w8 | 3 | 0.035981 | 1.873 |
| w9 | 19 | 0.170064 | 7.309 |
| w10 | 21 | -0.084133 | -13.344 |
| w11 | 18 | -0.129431 | -14.218 |
| w12 | 12 | -0.052387 | -0.429 |
| w13 | 30 | -0.055661 | 6.473 |
| w14 | 28 | 0.180253 | 53.781 |
| w15 | 32 | 0.256088 | 139.014 |
| w16 | 37 | 0.008226 | 30.445 |
| w17 | 24 | 0.140983 | 34.222 |
| w18 | 18 | 0.064268 | 2.27 |
| w19 | 20 | 0.071248 | -5.556 |
| w20 | 11 | -0.006104 | -6.022 |
| w21 | 13 | 0.131927 | 15.576 |
| w22 | 28 | -0.038592 | 3.233 |
| w23 | 21 | -0.101739 | -13.677 |
| w24 | 29 | -0.000625 | 6.778 |
| w25 | 11 | -0.10914 | -17.769 |
| w26 | 14 | -0.009539 | 25.097 |
| w27 | 32 | 0.245507 | 164.461 |
| w28 | 12 | -0.00376 | -0.268 |
| w29 | 36 | 0.191641 | 39.394 |
| w30 | 5 | -0.15419 | -9.002 |
| w31 | 18 | -0.170614 | -26.015 |
| w32 | 21 | 0.129853 | 2.536 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 9 | 0.041354 | 1.013 |
| w8 | 14 | -0.035266 | -10.628 |
| w9 | 11 | -0.016408 | -10.788 |
| w10 | 31 | 0.023838 | 7.529 |
| w11 | 19 | -0.124157 | -5.036 |
| w12 | 16 | 0.021992 | -3.383 |
| w13 | 26 | -0.091028 | 7.744 |
| w14 | 31 | 0.060839 | 8.207 |
| w15 | 38 | -0.084556 | -34.231 |
| w16 | 44 | -0.028759 | 34.047 |
| w17 | 33 | 0.112034 | 32.516 |
| w18 | 16 | 0.000243 | -1.392 |
| w19 | 23 | 0.024146 | -4.222 |
| w20 | 18 | 0.007562 | -3.669 |
| w21 | 8 | -0.023139 | -16.287 |
| w22 | 28 | 0.005801 | 16.744 |
| w23 | 12 | 0.378431 | 77.154 |
| w24 | 36 | -0.011457 | -9.367 |
| w25 | 35 | -0.00216 | 29.318 |
| w26 | 20 | -0.121766 | -26.199 |
| w27 | 38 | -0.088726 | 3.534 |
| w28 | 14 | -0.088763 | -13.365 |
| w29 | 49 | -0.169616 | -6.518 |
| w30 | 27 | -0.053043 | 6.047 |
| w31 | 11 | -0.005781 | -6.484 |
| w32 | 18 | -0.063639 | -19.782 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | 0.125324 | 105.901 |
| w2 | 21 | -0.099148 | -4.726 |
| w3 | 11 | 0.02572 | -3.088 |
| w4 | 38 | 0.208162 | 176.76 |
| w5 | 35 | 0.016993 | 58.458 |
| w6 | 38 | 0.14842 | 82.261 |
| w7 | 26 | 0.017131 | 3.804 |
| w8 | 10 | -0.017785 | 1.269 |
| w9 | 9 | 0.071558 | 0.048 |
| w10 | 27 | -0.062177 | -4.355 |
| w11 | 28 | 0.054291 | 13.739 |
| w12 | 13 | -0.160047 | -18.597 |
| w13 | 30 | -0.026985 | 29.621 |
| w14 | 44 | 0.201565 | 70.632 |
| w15 | 41 | 0.030918 | 37.059 |
| w16 | 51 | -0.001973 | 40.854 |
| w17 | 38 | 0.02289 | 7.994 |
| w18 | 29 | 0.123576 | 5.959 |
| w19 | 22 | 0.195625 | 7.665 |
| w20 | 16 | 0.016362 | 24.23 |
| w21 | 14 | -0.096458 | -3.025 |
| w22 | 37 | 0.077559 | 35.297 |
| w23 | 18 | -0.231357 | -23.862 |
| w24 | 46 | -0.120775 | -2.704 |
| w25 | 31 | 0.083981 | 11.703 |
| w26 | 11 | 0.03435 | 10.902 |
| w27 | 39 | -0.115132 | 7.384 |
| w28 | 0 | None | 0.0 |
| w29 | 51 | 0.086513 | 62.89 |
| w30 | 10 | -0.11978 | -10.952 |
| w31 | 26 | -0.10139 | -20.429 |
| w32 | 17 | 0.146859 | 11.446 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 34 | 0.007116 | 8.463 |
| w11 | 14 | -0.081678 | -3.929 |
| w12 | 16 | 0.02801 | -8.27 |
| w13 | 44 | 0.033549 | 37.195 |
| w14 | 50 | 0.159133 | 49.629 |
| w15 | 31 | 0.083893 | 13.916 |
| w16 | 44 | 0.061441 | 63.84 |
| w17 | 33 | 0.223408 | 104.273 |
| w18 | 10 | -0.053556 | -15.843 |
| w19 | 19 | 0.016674 | -11.973 |
| w20 | 14 | -0.038073 | -20.066 |
| w21 | 1 | -0.04557 | -1.451 |
| w22 | 28 | 0.081176 | 30.669 |
| w23 | 1 | -0.157623 | -11.263 |
| w24 | 41 | 0.13145 | 126.326 |
| w25 | 28 | 0.099198 | 3.139 |
| w26 | 11 | -0.086278 | -6.738 |
| w27 | 42 | 0.136823 | 100.435 |
| w28 | 12 | -0.142594 | -13.152 |
| w29 | 37 | 0.076909 | -0.028 |
| w30 | 6 | 0.083671 | -2.009 |
| w31 | 11 | -0.108425 | -14.142 |
| w32 | 32 | 0.136982 | 13.139 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 38 | -0.027935 | 6.931 |
| w13 | 23 | -0.038723 | -29.516 |
| w14 | 44 | 0.171999 | 71.425 |
| w15 | 19 | 0.001175 | 0.807 |
| w16 | 47 | -0.07977 | 13.696 |
| w17 | 28 | 0.15156 | 25.741 |
| w18 | 22 | -0.022964 | 20.438 |
| w19 | 21 | -0.092827 | -15.667 |
| w20 | 23 | 0.075889 | 12.598 |
| w21 | 22 | 0.177425 | 22.121 |
| w22 | 31 | 0.07066 | 34.124 |
| w23 | 2 | -0.035719 | -7.327 |
| w24 | 45 | 0.014897 | -7.304 |
| w25 | 31 | 0.105464 | 14.982 |
| w26 | 4 | -0.019821 | -6.64 |
| w27 | 35 | 0.017472 | 4.868 |
| w28 | 7 | 0.027154 | 4.659 |
| w29 | 36 | 0.035631 | -4.452 |
| w30 | 4 | 0.003218 | -5.866 |
| w31 | 23 | -0.005597 | -9.23 |
| w32 | 22 | 0.055273 | 4.79 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 18 | -0.004212 | -7.125 |
| w16 | 45 | -0.090094 | 22.763 |
| w17 | 21 | 0.116747 | 18.346 |
| w18 | 23 | 0.133659 | 39.371 |
| w19 | 14 | -0.010345 | -6.568 |
| w20 | 17 | 0.038544 | 0.352 |
| w21 | 16 | 0.016365 | -10.26 |
| w22 | 22 | 0.08616 | 11.55 |
| w23 | 6 | -0.122192 | -7.307 |
| w24 | 47 | 0.052898 | 63.179 |
| w25 | 26 | 0.176289 | 15.842 |
| w26 | 10 | -0.030333 | -5.66 |
| w27 | 24 | 0.221197 | 139.671 |
| w28 | 10 | 0.079693 | -0.921 |
| w29 | 25 | 0.039208 | 23.284 |
| w30 | 2 | -0.136778 | -3.628 |
| w31 | 25 | 0.120551 | -4.897 |
| w32 | 23 | 0.124076 | -1.737 |

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
| w15 | 19 | -0.061387 | 3.875 |
| w16 | 41 | -0.1163 | 11.716 |
| w17 | 26 | 0.113495 | 12.951 |
| w18 | 34 | 0.08059 | 8.458 |
| w19 | 22 | 0.051219 | -16.487 |
| w20 | 20 | -0.095595 | -15.832 |
| w21 | 13 | 0.072444 | -33.702 |
| w22 | 29 | 0.018268 | 29.175 |
| w23 | 36 | -0.057684 | -19.622 |
| w24 | 47 | 0.141976 | 33.31 |
| w25 | 30 | -0.086988 | -12.386 |
| w26 | 30 | 0.103717 | 17.629 |
| w27 | 37 | 0.097426 | 87.141 |
| w28 | 14 | -0.022128 | -3.439 |
| w29 | 49 | -0.127674 | -8.226 |
| w30 | 13 | -0.087502 | -10.79 |
| w31 | 39 | -0.154614 | -3.823 |
| w32 | 30 | 0.00499 | -9.903 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 39 | 0.054741 | 47.637 |
| w17 | 27 | 0.078955 | 17.631 |
| w18 | 22 | 0.023334 | 18.462 |
| w19 | 16 | 0.073902 | -8.79 |
| w20 | 14 | -0.033806 | -7.509 |
| w21 | 11 | -0.122243 | -19.892 |
| w22 | 26 | -0.135065 | -17.119 |
| w23 | 11 | -0.07789 | -9.528 |
| w24 | 39 | 0.001913 | 17.169 |
| w25 | 35 | 0.106506 | 7.816 |
| w26 | 7 | -0.079566 | -13.594 |
| w27 | 27 | 0.16284 | 56.843 |
| w28 | 2 | -0.230598 | -1.72 |
| w29 | 27 | 0.093316 | -9.815 |
| w30 | 15 | 0.046538 | -9.542 |
| w31 | 10 | -0.040641 | -13.058 |
| w32 | 18 | 0.059503 | -5.174 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 16 | 0.01136 | 5.408 |
| w21 | 11 | -0.036544 | -17.985 |
| w22 | 32 | -0.024498 | 4.042 |
| w23 | 6 | 0.108447 | 1.275 |
| w24 | 40 | 0.152922 | 140.923 |
| w25 | 26 | 0.16527 | 16.267 |
| w26 | 10 | -0.076742 | -20.138 |
| w27 | 45 | 0.131589 | 71.449 |
| w28 | 7 | -0.032176 | 3.226 |
| w29 | 39 | -0.025907 | -1.509 |
| w30 | 12 | -0.028073 | -14.842 |
| w31 | 20 | -0.067534 | -18.613 |
| w32 | 18 | 0.101665 | 2.392 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 31 | -0.007968 | 21.026 |
| w23 | 5 | 0.019784 | -4.242 |
| w24 | 39 | 0.195519 | 115.065 |
| w25 | 33 | 0.025264 | 36.957 |
| w26 | 16 | -0.022835 | -6.782 |
| w27 | 35 | -0.000374 | 39.548 |
| w28 | 3 | -0.04378 | -6.226 |
| w29 | 30 | 0.026626 | 2.4 |
| w30 | 21 | -0.002725 | -7.578 |
| w31 | 26 | -0.045755 | -17.377 |
| w32 | 29 | -0.094308 | 33.2 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 30 | -0.016622 | 24.468 |
| w25 | 36 | -0.017918 | 3.312 |
| w26 | 14 | -0.056047 | -8.517 |
| w27 | 60 | 0.079402 | 96.916 |
| w28 | 18 | 0.105253 | 9.334 |
| w29 | 30 | 0.03573 | -3.909 |
| w30 | 9 | 0.049687 | -11.818 |
| w31 | 15 | -0.157074 | -16.856 |
| w32 | 21 | 0.095173 | 11.871 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 42 | 0.151846 | 72.448 |
| w6 | 35 | 0.110553 | 48.796 |
| w7 | 15 | -0.009628 | -12.285 |
| w8 | 12 | 0.059682 | -3.882 |
| w9 | 9 | -0.125784 | -19.52 |
| w10 | 33 | -0.05339 | -11.883 |
| w11 | 26 | 0.024186 | 17.339 |
| w12 | 5 | 0.084893 | 5.254 |
| w13 | 27 | 0.070321 | 66.406 |
| w14 | 48 | -0.041764 | 0.106 |
| w15 | 27 | 0.073161 | -3.703 |
| w16 | 43 | -0.003849 | 41.789 |
| w17 | 23 | 0.153692 | 13.845 |
| w18 | 38 | 0.094406 | 0.364 |
| w19 | 29 | 0.147037 | 19.978 |
| w20 | 10 | -0.016329 | -3.846 |
| w21 | 8 | 0.111641 | -2.011 |
| w22 | 30 | -0.088687 | -4.789 |
| w23 | 7 | -0.113571 | -13.418 |
| w24 | 32 | 0.010054 | -6.281 |
| w25 | 25 | 0.056235 | 5.503 |
| w26 | 42 | 0.009292 | 19.729 |
| w27 | 44 | -0.093084 | 51.368 |
| w28 | 9 | 0.069756 | -0.759 |
| w29 | 30 | -0.004241 | -1.677 |
| w30 | 44 | 0.248047 | 226.092 |
| w31 | 18 | 0.051773 | 2.871 |
| w32 | 39 | 0.204833 | 46.672 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 47 | 0.111802 | 123.421 |
| w6 | 33 | 0.036637 | 31.247 |
| w7 | 21 | -0.02315 | -2.493 |
| w8 | 6 | 0.104577 | 0.461 |
| w9 | 10 | 0.128818 | -12.458 |
| w10 | 38 | -0.001109 | 9.51 |
| w11 | 31 | -0.160057 | -19.16 |
| w12 | 10 | 0.038002 | -3.766 |
| w13 | 34 | -0.070099 | 5.358 |
| w14 | 42 | -0.027849 | 6.35 |
| w15 | 44 | -0.169214 | -7.942 |
| w16 | 45 | -0.00624 | 33.552 |
| w17 | 29 | 0.088383 | 8.43 |
| w18 | 15 | -0.06053 | -24.613 |
| w19 | 34 | -0.030472 | -27.113 |
| w20 | 17 | 0.04423 | -6.603 |
| w21 | 13 | -0.078229 | -5.107 |
| w22 | 35 | 0.130844 | 18.553 |
| w23 | 16 | 0.109648 | 0.385 |
| w24 | 41 | -0.043031 | -2.657 |
| w25 | 12 | -0.006312 | -2.862 |
| w26 | 29 | 0.233246 | 31.282 |
| w27 | 31 | -0.061149 | -5.632 |
| w28 | 27 | 0.049779 | 19.28 |
| w29 | 33 | -0.012238 | 1.001 |
| w30 | 36 | -0.107679 | 5.218 |
| w31 | 21 | -0.10197 | -8.316 |
| w32 | 36 | -0.038395 | 6.604 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 25 | 0.071571 | 4.975 |
| w18 | 40 | -0.060634 | 19.635 |
| w19 | 23 | 0.019257 | -11.264 |
| w20 | 16 | 0.015075 | 3.013 |
| w21 | 8 | -0.160663 | -32.38 |
| w22 | 38 | 0.036956 | 17.34 |
| w23 | 6 | -0.088494 | -9.382 |
| w24 | 32 | 0.025468 | 4.056 |
| w25 | 23 | 0.155948 | 31.215 |
| w26 | 19 | -0.078258 | -14.416 |
| w27 | 30 | 0.23518 | 116.383 |
| w28 | 14 | -0.077089 | 3.643 |
| w29 | 30 | 0.127893 | 28.132 |
| w30 | 3 | -0.076322 | -0.816 |
| w31 | 13 | -0.062383 | -10.952 |
| w32 | 28 | 0.080936 | 37.844 |

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
| w17 | 34 | -0.004319 | 0.942 |
| w18 | 18 | -0.103975 | -7.915 |
| w19 | 18 | 0.067272 | -1.256 |
| w20 | 15 | 0.001269 | -5.524 |
| w21 | 16 | -0.004072 | -29.466 |
| w22 | 27 | 0.163382 | 35.343 |
| w23 | 11 | -0.178487 | -18.668 |
| w24 | 43 | 0.083299 | 69.14 |
| w25 | 30 | 0.216049 | 39.474 |
| w26 | 32 | 0.027932 | 8.716 |
| w27 | 40 | -0.011811 | 29.746 |
| w28 | 3 | 0.070928 | -2.375 |
| w29 | 48 | 0.048661 | -5.651 |
| w30 | 4 | -0.189912 | -13.741 |
| w31 | 1 | -0.021877 | -1.054 |
| w32 | 26 | -0.021241 | 10.9 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 11 | -0.203195 | -16.932 |
| w20 | 15 | -0.009657 | -13.518 |
| w21 | 20 | -0.1635 | -9.376 |
| w22 | 46 | -0.040726 | 68.559 |
| w23 | 17 | 0.063382 | 0.318 |
| w24 | 54 | 0.165239 | 191.972 |
| w25 | 22 | 0.052769 | -1.789 |
| w26 | 18 | 0.016251 | -0.292 |
| w27 | 36 | 0.096813 | 26.726 |
| w28 | 6 | 0.010892 | -8.464 |
| w29 | 44 | -0.083839 | -25.738 |
| w30 | 9 | -0.018127 | -3.967 |
| w31 | 13 | -0.121962 | -19.024 |
| w32 | 31 | -0.016463 | 13.473 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 33 | -0.012132 | 27.259 |
| w23 | 15 | 0.014285 | -8.501 |
| w24 | 31 | -0.083135 | 4.154 |
| w25 | 26 | 0.039216 | -4.235 |
| w26 | 12 | 0.082994 | 10.81 |
| w27 | 36 | -0.058367 | 4.995 |
| w28 | 12 | -0.095406 | -3.822 |
| w29 | 32 | 0.06272 | 11.406 |
| w30 | 6 | 0.010483 | -6.42 |
| w31 | 30 | -0.028041 | -12.494 |
| w32 | 21 | 0.053982 | 7.767 |

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
| w27 | 45 | 0.064336 | 28.98 |
| w28 | 10 | -0.022644 | -5.194 |
| w29 | 25 | -0.011424 | -3.08 |
| w30 | 13 | 0.089509 | -2.557 |
| w31 | 11 | -0.163366 | -15.93 |
| w32 | 29 | 0.150459 | 62.2 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 13 | 0.047439 | 2.345 |
| w18 | 6 | 0.00379 | -5.67 |
| w19 | 16 | 0.140672 | 6.782 |
| w20 | 16 | 0.012319 | 4.04 |
| w21 | 5 | 0.007453 | -6.536 |
| w22 | 30 | -0.018033 | 10.456 |
| w23 | 4 | -0.13428 | -8.353 |
| w24 | 36 | -0.013476 | 41.789 |
| w25 | 25 | 0.122237 | 15.57 |
| w26 | 14 | -0.080187 | -14.153 |
| w27 | 35 | 0.089708 | 25.655 |
| w28 | 3 | -0.027708 | -1.395 |
| w29 | 24 | -0.048911 | -14.042 |
| w30 | 12 | -0.15022 | -14.4 |
| w31 | 16 | -0.034294 | -15.945 |
| w32 | 18 | -0.031971 | -7.618 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 23 | 0.150163 | 23.751 |
| w18 | 17 | -0.173076 | -32.862 |
| w19 | 9 | 0.193275 | 7.646 |
| w20 | 10 | 0.049344 | -0.059 |
| w21 | 3 | 0.047002 | -0.471 |
| w22 | 32 | 0.049705 | 93.037 |
| w23 | 7 | -0.148095 | -15.344 |
| w24 | 33 | 0.100931 | 51.712 |
| w25 | 22 | 0.14373 | 41.709 |
| w26 | 8 | -0.030662 | -4.673 |
| w27 | 37 | -0.021518 | 0.068 |
| w28 | 3 | -0.216193 | -3.901 |
| w29 | 25 | 0.036365 | -8.022 |
| w30 | 5 | 0.027054 | -8.281 |
| w31 | 12 | -0.233093 | -20.277 |
| w32 | 22 | -0.01675 | -10.262 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 13 | 0.03947 | 5.566 |
| w29 | 25 | 0.059973 | -1.273 |
| w30 | 22 | -0.038612 | 6.013 |
| w31 | 28 | -0.03894 | -1.372 |
| w32 | 21 | 0.099079 | 12.15 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 19 | 0.21164 | 62.298 |
| w15 | 21 | 0.151571 | 64.836 |
| w16 | 28 | 0.046679 | 240.212 |
| w17 | 21 | 0.011738 | 5.993 |
| w18 | 10 | 0.144419 | 4.434 |
| w19 | 21 | -0.057859 | -11.275 |
| w20 | 12 | -0.011576 | -5.941 |
| w21 | 10 | 0.240461 | 105.901 |
| w22 | 29 | 0.030403 | 6.384 |
| w23 | 10 | -0.03444 | -8.082 |
| w24 | 30 | 0.05915 | 23.891 |
| w25 | 20 | 0.157955 | 62.812 |
| w26 | 13 | 0.064864 | -6.349 |
| w27 | 39 | 0.19932 | 139.939 |
| w28 | 8 | -0.120615 | -8.497 |
| w29 | 27 | 0.096973 | 47.259 |
| w30 | 14 | -0.023202 | -21.548 |
| w31 | 14 | -0.062214 | -12.326 |
| w32 | 22 | 0.14987 | 10.931 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 20 | 0.323284 | 142.147 |
| w26 | 16 | 0.074329 | 17.946 |
| w27 | 26 | 0.13787 | 39.323 |
| w28 | 9 | -0.148191 | -14.316 |
| w29 | 22 | 0.046899 | 13.925 |
| w30 | 6 | -0.084609 | -10.922 |
| w31 | 22 | 0.051827 | 8.406 |
| w32 | 27 | 0.097517 | -7.9 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

