# Backtest of 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d

- Plan: `../../../../../03_test_plan/hold2_rerun_run/plans/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 53 | -0.119174 | -4.169 |
| w2 | 53 | 0.119721 | 78.318 |
| w3 | 53 | -0.032903 | 58.063 |
| w4 | 47 | -0.055204 | -20.181 |
| w5 | 42 | 0.011611 | 73.438 |
| w6 | 49 | 0.04235 | 84.216 |
| w7 | 61 | -0.050572 | -11.975 |
| w8 | 58 | 0.016184 | -3.887 |
| w9 | 47 | 0.023447 | 63.207 |
| w10 | 41 | 0.034433 | 36.529 |
| w11 | 50 | 0.072979 | 54.708 |
| w12 | 56 | -0.074407 | -13.654 |
| w13 | 57 | 0.002944 | 8.309 |
| w14 | 53 | -0.027969 | -15.597 |
| w15 | 42 | 0.084541 | 102.213 |
| w16 | 55 | -0.026723 | 8.49 |
| w17 | 55 | 0.054992 | 2.155 |
| w18 | 60 | 0.003694 | -3.88 |
| w19 | 64 | -0.044088 | -11.727 |
| w20 | 60 | 0.021682 | 37.324 |
| w21 | 55 | -0.114984 | -34.554 |
| w22 | 42 | 0.016313 | 48.997 |
| w23 | 55 | -0.037534 | -22.324 |
| w24 | 42 | 0.023501 | 33.426 |
| w25 | 41 | 0.09651 | 57.774 |
| w26 | 67 | -0.071747 | -22.903 |
| w27 | 52 | -0.005823 | 48.192 |
| w28 | 52 | -0.108806 | -10.561 |
| w29 | 48 | -0.004311 | 13.669 |
| w30 | 67 | -0.048353 | -22.149 |
| w31 | 61 | 0.038313 | 17.561 |
| w32 | 58 | 0.175665 | -3.851 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 51 | -0.18972 | -35.818 |
| w2 | 54 | 0.034756 | 22.91 |
| w3 | 50 | -0.217927 | -39.636 |
| w4 | 48 | 0.076653 | 111.838 |
| w5 | 45 | -0.012408 | 46.223 |
| w6 | 46 | 0.079985 | 85.51 |
| w7 | 49 | -0.077099 | -11.272 |
| w8 | 58 | -0.018883 | 16.571 |
| w9 | 39 | -0.043814 | 5.156 |
| w10 | 45 | -0.061728 | 22.045 |
| w11 | 54 | 0.056977 | 25.327 |
| w12 | 53 | -0.057225 | -14.772 |
| w13 | 55 | 0.003781 | 1.659 |
| w14 | 59 | -0.105708 | -23.732 |
| w15 | 55 | -0.006537 | -9.934 |
| w16 | 50 | -0.06066 | 5.503 |
| w17 | 57 | 0.014179 | 9.116 |
| w18 | 49 | 0.004188 | 4.01 |
| w19 | 61 | -0.065144 | -17.167 |
| w20 | 60 | -0.043507 | 7.801 |
| w21 | 55 | -0.113056 | -30.8 |
| w22 | 64 | -0.060463 | -2.45 |
| w23 | 46 | -0.044152 | -2.34 |
| w24 | 53 | -0.127852 | -32.827 |
| w25 | 55 | -0.041742 | 1.853 |
| w26 | 46 | -0.087792 | -20.579 |
| w27 | 67 | -0.038337 | -15.535 |
| w28 | 50 | -0.063373 | -27.74 |
| w29 | 51 | -0.025974 | 22.111 |
| w30 | 58 | -0.22166 | -46.269 |
| w31 | 51 | 0.001959 | 17.301 |
| w32 | 51 | 0.084381 | -23.868 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 48 | 0.167189 | 117.584 |
| w7 | 44 | 0.021934 | 19.598 |
| w8 | 62 | -0.125251 | 2.305 |
| w9 | 42 | 0.023785 | -22.247 |
| w10 | 48 | -0.187867 | -29.563 |
| w11 | 65 | 0.016479 | -19.267 |
| w12 | 57 | -0.017119 | -27.165 |
| w13 | 51 | -0.001233 | 3.634 |
| w14 | 47 | 0.025639 | 42.617 |
| w15 | 51 | 0.150685 | 121.248 |
| w16 | 50 | 0.006218 | 60.544 |
| w17 | 53 | 0.024927 | 23.226 |
| w18 | 57 | -0.091804 | -13.053 |
| w19 | 55 | -0.002001 | 6.154 |
| w20 | 51 | -0.01361 | 30.28 |
| w21 | 53 | -0.05431 | -31.74 |
| w22 | 56 | -0.10771 | -24.805 |
| w23 | 47 | -0.057223 | -73.036 |
| w24 | 47 | -0.024773 | -3.576 |
| w25 | 51 | -0.045678 | -12.257 |
| w26 | 54 | -0.02129 | -0.455 |
| w27 | 54 | 0.271423 | 183.047 |
| w28 | 47 | -0.161722 | -27.972 |
| w29 | 43 | 0.007043 | 33.203 |
| w30 | 58 | -0.144773 | -5.733 |
| w31 | 55 | -0.008368 | -8.632 |
| w32 | 59 | 0.092872 | -19.669 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 52 | 0.057744 | -3.182 |
| w8 | 57 | -0.046881 | -6.262 |
| w9 | 47 | 0.090741 | 26.771 |
| w10 | 38 | 0.06161 | 21.665 |
| w11 | 47 | -0.013222 | 2.571 |
| w12 | 59 | -0.008778 | -52.006 |
| w13 | 47 | 0.004833 | 16.027 |
| w14 | 67 | -0.135385 | -31.49 |
| w15 | 55 | -0.092925 | -42.743 |
| w16 | 57 | 0.042832 | 38.478 |
| w17 | 57 | 0.000882 | 16.074 |
| w18 | 55 | -0.05862 | -8.864 |
| w19 | 56 | 0.00882 | 3.825 |
| w20 | 48 | 0.030848 | 41.766 |
| w21 | 51 | -0.197968 | -24.671 |
| w22 | 60 | 0.003958 | -25.427 |
| w23 | 46 | 0.128157 | -20.216 |
| w24 | 56 | -0.150965 | -37.423 |
| w25 | 52 | 0.079876 | 43.349 |
| w26 | 56 | -0.071272 | -25.471 |
| w27 | 59 | -0.051872 | -42.494 |
| w28 | 50 | -0.085577 | -1.684 |
| w29 | 53 | -0.22118 | 8.417 |
| w30 | 48 | -0.18474 | -36.239 |
| w31 | 58 | -0.119908 | -22.274 |
| w32 | 45 | 0.162409 | 36.514 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | 0.166515 | 190.276 |
| w2 | 46 | -0.06112 | -9.5 |
| w3 | 59 | 0.034503 | 7.614 |
| w4 | 47 | 0.008049 | 193.898 |
| w5 | 43 | 0.117346 | 120.837 |
| w6 | 47 | -0.046496 | 17.362 |
| w7 | 48 | 0.139549 | 54.269 |
| w8 | 59 | -0.024413 | 17.174 |
| w9 | 44 | 0.065371 | 44.806 |
| w10 | 39 | -0.05744 | -3.892 |
| w11 | 52 | 0.103147 | 39.53 |
| w12 | 58 | -0.056193 | -14.398 |
| w13 | 47 | 0.007225 | 41.551 |
| w14 | 42 | -0.033842 | 69.366 |
| w15 | 55 | -0.048683 | 4.462 |
| w16 | 56 | -0.049684 | 56.687 |
| w17 | 52 | 0.04902 | 32.557 |
| w18 | 71 | -0.107563 | -10.429 |
| w19 | 52 | 0.030301 | 7.933 |
| w20 | 59 | 0.08892 | 41.179 |
| w21 | 48 | -0.106685 | -18.551 |
| w22 | 51 | -0.054396 | 13.359 |
| w23 | 49 | -0.121283 | -11.399 |
| w24 | 59 | 0.003557 | -0.696 |
| w25 | 32 | 0.090938 | 46.746 |
| w26 | 60 | -0.012317 | -13.413 |
| w27 | 68 | -0.045031 | -42.892 |
| w28 | 57 | -0.159826 | 24.157 |
| w29 | 47 | -0.023349 | 55.107 |
| w30 | 52 | -0.122313 | -4.391 |
| w31 | 48 | 0.017719 | 7.42 |
| w32 | 52 | 0.162651 | 57.296 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 41 | 0.04519 | 38.033 |
| w11 | 54 | -0.021221 | -0.6 |
| w12 | 72 | -0.115629 | -44.887 |
| w13 | 53 | 0.068557 | 30.158 |
| w14 | 48 | -0.003388 | 47.358 |
| w15 | 57 | -0.030138 | -1.511 |
| w16 | 54 | 0.07753 | 88.331 |
| w17 | 41 | 0.046242 | 79.952 |
| w18 | 51 | -0.139878 | 2.82 |
| w19 | 53 | -0.002127 | 9.844 |
| w20 | 57 | -0.10799 | -8.473 |
| w21 | 40 | -0.138691 | 14.599 |
| w22 | 48 | -0.065621 | 1.648 |
| w23 | 56 | -0.072929 | 9.931 |
| w24 | 53 | 0.144979 | 64.549 |
| w25 | 54 | 0.051251 | 14.713 |
| w26 | 68 | -0.107235 | -20.029 |
| w27 | 48 | 0.170731 | -44.065 |
| w28 | 45 | -0.204108 | -42.754 |
| w29 | 52 | 0.03337 | 3.355 |
| w30 | 56 | -0.081096 | 2.957 |
| w31 | 53 | -0.163063 | -9.568 |
| w32 | 54 | 0.102286 | 3.202 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 43 | -0.16205 | -28.544 |
| w13 | 49 | 0.003115 | -30.015 |
| w14 | 50 | -0.020735 | 29.892 |
| w15 | 55 | -0.135707 | -47.791 |
| w16 | 46 | -0.057083 | 39.832 |
| w17 | 61 | -0.013842 | 8.159 |
| w18 | 48 | -0.072445 | -15.5 |
| w19 | 54 | -0.04925 | 6.675 |
| w20 | 48 | 0.040248 | 32.687 |
| w21 | 58 | -0.082054 | -15.989 |
| w22 | 58 | -0.015884 | -7.063 |
| w23 | 60 | -0.106023 | 37.227 |
| w24 | 53 | -0.023672 | -0.634 |
| w25 | 49 | 0.063423 | 21.537 |
| w26 | 56 | -0.112779 | 21.241 |
| w27 | 60 | 0.097644 | 1.719 |
| w28 | 59 | -0.181647 | -11.102 |
| w29 | 50 | -0.10082 | -30.119 |
| w30 | 54 | -0.118635 | 6.369 |
| w31 | 63 | -0.018848 | -15.849 |
| w32 | 47 | -0.00548 | -10.025 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 57 | -0.130337 | -19.828 |
| w16 | 57 | 0.008756 | 28.437 |
| w17 | 58 | -0.145322 | -7.816 |
| w18 | 36 | -0.028983 | 41.534 |
| w19 | 58 | -0.054254 | 2.88 |
| w20 | 57 | -0.101327 | -14.795 |
| w21 | 48 | -0.037314 | -25.586 |
| w22 | 53 | -0.032667 | 9.519 |
| w23 | 45 | -0.055299 | 12.731 |
| w24 | 55 | 0.056618 | 49.223 |
| w25 | 51 | 0.064039 | 11.516 |
| w26 | 56 | -0.060967 | -5.773 |
| w27 | 58 | 0.166345 | 51.676 |
| w28 | 60 | -0.038126 | 3.119 |
| w29 | 48 | 0.004884 | -2.703 |
| w30 | 58 | -0.203816 | -11.438 |
| w31 | 62 | -0.025922 | -41.05 |
| w32 | 63 | -0.071436 | -24.915 |

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
| w15 | 52 | -0.126505 | -32.975 |
| w16 | 53 | -0.034595 | 66.772 |
| w17 | 59 | 0.013638 | 13.263 |
| w18 | 57 | -0.080582 | -4.938 |
| w19 | 54 | -0.022534 | 3.99 |
| w20 | 56 | -0.071098 | -14.441 |
| w21 | 53 | -0.114225 | -22.636 |
| w22 | 51 | -0.145246 | -1.536 |
| w23 | 62 | -0.046385 | -11.67 |
| w24 | 51 | -0.101629 | 31.507 |
| w25 | 44 | 0.084398 | 33.636 |
| w26 | 62 | 0.060519 | 30.592 |
| w27 | 43 | 0.085817 | 66.291 |
| w28 | 55 | -0.259266 | -20.5 |
| w29 | 61 | -0.04875 | 29.347 |
| w30 | 56 | -0.05836 | -2.696 |
| w31 | 57 | 0.008048 | 25.12 |
| w32 | 59 | 0.065972 | 5.732 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 54 | 0.037492 | 31.167 |
| w17 | 60 | -0.004299 | -11.826 |
| w18 | 52 | -0.026947 | -0.696 |
| w19 | 55 | -0.014752 | 7.438 |
| w20 | 67 | -0.027185 | 9.547 |
| w21 | 53 | -0.183509 | -11.134 |
| w22 | 59 | -0.039732 | -4.822 |
| w23 | 55 | -0.039196 | 16.582 |
| w24 | 69 | 0.082459 | 45.831 |
| w25 | 52 | 0.084371 | 32.315 |
| w26 | 62 | -0.112012 | -6.442 |
| w27 | 56 | 0.110522 | 7.122 |
| w28 | 62 | -0.137288 | -2.651 |
| w29 | 56 | -0.023772 | -11.298 |
| w30 | 57 | -0.091735 | -29.668 |
| w31 | 51 | -0.109972 | -6.775 |
| w32 | 49 | 0.026935 | -4.53 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 52 | 0.077389 | 41.104 |
| w21 | 49 | -0.152802 | -16.978 |
| w22 | 51 | -0.008217 | -2.485 |
| w23 | 54 | -0.036047 | 32.828 |
| w24 | 55 | 0.211125 | 138.056 |
| w25 | 46 | 0.036351 | 7.622 |
| w26 | 62 | -0.077374 | -17.864 |
| w27 | 54 | 0.023281 | -3.361 |
| w28 | 57 | -0.077918 | 2.928 |
| w29 | 57 | -0.048028 | -11.863 |
| w30 | 48 | 0.034128 | 15.491 |
| w31 | 53 | -0.058977 | -15.021 |
| w32 | 48 | 0.06031 | -1.323 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 55 | -0.053366 | -8.597 |
| w23 | 48 | -0.03968 | 23.998 |
| w24 | 61 | 0.116381 | 78.62 |
| w25 | 50 | 0.069805 | 36.455 |
| w26 | 61 | 0.000746 | 2.505 |
| w27 | 51 | 0.028112 | 21.542 |
| w28 | 59 | -0.102351 | 9.54 |
| w29 | 54 | -0.060231 | -15.435 |
| w30 | 61 | -0.088343 | -25.07 |
| w31 | 51 | 0.01298 | -10.087 |
| w32 | 58 | 0.042026 | -4.898 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 51 | -0.001262 | 21.651 |
| w25 | 50 | 0.018856 | 32.147 |
| w26 | 55 | -0.048637 | -13.673 |
| w27 | 47 | -0.055297 | 52.733 |
| w28 | 63 | -0.009317 | -7.452 |
| w29 | 54 | -0.056718 | -19.501 |
| w30 | 49 | -0.071448 | -19.488 |
| w31 | 48 | 0.047323 | 7.98 |
| w32 | 47 | 0.063289 | -50.447 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 47 | 0.127145 | 102.586 |
| w6 | 42 | -0.037563 | -14.999 |
| w7 | 50 | 0.017845 | 11.845 |
| w8 | 60 | -0.067144 | -15.939 |
| w9 | 52 | -0.058519 | -10.781 |
| w10 | 54 | -0.007747 | 4.626 |
| w11 | 46 | 0.080632 | 17.793 |
| w12 | 48 | -0.123213 | -21.652 |
| w13 | 46 | 0.116645 | 65.801 |
| w14 | 42 | -0.107774 | 13.719 |
| w15 | 51 | -0.168804 | -32.306 |
| w16 | 51 | 0.002287 | 38.019 |
| w17 | 62 | -0.026047 | 0.487 |
| w18 | 57 | -0.033127 | -35.422 |
| w19 | 55 | 0.048129 | -3.959 |
| w20 | 52 | -0.036307 | 5.379 |
| w21 | 60 | -0.186835 | 4.959 |
| w22 | 53 | -0.136765 | -21.707 |
| w23 | 57 | -0.04001 | 6.048 |
| w24 | 61 | -0.131366 | -41.634 |
| w25 | 64 | 0.064413 | 11.5 |
| w26 | 53 | 0.063158 | -24.679 |
| w27 | 56 | -0.059946 | -12.353 |
| w28 | 56 | -0.085366 | -20.54 |
| w29 | 65 | -0.036301 | -15.19 |
| w30 | 48 | 0.117943 | 209.578 |
| w31 | 54 | -0.009008 | -6.558 |
| w32 | 45 | 0.049353 | 4.11 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 60 | 0.084321 | 158.469 |
| w6 | 46 | 0.079427 | 24.957 |
| w7 | 59 | -0.047973 | -9.039 |
| w8 | 58 | -0.043733 | 0.796 |
| w9 | 48 | 0.009812 | 20.991 |
| w10 | 40 | -0.067371 | 12.413 |
| w11 | 53 | -0.010643 | -2.322 |
| w12 | 61 | -0.044764 | 12.78 |
| w13 | 52 | 0.03262 | 6.719 |
| w14 | 51 | -0.132121 | 11.582 |
| w15 | 51 | -0.137625 | 5.403 |
| w16 | 45 | -0.001643 | 36.088 |
| w17 | 58 | -0.068102 | -12.751 |
| w18 | 49 | -0.144927 | -19.859 |
| w19 | 62 | -0.088199 | -41.372 |
| w20 | 60 | -0.008669 | 2.544 |
| w21 | 59 | -0.162846 | -37.844 |
| w22 | 54 | -0.086179 | -2.112 |
| w23 | 67 | 0.043769 | 35.31 |
| w24 | 62 | -0.132538 | -15.444 |
| w25 | 62 | -0.221874 | -36.211 |
| w26 | 47 | -0.057382 | -21.831 |
| w27 | 59 | -0.023179 | -31.172 |
| w28 | 58 | -0.062258 | 19.646 |
| w29 | 40 | 0.10918 | 58.752 |
| w30 | 66 | -0.206825 | -5.541 |
| w31 | 49 | 0.044844 | -7.944 |
| w32 | 54 | -0.054821 | 56.026 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 50 | -0.127429 | -29.761 |
| w18 | 44 | -0.157382 | 2.871 |
| w19 | 60 | -0.080709 | -11.14 |
| w20 | 49 | 0.013725 | 12.627 |
| w21 | 46 | -0.175579 | -29.981 |
| w22 | 53 | 0.039771 | 11.251 |
| w23 | 51 | -0.0272 | 37.733 |
| w24 | 54 | -0.096766 | -9.659 |
| w25 | 51 | 0.084422 | 32.064 |
| w26 | 60 | -0.090028 | -11.34 |
| w27 | 61 | 0.153209 | 90.02 |
| w28 | 49 | -0.03001 | 3.718 |
| w29 | 57 | 0.051998 | 24.762 |
| w30 | 53 | -0.189056 | -23.441 |
| w31 | 51 | 0.002172 | 19.287 |
| w32 | 58 | 0.034166 | 10.2 |

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
| w17 | 60 | -0.085071 | -21.707 |
| w18 | 52 | -0.026967 | 1.985 |
| w19 | 56 | 0.003454 | 0.953 |
| w20 | 55 | 0.004541 | 12.219 |
| w21 | 60 | -0.125571 | -29.924 |
| w22 | 53 | -0.013828 | -4.612 |
| w23 | 52 | -0.022621 | 22.166 |
| w24 | 63 | -0.070727 | 7.283 |
| w25 | 44 | -0.017189 | -10.817 |
| w26 | 61 | -0.068036 | -37.594 |
| w27 | 58 | -0.059616 | -31.107 |
| w28 | 57 | -0.137976 | -7.123 |
| w29 | 53 | -0.099948 | -10.67 |
| w30 | 57 | -0.16699 | -1.2 |
| w31 | 52 | -0.163887 | -8.553 |
| w32 | 46 | 0.103523 | -11.715 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 50 | 0.027826 | 54.079 |
| w20 | 48 | 0.019381 | 16.825 |
| w21 | 46 | -0.09212 | -14.53 |
| w22 | 55 | 0.011629 | 85.583 |
| w23 | 60 | -0.067908 | -12.91 |
| w24 | 49 | 0.113521 | 223.18 |
| w25 | 48 | -0.024825 | -6.07 |
| w26 | 62 | -0.084183 | -51.788 |
| w27 | 66 | -0.040283 | -31.354 |
| w28 | 53 | -0.09646 | 15.06 |
| w29 | 56 | -0.10937 | -23.434 |
| w30 | 50 | -0.108154 | -19.843 |
| w31 | 58 | 0.003291 | 0.957 |
| w32 | 50 | -0.012642 | 8.624 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 51 | 0.038624 | 29.081 |
| w23 | 53 | -0.135591 | -29.254 |
| w24 | 54 | -0.094035 | -12.687 |
| w25 | 56 | -0.065214 | -27.074 |
| w26 | 55 | -0.058819 | -17.263 |
| w27 | 61 | -0.104967 | -48.721 |
| w28 | 47 | -0.058986 | -7.003 |
| w29 | 52 | -0.021177 | -23.976 |
| w30 | 59 | -0.229254 | -20.463 |
| w31 | 46 | 0.042188 | 2.681 |
| w32 | 55 | 0.100489 | 12.23 |

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
| w27 | 64 | 0.031186 | -13.292 |
| w28 | 53 | -0.167477 | -11.311 |
| w29 | 48 | -0.033567 | -2.986 |
| w30 | 61 | -0.064282 | 7.317 |
| w31 | 52 | -0.146421 | -9.254 |
| w32 | 58 | -0.02699 | 24.961 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 53 | 0.000254 | 4.087 |
| w18 | 49 | -0.032637 | 6.93 |
| w19 | 56 | 0.004563 | 14.354 |
| w20 | 43 | 0.11533 | 12.236 |
| w21 | 54 | -0.134337 | -12.453 |
| w22 | 54 | -0.056525 | -2.746 |
| w23 | 52 | 0.011748 | -5.401 |
| w24 | 62 | 0.000363 | 20.227 |
| w25 | 47 | 0.09925 | 23.481 |
| w26 | 52 | -0.099582 | -13.784 |
| w27 | 52 | 0.012734 | -13.496 |
| w28 | 58 | -0.112712 | 3.671 |
| w29 | 56 | -0.119533 | -12.867 |
| w30 | 52 | -0.05085 | -50.875 |
| w31 | 50 | -0.075084 | -6.895 |
| w32 | 55 | -0.057402 | 12.916 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 52 | 0.01717 | 29.446 |
| w18 | 54 | -0.059109 | -0.539 |
| w19 | 57 | -0.058911 | 4.362 |
| w20 | 54 | 0.011127 | 1.641 |
| w21 | 54 | -0.166862 | 0.302 |
| w22 | 57 | 0.074134 | 45.216 |
| w23 | 55 | -0.066498 | -12.013 |
| w24 | 61 | 0.035592 | 17.5 |
| w25 | 41 | 0.114833 | 47.054 |
| w26 | 52 | -0.007772 | 3.285 |
| w27 | 54 | 0.03088 | 0.204 |
| w28 | 56 | -0.051324 | 19.959 |
| w29 | 54 | -0.068469 | -10.617 |
| w30 | 60 | -0.126107 | -11.604 |
| w31 | 52 | -0.126135 | -7.698 |
| w32 | 54 | 0.056501 | -8.486 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 69 | -0.011563 | -21.018 |
| w29 | 46 | -0.056603 | -4.699 |
| w30 | 56 | -0.075299 | -22.114 |
| w31 | 53 | 0.099553 | -3.018 |
| w32 | 63 | -0.029675 | 4.557 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 60 | -0.011286 | -65.585 |
| w15 | 54 | 0.118574 | 58.605 |
| w16 | 43 | -0.086298 | 327.476 |
| w17 | 45 | 0.029368 | 5.256 |
| w18 | 47 | -0.097776 | -7.539 |
| w19 | 54 | -0.108406 | -22.183 |
| w20 | 50 | 0.042048 | 30.789 |
| w21 | 57 | 0.080491 | -49.062 |
| w22 | 57 | -0.095357 | -26.04 |
| w23 | 50 | -0.060712 | -12.14 |
| w24 | 65 | 0.041835 | 8.5 |
| w25 | 46 | 0.120832 | 91.118 |
| w26 | 47 | -0.079011 | -8.205 |
| w27 | 42 | 0.165722 | 101.714 |
| w28 | 51 | -0.059606 | 2.289 |
| w29 | 49 | 0.026001 | 6.453 |
| w30 | 69 | -0.074468 | -10.782 |
| w31 | 48 | -0.035744 | -2.961 |
| w32 | 52 | 0.091742 | 42.629 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 39 | 0.239342 | 217.601 |
| w26 | 53 | 0.049469 | 8.291 |
| w27 | 65 | 0.037054 | 1.419 |
| w28 | 49 | -0.006203 | 17.888 |
| w29 | 53 | -0.014313 | 3.034 |
| w30 | 53 | -0.087284 | -8.43 |
| w31 | 53 | -0.056411 | -12.279 |
| w32 | 42 | 0.091969 | -11.376 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

