# Backtest of 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d

- Plan: `../../../../../03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 55 | -0.047042 | -3.524 |
| w2 | 39 | 0.063287 | 36.391 |
| w3 | 42 | -0.002528 | 71.273 |
| w4 | 56 | -0.167999 | -34.832 |
| w5 | 36 | 0.034787 | 109.432 |
| w6 | 48 | -0.000479 | 80.637 |
| w7 | 48 | -0.100506 | -13.947 |
| w8 | 47 | -0.089518 | -20.455 |
| w9 | 48 | 0.023212 | 57.449 |
| w10 | 41 | 0.024705 | 29.588 |
| w11 | 51 | -0.033015 | 22.836 |
| w12 | 48 | -0.064297 | -10.302 |
| w13 | 53 | -0.018651 | 12.026 |
| w14 | 39 | 0.010093 | 22.068 |
| w15 | 33 | 0.129252 | 137.404 |
| w16 | 40 | -0.073681 | 11.442 |
| w17 | 45 | 0.107366 | 46.852 |
| w18 | 38 | 0.032662 | 10.46 |
| w19 | 65 | -0.074597 | -17.587 |
| w20 | 49 | 0.007659 | 23.242 |
| w21 | 57 | -0.138563 | -29.537 |
| w22 | 33 | -0.043673 | 16.318 |
| w23 | 49 | -0.00237 | -5.759 |
| w24 | 48 | 0.031856 | 39.065 |
| w25 | 31 | 0.103486 | 39.289 |
| w26 | 57 | -0.127223 | -28.025 |
| w27 | 48 | 0.029132 | 63.506 |
| w28 | 59 | -0.077335 | -22.029 |
| w29 | 54 | -0.002584 | 4.247 |
| w30 | 51 | 0.030657 | 13.873 |
| w31 | 47 | 0.024771 | 0.242 |
| w32 | 56 | 0.131003 | 10.338 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 63 | -0.088648 | -6.712 |
| w2 | 45 | -0.008709 | 7.778 |
| w3 | 59 | -0.219213 | -58.124 |
| w4 | 47 | 0.108247 | 100.51 |
| w5 | 45 | -0.04841 | 25.787 |
| w6 | 42 | 0.029348 | 58.694 |
| w7 | 35 | -0.061155 | -10.737 |
| w8 | 48 | -0.101074 | -3.098 |
| w9 | 48 | -0.023213 | 19.816 |
| w10 | 44 | -0.069132 | 12.159 |
| w11 | 45 | 0.084004 | 20.652 |
| w12 | 53 | -0.121041 | -13.449 |
| w13 | 47 | 0.013224 | 15.686 |
| w14 | 38 | -0.038873 | -9.03 |
| w15 | 45 | 0.053571 | 37.422 |
| w16 | 50 | -0.111308 | 5.112 |
| w17 | 44 | -0.009858 | 1.879 |
| w18 | 56 | 0.020214 | 2.671 |
| w19 | 64 | -0.084703 | -6.734 |
| w20 | 51 | -0.011918 | 21.911 |
| w21 | 65 | -0.085851 | -15.659 |
| w22 | 66 | -0.070639 | -11.64 |
| w23 | 51 | -0.170626 | -50.955 |
| w24 | 55 | -0.133595 | -22.111 |
| w25 | 53 | 0.028998 | 20.06 |
| w26 | 54 | -0.185282 | -5.631 |
| w27 | 65 | 0.000708 | 43.143 |
| w28 | 48 | -0.09432 | -14.194 |
| w29 | 47 | 0.028132 | 25.579 |
| w30 | 64 | -0.162951 | -32.661 |
| w31 | 51 | 0.009113 | 11.909 |
| w32 | 63 | 0.021155 | 5.468 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 55 | 0.134652 | 83.274 |
| w7 | 25 | -0.050513 | -8.978 |
| w8 | 39 | -0.146874 | -12.193 |
| w9 | 42 | -0.019579 | -15.426 |
| w10 | 62 | -0.18346 | -30.434 |
| w11 | 50 | -0.003864 | -11.893 |
| w12 | 58 | -0.027395 | 6.159 |
| w13 | 56 | -0.030644 | -3.493 |
| w14 | 52 | 0.039008 | 23.07 |
| w15 | 36 | 0.186537 | 160.13 |
| w16 | 38 | -0.025638 | 42.597 |
| w17 | 35 | 0.050097 | 20.152 |
| w18 | 46 | -0.067374 | -5.356 |
| w19 | 58 | -0.035725 | -0.886 |
| w20 | 36 | 0.041727 | 36.184 |
| w21 | 50 | -0.001625 | -2.394 |
| w22 | 48 | -0.106243 | -14.779 |
| w23 | 44 | -0.067374 | -26.301 |
| w24 | 46 | -0.045911 | -3.933 |
| w25 | 56 | 0.016086 | 13.903 |
| w26 | 59 | 0.001665 | -8.992 |
| w27 | 45 | 0.267732 | 207.632 |
| w28 | 44 | -0.231487 | -23.988 |
| w29 | 55 | 0.018197 | 27.151 |
| w30 | 59 | -0.065075 | 5.832 |
| w31 | 48 | -0.056018 | -28.703 |
| w32 | 57 | 0.056051 | -31.308 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 39 | -0.054303 | -18.912 |
| w8 | 32 | -0.061107 | -8.124 |
| w9 | 51 | -0.043507 | -5.74 |
| w10 | 40 | 0.052584 | 41.083 |
| w11 | 40 | -0.054057 | -2.934 |
| w12 | 46 | -0.059331 | -9.586 |
| w13 | 37 | 0.032287 | 26.895 |
| w14 | 43 | -0.056308 | -18.395 |
| w15 | 56 | -0.073969 | -10.968 |
| w16 | 44 | -0.0025 | 51.432 |
| w17 | 37 | 0.028514 | 24.261 |
| w18 | 55 | -0.073753 | -11.423 |
| w19 | 63 | -0.014643 | -1.886 |
| w20 | 46 | 0.038284 | 32.299 |
| w21 | 72 | -0.249675 | -23.421 |
| w22 | 52 | -0.011736 | -4.508 |
| w23 | 39 | 0.110726 | 32.835 |
| w24 | 52 | -0.141946 | -13.418 |
| w25 | 46 | 0.041017 | 40.564 |
| w26 | 50 | -0.122592 | -19.248 |
| w27 | 54 | -0.004972 | -2.002 |
| w28 | 50 | -0.066798 | -19.096 |
| w29 | 57 | -0.128755 | -1.844 |
| w30 | 67 | -0.040397 | -3.756 |
| w31 | 60 | -0.142195 | -17.772 |
| w32 | 41 | 0.114471 | 71.8 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | 0.167238 | 230.046 |
| w2 | 59 | -0.053782 | -5.706 |
| w3 | 64 | 0.034526 | 15.669 |
| w4 | 36 | 0.026943 | 277.836 |
| w5 | 34 | 0.113055 | 94.844 |
| w6 | 36 | 0.053624 | 71.061 |
| w7 | 45 | 0.080506 | 20.662 |
| w8 | 38 | 0.019319 | 17.401 |
| w9 | 37 | 0.026549 | 50.157 |
| w10 | 46 | -0.138773 | -13.928 |
| w11 | 40 | 0.063598 | 25.793 |
| w12 | 44 | -0.072174 | -9.119 |
| w13 | 44 | -0.008716 | 22.611 |
| w14 | 46 | -0.010057 | 51.95 |
| w15 | 47 | 0.062691 | 43.72 |
| w16 | 41 | 0.028663 | 83.923 |
| w17 | 42 | 0.012434 | 20.049 |
| w18 | 51 | -0.006479 | 1.271 |
| w19 | 54 | 0.008187 | 3.743 |
| w20 | 57 | 0.104483 | 68.138 |
| w21 | 51 | -0.154083 | -28.003 |
| w22 | 41 | -0.040896 | 21.102 |
| w23 | 52 | -0.064562 | -11.226 |
| w24 | 57 | 0.033051 | 15.483 |
| w25 | 36 | 0.04547 | 14.865 |
| w26 | 50 | -0.058751 | -27.772 |
| w27 | 46 | 0.008828 | 4.662 |
| w28 | 57 | -0.123752 | 7.845 |
| w29 | 44 | -0.031027 | 64.832 |
| w30 | 41 | 0.013643 | 7.056 |
| w31 | 52 | 0.04671 | 19.771 |
| w32 | 53 | 0.126516 | 41.732 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 50 | 0.028284 | 43.038 |
| w11 | 41 | 0.021703 | 14.485 |
| w12 | 62 | -0.100955 | -11.896 |
| w13 | 40 | 0.051345 | 48.173 |
| w14 | 49 | -0.12527 | 11.957 |
| w15 | 61 | 0.009036 | -25.37 |
| w16 | 34 | 0.088592 | 97.742 |
| w17 | 51 | 0.025728 | 49.247 |
| w18 | 41 | -0.075935 | -0.146 |
| w19 | 58 | -0.023433 | -16.925 |
| w20 | 59 | -0.089104 | -12.636 |
| w21 | 59 | -0.237303 | 6.321 |
| w22 | 45 | -0.072524 | -2.804 |
| w23 | 45 | -0.043211 | 4.554 |
| w24 | 50 | 0.089276 | 122.677 |
| w25 | 34 | 0.072364 | 13.058 |
| w26 | 61 | -0.164331 | -24.109 |
| w27 | 51 | 0.169556 | 116.863 |
| w28 | 47 | -0.251601 | -46.848 |
| w29 | 50 | -0.030818 | 2.73 |
| w30 | 44 | 0.037145 | 45.669 |
| w31 | 56 | -0.115863 | -8.425 |
| w32 | 57 | 0.048797 | 26.45 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 58 | -0.165028 | -19.163 |
| w13 | 48 | 0.008115 | 21.456 |
| w14 | 52 | -0.091183 | -9.22 |
| w15 | 60 | -0.25284 | -47.267 |
| w16 | 33 | 0.041419 | 75.032 |
| w17 | 46 | -0.018627 | 13.909 |
| w18 | 54 | 0.003415 | -4.036 |
| w19 | 51 | 0.000789 | 6.329 |
| w20 | 56 | 0.117732 | 51.35 |
| w21 | 57 | -0.127742 | -24.939 |
| w22 | 50 | 0.027119 | 6.084 |
| w23 | 59 | -0.062797 | 18.598 |
| w24 | 54 | -0.056496 | -9.13 |
| w25 | 51 | 0.071659 | 18.606 |
| w26 | 46 | -0.08038 | 24.876 |
| w27 | 57 | 0.084641 | 22.154 |
| w28 | 47 | -0.226224 | -31.941 |
| w29 | 67 | -0.106448 | -33.757 |
| w30 | 39 | -0.020508 | 34.122 |
| w31 | 53 | -0.084918 | -24.944 |
| w32 | 60 | -0.063083 | -30.711 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 46 | -0.111713 | -28.609 |
| w16 | 39 | 0.018374 | 58.494 |
| w17 | 58 | -0.101536 | -0.413 |
| w18 | 44 | 0.052042 | 23.333 |
| w19 | 53 | -0.055934 | 19.497 |
| w20 | 52 | -0.04935 | 3.188 |
| w21 | 57 | -0.093361 | -45.919 |
| w22 | 49 | -0.01417 | -9.81 |
| w23 | 46 | -0.092821 | 20.081 |
| w24 | 60 | 0.030925 | 35.434 |
| w25 | 31 | 0.090147 | 14.226 |
| w26 | 51 | -0.165732 | -16.714 |
| w27 | 55 | 0.139942 | 92.043 |
| w28 | 44 | -0.05393 | -3.782 |
| w29 | 51 | 0.008235 | 6.565 |
| w30 | 57 | -0.076647 | 23.012 |
| w31 | 60 | -0.023379 | -23.941 |
| w32 | 64 | -0.092334 | -26.942 |

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
| w15 | 51 | -0.057466 | -18.876 |
| w16 | 42 | -0.067128 | 61.834 |
| w17 | 27 | 0.015003 | 13.73 |
| w18 | 58 | -0.067127 | -17.876 |
| w19 | 57 | -0.059651 | -9.597 |
| w20 | 60 | -0.100845 | -38.85 |
| w21 | 66 | -0.040105 | -2.695 |
| w22 | 58 | -0.105067 | -14.705 |
| w23 | 67 | -0.103268 | -18.385 |
| w24 | 54 | -0.064487 | 30.885 |
| w25 | 43 | 0.084191 | 26.118 |
| w26 | 68 | -0.067309 | -6.021 |
| w27 | 50 | 0.05431 | 198.343 |
| w28 | 55 | -0.11761 | -15.241 |
| w29 | 59 | -0.011199 | 35.984 |
| w30 | 56 | 0.009174 | 2.214 |
| w31 | 69 | -0.040037 | 3.27 |
| w32 | 61 | -0.043875 | -3.155 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 30 | 0.120817 | 66.924 |
| w17 | 52 | -0.040488 | -19.52 |
| w18 | 47 | 0.00266 | 0.069 |
| w19 | 56 | -0.00432 | 1.782 |
| w20 | 55 | 0.001946 | 15.175 |
| w21 | 60 | -0.207506 | -14.634 |
| w22 | 50 | -0.028686 | -2.873 |
| w23 | 56 | -0.036554 | -2.568 |
| w24 | 55 | 0.079305 | 50.896 |
| w25 | 37 | 0.071085 | 7.271 |
| w26 | 56 | -0.063545 | 0.162 |
| w27 | 45 | 0.094264 | 12.026 |
| w28 | 47 | -0.279266 | -18.038 |
| w29 | 63 | -0.032312 | -7.445 |
| w30 | 44 | -0.040758 | -23.155 |
| w31 | 45 | -0.131067 | -31.335 |
| w32 | 44 | -0.005765 | 1.837 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 48 | 0.115139 | 65.464 |
| w21 | 47 | -0.231025 | -22.697 |
| w22 | 41 | -0.034793 | -3.066 |
| w23 | 46 | -0.017701 | 20.327 |
| w24 | 43 | 0.218021 | 261.384 |
| w25 | 40 | 0.022095 | -1.802 |
| w26 | 54 | -0.142373 | -20.608 |
| w27 | 53 | -0.041354 | -0.352 |
| w28 | 47 | -0.088167 | -3.446 |
| w29 | 61 | -0.087319 | -15.885 |
| w30 | 46 | 0.035587 | 11.62 |
| w31 | 52 | -0.050739 | -7.855 |
| w32 | 45 | 0.034172 | 19.525 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 42 | -0.037005 | -3.176 |
| w23 | 57 | -0.023709 | 13.67 |
| w24 | 52 | 0.122734 | 116.921 |
| w25 | 32 | 0.088988 | 34.958 |
| w26 | 50 | -0.04675 | -6.173 |
| w27 | 61 | -0.085099 | -22.216 |
| w28 | 50 | -0.21263 | -10.518 |
| w29 | 60 | -0.035169 | -3.295 |
| w30 | 59 | -0.109227 | -34.956 |
| w31 | 44 | -0.048138 | -11.542 |
| w32 | 51 | 0.040128 | 33.021 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 56 | 0.035565 | 14.696 |
| w25 | 46 | 0.032907 | -4.001 |
| w26 | 53 | -0.136884 | -33.102 |
| w27 | 36 | -0.073143 | 65.435 |
| w28 | 64 | -0.026302 | -7.801 |
| w29 | 40 | -0.007135 | -1.4 |
| w30 | 42 | 0.037202 | 25.269 |
| w31 | 42 | -0.016903 | -4.987 |
| w32 | 60 | -0.042026 | -21.762 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 30 | 0.151251 | 116.056 |
| w6 | 55 | -0.102673 | -7.447 |
| w7 | 51 | -0.011633 | -7.438 |
| w8 | 57 | -0.087774 | -22.501 |
| w9 | 54 | -0.01924 | 15.982 |
| w10 | 49 | -0.028231 | 7.412 |
| w11 | 47 | 0.065838 | 16.063 |
| w12 | 48 | -0.181897 | -14.828 |
| w13 | 29 | 0.08069 | 71.858 |
| w14 | 51 | -0.098794 | 8.546 |
| w15 | 49 | -0.097318 | -16.943 |
| w16 | 56 | -0.19721 | 11.239 |
| w17 | 46 | -0.01048 | 7.426 |
| w18 | 52 | -0.025337 | -7.041 |
| w19 | 53 | 0.008233 | -16.026 |
| w20 | 58 | -0.016225 | -8.293 |
| w21 | 66 | -0.152875 | -10.528 |
| w22 | 62 | -0.076157 | -14.764 |
| w23 | 57 | -0.043249 | -3.295 |
| w24 | 57 | -0.089412 | -21.984 |
| w25 | 35 | 0.084541 | 36.358 |
| w26 | 50 | 0.028651 | 10.369 |
| w27 | 58 | -0.001386 | 15.607 |
| w28 | 43 | -0.13613 | -26.148 |
| w29 | 57 | -0.064687 | -31.261 |
| w30 | 27 | 0.159445 | 310.243 |
| w31 | 47 | 0.026381 | 4.02 |
| w32 | 48 | 0.045556 | 40.43 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 53 | 0.066288 | 131.378 |
| w6 | 26 | 0.066527 | 104.078 |
| w7 | 43 | -0.124375 | -22.297 |
| w8 | 46 | -0.122734 | -17.634 |
| w9 | 49 | 0.003804 | 14.19 |
| w10 | 54 | -0.071455 | 3.399 |
| w11 | 56 | -0.068703 | -7.299 |
| w12 | 64 | -0.079446 | -0.546 |
| w13 | 43 | -0.015807 | 8.399 |
| w14 | 38 | -0.001364 | 34.265 |
| w15 | 47 | -0.059911 | 7.723 |
| w16 | 41 | -0.051227 | 40.464 |
| w17 | 49 | -0.040563 | -5.887 |
| w18 | 56 | -0.119428 | -19.68 |
| w19 | 48 | -0.048835 | -20.765 |
| w20 | 56 | -0.094072 | -16.133 |
| w21 | 65 | -0.155118 | -42.364 |
| w22 | 60 | -0.048698 | -11.249 |
| w23 | 52 | -0.005392 | 1.307 |
| w24 | 64 | -0.087896 | -12.706 |
| w25 | 63 | -0.244948 | -53.262 |
| w26 | 64 | -0.041204 | -2.104 |
| w27 | 65 | -0.031057 | -31.14 |
| w28 | 59 | -0.10015 | -1.363 |
| w29 | 39 | 0.090548 | 32.442 |
| w30 | 71 | -0.170115 | -0.451 |
| w31 | 46 | -0.059668 | -11.882 |
| w32 | 59 | -0.011142 | 38.929 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 59 | -0.123571 | -14.992 |
| w18 | 49 | -0.191971 | -8.45 |
| w19 | 54 | -0.08866 | -20.186 |
| w20 | 57 | 0.031076 | 10.977 |
| w21 | 48 | -0.235361 | -35.311 |
| w22 | 29 | 0.020666 | 13.842 |
| w23 | 56 | -0.052194 | 0.628 |
| w24 | 45 | -0.108015 | -17.622 |
| w25 | 43 | 0.1115 | 40.452 |
| w26 | 56 | -0.109915 | -21.246 |
| w27 | 55 | 0.134767 | 96.078 |
| w28 | 48 | 0.008045 | -0.505 |
| w29 | 45 | 0.045815 | 11.491 |
| w30 | 39 | -0.063002 | 14.656 |
| w31 | 49 | 0.01894 | 12.45 |
| w32 | 61 | 0.031744 | -7.798 |

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
| w17 | 57 | -0.085551 | -24.348 |
| w18 | 54 | -0.066596 | -15.127 |
| w19 | 42 | -0.065357 | -14.865 |
| w20 | 57 | -0.031763 | -14.201 |
| w21 | 55 | -0.179022 | -39.369 |
| w22 | 41 | -0.000934 | 12.992 |
| w23 | 56 | -0.049337 | -22.837 |
| w24 | 48 | -0.081391 | -13.057 |
| w25 | 49 | 0.060507 | 15.824 |
| w26 | 72 | -0.123449 | -35.324 |
| w27 | 55 | 0.000491 | 27.369 |
| w28 | 43 | -0.148419 | -6.444 |
| w29 | 49 | -0.085348 | -7.593 |
| w30 | 74 | -0.126596 | -8.263 |
| w31 | 64 | -0.208137 | -31.247 |
| w32 | 50 | 0.038245 | -24.382 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 46 | -0.034507 | 15.637 |
| w20 | 43 | 0.050076 | 12.604 |
| w21 | 56 | -0.073936 | -17.698 |
| w22 | 36 | 0.037015 | 120.758 |
| w23 | 47 | -0.105869 | -13.958 |
| w24 | 49 | 0.03978 | 157.465 |
| w25 | 42 | 0.005522 | 2.254 |
| w26 | 56 | -0.141489 | -35.551 |
| w27 | 63 | -0.044847 | -21.584 |
| w28 | 49 | -0.144817 | -8.534 |
| w29 | 63 | -0.055958 | -4.074 |
| w30 | 48 | -0.009408 | 31.512 |
| w31 | 50 | -0.02712 | -8.015 |
| w32 | 42 | 0.022359 | 13.453 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 44 | 0.053625 | 20.261 |
| w23 | 58 | -0.102821 | -24.742 |
| w24 | 48 | -0.00831 | -3.793 |
| w25 | 63 | -0.041565 | -10.369 |
| w26 | 56 | -0.049943 | 6.489 |
| w27 | 47 | -0.090366 | -30.037 |
| w28 | 34 | -0.015975 | 2.026 |
| w29 | 58 | -0.068742 | 3.572 |
| w30 | 53 | -0.092837 | -10.998 |
| w31 | 49 | 0.046846 | 14.698 |
| w32 | 44 | 0.023906 | -5.236 |

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
| w27 | 50 | -0.025638 | -1.911 |
| w28 | 44 | -0.087558 | -11.925 |
| w29 | 60 | -0.053647 | -6.109 |
| w30 | 52 | -0.012094 | 1.928 |
| w31 | 44 | -0.072379 | -12.456 |
| w32 | 50 | -0.006917 | 22.492 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 29 | 0.004 | 2.486 |
| w18 | 54 | -0.038886 | 24.471 |
| w19 | 52 | -0.013862 | 7.491 |
| w20 | 37 | 0.079912 | 19.626 |
| w21 | 35 | -0.194156 | -18.382 |
| w22 | 39 | -0.026737 | 5.57 |
| w23 | 50 | -0.069609 | -6.001 |
| w24 | 55 | 0.015513 | 7.7 |
| w25 | 45 | 0.06062 | 2.014 |
| w26 | 45 | -0.147806 | -8.426 |
| w27 | 62 | -0.010818 | -24.658 |
| w28 | 48 | -0.193686 | -12.821 |
| w29 | 61 | -0.085711 | -14.949 |
| w30 | 45 | -0.171637 | -31.561 |
| w31 | 45 | -0.086215 | -9.338 |
| w32 | 51 | -0.057639 | -14.816 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 44 | 0.034599 | 21.807 |
| w18 | 47 | -0.01097 | -13.001 |
| w19 | 47 | -0.069728 | -4.482 |
| w20 | 45 | 0.012197 | 0.892 |
| w21 | 56 | -0.194207 | -6.766 |
| w22 | 29 | 0.086216 | 108.911 |
| w23 | 58 | -0.117809 | -24.464 |
| w24 | 47 | 0.047198 | 40.852 |
| w25 | 28 | 0.158572 | 66.649 |
| w26 | 47 | -0.081786 | -5.619 |
| w27 | 62 | -0.064229 | -15.729 |
| w28 | 39 | -0.137111 | -2.564 |
| w29 | 56 | -0.033469 | -8.58 |
| w30 | 47 | -0.100526 | 3.559 |
| w31 | 50 | -0.136115 | -15.534 |
| w32 | 42 | 0.007263 | 8.382 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 65 | 0.012365 | -0.815 |
| w29 | 44 | -0.015285 | -4.805 |
| w30 | 48 | -0.070621 | -39.125 |
| w31 | 42 | 0.037327 | -0.784 |
| w32 | 48 | -0.052276 | -30.71 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 39 | 0.009524 | -6.756 |
| w15 | 49 | 0.09001 | 73.138 |
| w16 | 18 | -0.014943 | 203.292 |
| w17 | 31 | 0.058698 | 6.313 |
| w18 | 45 | -0.027796 | 0.847 |
| w19 | 59 | -0.071424 | -18.318 |
| w20 | 48 | -0.020573 | -0.293 |
| w21 | 49 | 0.007618 | 11.092 |
| w22 | 56 | -0.096942 | -17.612 |
| w23 | 60 | -0.051991 | -11.307 |
| w24 | 53 | 0.065667 | 38.399 |
| w25 | 35 | 0.181355 | 94.088 |
| w26 | 55 | -0.111996 | -20.067 |
| w27 | 41 | 0.169833 | 177.889 |
| w28 | 42 | -0.066792 | 2.594 |
| w29 | 47 | -0.015819 | 6.406 |
| w30 | 48 | -0.020325 | 7.683 |
| w31 | 48 | -0.014795 | 3.103 |
| w32 | 36 | 0.052279 | 21.297 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 37 | 0.254113 | 184.825 |
| w26 | 45 | -0.044244 | -13.458 |
| w27 | 53 | 0.012746 | 18.103 |
| w28 | 40 | -0.015774 | 11.653 |
| w29 | 41 | 0.018531 | 9.35 |
| w30 | 46 | -0.027891 | 15.122 |
| w31 | 44 | -0.071053 | -21.278 |
| w32 | 54 | 0.051453 | -11.973 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

