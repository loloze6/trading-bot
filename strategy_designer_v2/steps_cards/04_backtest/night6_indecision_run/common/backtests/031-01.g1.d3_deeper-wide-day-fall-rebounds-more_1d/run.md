# Backtest of 031-01.g1.d3_deeper-wide-day-fall-rebounds-more_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.g1.d3_deeper-wide-day-fall-rebounds-more_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.178937 | 12.669 |
| w2 | 4 | -0.075731 | -3.094 |
| w3 | 1 | 0.0816 | 3.9 |
| w4 | 4 | 0.066107 | 8.883 |
| w5 | 2 | -0.100843 | -6.076 |
| w6 | 3 | 0.088344 | 6.423 |
| w7 | 2 | 0.069161 | 4.539 |
| w8 | 3 | 0.090651 | 4.495 |
| w9 | 5 | -0.054472 | -12.425 |
| w10 | 3 | 0.046624 | 3.881 |
| w11 | 3 | 0.018731 | 1.97 |
| w12 | 3 | 0.032934 | 0.548 |
| w13 | 5 | 0.118323 | 9.273 |
| w14 | 2 | 0.070125 | 3.532 |
| w15 | 2 | 0.066744 | 4.193 |
| w16 | 3 | -0.022683 | -0.434 |
| w17 | 3 | 0.028423 | 1.086 |
| w18 | 3 | -0.021673 | -2.093 |
| w19 | 8 | -0.06968 | -10.5 |
| w20 | 5 | 0.069466 | 4.769 |
| w21 | 6 | 0.276631 | 22.548 |
| w22 | 5 | 0.004301 | 4.924 |
| w23 | 6 | 0.171385 | 12.732 |
| w24 | 1 | -0.030349 | -0.577 |
| w25 | 2 | 0.233069 | 10.112 |
| w26 | 2 | -0.045476 | -3.459 |
| w27 | 5 | -0.051485 | -2.144 |
| w28 | 6 | -0.024697 | -4.591 |
| w29 | 4 | 0.069019 | 4.008 |
| w30 | 4 | -0.081568 | -8.786 |
| w31 | 3 | 0.249089 | 19.682 |
| w32 | 5 | -0.220924 | -20.582 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.014907 | -1.977 |
| w2 | 3 | 0.007352 | 0.276 |
| w3 | 1 | -0.009396 | -0.085 |
| w4 | 5 | 0.043193 | 7.059 |
| w5 | 2 | -0.108621 | -2.513 |
| w6 | 3 | 0.094591 | 9.423 |
| w7 | 1 | 0.078008 | 4.279 |
| w8 | 4 | -0.133199 | -11.887 |
| w9 | 6 | 0.037021 | -2.356 |
| w10 | 2 | -0.030089 | -0.743 |
| w11 | 3 | 0.045028 | 2.661 |
| w12 | 2 | 0.125638 | 7.046 |
| w13 | 7 | 0.128019 | 10.291 |
| w14 | 4 | 0.118412 | 9.959 |
| w15 | 4 | 0.133568 | 12.141 |
| w16 | 3 | -0.03424 | -1.103 |
| w17 | 3 | 0.047585 | 5.262 |
| w18 | 6 | 0.111121 | 8.933 |
| w19 | 9 | -0.075992 | -11.47 |
| w20 | 8 | 0.0635 | 4.421 |
| w21 | 5 | 0.220472 | 18.955 |
| w22 | 5 | -0.01805 | -2.563 |
| w23 | 3 | -0.044142 | -3.577 |
| w24 | 3 | 0.108361 | 7.486 |
| w25 | 3 | 0.092789 | 6.523 |
| w26 | 3 | -0.27254 | -24.433 |
| w27 | 4 | -0.099509 | -6.744 |
| w28 | 6 | -0.083777 | -7.715 |
| w29 | 5 | 0.121085 | 9.004 |
| w30 | 2 | -0.027866 | -2.269 |
| w31 | 3 | 0.218645 | 9.751 |
| w32 | 5 | 0.069445 | 4.377 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 5 | -0.050512 | -2.028 |
| w7 | 3 | 0.048512 | 3.055 |
| w8 | 4 | 0.008894 | -6.033 |
| w9 | 6 | 0.193225 | 23.557 |
| w10 | 6 | 0.248111 | 21.826 |
| w11 | 3 | 0.139051 | 7.098 |
| w12 | 2 | -0.064638 | -8.717 |
| w13 | 5 | 0.135536 | 8.3 |
| w14 | 1 | 0.122727 | 2.298 |
| w15 | 3 | 0.21962 | 18.412 |
| w16 | 3 | 0.085339 | 10.362 |
| w17 | 3 | -0.012426 | -2.359 |
| w18 | 4 | 0.151274 | 9.607 |
| w19 | 7 | 0.137861 | 11.299 |
| w20 | 4 | 0.094091 | 5.022 |
| w21 | 6 | 0.449053 | 69.411 |
| w22 | 5 | 0.134737 | 13.957 |
| w23 | 1 | -0.098886 | -3.081 |
| w24 | 1 | 0.009882 | 0.293 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | -0.081354 | -13.408 |
| w27 | 3 | -0.127763 | -7.708 |
| w28 | 5 | 0.071758 | 6.605 |
| w29 | 3 | 0.04313 | 3.113 |
| w30 | 3 | 0.037783 | 0.77 |
| w31 | 5 | 0.204976 | 11.29 |
| w32 | 2 | -0.015196 | -1.741 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 2 | -0.016766 | -1.042 |
| w8 | 2 | 0.061248 | 1.998 |
| w9 | 7 | -0.044292 | -11.019 |
| w10 | 2 | 0.009585 | 1.949 |
| w11 | 3 | 0.075642 | 4.096 |
| w12 | 2 | 0.021192 | -0.502 |
| w13 | 7 | 0.06175 | 3.219 |
| w14 | 3 | 0.103727 | 5.237 |
| w15 | 4 | 0.033687 | -1.237 |
| w16 | 4 | 0.058394 | 8.016 |
| w17 | 3 | 0.014506 | 2.202 |
| w18 | 4 | 0.032518 | 0.033 |
| w19 | 6 | 0.036951 | -1.86 |
| w20 | 10 | 0.1214 | 9.061 |
| w21 | 8 | 0.183866 | 10.372 |
| w22 | 3 | -0.002911 | -0.573 |
| w23 | 5 | 0.161188 | 26.56 |
| w24 | 5 | 0.077084 | 5.282 |
| w25 | 3 | -0.006031 | -0.301 |
| w26 | 1 | -0.039621 | -2.428 |
| w27 | 5 | -0.023454 | -1.456 |
| w28 | 7 | 0.026808 | -0.129 |
| w29 | 2 | -0.004535 | 0.136 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | 0.200404 | 13.881 |
| w32 | 5 | 0.062903 | 2.62 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.052087 | 11.689 |
| w2 | 4 | -0.002958 | -2.792 |
| w3 | 3 | 0.244583 | 16.912 |
| w4 | 2 | 0.280192 | 23.041 |
| w5 | 2 | 0.075303 | 4.207 |
| w6 | 4 | 0.15754 | 14.578 |
| w7 | 3 | 0.089701 | 6.381 |
| w8 | 6 | -0.005582 | -6.434 |
| w9 | 4 | 0.129072 | 7.159 |
| w10 | 2 | 0.053256 | 2.61 |
| w11 | 5 | 0.050147 | 4.742 |
| w12 | 4 | -0.135084 | -17.228 |
| w13 | 7 | 0.126295 | 12.571 |
| w14 | 2 | 0.033692 | 2.155 |
| w15 | 2 | 0.059974 | 4.872 |
| w16 | 3 | 0.141058 | 12.349 |
| w17 | 2 | -0.046534 | -3.257 |
| w18 | 6 | 0.095113 | 8.127 |
| w19 | 6 | -0.030279 | -4.031 |
| w20 | 8 | -0.050655 | -10.862 |
| w21 | 6 | 0.279279 | 24.049 |
| w22 | 6 | 0.036664 | 6.517 |
| w23 | 4 | 0.024071 | 1.386 |
| w24 | 2 | 0.056154 | 5.028 |
| w25 | 3 | 0.243761 | 17.452 |
| w26 | 4 | -0.222906 | -25.728 |
| w27 | 4 | -0.065831 | -4.312 |
| w28 | 8 | 0.150504 | 12.068 |
| w29 | 4 | -0.026789 | -0.471 |
| w30 | 4 | -0.076453 | -8.631 |
| w31 | 4 | 0.257591 | 22.73 |
| w32 | 2 | -0.079716 | -5.726 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 5 | 0.008646 | 1.085 |
| w11 | 5 | 0.175467 | 13.747 |
| w12 | 4 | 0.184146 | 14.475 |
| w13 | 5 | 0.168774 | 12.774 |
| w14 | 4 | 0.164808 | 11.504 |
| w15 | 5 | 0.119461 | 14.143 |
| w16 | 1 | 0.035285 | 1.912 |
| w17 | 3 | 0.199587 | 21.522 |
| w18 | 3 | -0.091825 | -10.046 |
| w19 | 7 | -0.050485 | -6.092 |
| w20 | 8 | 0.037038 | 0.416 |
| w21 | 10 | 0.298429 | 28.506 |
| w22 | 3 | -0.044282 | -1.783 |
| w23 | 4 | -0.075737 | -10.343 |
| w24 | 3 | -0.029088 | -0.493 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.056995 | -5.111 |
| w27 | 3 | -0.075884 | -7.436 |
| w28 | 6 | 0.05079 | 2.711 |
| w29 | 4 | 0.113856 | 8.499 |
| w30 | 1 | 0.002559 | -0.386 |
| w31 | 3 | 0.102965 | 4.662 |
| w32 | 6 | -0.204969 | -32.575 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 3 | 0.150448 | 10.662 |
| w13 | 4 | 0.199834 | 15.593 |
| w14 | 6 | 0.287555 | 32.508 |
| w15 | 4 | 0.24808 | 20.75 |
| w16 | 2 | 0.113532 | 9.058 |
| w17 | 4 | -0.027115 | -1.067 |
| w18 | 3 | -0.058938 | -4.449 |
| w19 | 5 | 0.091105 | 5.915 |
| w20 | 4 | 0.037943 | 2.39 |
| w21 | 4 | 0.267438 | 19.576 |
| w22 | 6 | 0.018247 | 1.233 |
| w23 | 4 | 0.073418 | 1.545 |
| w24 | 4 | -0.043469 | -4.594 |
| w25 | 2 | 0.086225 | 1.704 |
| w26 | 3 | -0.143977 | -14.647 |
| w27 | 4 | 0.041732 | 2.201 |
| w28 | 7 | 0.117167 | 8.386 |
| w29 | 4 | 0.007365 | -0.511 |
| w30 | 3 | 0.028534 | -0.791 |
| w31 | 4 | 0.199449 | 12.089 |
| w32 | 3 | 0.017533 | -0.77 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 3 | 0.037561 | -1.257 |
| w16 | 4 | -0.047872 | -1.14 |
| w17 | 7 | 0.136893 | 16.33 |
| w18 | 2 | 0.08282 | 6.899 |
| w19 | 3 | -0.06377 | -8.649 |
| w20 | 8 | 0.078523 | 5.635 |
| w21 | 8 | 0.287914 | 36.478 |
| w22 | 7 | 0.052402 | 4.421 |
| w23 | 1 | -0.027814 | -2.328 |
| w24 | 4 | 0.07544 | 7.194 |
| w25 | 1 | 0.061192 | 2.684 |
| w26 | 2 | 0.091677 | 4.167 |
| w27 | 2 | 0.118806 | 9.211 |
| w28 | 6 | 0.143273 | 9.464 |
| w29 | 6 | 0.041148 | 3.336 |
| w30 | 3 | 0.043321 | -0.748 |
| w31 | 3 | 0.120583 | 6.912 |
| w32 | 5 | -0.026812 | -4.327 |

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
| w15 | 3 | 0.019001 | 0.937 |
| w16 | 3 | 0.021157 | 2.145 |
| w17 | 3 | -0.039931 | -3.318 |
| w18 | 4 | 0.108765 | 8.487 |
| w19 | 8 | 0.037854 | 1.926 |
| w20 | 7 | 0.202608 | 27.109 |
| w21 | 6 | 0.227945 | 19.591 |
| w22 | 6 | 0.238115 | 29.253 |
| w23 | 4 | -0.171229 | -11.579 |
| w24 | 4 | 0.276339 | 24.294 |
| w25 | 6 | 0.046935 | 3.287 |
| w26 | 5 | -0.087975 | -9.11 |
| w27 | 6 | -0.020554 | 2.173 |
| w28 | 4 | 0.087512 | 5.993 |
| w29 | 3 | -0.057044 | -3.242 |
| w30 | 2 | 0.034638 | 0.496 |
| w31 | 5 | 0.054054 | 1.939 |
| w32 | 5 | -0.021225 | -2.879 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 2 | 0.054279 | 4.829 |
| w17 | 5 | 0.050094 | 8.679 |
| w18 | 3 | -0.017434 | -1.957 |
| w19 | 6 | 0.048879 | 2.023 |
| w20 | 4 | 0.055477 | 2.083 |
| w21 | 7 | 0.208133 | 13.414 |
| w22 | 5 | 0.038563 | 3.225 |
| w23 | 1 | None | -0.429 |
| w24 | 1 | -0.085052 | -4.57 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.14005 | -12.187 |
| w27 | 6 | 0.024058 | 0.857 |
| w28 | 7 | 0.05812 | 1.211 |
| w29 | 6 | 0.001396 | -2.324 |
| w30 | 2 | -0.00853 | -1.305 |
| w31 | 2 | 0.115886 | 6.909 |
| w32 | 5 | 0.12709 | 6.498 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 4 | 0.046718 | 2.098 |
| w21 | 5 | 0.29838 | 24.552 |
| w22 | 7 | 0.034929 | 4.862 |
| w23 | 0 | 0.0606 | 0.0 |
| w24 | 4 | 0.022468 | 3.112 |
| w25 | 1 | 0.162874 | 7.601 |
| w26 | 2 | -0.102854 | -6.676 |
| w27 | 3 | 0.048763 | 3.756 |
| w28 | 6 | -0.006057 | -2.985 |
| w29 | 5 | 0.023711 | 1.77 |
| w30 | 4 | 0.048383 | 1.884 |
| w31 | 5 | 0.102028 | 5.857 |
| w32 | 5 | -0.005921 | -2.826 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 6 | 0.005954 | 0.34 |
| w23 | 2 | 0.057101 | 2.182 |
| w24 | 3 | 0.012853 | 2.099 |
| w25 | 4 | 0.01288 | 1.036 |
| w26 | 2 | -0.161854 | -8.579 |
| w27 | 2 | -0.043627 | -2.168 |
| w28 | 6 | -0.056817 | -8.631 |
| w29 | 2 | 0.050158 | 2.841 |
| w30 | 6 | -0.068161 | -5.35 |
| w31 | 2 | 0.105268 | 5.789 |
| w32 | 5 | -0.172267 | -11.733 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 4 | -0.012308 | -0.57 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | 0.01917 | 0.229 |
| w27 | 1 | 0.075635 | 3.18 |
| w28 | 5 | -0.016579 | -1.364 |
| w29 | 4 | 0.009705 | 0.594 |
| w30 | 5 | 0.058622 | 3.579 |
| w31 | 2 | 0.279814 | 12.451 |
| w32 | 4 | 0.132985 | 12.274 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 0 | None | 0.0 |
| w6 | 4 | 0.138065 | 13.38 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | 0.18567 | 10.997 |
| w9 | 6 | -0.135123 | -24.848 |
| w10 | 4 | -0.014626 | -1.372 |
| w11 | 5 | 0.168297 | 13.715 |
| w12 | 4 | -0.015247 | -3.172 |
| w13 | 5 | -0.007478 | -0.979 |
| w14 | 3 | 0.116872 | 7.607 |
| w15 | 7 | 0.063138 | 5.402 |
| w16 | 3 | 0.069336 | 8.276 |
| w17 | 7 | 0.150888 | 20.224 |
| w18 | 4 | -0.016168 | -1.757 |
| w19 | 6 | -0.101788 | -10.903 |
| w20 | 4 | 0.064193 | 3.412 |
| w21 | 6 | 0.283555 | 24.589 |
| w22 | 4 | 0.083965 | 7.603 |
| w23 | 2 | -0.104414 | -7.007 |
| w24 | 4 | 0.076294 | 6.675 |
| w25 | 2 | -0.036067 | -2.1 |
| w26 | 3 | -0.023631 | -0.796 |
| w27 | 2 | 0.09464 | 5.06 |
| w28 | 5 | 0.03337 | -0.043 |
| w29 | 3 | 0.147441 | 12.023 |
| w30 | 6 | 0.118242 | 18.651 |
| w31 | 2 | 0.136125 | 7.07 |
| w32 | 3 | -0.04137 | -0.36 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 2 | -0.088837 | -5.374 |
| w6 | 2 | 0.178267 | 10.756 |
| w7 | 2 | 0.071593 | 4.023 |
| w8 | 4 | 0.14327 | 9.737 |
| w9 | 5 | 0.008707 | -4.296 |
| w10 | 4 | 0.038219 | 2.496 |
| w11 | 5 | 0.038528 | 2.53 |
| w12 | 7 | 0.100343 | 4.775 |
| w13 | 6 | 0.071856 | 3.806 |
| w14 | 3 | 0.068069 | 5.321 |
| w15 | 5 | 0.142147 | 13.973 |
| w16 | 5 | 0.040983 | 6.885 |
| w17 | 4 | 0.28299 | 22.297 |
| w18 | 4 | -0.02829 | -4.198 |
| w19 | 5 | -0.029946 | -3.296 |
| w20 | 4 | -0.068082 | -4.398 |
| w21 | 6 | 0.220707 | 15.854 |
| w22 | 6 | 0.107869 | 10.395 |
| w23 | 1 | 0.019445 | 0.343 |
| w24 | 2 | 0.072822 | 3.303 |
| w25 | 5 | 0.297148 | 31.977 |
| w26 | 5 | 0.243969 | 20.766 |
| w27 | 4 | 0.099468 | 11.734 |
| w28 | 7 | 0.122375 | 12.623 |
| w29 | 4 | -0.03154 | -3.838 |
| w30 | 2 | -0.111227 | -4.509 |
| w31 | 7 | 0.073899 | 8.245 |
| w32 | 6 | 0.050859 | 12.47 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 3 | 0.041556 | 2.125 |
| w18 | 5 | 0.045909 | 4.76 |
| w19 | 4 | 0.106786 | 5.972 |
| w20 | 4 | -0.064241 | -6.378 |
| w21 | 5 | 0.11606 | 0.34 |
| w22 | 3 | -0.021316 | -1.393 |
| w23 | 4 | 0.252271 | 18.602 |
| w24 | 2 | -0.041525 | -2.499 |
| w25 | 1 | 0.360942 | 16.196 |
| w26 | 2 | -0.127623 | -9.537 |
| w27 | 2 | -0.083926 | -4.246 |
| w28 | 7 | 0.06394 | 5.717 |
| w29 | 4 | -0.026135 | -2.621 |
| w30 | 1 | -0.034102 | -1.691 |
| w31 | 3 | 0.209065 | 9.339 |
| w32 | 4 | -0.058253 | -5.733 |

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
| w17 | 4 | 0.057206 | 5.03 |
| w18 | 4 | 0.01138 | 0.726 |
| w19 | 6 | 0.018724 | -1.477 |
| w20 | 5 | -0.01552 | -2.667 |
| w21 | 8 | 0.264393 | 24.305 |
| w22 | 4 | 0.085117 | 7.661 |
| w23 | 4 | 0.096757 | 5.056 |
| w24 | 4 | 0.000837 | 3.327 |
| w25 | 3 | -0.194108 | -14.924 |
| w26 | 3 | -0.051484 | -3.447 |
| w27 | 4 | 0.071741 | 9.422 |
| w28 | 5 | 0.171076 | 12.897 |
| w29 | 2 | 0.009107 | 0.743 |
| w30 | 2 | -0.008501 | -1.931 |
| w31 | 4 | 0.021427 | -2.693 |
| w32 | 7 | -0.093136 | -8.361 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 4 | -0.072775 | -10.403 |
| w20 | 5 | -0.189743 | -14.123 |
| w21 | 5 | 0.0146 | -2.712 |
| w22 | 5 | -0.025357 | -0.204 |
| w23 | 3 | 0.029723 | 1.243 |
| w24 | 5 | -0.042114 | -2.671 |
| w25 | 2 | 0.156142 | 7.559 |
| w26 | 3 | -0.086742 | -6.007 |
| w27 | 3 | -0.023447 | -0.931 |
| w28 | 5 | 0.020869 | -1.087 |
| w29 | 6 | -0.071671 | -7.727 |
| w30 | 5 | 0.032214 | -0.871 |
| w31 | 3 | 0.114634 | 5.296 |
| w32 | 1 | -0.087994 | -3.485 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 4 | 0.025269 | 1.613 |
| w23 | 2 | 0.225499 | 11.732 |
| w24 | 5 | 0.087347 | 12.828 |
| w25 | 3 | -0.083068 | -3.949 |
| w26 | 3 | 0.086908 | 4.893 |
| w27 | 2 | -0.112642 | -7.491 |
| w28 | 5 | -0.057129 | -7.134 |
| w29 | 4 | -0.022362 | -1.919 |
| w30 | 5 | 0.073738 | 3.432 |
| w31 | 6 | 0.082501 | 4.83 |
| w32 | 4 | 0.009373 | -0.168 |

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
| w27 | 3 | 0.053325 | 1.998 |
| w28 | 5 | 0.079243 | 5.256 |
| w29 | 4 | 0.049994 | 3.316 |
| w30 | 1 | -0.058212 | -3.175 |
| w31 | 3 | 0.143359 | 7.678 |
| w32 | 5 | 0.094582 | 9.363 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | 0.09519 | 5.958 |
| w18 | 3 | -0.157572 | -12.024 |
| w19 | 6 | 0.080454 | 3.106 |
| w20 | 4 | -0.040375 | -5.245 |
| w21 | 5 | 0.175422 | 10.977 |
| w22 | 5 | 0.049076 | 7.269 |
| w23 | 1 | 0.003222 | -0.405 |
| w24 | 4 | -0.098918 | -8.845 |
| w25 | 1 | 0.056172 | 2.29 |
| w26 | 1 | -0.035163 | -1.299 |
| w27 | 4 | 0.008725 | 1.571 |
| w28 | 7 | 0.01343 | -2.202 |
| w29 | 5 | 0.043614 | 1.203 |
| w30 | 2 | -0.006154 | -0.153 |
| w31 | 4 | 0.163623 | 9.114 |
| w32 | 6 | 0.054685 | 2.806 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 2 | -0.005873 | -0.207 |
| w18 | 3 | 0.225098 | 16.133 |
| w19 | 7 | 0.104819 | 5.511 |
| w20 | 5 | -0.009856 | -1.676 |
| w21 | 4 | 0.255684 | 18.387 |
| w22 | 5 | -0.023518 | 0.591 |
| w23 | 2 | -0.001205 | -0.875 |
| w24 | 4 | -0.004798 | 1.476 |
| w25 | 3 | -0.022137 | -0.739 |
| w26 | 3 | -0.097335 | -7.914 |
| w27 | 1 | -0.07361 | -3.261 |
| w28 | 7 | 0.020422 | -3.392 |
| w29 | 7 | 0.106005 | 10.619 |
| w30 | 4 | 0.141222 | 8.915 |
| w31 | 2 | 0.275414 | 11.047 |
| w32 | 3 | 0.053042 | 1.488 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 4 | -0.013086 | -3.569 |
| w29 | 4 | 0.164137 | 14.507 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | 0.060254 | 5.492 |
| w32 | 6 | 0.157969 | 17.653 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 2 | 0.02662 | 3.194 |
| w15 | 3 | 0.089567 | 1.86 |
| w16 | 3 | 0.032007 | 4.258 |
| w17 | 4 | 0.063344 | 4.226 |
| w18 | 0 | None | 0.0 |
| w19 | 4 | 0.0725 | 4.411 |
| w20 | 7 | -0.066279 | -12.133 |
| w21 | 5 | 0.099222 | 9.778 |
| w22 | 6 | 0.12042 | 11.445 |
| w23 | 1 | -0.278682 | -12.061 |
| w24 | 2 | 0.016125 | 2.435 |
| w25 | 1 | -0.0482 | -3.099 |
| w26 | 2 | -0.061207 | -4.256 |
| w27 | 3 | -0.032804 | -2.981 |
| w28 | 8 | 0.00934 | -2.318 |
| w29 | 5 | -0.002781 | -0.675 |
| w30 | 1 | -0.06556 | -1.422 |
| w31 | 3 | 0.17291 | 9.85 |
| w32 | 3 | 0.044583 | 1.565 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 3 | 0.234598 | 19.187 |
| w26 | 1 | 0.070824 | 1.089 |
| w27 | 3 | -0.099879 | -6.168 |
| w28 | 4 | -0.100601 | -10.985 |
| w29 | 4 | 0.01529 | 0.81 |
| w30 | 3 | 0.199255 | 11.827 |
| w31 | 4 | 0.221821 | 14.343 |
| w32 | 5 | 0.023068 | 0.337 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

