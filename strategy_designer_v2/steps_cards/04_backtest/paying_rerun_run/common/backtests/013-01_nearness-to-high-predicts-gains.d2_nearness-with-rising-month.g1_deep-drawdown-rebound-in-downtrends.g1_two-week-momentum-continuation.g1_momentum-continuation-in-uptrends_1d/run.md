# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1d

- Plan: `../../../../../03_test_plan/hold_paying_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.021365 | -4.364 |
| w2 | 17 | 0.094183 | 68.224 |
| w3 | 36 | 0.017436 | 82.443 |
| w4 | 33 | -0.049764 | -6.323 |
| w5 | 40 | -0.021159 | 98.353 |
| w6 | 34 | 0.110012 | 142.3 |
| w7 | 2 | -0.127594 | -6.018 |
| w8 | 8 | 0.015585 | 0.393 |
| w9 | 6 | -0.064672 | -12.959 |
| w10 | 18 | -0.009756 | 26.391 |
| w11 | 33 | 0.086181 | 59.146 |
| w12 | 1 | -0.011748 | -2.055 |
| w13 | 21 | -0.034952 | 0.184 |
| w14 | 34 | 0.040407 | 30.504 |
| w15 | 36 | 0.097244 | 140.76 |
| w16 | 31 | 0.03459 | 32.118 |
| w17 | 19 | 0.085814 | -2.899 |
| w18 | 19 | 0.13027 | 16.629 |
| w19 | 13 | 0.001408 | -0.228 |
| w20 | 1 | -0.108446 | -1.997 |
| w21 | 12 | -0.126219 | -25.058 |
| w22 | 36 | 0.020686 | 54.996 |
| w23 | 10 | 0.043798 | -0.525 |
| w24 | 28 | 0.036905 | 54.058 |
| w25 | 19 | 0.128003 | 62.897 |
| w26 | 16 | -0.085609 | -31.083 |
| w27 | 24 | 0.064194 | 39.199 |
| w28 | 15 | -0.061128 | -11.071 |
| w29 | 36 | 0.001085 | 17.631 |
| w30 | 7 | -0.098164 | -16.256 |
| w31 | 20 | 0.018447 | -11.525 |
| w32 | 13 | 0.184969 | 30.042 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.020589 | -4.973 |
| w2 | 23 | 0.062284 | 9.392 |
| w3 | 19 | -0.166356 | -17.156 |
| w4 | 26 | -0.059606 | 91.472 |
| w5 | 25 | -0.02502 | 41.307 |
| w6 | 20 | 0.13902 | 122.75 |
| w7 | 0 | -0.107391 | 0.0 |
| w8 | 0 | -0.000363 | 0.0 |
| w9 | 1 | -0.070286 | -5.937 |
| w10 | 26 | -0.05392 | 25.314 |
| w11 | 23 | 0.091412 | 18.4 |
| w12 | 0 | None | 0.0 |
| w13 | 18 | -0.038491 | 7.028 |
| w14 | 17 | -0.058055 | 6.459 |
| w15 | 22 | 0.035068 | 54.299 |
| w16 | 36 | -0.081063 | 8.066 |
| w17 | 15 | -0.022589 | -2.725 |
| w18 | 28 | -0.069984 | -10.127 |
| w19 | 9 | 0.009171 | -1.389 |
| w20 | 4 | -0.051408 | -3.586 |
| w21 | 17 | -0.058804 | -11.057 |
| w22 | 29 | -0.077627 | 1.357 |
| w23 | 17 | -0.115006 | 2.587 |
| w24 | 21 | -0.098533 | -6.26 |
| w25 | 19 | -0.054957 | -0.142 |
| w26 | 2 | -0.072922 | -1.144 |
| w27 | 26 | 0.037467 | 32.151 |
| w28 | 15 | -0.119858 | -16.122 |
| w29 | 21 | -0.035128 | 0.575 |
| w30 | 8 | -0.41668 | -34.331 |
| w31 | 6 | -0.021356 | -2.019 |
| w32 | 11 | -0.01928 | -12.075 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 30 | 0.150279 | 110.257 |
| w7 | 9 | 0.009923 | -2.224 |
| w8 | 4 | -0.076691 | -3.83 |
| w9 | 9 | -0.052753 | -6.29 |
| w10 | 9 | -0.073126 | -10.579 |
| w11 | 17 | 0.115717 | 25.096 |
| w12 | 12 | -0.032691 | -7.071 |
| w13 | 9 | -4.8e-05 | 10.358 |
| w14 | 16 | 0.13638 | 42.663 |
| w15 | 10 | 0.240298 | 179.175 |
| w16 | 22 | 0.030772 | 39.442 |
| w17 | 14 | 0.046033 | 17.483 |
| w18 | 16 | -0.028318 | -6.304 |
| w19 | 10 | -0.143306 | -15.274 |
| w20 | 3 | -0.013985 | -1.621 |
| w21 | 15 | 0.049171 | 24.961 |
| w22 | 29 | -0.024945 | 26.775 |
| w23 | 9 | -0.053391 | -11.464 |
| w24 | 10 | 0.059099 | 25.028 |
| w25 | 12 | -0.049615 | -5.768 |
| w26 | 13 | 0.087513 | 20.273 |
| w27 | 22 | 0.353044 | 262.289 |
| w28 | 8 | -0.082722 | -10.92 |
| w29 | 29 | 0.070148 | 38.445 |
| w30 | 3 | -0.029533 | -0.844 |
| w31 | 7 | -0.022569 | -17.021 |
| w32 | 8 | 0.056137 | -0.009 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 2 | -0.026266 | -5.348 |
| w8 | 8 | 0.101063 | 3.914 |
| w9 | 2 | -0.046575 | -14.599 |
| w10 | 10 | 0.096602 | 36.021 |
| w11 | 19 | 0.008085 | -0.207 |
| w12 | 6 | -0.03934 | -26.712 |
| w13 | 13 | -0.028232 | 3.476 |
| w14 | 11 | 0.009205 | -2.177 |
| w15 | 20 | -0.121684 | 2.332 |
| w16 | 37 | 0.014065 | 42.444 |
| w17 | 20 | -0.095183 | 1.137 |
| w18 | 13 | -0.140252 | -19.691 |
| w19 | 4 | 0.00223 | -5.291 |
| w20 | 0 | -0.025909 | 0.0 |
| w21 | 10 | -0.185781 | -24.188 |
| w22 | 30 | 0.029922 | 1.952 |
| w23 | 8 | 0.272991 | 83.843 |
| w24 | 22 | -0.203326 | -27.663 |
| w25 | 31 | 0.020196 | 32.735 |
| w26 | 6 | -0.043378 | -3.609 |
| w27 | 30 | 0.055288 | 18.262 |
| w28 | 9 | 0.054314 | 0.393 |
| w29 | 52 | -0.249867 | 4.362 |
| w30 | 24 | -0.264092 | -31.691 |
| w31 | 9 | -0.110558 | -11.623 |
| w32 | 7 | -0.025469 | -9.056 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | 0.135339 | 158.994 |
| w2 | 21 | -0.100214 | -13.54 |
| w3 | 8 | 0.083058 | -2.211 |
| w4 | 35 | 0.133681 | 214.222 |
| w5 | 26 | 0.13296 | 82.291 |
| w6 | 22 | -0.018646 | 30.341 |
| w7 | 14 | -0.061022 | -0.201 |
| w8 | 3 | -0.142479 | -4.631 |
| w9 | 1 | -0.019585 | -2.02 |
| w10 | 27 | -0.016807 | 0.84 |
| w11 | 21 | 0.191092 | 52.281 |
| w12 | 8 | -0.068763 | -26.703 |
| w13 | 10 | 0.045675 | 36.66 |
| w14 | 31 | 0.093158 | 67.526 |
| w15 | 22 | -0.026182 | 20.42 |
| w16 | 46 | -0.027991 | 68.492 |
| w17 | 26 | 0.07158 | 31.502 |
| w18 | 29 | 0.001519 | -5.546 |
| w19 | 10 | 0.065393 | 5.246 |
| w20 | 4 | -0.020196 | -1.371 |
| w21 | 10 | -0.085865 | -29.881 |
| w22 | 30 | -0.065628 | 23.357 |
| w23 | 17 | -0.087032 | -17.909 |
| w24 | 24 | -0.054044 | 16.269 |
| w25 | 32 | 0.099937 | 53.171 |
| w26 | 8 | 0.038483 | -3.132 |
| w27 | 28 | 0.026714 | 10.132 |
| w28 | 5 | -0.056258 | -4.26 |
| w29 | 28 | 0.024434 | 54.7 |
| w30 | 7 | -0.300797 | -13.383 |
| w31 | 12 | -0.006597 | -11.735 |
| w32 | 6 | 0.11353 | 17.779 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 19 | 0.133772 | 61.843 |
| w11 | 19 | 0.016283 | -3.156 |
| w12 | 0 | None | 0.0 |
| w13 | 18 | 0.002035 | 18.911 |
| w14 | 26 | 0.011815 | 37.918 |
| w15 | 13 | 0.044305 | 36.995 |
| w16 | 32 | 0.13691 | 108.385 |
| w17 | 18 | 0.02953 | 57.025 |
| w18 | 4 | 0.048104 | -7.336 |
| w19 | 5 | 0.028926 | -1.738 |
| w20 | 13 | -0.034711 | -15.115 |
| w21 | 5 | -0.05418 | -6.972 |
| w22 | 27 | -0.140772 | 5.638 |
| w23 | 3 | -0.06312 | -1.152 |
| w24 | 18 | 0.153418 | 154.528 |
| w25 | 13 | 0.052663 | 7.761 |
| w26 | 5 | -0.120686 | -10.521 |
| w27 | 16 | 0.316505 | 150.991 |
| w28 | 9 | -0.178916 | -15.197 |
| w29 | 26 | -0.038969 | -8.644 |
| w30 | 6 | -0.197337 | -12.113 |
| w31 | 0 | None | 0.0 |
| w32 | 17 | -0.119974 | -11.305 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 27 | -0.08866 | 14.134 |
| w13 | 18 | -0.109117 | -23.327 |
| w14 | 24 | 0.075832 | 65.027 |
| w15 | 15 | -0.162611 | -3.206 |
| w16 | 23 | 0.013319 | 49.409 |
| w17 | 13 | 0.003921 | 13.677 |
| w18 | 19 | 0.016103 | 3.807 |
| w19 | 16 | -0.056998 | -12.914 |
| w20 | 16 | -0.01121 | -0.726 |
| w21 | 22 | -0.098957 | -1.27 |
| w22 | 19 | -0.010564 | 7.403 |
| w23 | 2 | -0.111928 | -0.139 |
| w24 | 19 | -0.002154 | 34.609 |
| w25 | 14 | 0.050185 | 6.023 |
| w26 | 0 | None | 0.0 |
| w27 | 11 | 0.230709 | 75.597 |
| w28 | 6 | -0.076623 | -7.514 |
| w29 | 19 | -0.138353 | -17.244 |
| w30 | 5 | -0.002249 | -1.598 |
| w31 | 10 | -0.104766 | -19.427 |
| w32 | 14 | -0.124794 | -23.8 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 9 | -0.094941 | -7.512 |
| w16 | 30 | 0.069015 | 65.146 |
| w17 | 11 | -0.083229 | -10.164 |
| w18 | 17 | 0.071308 | 32.057 |
| w19 | 3 | -0.123474 | -19.741 |
| w20 | 5 | -0.033152 | -13.186 |
| w21 | 17 | -0.003057 | -24.544 |
| w22 | 13 | -0.098936 | -3.397 |
| w23 | 3 | -0.083272 | -7.376 |
| w24 | 20 | 0.150193 | 126.305 |
| w25 | 9 | 0.003486 | -1.791 |
| w26 | 3 | -0.02435 | -5.819 |
| w27 | 12 | 0.279949 | 171.102 |
| w28 | 6 | 0.007466 | -4.092 |
| w29 | 13 | -0.021196 | -6.07 |
| w30 | 0 | None | 0.0 |
| w31 | 6 | 0.019354 | -1.972 |
| w32 | 19 | -0.114908 | -28.314 |

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
| w15 | 16 | -0.046881 | -16.052 |
| w16 | 25 | 0.01663 | 93.725 |
| w17 | 13 | 0.030189 | 11.262 |
| w18 | 22 | -0.133339 | -11.955 |
| w19 | 12 | -0.062461 | -10.566 |
| w20 | 18 | -0.103412 | 5.345 |
| w21 | 10 | -0.09329 | -19.333 |
| w22 | 25 | -0.068055 | 15.782 |
| w23 | 40 | -0.011144 | 4.249 |
| w24 | 44 | -0.085685 | 41.559 |
| w25 | 19 | 0.104204 | 36.831 |
| w26 | 33 | 0.109085 | 47.206 |
| w27 | 29 | 0.003113 | 78.185 |
| w28 | 21 | -0.055812 | -5.029 |
| w29 | 55 | -0.035433 | 36.8 |
| w30 | 8 | -0.128735 | -11.379 |
| w31 | 33 | -0.076688 | 1.832 |
| w32 | 27 | -0.019283 | -1.591 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 34 | 0.02887 | 33.552 |
| w17 | 13 | -0.150226 | -16.334 |
| w18 | 29 | 0.047321 | 3.365 |
| w19 | 9 | 0.016231 | -6.262 |
| w20 | 6 | -0.01664 | -9.039 |
| w21 | 3 | -0.090249 | -26.625 |
| w22 | 22 | -0.110119 | -11.902 |
| w23 | 5 | -0.100534 | -6.11 |
| w24 | 21 | 0.050294 | 51.539 |
| w25 | 16 | 0.075175 | 5.296 |
| w26 | 0 | None | 0.0 |
| w27 | 9 | 0.272273 | 124.325 |
| w28 | 1 | -0.000565 | -1.111 |
| w29 | 14 | -0.073217 | -10.618 |
| w30 | 10 | -0.155119 | -26.049 |
| w31 | 2 | -0.085009 | -0.095 |
| w32 | 6 | -0.158598 | -14.586 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 9 | 0.002543 | 0.122 |
| w21 | 3 | -0.154124 | -39.183 |
| w22 | 23 | -0.048396 | 0.321 |
| w23 | 1 | -0.11755 | -1.821 |
| w24 | 23 | 0.224887 | 203.356 |
| w25 | 16 | 0.095709 | 18.994 |
| w26 | 5 | 0.006284 | -9.123 |
| w27 | 26 | 0.091546 | 28.91 |
| w28 | 7 | -0.009834 | -5.21 |
| w29 | 24 | -0.072266 | -0.95 |
| w30 | 6 | 0.095686 | 11.06 |
| w31 | 6 | -0.056025 | -3.159 |
| w32 | 10 | 0.021971 | -5.844 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 17 | -0.023189 | -12.884 |
| w23 | 0 | None | 0.0 |
| w24 | 28 | -0.003689 | 100.398 |
| w25 | 25 | 0.111187 | 32.556 |
| w26 | 7 | -0.0585 | -2.335 |
| w27 | 26 | 0.023907 | 8.149 |
| w28 | 3 | -3.9e-05 | -2.99 |
| w29 | 18 | -0.07203 | -18.213 |
| w30 | 13 | -0.118187 | -18.521 |
| w31 | 10 | -0.010257 | -0.377 |
| w32 | 16 | 0.024743 | 25.635 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 17 | -0.047234 | 18.621 |
| w25 | 32 | -0.020838 | 14.305 |
| w26 | 2 | -0.102031 | -8.017 |
| w27 | 33 | 0.027002 | 64.284 |
| w28 | 6 | -0.008045 | -1.4 |
| w29 | 17 | -0.079091 | -2.178 |
| w30 | 1 | 0.043997 | 1.211 |
| w31 | 7 | -0.08768 | -19.593 |
| w32 | 14 | 0.007696 | -2.809 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 22 | 0.076758 | 56.868 |
| w6 | 28 | -0.056469 | 0.238 |
| w7 | 8 | -0.157846 | -9.557 |
| w8 | 3 | -0.169213 | -6.865 |
| w9 | 3 | -0.122144 | -18.607 |
| w10 | 16 | 0.05909 | 22.229 |
| w11 | 25 | 0.054312 | 17.912 |
| w12 | 0 | None | 0.0 |
| w13 | 14 | 0.126913 | 50.353 |
| w14 | 30 | -0.012688 | 26.685 |
| w15 | 15 | -0.058465 | 2.772 |
| w16 | 32 | -0.04835 | 39.423 |
| w17 | 15 | -0.041366 | -7.223 |
| w18 | 17 | -0.166805 | -19.201 |
| w19 | 11 | -0.034445 | -5.256 |
| w20 | 4 | -0.088368 | -8.756 |
| w21 | 1 | -0.025685 | -3.185 |
| w22 | 23 | -0.10843 | -14.021 |
| w23 | 2 | -0.180934 | -5.461 |
| w24 | 27 | -0.070667 | -3.595 |
| w25 | 9 | 0.07061 | 7.333 |
| w26 | 21 | 0.114448 | 20.86 |
| w27 | 20 | -0.065732 | 0.511 |
| w28 | 9 | -0.04295 | -10.596 |
| w29 | 34 | -0.024322 | 1.181 |
| w30 | 34 | 0.105309 | 314.591 |
| w31 | 5 | 0.033442 | 0.201 |
| w32 | 20 | 0.044607 | 49.7 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 34 | 0.017582 | 119.918 |
| w6 | 13 | 0.086715 | 102.0 |
| w7 | 13 | -0.085951 | -14.938 |
| w8 | 0 | None | 0.0 |
| w9 | 7 | -0.249009 | -21.721 |
| w10 | 26 | 0.010454 | 12.578 |
| w11 | 30 | 0.034327 | 4.195 |
| w12 | 2 | 0.000503 | -2.753 |
| w13 | 21 | 0.000206 | 17.197 |
| w14 | 34 | -0.002243 | 36.632 |
| w15 | 35 | -0.053981 | 28.736 |
| w16 | 32 | -0.059886 | 21.58 |
| w17 | 17 | -0.055461 | -7.396 |
| w18 | 16 | 0.012036 | -16.142 |
| w19 | 22 | -0.059323 | -16.446 |
| w20 | 2 | -0.077248 | -1.854 |
| w21 | 21 | -0.176846 | -23.483 |
| w22 | 21 | 0.004164 | 2.522 |
| w23 | 10 | 0.022534 | -1.187 |
| w24 | 29 | -0.037113 | 0.767 |
| w25 | 0 | None | 0.0 |
| w26 | 24 | -0.051598 | 11.376 |
| w27 | 28 | 0.114985 | 22.774 |
| w28 | 29 | 0.061355 | 17.15 |
| w29 | 14 | 0.183297 | 43.476 |
| w30 | 33 | -0.231394 | -9.224 |
| w31 | 15 | -0.000921 | 1.758 |
| w32 | 23 | 0.049991 | 25.25 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 13 | -0.211898 | -21.099 |
| w18 | 37 | -0.131243 | -4.654 |
| w19 | 10 | -0.10818 | -26.139 |
| w20 | 6 | -0.112778 | -13.761 |
| w21 | 5 | -0.049143 | -2.109 |
| w22 | 20 | 0.155697 | 34.36 |
| w23 | 3 | -0.085405 | -4.826 |
| w24 | 24 | -0.078225 | 12.581 |
| w25 | 7 | 0.045282 | 5.375 |
| w26 | 4 | -0.036533 | -3.651 |
| w27 | 11 | 0.2256 | 203.103 |
| w28 | 9 | 0.026662 | 3.857 |
| w29 | 14 | 0.124968 | 30.779 |
| w30 | 1 | -0.045426 | -1.095 |
| w31 | 7 | -0.029909 | -19.794 |
| w32 | 18 | 0.04153 | 11.018 |

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
| w17 | 16 | -0.149779 | -23.589 |
| w18 | 4 | -0.048256 | -5.599 |
| w19 | 11 | 0.083805 | 6.424 |
| w20 | 9 | -0.026375 | 1.698 |
| w21 | 7 | -0.112118 | -28.838 |
| w22 | 18 | 0.10732 | 19.333 |
| w23 | 12 | 0.021259 | -1.012 |
| w24 | 22 | -0.006114 | 21.039 |
| w25 | 15 | -0.054929 | -10.81 |
| w26 | 27 | -0.08807 | -12.877 |
| w27 | 37 | -0.042655 | 34.188 |
| w28 | 4 | -0.112673 | -8.154 |
| w29 | 41 | -0.086931 | -2.192 |
| w30 | 5 | -0.065244 | -9.091 |
| w31 | 3 | -0.046885 | -11.342 |
| w32 | 11 | -0.013948 | 10.399 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 13 | 0.020649 | -0.959 |
| w20 | 6 | -0.019757 | -13.457 |
| w21 | 22 | -0.066747 | -14.303 |
| w22 | 32 | 0.027073 | 144.499 |
| w23 | 22 | -0.026382 | -6.387 |
| w24 | 25 | 0.194451 | 273.88 |
| w25 | 10 | -0.009159 | -13.66 |
| w26 | 8 | -0.066501 | -29.708 |
| w27 | 20 | -0.022738 | -0.73 |
| w28 | 4 | 0.044676 | -4.682 |
| w29 | 31 | -0.050295 | -0.607 |
| w30 | 4 | 0.036337 | -3.82 |
| w31 | 8 | -0.026191 | 2.982 |
| w32 | 30 | -0.004888 | 22.432 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 27 | 0.042823 | 14.161 |
| w23 | 8 | -0.000237 | -8.221 |
| w24 | 22 | -0.041856 | 16.597 |
| w25 | 24 | 0.003212 | -3.21 |
| w26 | 8 | -0.109817 | -15.144 |
| w27 | 21 | -0.061323 | -3.051 |
| w28 | 11 | -0.096535 | -12.798 |
| w29 | 17 | -0.046665 | -11.792 |
| w30 | 4 | -0.134245 | -9.308 |
| w31 | 10 | 0.000121 | 0.533 |
| w32 | 16 | -0.026107 | 3.201 |

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
| w27 | 21 | 0.179779 | 66.99 |
| w28 | 6 | -0.044272 | -4.141 |
| w29 | 11 | -0.035099 | -7.195 |
| w30 | 9 | 0.000873 | -8.267 |
| w31 | 5 | -0.03858 | -4.178 |
| w32 | 18 | 0.03934 | 32.075 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 9 | -0.028598 | 2.128 |
| w18 | 9 | -0.145903 | -12.587 |
| w19 | 3 | 0.027841 | -6.541 |
| w20 | 2 | -0.027943 | -9.127 |
| w21 | 5 | -0.113297 | -25.516 |
| w22 | 23 | -0.123199 | -7.933 |
| w23 | 4 | -0.139428 | -6.031 |
| w24 | 16 | -0.036314 | 51.544 |
| w25 | 18 | 0.082208 | 9.91 |
| w26 | 0 | None | 0.0 |
| w27 | 11 | 0.164277 | 63.157 |
| w28 | 8 | 0.023344 | -2.049 |
| w29 | 12 | -0.227897 | -25.817 |
| w30 | 1 | -0.193307 | -13.317 |
| w31 | 8 | -0.095054 | 0.578 |
| w32 | 7 | -0.140441 | -30.506 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 10 | 0.053915 | 8.317 |
| w18 | 13 | -0.047659 | -6.477 |
| w19 | 5 | -0.01044 | -0.374 |
| w20 | 4 | -0.029273 | -9.005 |
| w21 | 5 | -0.133233 | -40.524 |
| w22 | 27 | 0.098412 | 73.033 |
| w23 | 4 | -0.145411 | -15.279 |
| w24 | 24 | 0.057487 | 71.672 |
| w25 | 16 | 0.134519 | 40.946 |
| w26 | 0 | None | 0.0 |
| w27 | 16 | 0.133709 | 31.498 |
| w28 | 4 | 0.007944 | -2.997 |
| w29 | 15 | -0.104205 | -17.037 |
| w30 | 4 | 0.03969 | -4.464 |
| w31 | 0 | None | 0.0 |
| w32 | 9 | -0.045131 | -24.754 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 6 | -0.04443 | -27.312 |
| w29 | 17 | -0.061798 | -3.306 |
| w30 | 9 | -0.044562 | -11.89 |
| w31 | 9 | 0.054008 | 4.388 |
| w32 | 10 | -0.020006 | -2.423 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 23 | 0.051778 | 18.078 |
| w15 | 12 | 0.101304 | 76.241 |
| w16 | 15 | 0.019948 | 269.681 |
| w17 | 15 | -0.100878 | -9.925 |
| w18 | 8 | -0.086354 | -11.412 |
| w19 | 6 | -0.078504 | -10.864 |
| w20 | 3 | -0.114654 | -10.221 |
| w21 | 15 | 0.027835 | 39.575 |
| w22 | 10 | -0.031267 | -12.687 |
| w23 | 9 | 0.001231 | 2.763 |
| w24 | 23 | 0.035486 | 38.755 |
| w25 | 12 | 0.11494 | 56.127 |
| w26 | 2 | -0.114616 | 2.657 |
| w27 | 21 | 0.215172 | 149.453 |
| w28 | 3 | 0.006505 | -3.171 |
| w29 | 21 | -0.049267 | 3.3 |
| w30 | 8 | -0.103057 | -14.306 |
| w31 | 8 | 0.091989 | 10.764 |
| w32 | 7 | -0.020096 | -10.074 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 10 | 0.302751 | 179.41 |
| w26 | 14 | 0.065768 | 19.211 |
| w27 | 22 | 0.013826 | 27.71 |
| w28 | 3 | -2.9e-05 | -3.055 |
| w29 | 13 | 0.044105 | 18.325 |
| w30 | 0 | None | 0.0 |
| w31 | 11 | -0.01294 | -5.675 |
| w32 | 15 | 0.06782 | 6.485 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

