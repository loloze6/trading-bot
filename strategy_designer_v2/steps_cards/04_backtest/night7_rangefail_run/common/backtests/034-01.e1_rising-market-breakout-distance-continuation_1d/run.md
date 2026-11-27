# Backtest of 034-01.e1_rising-market-breakout-distance-continuation_1d

- Plan: `../../../../../03_test_plan/night7_rangefail_run/plans/034-01.e1_rising-market-breakout-distance-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.028438 | 0.215 |
| w2 | 15 | 0.15552 | 34.975 |
| w3 | 18 | 0.094009 | 20.197 |
| w4 | 24 | -0.065857 | -18.235 |
| w5 | 21 | -0.004243 | 27.17 |
| w6 | 27 | 0.169642 | 44.502 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | -0.047935 | -0.958 |
| w9 | 2 | -0.04986 | -1.178 |
| w10 | 13 | 0.122958 | 8.88 |
| w11 | 23 | 0.048175 | 35.55 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | -0.04521 | 1.32 |
| w14 | 12 | -0.220115 | -8.612 |
| w15 | 24 | 0.053098 | 22.173 |
| w16 | 16 | 0.079031 | 23.735 |
| w17 | 7 | -0.035279 | -1.302 |
| w18 | 12 | -0.05604 | -5.029 |
| w19 | 4 | 0.053566 | 1.201 |
| w20 | 0 | -0.001974 | 0.0 |
| w21 | 0 | -0.041525 | 0.0 |
| w22 | 14 | 0.047242 | 24.154 |
| w23 | 2 | -0.147659 | -1.572 |
| w24 | 12 | 0.143304 | 24.601 |
| w25 | 18 | -0.031538 | 11.942 |
| w26 | 0 | None | 0.0 |
| w27 | 21 | 0.091044 | 6.133 |
| w28 | 2 | -0.011129 | -0.597 |
| w29 | 15 | -0.098384 | -2.269 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | -0.053775 | -0.781 |
| w32 | 5 | 0.131575 | 4.736 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.0768 | 9.025 |
| w2 | 9 | 0.025294 | -3.156 |
| w3 | 1 | -0.114192 | -5.545 |
| w4 | 9 | -0.091278 | 5.928 |
| w5 | 13 | -0.01872 | 0.532 |
| w6 | 17 | 0.189337 | 43.081 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 15 | 0.063165 | 7.719 |
| w11 | 8 | -0.037764 | -2.095 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | -0.052967 | -1.691 |
| w14 | 10 | -0.082143 | 5.252 |
| w15 | 10 | 0.045004 | 7.342 |
| w16 | 21 | 0.002491 | 5.528 |
| w17 | 2 | -0.063834 | -5.777 |
| w18 | 7 | -0.014925 | -6.41 |
| w19 | 2 | -0.07398 | -0.28 |
| w20 | 0 | -0.009839 | 0.0 |
| w21 | 4 | 0.029139 | -2.32 |
| w22 | 10 | -0.087122 | 3.789 |
| w23 | 3 | -0.075767 | -1.478 |
| w24 | 5 | -0.092896 | -8.557 |
| w25 | 5 | -0.019648 | -4.973 |
| w26 | 0 | None | 0.0 |
| w27 | 11 | -0.040043 | -0.477 |
| w28 | 3 | -0.018609 | -2.714 |
| w29 | 6 | 0.00707 | -0.105 |
| w30 | 0 | -0.071878 | 0.0 |
| w31 | 0 | -0.019916 | 0.0 |
| w32 | 4 | -0.114597 | -11.897 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 12 | 0.120333 | 24.467 |
| w7 | 1 | -0.01668 | -0.636 |
| w8 | 0 | None | 0.0 |
| w9 | 4 | 0.070562 | -1.926 |
| w10 | 3 | -0.098662 | 3.031 |
| w11 | 3 | 0.130359 | -2.741 |
| w12 | 2 | -0.175785 | -1.741 |
| w13 | 5 | 0.098843 | 3.294 |
| w14 | 10 | 0.129774 | 17.86 |
| w15 | 7 | 0.223338 | 104.592 |
| w16 | 11 | 0.08757 | 21.568 |
| w17 | 3 | 0.018042 | 5.454 |
| w18 | 3 | -0.268716 | -7.191 |
| w19 | 2 | 0.005638 | -0.101 |
| w20 | 0 | None | 0.0 |
| w21 | 6 | -0.038681 | 5.726 |
| w22 | 4 | -0.205 | -4.453 |
| w23 | 1 | -0.153749 | -2.819 |
| w24 | 7 | 0.117332 | 3.634 |
| w25 | 1 | -0.133584 | -3.094 |
| w26 | 1 | -0.017941 | -0.433 |
| w27 | 12 | 0.357073 | 60.177 |
| w28 | 4 | 0.056351 | 4.401 |
| w29 | 8 | 0.021804 | 4.684 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 3 | 0.337585 | 11.535 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 1 | -0.024848 | -0.254 |
| w8 | 2 | 0.028043 | -1.177 |
| w9 | 1 | -0.014692 | -3.094 |
| w10 | 7 | 0.20228 | 9.938 |
| w11 | 8 | -0.037965 | 2.11 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | -0.08135 | -1.67 |
| w14 | 10 | -0.000572 | 2.227 |
| w15 | 5 | -0.210325 | -9.747 |
| w16 | 14 | 0.064699 | 5.899 |
| w17 | 4 | 0.002869 | -2.578 |
| w18 | 3 | -0.14666 | -8.567 |
| w19 | 1 | -0.07154 | -1.044 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | -0.062442 | 0.0 |
| w22 | 8 | 0.039352 | 1.911 |
| w23 | 6 | 0.129764 | 27.993 |
| w24 | 1 | -0.144007 | -3.161 |
| w25 | 12 | 0.12356 | 19.904 |
| w26 | 1 | 0.03529 | -1.377 |
| w27 | 11 | 0.000566 | -1.89 |
| w28 | 2 | -0.066856 | -0.141 |
| w29 | 18 | -0.291631 | -16.885 |
| w30 | 2 | -0.140304 | -2.384 |
| w31 | 1 | -0.057365 | -1.083 |
| w32 | 3 | 0.157404 | 9.326 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | 0.071672 | 49.856 |
| w2 | 7 | -0.033599 | -4.992 |
| w3 | 2 | 0.026326 | 0.95 |
| w4 | 20 | 0.239292 | 54.845 |
| w5 | 20 | 0.042504 | 36.954 |
| w6 | 16 | 0.20652 | 24.237 |
| w7 | 9 | 0.090798 | 6.91 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 10 | -0.101084 | -1.096 |
| w11 | 11 | 0.104252 | 22.265 |
| w12 | 0 | None | 0.0 |
| w13 | 10 | 0.021272 | 9.994 |
| w14 | 16 | -0.006524 | 33.095 |
| w15 | 14 | -0.044142 | -10.503 |
| w16 | 25 | 0.116269 | 26.686 |
| w17 | 14 | -0.103829 | 12.505 |
| w18 | 12 | -0.049545 | 0.587 |
| w19 | 4 | 0.061314 | 0.562 |
| w20 | 2 | 0.047713 | 0.269 |
| w21 | 1 | 0.023884 | -1.745 |
| w22 | 14 | 0.061869 | 14.276 |
| w23 | 1 | -0.140053 | -1.719 |
| w24 | 13 | -0.082144 | -2.349 |
| w25 | 13 | 0.015985 | 16.165 |
| w26 | 1 | -0.04389 | -0.196 |
| w27 | 7 | -0.033047 | 1.985 |
| w28 | 0 | None | 0.0 |
| w29 | 21 | 0.06278 | 5.232 |
| w30 | 1 | -0.13343 | -1.237 |
| w31 | 2 | -0.106388 | -0.459 |
| w32 | 2 | 0.079987 | 10.949 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 11 | 0.035949 | 6.827 |
| w11 | 2 | 0.071253 | -0.533 |
| w12 | 0 | None | 0.0 |
| w13 | 11 | -0.026705 | 1.311 |
| w14 | 18 | -0.0253 | 29.62 |
| w15 | 9 | 0.16013 | 11.264 |
| w16 | 23 | 0.158088 | 29.561 |
| w17 | 15 | 0.053455 | 18.078 |
| w18 | 0 | -0.00011 | 0.0 |
| w19 | 0 | -0.010647 | 0.0 |
| w20 | 2 | 0.040298 | -0.124 |
| w21 | 0 | 0.001131 | 0.0 |
| w22 | 7 | -0.046694 | 2.163 |
| w23 | 0 | None | 0.0 |
| w24 | 17 | 0.168683 | 19.121 |
| w25 | 4 | 0.058602 | 4.597 |
| w26 | 0 | None | 0.0 |
| w27 | 12 | 0.30274 | 30.575 |
| w28 | 2 | -0.256302 | -2.922 |
| w29 | 5 | -0.037736 | -0.651 |
| w30 | 0 | -0.06537 | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.029346 | -2.209 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 11 | -0.035668 | -1.69 |
| w13 | 3 | -0.034486 | -6.49 |
| w14 | 17 | 0.076078 | 13.409 |
| w15 | 4 | -0.098451 | 1.105 |
| w16 | 17 | 0.028225 | 15.262 |
| w17 | 10 | 0.034572 | 1.937 |
| w18 | 8 | -0.199075 | -4.533 |
| w19 | 2 | -0.18186 | -2.294 |
| w20 | 2 | -0.013593 | -7.441 |
| w21 | 7 | 0.093558 | 0.434 |
| w22 | 8 | -0.117326 | -0.176 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | -0.161376 | -9.016 |
| w25 | 3 | -0.059984 | -0.764 |
| w26 | 0 | None | 0.0 |
| w27 | 8 | 0.011311 | -0.497 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.12082 | 2.367 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | -0.104707 | 0.0 |
| w32 | 2 | -0.089501 | -7.837 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 2 | 0.012126 | -1.24 |
| w16 | 18 | 0.086815 | 23.637 |
| w17 | 4 | 0.06538 | 1.871 |
| w18 | 6 | 0.037863 | 22.634 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | -0.00162 | 0.0 |
| w21 | 6 | 0.039735 | -0.809 |
| w22 | 1 | -0.145131 | -1.106 |
| w23 | 0 | None | 0.0 |
| w24 | 15 | -0.027865 | 5.385 |
| w25 | 6 | 0.06507 | -1.181 |
| w26 | 0 | None | 0.0 |
| w27 | 11 | 0.14754 | 10.675 |
| w28 | 2 | 0.062985 | 0.02 |
| w29 | 5 | -0.025881 | 0.281 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | -0.055302 | -1.294 |
| w32 | 3 | -0.004033 | -2.631 |

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
| w15 | 5 | -0.196927 | -1.755 |
| w16 | 21 | -0.033914 | 21.314 |
| w17 | 4 | 0.038638 | 4.219 |
| w18 | 8 | -0.067838 | -2.552 |
| w19 | 5 | 0.040569 | 4.568 |
| w20 | 2 | -0.226001 | -1.997 |
| w21 | 0 | None | 0.0 |
| w22 | 13 | -0.144394 | -2.415 |
| w23 | 8 | 0.036188 | -6.697 |
| w24 | 14 | 0.009419 | 5.184 |
| w25 | 20 | 0.020046 | 0.937 |
| w26 | 5 | 0.102633 | 7.574 |
| w27 | 16 | 0.041273 | 24.041 |
| w28 | 0 | None | 0.0 |
| w29 | 24 | -0.143808 | -9.567 |
| w30 | 0 | None | 0.0 |
| w31 | 8 | -0.049388 | -3.782 |
| w32 | 17 | 0.04301 | -2.294 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 20 | -0.020026 | 12.63 |
| w17 | 4 | -0.058149 | -4.455 |
| w18 | 10 | -0.04843 | 0.532 |
| w19 | 3 | -0.023893 | -2.234 |
| w20 | 0 | -0.042132 | 0.0 |
| w21 | 0 | 0.013599 | 0.0 |
| w22 | 4 | -0.141533 | -2.06 |
| w23 | 0 | None | 0.0 |
| w24 | 13 | -0.052444 | 2.589 |
| w25 | 8 | 0.025728 | -3.501 |
| w26 | 0 | None | 0.0 |
| w27 | 7 | 0.185535 | 2.842 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | 0.126856 | 3.407 |
| w30 | 1 | -0.064471 | -1.48 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 4 | -0.006597 | 0.408 |
| w21 | 0 | None | 0.0 |
| w22 | 7 | -0.08726 | -1.16 |
| w23 | 0 | None | 0.0 |
| w24 | 17 | 0.100287 | 29.849 |
| w25 | 4 | 0.044066 | 2.581 |
| w26 | 0 | None | 0.0 |
| w27 | 7 | -0.105866 | -5.798 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.047608 | -0.151 |
| w30 | 5 | 0.021017 | 1.161 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | 0.077808 | 3.702 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 5 | -0.177998 | -1.839 |
| w23 | 0 | None | 0.0 |
| w24 | 16 | 0.074734 | 23.907 |
| w25 | 12 | -0.106491 | 0.48 |
| w26 | 3 | -0.0608 | -2.292 |
| w27 | 7 | -0.154015 | -4.993 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | -0.007503 | 0.704 |
| w30 | 1 | -0.023907 | -1.108 |
| w31 | 1 | -0.092589 | -0.126 |
| w32 | 6 | 0.073434 | 14.794 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 7 | -0.093459 | 3.971 |
| w25 | 14 | 0.017046 | 3.226 |
| w26 | 0 | -0.028582 | 0.0 |
| w27 | 28 | 0.061838 | 15.162 |
| w28 | 3 | 0.036956 | -0.521 |
| w29 | 3 | -0.099245 | -1.51 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | 0.126035 | 2.407 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 15 | 0.378464 | 55.986 |
| w6 | 15 | -0.001755 | 3.748 |
| w7 | 1 | -0.10006 | -0.836 |
| w8 | 2 | 0.004164 | 0.204 |
| w9 | 1 | -0.019877 | -1.161 |
| w10 | 5 | 0.129812 | 5.254 |
| w11 | 8 | 0.040629 | 0.732 |
| w12 | 0 | None | 0.0 |
| w13 | 8 | 0.029958 | 9.829 |
| w14 | 14 | -0.111182 | -5.926 |
| w15 | 2 | -0.059831 | -0.657 |
| w16 | 19 | 0.004772 | 17.02 |
| w17 | 3 | -0.003169 | -1.216 |
| w18 | 6 | -0.161651 | -5.024 |
| w19 | 3 | 0.02871 | 0.067 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 5 | -0.028705 | -2.322 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | -0.163752 | -6.231 |
| w25 | 3 | -0.083536 | -3.242 |
| w26 | 8 | 0.131449 | 7.159 |
| w27 | 9 | -0.025121 | 7.076 |
| w28 | 0 | None | 0.0 |
| w29 | 9 | -0.011934 | 5.509 |
| w30 | 29 | 0.061442 | 59.384 |
| w31 | 3 | 0.027319 | 4.599 |
| w32 | 14 | 0.145077 | 40.048 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 13 | -0.000632 | 18.293 |
| w6 | 14 | -0.175095 | 1.106 |
| w7 | 0 | -0.050385 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 9 | 0.131087 | 10.495 |
| w11 | 11 | -0.083399 | -6.486 |
| w12 | 0 | None | 0.0 |
| w13 | 10 | -0.078229 | 3.649 |
| w14 | 17 | -0.207079 | -0.996 |
| w15 | 15 | -0.141895 | -6.26 |
| w16 | 21 | -0.107639 | 3.341 |
| w17 | 6 | 0.049479 | 1.262 |
| w18 | 0 | None | 0.0 |
| w19 | 6 | -0.1025 | -0.146 |
| w20 | 0 | -0.00988 | 0.0 |
| w21 | 2 | -0.242398 | -2.685 |
| w22 | 9 | 0.012274 | 2.086 |
| w23 | 0 | -0.033048 | 0.0 |
| w24 | 9 | -0.072515 | -2.507 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | 0.076692 | 5.231 |
| w27 | 6 | -0.11299 | 1.552 |
| w28 | 6 | 0.115172 | 3.444 |
| w29 | 11 | 0.09887 | 8.966 |
| w30 | 10 | -0.230583 | -8.786 |
| w31 | 6 | 0.190805 | 17.075 |
| w32 | 13 | 0.052704 | 16.504 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 0 | -0.055675 | 0.0 |
| w18 | 12 | 0.039065 | 11.348 |
| w19 | 2 | -0.082348 | -1.006 |
| w20 | 2 | -0.104162 | -0.313 |
| w21 | 1 | -0.035599 | -0.962 |
| w22 | 13 | -0.042647 | 5.623 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | -0.091884 | 0.142 |
| w25 | 5 | -0.216266 | 3.763 |
| w26 | 0 | None | 0.0 |
| w27 | 11 | 0.051943 | 17.708 |
| w28 | 3 | -0.069312 | -0.563 |
| w29 | 8 | 0.003127 | -0.803 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 10 | 0.102967 | 5.941 |

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
| w17 | 7 | -0.269361 | -5.842 |
| w18 | 0 | -0.023676 | 0.0 |
| w19 | 2 | -0.014492 | 2.634 |
| w20 | 2 | -0.052799 | -0.311 |
| w21 | 0 | -0.196589 | 0.0 |
| w22 | 8 | 0.107199 | 6.608 |
| w23 | 0 | 0.003185 | 0.0 |
| w24 | 15 | -0.061834 | -3.02 |
| w25 | 3 | 0.056018 | -1.644 |
| w26 | 5 | -0.032007 | -5.195 |
| w27 | 13 | 0.061284 | 7.862 |
| w28 | 1 | -0.099114 | -1.802 |
| w29 | 16 | 0.012906 | 1.347 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 4 | 0.165168 | 14.335 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 3 | -0.07266 | -0.115 |
| w20 | 1 | -0.068634 | -2.513 |
| w21 | 9 | -0.033516 | 0.574 |
| w22 | 19 | -0.052515 | 16.491 |
| w23 | 5 | -0.048344 | -3.158 |
| w24 | 23 | 0.129212 | 54.402 |
| w25 | 4 | -0.119942 | -5.413 |
| w26 | 3 | -0.06957 | -3.008 |
| w27 | 5 | -0.034192 | 0.796 |
| w28 | 0 | None | 0.0 |
| w29 | 9 | 0.004899 | 1.259 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | -0.006126 | 0.081 |
| w32 | 12 | 0.025122 | 7.142 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 4 | -0.156358 | -0.842 |
| w23 | 1 | -0.064819 | -2.229 |
| w24 | 11 | -0.166292 | -5.139 |
| w25 | 8 | -0.164382 | -7.147 |
| w26 | 0 | -0.051579 | 0.0 |
| w27 | 9 | -0.068941 | -2.288 |
| w28 | 1 | -0.150434 | -3.346 |
| w29 | 9 | 0.094135 | 6.237 |
| w30 | 1 | -0.090884 | -0.66 |
| w31 | 1 | -0.062217 | -8.075 |
| w32 | 2 | -0.125805 | -0.465 |

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
| w27 | 11 | 0.077396 | 6.875 |
| w28 | 1 | -0.033309 | -2.923 |
| w29 | 2 | -0.223127 | -5.232 |
| w30 | 2 | 0.077077 | -0.778 |
| w31 | 0 | None | 0.0 |
| w32 | 8 | 0.133702 | 37.767 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 2 | -0.040595 | -0.661 |
| w18 | 2 | 0.170093 | -5.162 |
| w19 | 2 | 0.132908 | 3.314 |
| w20 | 1 | -0.135553 | -3.724 |
| w21 | 0 | -0.212649 | 0.0 |
| w22 | 6 | -0.039237 | 2.898 |
| w23 | 0 | None | 0.0 |
| w24 | 18 | -0.170219 | 0.487 |
| w25 | 9 | 0.053014 | 3.225 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | -0.024783 | 2.247 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | 0.004061 | 0.4 |
| w30 | 1 | -0.119434 | -4.546 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.126209 | 1.398 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 7 | 0.087666 | 2.969 |
| w18 | 5 | -0.069108 | -3.001 |
| w19 | 2 | -0.020607 | -1.315 |
| w20 | 0 | None | 0.0 |
| w21 | 1 | -0.273999 | -3.992 |
| w22 | 16 | -0.053302 | 27.693 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | -0.150439 | -0.801 |
| w25 | 12 | 0.070257 | 12.554 |
| w26 | 0 | None | 0.0 |
| w27 | 11 | -0.063491 | -1.363 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.030528 | 1.085 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.039739 | -0.303 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 1 | -0.044037 | -0.456 |
| w29 | 2 | 0.023948 | 2.441 |
| w30 | 3 | 0.026939 | -4.772 |
| w31 | 3 | 0.108711 | -0.438 |
| w32 | 5 | -0.096609 | -1.408 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 4 | 0.308028 | 11.2 |
| w15 | 8 | -0.033619 | 4.578 |
| w16 | 14 | 0.142089 | 133.212 |
| w17 | 4 | 0.022772 | -1.272 |
| w18 | 0 | 0.019635 | 0.0 |
| w19 | 1 | -0.330092 | -8.7 |
| w20 | 4 | -0.120293 | -5.869 |
| w21 | 6 | 0.208384 | 48.557 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | -0.145945 | -4.36 |
| w24 | 10 | -0.237861 | -13.662 |
| w25 | 9 | -0.011887 | 22.861 |
| w26 | 1 | -0.049294 | -0.274 |
| w27 | 14 | 0.366469 | 39.564 |
| w28 | 1 | -0.075737 | -2.188 |
| w29 | 5 | -0.037459 | -0.167 |
| w30 | 4 | 0.138055 | 1.523 |
| w31 | 2 | 0.0561 | 1.388 |
| w32 | 5 | -0.007673 | -3.727 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 7 | 0.341875 | 27.818 |
| w26 | 9 | 0.044896 | 3.917 |
| w27 | 9 | 0.160467 | 15.895 |
| w28 | 0 | -0.010209 | 0.0 |
| w29 | 5 | 0.107594 | 3.668 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | -0.036601 | -1.481 |
| w32 | 6 | 0.228374 | 12.078 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

