# Backtest of 031-01.b1.e2_wide-day-in-strong-run_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.b1.e2_wide-day-in-strong-run_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | -0.031722 | -8.907 |
| w2 | 27 | 0.188191 | 54.264 |
| w3 | 51 | 0.052099 | 37.692 |
| w4 | 45 | -0.239588 | -29.774 |
| w5 | 38 | -0.000172 | 43.23 |
| w6 | 41 | 0.117314 | 44.329 |
| w7 | 19 | -0.06158 | -0.19 |
| w8 | 26 | 0.104433 | 5.243 |
| w9 | 17 | -0.019445 | -3.597 |
| w10 | 32 | -0.020506 | 5.502 |
| w11 | 38 | 0.08498 | 28.72 |
| w12 | 20 | 0.053616 | -4.292 |
| w13 | 44 | -0.043865 | 2.159 |
| w14 | 35 | 0.019521 | 9.613 |
| w15 | 50 | 0.014835 | 25.905 |
| w16 | 41 | -0.034295 | 13.917 |
| w17 | 27 | 0.09012 | 4.023 |
| w18 | 27 | 0.003402 | 0.333 |
| w19 | 26 | -0.010773 | -3.204 |
| w20 | 29 | 0.02945 | -9.232 |
| w21 | 25 | -0.050225 | -11.016 |
| w22 | 36 | 0.154135 | 72.079 |
| w23 | 33 | -0.070937 | -15.879 |
| w24 | 44 | 0.056815 | 34.904 |
| w25 | 42 | 0.04786 | 22.89 |
| w26 | 31 | -0.034011 | -4.169 |
| w27 | 42 | 0.100325 | 21.832 |
| w28 | 25 | -0.103512 | -8.123 |
| w29 | 46 | -0.063423 | 1.428 |
| w30 | 27 | 0.146666 | 6.011 |
| w31 | 27 | -0.087959 | -7.16 |
| w32 | 32 | 0.247661 | 29.859 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.051 | 5.752 |
| w2 | 32 | -0.124715 | -31.856 |
| w3 | 49 | -0.113445 | -16.193 |
| w4 | 38 | -0.100148 | -1.485 |
| w5 | 34 | -0.011638 | 18.901 |
| w6 | 39 | 0.162329 | 66.881 |
| w7 | 25 | -0.091237 | -5.676 |
| w8 | 19 | -0.029999 | -12.511 |
| w9 | 26 | -0.041625 | -12.156 |
| w10 | 28 | 0.008359 | 9.108 |
| w11 | 28 | 0.016168 | 1.138 |
| w12 | 30 | 0.019624 | -5.48 |
| w13 | 37 | -0.025253 | 7.326 |
| w14 | 29 | 0.008384 | 15.476 |
| w15 | 44 | 0.043315 | 25.202 |
| w16 | 36 | -0.057796 | 5.763 |
| w17 | 28 | 0.110263 | 14.256 |
| w18 | 24 | 0.002046 | 3.584 |
| w19 | 24 | -0.084623 | -7.697 |
| w20 | 25 | -0.037934 | -5.877 |
| w21 | 38 | -0.025118 | -3.483 |
| w22 | 42 | -0.121369 | -3.987 |
| w23 | 26 | 0.013098 | -3.755 |
| w24 | 36 | -0.122235 | -13.161 |
| w25 | 33 | 0.024814 | 18.48 |
| w26 | 26 | -0.023698 | -4.747 |
| w27 | 42 | 0.030922 | 23.139 |
| w28 | 22 | -0.003014 | -8.962 |
| w29 | 23 | 0.11175 | 14.454 |
| w30 | 23 | -0.142255 | -18.857 |
| w31 | 24 | -0.093747 | -8.428 |
| w32 | 24 | 0.098267 | 6.258 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 32 | 0.089607 | 65.342 |
| w7 | 22 | 0.120835 | 11.156 |
| w8 | 12 | -0.077274 | -16.651 |
| w9 | 28 | 0.213489 | 35.935 |
| w10 | 27 | -0.061376 | -5.449 |
| w11 | 23 | 0.003651 | 14.854 |
| w12 | 21 | -0.037141 | -4.327 |
| w13 | 40 | -0.10777 | -12.672 |
| w14 | 30 | 0.216438 | 53.387 |
| w15 | 37 | 0.246216 | 115.303 |
| w16 | 30 | 0.072769 | 31.577 |
| w17 | 22 | 0.129409 | 31.298 |
| w18 | 21 | -0.034574 | -0.922 |
| w19 | 20 | -0.00183 | 0.68 |
| w20 | 17 | 0.021145 | -4.254 |
| w21 | 26 | 0.156492 | 21.907 |
| w22 | 39 | -0.073207 | 1.017 |
| w23 | 22 | -0.067054 | -0.892 |
| w24 | 38 | 0.00056 | 15.008 |
| w25 | 27 | -0.058974 | -16.067 |
| w26 | 24 | 0.07099 | 8.1 |
| w27 | 35 | 0.251176 | 155.547 |
| w28 | 28 | -0.122272 | -10.416 |
| w29 | 27 | 0.186268 | 35.481 |
| w30 | 18 | -0.002806 | -3.152 |
| w31 | 25 | -0.059326 | -8.343 |
| w32 | 27 | 0.282132 | 27.11 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 24 | 0.147602 | 20.748 |
| w8 | 18 | -0.042651 | -11.672 |
| w9 | 18 | 0.275476 | 36.962 |
| w10 | 32 | 0.052324 | 7.138 |
| w11 | 28 | -0.101617 | -8.766 |
| w12 | 25 | 0.044092 | -1.451 |
| w13 | 40 | -0.077732 | 6.749 |
| w14 | 29 | 0.009658 | 9.66 |
| w15 | 34 | -0.128606 | -31.481 |
| w16 | 35 | 0.001588 | 23.617 |
| w17 | 23 | 0.027761 | 15.857 |
| w18 | 24 | -0.05735 | -10.492 |
| w19 | 29 | 0.008027 | -7.069 |
| w20 | 20 | -0.006083 | -10.224 |
| w21 | 27 | -0.050988 | -13.487 |
| w22 | 34 | 0.061469 | 18.128 |
| w23 | 23 | 0.262294 | 50.059 |
| w24 | 33 | -0.056033 | -0.238 |
| w25 | 29 | 0.054884 | 36.539 |
| w26 | 21 | -0.010982 | -6.278 |
| w27 | 31 | 0.010768 | 9.595 |
| w28 | 21 | -0.020723 | 3.056 |
| w29 | 49 | -0.237695 | -17.266 |
| w30 | 34 | -0.144636 | -8.488 |
| w31 | 25 | -0.101122 | -10.37 |
| w32 | 24 | 0.265866 | 35.802 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | 0.158332 | 78.718 |
| w2 | 32 | -0.011808 | -3.109 |
| w3 | 25 | 0.002688 | -2.954 |
| w4 | 38 | 0.184233 | 147.819 |
| w5 | 40 | -0.084773 | 33.652 |
| w6 | 40 | 0.16798 | 38.242 |
| w7 | 25 | 0.051744 | 14.317 |
| w8 | 20 | -0.003297 | -4.684 |
| w9 | 24 | -0.071628 | -15.345 |
| w10 | 29 | -0.048335 | 7.913 |
| w11 | 31 | 0.049634 | 17.176 |
| w12 | 27 | 0.026202 | -0.213 |
| w13 | 39 | -0.052738 | 18.645 |
| w14 | 33 | 0.137197 | 42.935 |
| w15 | 38 | -0.029995 | 1.539 |
| w16 | 33 | -0.009266 | 22.533 |
| w17 | 33 | 0.018916 | 20.239 |
| w18 | 32 | -0.045965 | -3.373 |
| w19 | 26 | 0.034797 | -3.617 |
| w20 | 26 | 0.055019 | 3.494 |
| w21 | 23 | 0.050895 | 1.307 |
| w22 | 42 | 0.099528 | 40.967 |
| w23 | 29 | -0.171766 | -23.444 |
| w24 | 51 | -0.100234 | -2.057 |
| w25 | 42 | 0.09572 | 34.794 |
| w26 | 19 | 0.046284 | 6.513 |
| w27 | 33 | -0.037463 | 9.424 |
| w28 | 19 | -0.251877 | -25.208 |
| w29 | 38 | 0.130925 | 38.69 |
| w30 | 21 | -0.057977 | -8.641 |
| w31 | 35 | -0.136628 | -17.369 |
| w32 | 30 | 0.15071 | 17.211 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 34 | 0.032405 | 18.053 |
| w11 | 22 | -0.085753 | -3.04 |
| w12 | 23 | -0.021101 | -4.892 |
| w13 | 46 | -0.012647 | 19.075 |
| w14 | 31 | 0.093748 | 35.244 |
| w15 | 33 | 0.015461 | 6.816 |
| w16 | 39 | 0.085792 | 44.678 |
| w17 | 37 | 0.065346 | 41.348 |
| w18 | 18 | -0.210186 | -31.597 |
| w19 | 17 | 0.080036 | 3.828 |
| w20 | 24 | -0.105625 | -17.429 |
| w21 | 12 | 0.052677 | -5.324 |
| w22 | 48 | -0.000207 | 15.294 |
| w23 | 15 | -0.152891 | -19.327 |
| w24 | 46 | 0.185339 | 101.023 |
| w25 | 34 | 0.130214 | 7.423 |
| w26 | 24 | -0.021114 | -4.472 |
| w27 | 32 | 0.24637 | 79.952 |
| w28 | 20 | -0.125078 | -10.599 |
| w29 | 36 | 0.156198 | 24.287 |
| w30 | 18 | -0.040968 | -13.448 |
| w31 | 23 | -0.178165 | -18.468 |
| w32 | 32 | 0.185908 | 27.397 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 39 | -0.001251 | 10.034 |
| w13 | 26 | -0.083095 | -19.625 |
| w14 | 48 | 0.115874 | 62.422 |
| w15 | 24 | -0.008615 | 9.995 |
| w16 | 38 | 0.025937 | 33.2 |
| w17 | 37 | 0.058414 | 5.549 |
| w18 | 29 | -0.199998 | -14.76 |
| w19 | 23 | 0.008985 | 2.829 |
| w20 | 33 | -0.093523 | -16.529 |
| w21 | 24 | 0.001328 | -6.05 |
| w22 | 40 | 0.064998 | 20.908 |
| w23 | 17 | -0.114914 | -17.862 |
| w24 | 44 | -0.054159 | -8.168 |
| w25 | 31 | 0.141768 | 16.076 |
| w26 | 20 | -0.067017 | -11.84 |
| w27 | 36 | 0.058064 | 13.724 |
| w28 | 26 | -0.160256 | -13.901 |
| w29 | 29 | 0.106343 | -2.188 |
| w30 | 7 | -0.014839 | -5.274 |
| w31 | 38 | 0.04249 | -8.194 |
| w32 | 31 | 0.005499 | -12.991 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 27 | -0.049935 | -8.271 |
| w16 | 32 | 0.043338 | 29.298 |
| w17 | 28 | -0.024455 | -3.478 |
| w18 | 31 | 0.092715 | 15.999 |
| w19 | 17 | 0.070601 | 0.966 |
| w20 | 25 | 0.033161 | -1.783 |
| w21 | 24 | 0.018249 | -6.951 |
| w22 | 34 | -0.020298 | -10.164 |
| w23 | 21 | -0.157559 | -14.302 |
| w24 | 50 | -0.053756 | 28.017 |
| w25 | 31 | 0.142132 | 20.249 |
| w26 | 20 | 0.051765 | -0.709 |
| w27 | 32 | 0.08161 | 43.199 |
| w28 | 24 | -0.119573 | -14.413 |
| w29 | 31 | 0.126321 | 15.012 |
| w30 | 12 | -0.096162 | -7.744 |
| w31 | 26 | 0.14043 | 8.608 |
| w32 | 24 | 0.105031 | 7.7 |

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
| w15 | 27 | -0.128223 | -18.83 |
| w16 | 44 | -0.05397 | 24.306 |
| w17 | 28 | 0.074768 | 12.284 |
| w18 | 22 | -0.144709 | -14.071 |
| w19 | 27 | 0.048026 | 3.058 |
| w20 | 24 | 0.012721 | 8.137 |
| w21 | 27 | -0.164041 | -31.26 |
| w22 | 28 | -0.05509 | 6.91 |
| w23 | 40 | -0.047599 | -11.126 |
| w24 | 40 | -0.064729 | 9.538 |
| w25 | 45 | -0.021022 | -10.69 |
| w26 | 38 | 0.216382 | 37.655 |
| w27 | 39 | 0.047231 | 63.665 |
| w28 | 23 | -0.132116 | -8.84 |
| w29 | 56 | -0.149802 | -5.85 |
| w30 | 29 | -0.062166 | -5.681 |
| w31 | 50 | -0.234359 | -1.026 |
| w32 | 35 | 0.101048 | -2.534 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 37 | 0.055958 | 24.34 |
| w17 | 43 | 0.067426 | 18.268 |
| w18 | 24 | 0.000847 | 1.062 |
| w19 | 29 | 0.060807 | -8.668 |
| w20 | 24 | -0.034417 | -9.803 |
| w21 | 19 | -0.126872 | -21.443 |
| w22 | 40 | -0.007806 | 14.195 |
| w23 | 23 | -0.095483 | -18.737 |
| w24 | 43 | 0.028388 | 24.236 |
| w25 | 29 | 0.137834 | 14.532 |
| w26 | 29 | -0.082802 | -13.561 |
| w27 | 35 | 0.115797 | 28.087 |
| w28 | 24 | -0.219017 | -12.484 |
| w29 | 23 | 0.151512 | 6.07 |
| w30 | 20 | -0.074617 | -16.721 |
| w31 | 20 | -0.066824 | -16.616 |
| w32 | 29 | 0.135203 | 1.903 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 22 | 0.010594 | -4.495 |
| w21 | 22 | -0.031536 | -10.895 |
| w22 | 33 | 0.043018 | 22.987 |
| w23 | 20 | -0.000979 | -12.217 |
| w24 | 44 | 0.149616 | 111.543 |
| w25 | 26 | 0.125858 | 18.684 |
| w26 | 25 | 0.003222 | -10.078 |
| w27 | 34 | 0.038894 | 16.531 |
| w28 | 22 | -0.137973 | -9.499 |
| w29 | 36 | 0.004733 | 1.383 |
| w30 | 22 | 0.000362 | -12.211 |
| w31 | 27 | -0.074816 | -11.926 |
| w32 | 22 | 0.089688 | 5.308 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 33 | -0.00734 | 21.543 |
| w23 | 22 | -0.038335 | -11.015 |
| w24 | 35 | 0.194633 | 99.304 |
| w25 | 34 | 0.047267 | 30.924 |
| w26 | 25 | 0.023721 | 1.425 |
| w27 | 35 | 0.056728 | 19.602 |
| w28 | 22 | -0.139668 | -11.789 |
| w29 | 25 | 0.058882 | 4.543 |
| w30 | 19 | 0.0361 | -3.431 |
| w31 | 26 | -0.014595 | -0.742 |
| w32 | 28 | 0.053694 | 30.184 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 42 | -0.046637 | 13.789 |
| w25 | 36 | -0.012503 | 9.958 |
| w26 | 26 | 0.070068 | -1.347 |
| w27 | 46 | 0.068597 | 42.977 |
| w28 | 19 | 0.073261 | 5.913 |
| w29 | 35 | 0.029125 | 2.56 |
| w30 | 21 | 0.0624 | -4.066 |
| w31 | 26 | -0.028052 | -5.443 |
| w32 | 26 | 0.259455 | 56.141 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 33 | 0.106961 | 64.91 |
| w6 | 35 | 0.00017 | 11.751 |
| w7 | 25 | 0.038394 | 4.395 |
| w8 | 19 | 0.089263 | 2.27 |
| w9 | 28 | -0.023237 | -19.142 |
| w10 | 31 | 0.041728 | 11.78 |
| w11 | 27 | 0.072354 | 21.943 |
| w12 | 25 | -0.050068 | -9.627 |
| w13 | 39 | 0.064083 | 48.446 |
| w14 | 38 | -0.089038 | -0.2 |
| w15 | 30 | -0.071907 | -17.285 |
| w16 | 35 | 0.091908 | 41.089 |
| w17 | 30 | 0.022831 | 10.643 |
| w18 | 29 | 0.018703 | 10.576 |
| w19 | 26 | 0.072672 | 17.317 |
| w20 | 23 | 0.010542 | -2.443 |
| w21 | 26 | -0.034 | -16.621 |
| w22 | 37 | -0.100291 | -2.825 |
| w23 | 26 | -0.020687 | -15.214 |
| w24 | 39 | -0.076074 | -4.497 |
| w25 | 30 | 0.116066 | 15.82 |
| w26 | 30 | 0.145082 | 22.994 |
| w27 | 37 | -0.032734 | 20.864 |
| w28 | 26 | -0.130798 | -11.689 |
| w29 | 34 | 0.034151 | 15.121 |
| w30 | 44 | 0.189605 | 101.969 |
| w31 | 26 | -0.007605 | -7.992 |
| w32 | 35 | 0.21148 | 69.21 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 43 | 0.070982 | 86.181 |
| w6 | 31 | 0.021013 | 23.233 |
| w7 | 23 | 0.017339 | 4.205 |
| w8 | 22 | 0.003578 | -2.879 |
| w9 | 25 | 0.024076 | -11.1 |
| w10 | 32 | 0.011509 | 12.72 |
| w11 | 36 | -0.035382 | -4.819 |
| w12 | 22 | -0.184586 | -16.053 |
| w13 | 46 | -0.007789 | 24.078 |
| w14 | 41 | -0.097364 | -1.407 |
| w15 | 52 | -0.172012 | -13.774 |
| w16 | 40 | 0.001553 | 25.751 |
| w17 | 29 | 0.041336 | 11.292 |
| w18 | 24 | -0.107334 | -20.202 |
| w19 | 31 | -0.11199 | -13.351 |
| w20 | 26 | 0.005618 | -0.409 |
| w21 | 36 | -0.162329 | -7.08 |
| w22 | 36 | -0.070383 | 0.071 |
| w23 | 21 | 0.100858 | -7.061 |
| w24 | 46 | -0.095926 | -4.441 |
| w25 | 22 | 0.039539 | 0.348 |
| w26 | 28 | 0.089249 | 12.892 |
| w27 | 34 | 0.007077 | 11.533 |
| w28 | 31 | 0.007186 | 4.211 |
| w29 | 29 | -0.078564 | -2.137 |
| w30 | 41 | -0.161831 | -13.972 |
| w31 | 28 | 0.043488 | 6.824 |
| w32 | 45 | -0.139506 | -6.646 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 32 | -0.017982 | -8.131 |
| w18 | 33 | 0.060334 | 20.699 |
| w19 | 29 | 0.05902 | -6.678 |
| w20 | 29 | -0.065064 | -6.357 |
| w21 | 19 | -0.130507 | -25.129 |
| w22 | 38 | 0.112309 | 29.503 |
| w23 | 26 | -0.018596 | -6.663 |
| w24 | 44 | -0.074775 | 9.429 |
| w25 | 34 | 0.154891 | 27.169 |
| w26 | 38 | -0.010159 | -2.175 |
| w27 | 31 | 0.128352 | 80.687 |
| w28 | 22 | -0.196103 | -10.032 |
| w29 | 25 | 0.202187 | 28.894 |
| w30 | 16 | -0.087556 | -2.395 |
| w31 | 27 | -0.105817 | -14.026 |
| w32 | 33 | 0.138503 | 53.567 |

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
| w17 | 36 | -0.008376 | 4.088 |
| w18 | 28 | 0.039809 | -1.615 |
| w19 | 19 | 0.077635 | 1.075 |
| w20 | 26 | -0.006831 | -4.512 |
| w21 | 21 | -0.13876 | -23.254 |
| w22 | 32 | 0.131343 | 39.054 |
| w23 | 26 | 0.018444 | -11.811 |
| w24 | 43 | 0.023466 | 42.309 |
| w25 | 34 | 0.068831 | 9.636 |
| w26 | 33 | 0.030688 | 8.164 |
| w27 | 40 | -0.025096 | 14.642 |
| w28 | 12 | -0.003096 | -1.432 |
| w29 | 41 | -0.035029 | 12.502 |
| w30 | 16 | -0.044928 | -7.58 |
| w31 | 22 | -0.041278 | -3.539 |
| w32 | 30 | 0.154348 | 35.461 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 17 | -0.062959 | 1.047 |
| w20 | 25 | -0.034365 | -7.616 |
| w21 | 31 | -0.058232 | -7.012 |
| w22 | 48 | -0.001332 | 59.984 |
| w23 | 25 | 0.103396 | 2.413 |
| w24 | 47 | 0.24149 | 126.713 |
| w25 | 24 | -0.055167 | -13.766 |
| w26 | 30 | -0.066763 | -19.36 |
| w27 | 33 | 0.056566 | 14.239 |
| w28 | 23 | -0.120719 | -12.389 |
| w29 | 33 | -0.028229 | -4.192 |
| w30 | 13 | -0.014799 | -5.114 |
| w31 | 34 | -0.098053 | -17.535 |
| w32 | 39 | 0.079726 | 26.45 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 31 | 0.022298 | 20.452 |
| w23 | 29 | -0.047997 | -10.836 |
| w24 | 36 | -0.076184 | 3.132 |
| w25 | 34 | -0.078764 | -14.742 |
| w26 | 24 | 0.066392 | 6.636 |
| w27 | 37 | -0.05609 | -12.457 |
| w28 | 21 | -0.058598 | -6.198 |
| w29 | 31 | 0.115475 | 16.69 |
| w30 | 16 | 0.047087 | -5.12 |
| w31 | 26 | -0.068769 | -11.759 |
| w32 | 26 | 0.104339 | 20.688 |

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
| w27 | 40 | 0.100559 | 38.986 |
| w28 | 26 | -0.185686 | -15.86 |
| w29 | 35 | 0.01711 | -7.244 |
| w30 | 18 | 0.065336 | -1.566 |
| w31 | 29 | -0.203936 | -26.455 |
| w32 | 40 | 0.130946 | 51.375 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 27 | -0.01313 | 0.879 |
| w18 | 19 | -0.056537 | -17.445 |
| w19 | 24 | 0.032454 | -4.322 |
| w20 | 19 | 0.060218 | 8.301 |
| w21 | 27 | -0.064212 | -15.192 |
| w22 | 32 | 0.041613 | 21.396 |
| w23 | 21 | -0.127862 | -21.571 |
| w24 | 39 | -0.148731 | -5.773 |
| w25 | 23 | 0.124989 | 10.135 |
| w26 | 29 | 0.010908 | -3.299 |
| w27 | 36 | -0.042391 | -7.273 |
| w28 | 21 | -0.186617 | -17.336 |
| w29 | 27 | -0.008321 | -14.728 |
| w30 | 13 | 0.18276 | 8.448 |
| w31 | 24 | -0.100385 | -20.066 |
| w32 | 18 | 0.040675 | 4.754 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 34 | 0.066533 | 6.576 |
| w18 | 29 | -0.146412 | -22.689 |
| w19 | 26 | 0.088823 | -11.514 |
| w20 | 25 | -0.015652 | -8.115 |
| w21 | 24 | -0.021604 | -11.038 |
| w22 | 40 | 0.046006 | 71.288 |
| w23 | 25 | 0.047252 | -8.777 |
| w24 | 38 | 0.027907 | 31.062 |
| w25 | 29 | 0.112682 | 35.116 |
| w26 | 21 | -0.031589 | -8.877 |
| w27 | 34 | 0.058294 | 9.465 |
| w28 | 18 | -0.036526 | -7.049 |
| w29 | 30 | 0.088095 | -4.144 |
| w30 | 10 | -0.06757 | -7.253 |
| w31 | 19 | -0.178377 | -19.36 |
| w32 | 27 | 0.207299 | 17.074 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 28 | 0.004787 | -1.155 |
| w29 | 27 | 0.090207 | 13.27 |
| w30 | 23 | -0.010277 | 4.917 |
| w31 | 31 | 0.061109 | 12.329 |
| w32 | 34 | 0.089469 | 11.472 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 22 | 0.163586 | 58.588 |
| w15 | 31 | 0.042396 | 23.637 |
| w16 | 21 | 0.051979 | 216.589 |
| w17 | 26 | -0.007393 | 0.511 |
| w18 | 26 | -0.069158 | -16.666 |
| w19 | 33 | -0.095909 | -19.725 |
| w20 | 23 | -0.070716 | -2.354 |
| w21 | 20 | 0.303063 | 92.372 |
| w22 | 42 | 0.035141 | 11.514 |
| w23 | 26 | -0.077868 | -9.858 |
| w24 | 35 | 0.013392 | 19.133 |
| w25 | 31 | 0.218156 | 55.985 |
| w26 | 24 | -0.034293 | -10.706 |
| w27 | 37 | 0.182755 | 68.434 |
| w28 | 23 | -0.190399 | -17.913 |
| w29 | 34 | 0.0873 | 27.949 |
| w30 | 17 | 0.022854 | -4.074 |
| w31 | 33 | -0.117681 | -15.41 |
| w32 | 21 | 0.233956 | 22.926 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 24 | 0.386307 | 165.35 |
| w26 | 21 | 0.094381 | 7.38 |
| w27 | 29 | 0.202125 | 49.844 |
| w28 | 22 | -0.181948 | -18.376 |
| w29 | 26 | 0.102657 | 1.933 |
| w30 | 15 | -0.00526 | -8.022 |
| w31 | 25 | -0.023736 | 2.061 |
| w32 | 29 | 0.221463 | 17.691 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

