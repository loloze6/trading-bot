# Backtest of 034-02_rising-break-swings-continues_1d

- Plan: `../../../../../03_test_plan/night7_rangefail_run/plans/034-02_rising-break-swings-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.028438 | 0.058 |
| w2 | 10 | 0.15552 | 42.345 |
| w3 | 18 | 0.094009 | 34.739 |
| w4 | 22 | -0.065857 | -24.541 |
| w5 | 21 | -0.004243 | 24.338 |
| w6 | 22 | 0.169642 | 65.774 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | -0.047935 | -0.703 |
| w9 | 2 | -0.04986 | -1.623 |
| w10 | 11 | 0.122958 | 12.87 |
| w11 | 18 | 0.048175 | 29.184 |
| w12 | 0 | None | 0.0 |
| w13 | 6 | -0.04521 | 0.462 |
| w14 | 10 | -0.220115 | 3.463 |
| w15 | 16 | 0.053098 | 39.465 |
| w16 | 12 | 0.079031 | 9.014 |
| w17 | 6 | -0.035279 | 0.211 |
| w18 | 11 | -0.05604 | -0.024 |
| w19 | 4 | 0.053566 | 0.697 |
| w20 | 0 | -0.001974 | 0.0 |
| w21 | 0 | -0.041525 | 0.0 |
| w22 | 15 | 0.047242 | 27.891 |
| w23 | 2 | -0.147659 | -2.072 |
| w24 | 13 | 0.143304 | 22.862 |
| w25 | 15 | -0.031538 | 6.294 |
| w26 | 0 | None | 0.0 |
| w27 | 18 | 0.091044 | 5.109 |
| w28 | 2 | -0.011129 | -0.149 |
| w29 | 13 | -0.098384 | -3.537 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | -0.053775 | 1.231 |
| w32 | 5 | 0.131575 | 6.614 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.0768 | 6.27 |
| w2 | 9 | 0.025294 | -4.77 |
| w3 | 1 | -0.114192 | -0.668 |
| w4 | 8 | -0.091278 | 7.452 |
| w5 | 10 | -0.01872 | 12.905 |
| w6 | 15 | 0.189337 | 54.04 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 14 | 0.063165 | 4.456 |
| w11 | 7 | -0.037764 | 4.68 |
| w12 | 0 | None | 0.0 |
| w13 | 6 | -0.052967 | -1.747 |
| w14 | 9 | -0.082143 | 11.025 |
| w15 | 10 | 0.045004 | 9.421 |
| w16 | 14 | 0.002491 | 15.69 |
| w17 | 2 | -0.063834 | -1.881 |
| w18 | 7 | -0.014925 | -11.969 |
| w19 | 2 | -0.07398 | -0.16 |
| w20 | 0 | -0.009839 | 0.0 |
| w21 | 4 | 0.029139 | -17.322 |
| w22 | 8 | -0.087122 | 0.936 |
| w23 | 3 | -0.075767 | -3.603 |
| w24 | 5 | -0.092896 | -7.073 |
| w25 | 5 | -0.019648 | -9.495 |
| w26 | 0 | None | 0.0 |
| w27 | 11 | -0.040043 | 7.777 |
| w28 | 3 | -0.018609 | -2.487 |
| w29 | 7 | 0.00707 | -4.009 |
| w30 | 0 | -0.071878 | 0.0 |
| w31 | 0 | -0.019916 | 0.0 |
| w32 | 4 | -0.114597 | -13.504 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 12 | 0.120333 | 23.225 |
| w7 | 1 | -0.01668 | -1.6 |
| w8 | 0 | None | 0.0 |
| w9 | 4 | 0.070562 | -0.796 |
| w10 | 3 | -0.098662 | 2.496 |
| w11 | 3 | 0.130359 | -1.512 |
| w12 | 3 | -0.175785 | -2.97 |
| w13 | 5 | 0.098843 | -0.711 |
| w14 | 8 | 0.129774 | 18.549 |
| w15 | 4 | 0.223338 | 127.372 |
| w16 | 9 | 0.08757 | 35.618 |
| w17 | 2 | 0.018042 | 7.211 |
| w18 | 3 | -0.268716 | -7.412 |
| w19 | 3 | 0.005638 | -0.427 |
| w20 | 0 | None | 0.0 |
| w21 | 6 | -0.038681 | -7.949 |
| w22 | 5 | -0.205 | -2.578 |
| w23 | 1 | -0.153749 | -1.517 |
| w24 | 9 | 0.117332 | 1.284 |
| w25 | 1 | -0.133584 | -6.828 |
| w26 | 2 | -0.017941 | 1.204 |
| w27 | 11 | 0.357073 | 67.715 |
| w28 | 5 | 0.056351 | 1.29 |
| w29 | 7 | 0.021804 | 6.947 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | 0.337585 | 7.972 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 1 | -0.024848 | -0.695 |
| w8 | 2 | 0.028043 | -1.814 |
| w9 | 1 | -0.014692 | -3.438 |
| w10 | 8 | 0.20228 | 16.192 |
| w11 | 10 | -0.037965 | 0.109 |
| w12 | 0 | None | 0.0 |
| w13 | 8 | -0.08135 | -4.014 |
| w14 | 8 | -0.000572 | 11.394 |
| w15 | 5 | -0.210325 | -12.263 |
| w16 | 14 | 0.064699 | 12.012 |
| w17 | 4 | 0.002869 | -2.872 |
| w18 | 3 | -0.14666 | -9.766 |
| w19 | 2 | -0.07154 | -0.1 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | -0.062442 | 0.0 |
| w22 | 7 | 0.039352 | -3.012 |
| w23 | 5 | 0.129764 | 27.691 |
| w24 | 1 | -0.144007 | -3.66 |
| w25 | 10 | 0.12356 | 20.594 |
| w26 | 1 | 0.03529 | -1.253 |
| w27 | 9 | 0.000566 | -6.507 |
| w28 | 2 | -0.066856 | -0.218 |
| w29 | 18 | -0.291631 | -16.841 |
| w30 | 2 | -0.140304 | -4.235 |
| w31 | 1 | -0.057365 | -1.474 |
| w32 | 3 | 0.157404 | 8.287 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.071672 | 62.401 |
| w2 | 7 | -0.033599 | -5.419 |
| w3 | 2 | 0.026326 | 1.817 |
| w4 | 17 | 0.239292 | 139.734 |
| w5 | 19 | 0.042504 | 43.007 |
| w6 | 15 | 0.20652 | 21.188 |
| w7 | 6 | 0.090798 | 8.96 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 10 | -0.101084 | 3.265 |
| w11 | 9 | 0.104252 | 30.465 |
| w12 | 0 | None | 0.0 |
| w13 | 9 | 0.021272 | 9.355 |
| w14 | 12 | -0.006524 | 49.864 |
| w15 | 11 | -0.044142 | -13.654 |
| w16 | 25 | 0.116269 | 21.894 |
| w17 | 11 | -0.103829 | 11.305 |
| w18 | 14 | -0.049545 | 0.898 |
| w19 | 5 | 0.061314 | 0.635 |
| w20 | 2 | 0.047713 | -0.033 |
| w21 | 1 | 0.023884 | -2.627 |
| w22 | 15 | 0.061869 | 13.174 |
| w23 | 1 | -0.140053 | -2.226 |
| w24 | 10 | -0.082144 | -2.113 |
| w25 | 13 | 0.015985 | 13.712 |
| w26 | 1 | -0.04389 | 0.101 |
| w27 | 7 | -0.033047 | 2.233 |
| w28 | 0 | None | 0.0 |
| w29 | 15 | 0.06278 | 11.075 |
| w30 | 1 | -0.13343 | -3.627 |
| w31 | 1 | -0.106388 | 0.521 |
| w32 | 2 | 0.079987 | 13.802 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 10 | 0.035949 | 18.198 |
| w11 | 2 | 0.071253 | 0.518 |
| w12 | 0 | None | 0.0 |
| w13 | 9 | -0.026705 | -0.53 |
| w14 | 16 | -0.0253 | 47.682 |
| w15 | 8 | 0.16013 | 16.485 |
| w16 | 24 | 0.158088 | 38.248 |
| w17 | 13 | 0.053455 | 25.82 |
| w18 | 0 | -0.00011 | 0.0 |
| w19 | 0 | -0.010647 | 0.0 |
| w20 | 2 | 0.040298 | -1.837 |
| w21 | 0 | 0.001131 | 0.0 |
| w22 | 8 | -0.046694 | 1.37 |
| w23 | 0 | None | 0.0 |
| w24 | 10 | 0.168683 | 55.838 |
| w25 | 4 | 0.058602 | 4.342 |
| w26 | 0 | None | 0.0 |
| w27 | 8 | 0.30274 | 45.168 |
| w28 | 2 | -0.256302 | -4.795 |
| w29 | 5 | -0.037736 | -3.369 |
| w30 | 0 | -0.06537 | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.029346 | -4.774 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 11 | -0.035668 | 1.296 |
| w13 | 3 | -0.034486 | -8.593 |
| w14 | 15 | 0.076078 | 22.466 |
| w15 | 4 | -0.098451 | -3.524 |
| w16 | 15 | 0.028225 | 12.647 |
| w17 | 10 | 0.034572 | -1.271 |
| w18 | 8 | -0.199075 | -1.559 |
| w19 | 2 | -0.18186 | -2.998 |
| w20 | 2 | -0.013593 | -6.259 |
| w21 | 5 | 0.093558 | -9.715 |
| w22 | 8 | -0.117326 | -2.697 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | -0.161376 | 3.372 |
| w25 | 2 | -0.059984 | 3.947 |
| w26 | 0 | None | 0.0 |
| w27 | 8 | 0.011311 | 5.465 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.12082 | 1.219 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | -0.104707 | 0.0 |
| w32 | 2 | -0.089501 | -6.875 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 2 | 0.012126 | -0.827 |
| w16 | 15 | 0.086815 | 16.287 |
| w17 | 3 | 0.06538 | -0.695 |
| w18 | 5 | 0.037863 | 24.433 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | -0.00162 | 0.0 |
| w21 | 5 | 0.039735 | -18.104 |
| w22 | 1 | -0.145131 | -1.248 |
| w23 | 0 | None | 0.0 |
| w24 | 16 | -0.027865 | 5.806 |
| w25 | 3 | 0.06507 | 0.131 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | 0.14754 | 30.568 |
| w28 | 2 | 0.062985 | -0.318 |
| w29 | 4 | -0.025881 | 1.189 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | -0.055302 | -2.53 |
| w32 | 3 | -0.004033 | -6.245 |

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
| w15 | 3 | -0.196927 | -1.037 |
| w16 | 17 | -0.033914 | 32.343 |
| w17 | 3 | 0.038638 | 1.987 |
| w18 | 8 | -0.067838 | -3.113 |
| w19 | 4 | 0.040569 | 2.515 |
| w20 | 2 | -0.226001 | -8.865 |
| w21 | 0 | None | 0.0 |
| w22 | 12 | -0.144394 | -3.117 |
| w23 | 8 | 0.036188 | -13.072 |
| w24 | 14 | 0.009419 | 1.536 |
| w25 | 18 | 0.020046 | 1.924 |
| w26 | 5 | 0.102633 | 12.425 |
| w27 | 12 | 0.041273 | 35.85 |
| w28 | 0 | None | 0.0 |
| w29 | 23 | -0.143808 | -7.618 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | -0.049388 | -2.899 |
| w32 | 11 | 0.04301 | 0.796 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 18 | -0.020026 | 14.332 |
| w17 | 4 | -0.058149 | -12.823 |
| w18 | 11 | -0.04843 | 4.386 |
| w19 | 2 | -0.023893 | -1.662 |
| w20 | 0 | -0.042132 | 0.0 |
| w21 | 0 | 0.013599 | 0.0 |
| w22 | 4 | -0.141533 | -1.971 |
| w23 | 0 | None | 0.0 |
| w24 | 13 | -0.052444 | 12.934 |
| w25 | 7 | 0.025728 | 5.973 |
| w26 | 0 | None | 0.0 |
| w27 | 7 | 0.185535 | 3.803 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | 0.126856 | 2.771 |
| w30 | 1 | -0.064471 | 0.191 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 4 | -0.006597 | -0.042 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | -0.08726 | -1.058 |
| w23 | 0 | None | 0.0 |
| w24 | 16 | 0.100287 | 62.587 |
| w25 | 3 | 0.044066 | 3.728 |
| w26 | 0 | None | 0.0 |
| w27 | 8 | -0.105866 | -1.751 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.047608 | -1.792 |
| w30 | 5 | 0.021017 | 2.695 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | 0.077808 | 0.188 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 6 | -0.177998 | -3.024 |
| w23 | 0 | None | 0.0 |
| w24 | 15 | 0.074734 | 32.685 |
| w25 | 11 | -0.106491 | 11.863 |
| w26 | 3 | -0.0608 | 0.025 |
| w27 | 7 | -0.154015 | 0.53 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | -0.007503 | -1.516 |
| w30 | 1 | -0.023907 | -1.399 |
| w31 | 1 | -0.092589 | 0.406 |
| w32 | 6 | 0.073434 | 14.257 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 7 | -0.093459 | 2.542 |
| w25 | 12 | 0.017046 | 3.341 |
| w26 | 0 | -0.028582 | 0.0 |
| w27 | 28 | 0.061838 | 22.233 |
| w28 | 3 | 0.036956 | -1.298 |
| w29 | 3 | -0.099245 | -2.017 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | 0.126035 | -5.175 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 16 | 0.378464 | 41.312 |
| w6 | 12 | -0.001755 | 8.676 |
| w7 | 1 | -0.10006 | -1.131 |
| w8 | 2 | 0.004164 | -0.207 |
| w9 | 1 | -0.019877 | -1.824 |
| w10 | 5 | 0.129812 | 8.664 |
| w11 | 8 | 0.040629 | 2.52 |
| w12 | 0 | None | 0.0 |
| w13 | 8 | 0.029958 | 3.534 |
| w14 | 9 | -0.111182 | 12.17 |
| w15 | 2 | -0.059831 | 0.952 |
| w16 | 15 | 0.004772 | 22.603 |
| w17 | 5 | -0.003169 | -1.153 |
| w18 | 6 | -0.161651 | -6.07 |
| w19 | 3 | 0.02871 | 1.042 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 5 | -0.028705 | -4.834 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | -0.163752 | -5.217 |
| w25 | 3 | -0.083536 | 1.065 |
| w26 | 6 | 0.131449 | 8.881 |
| w27 | 8 | -0.025121 | 9.101 |
| w28 | 0 | None | 0.0 |
| w29 | 9 | -0.011934 | -0.685 |
| w30 | 22 | 0.061442 | 78.637 |
| w31 | 2 | 0.027319 | 3.086 |
| w32 | 11 | 0.145077 | 39.813 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 10 | -0.000632 | 36.569 |
| w6 | 11 | -0.175095 | -2.918 |
| w7 | 0 | -0.050385 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 9 | 0.131087 | 16.114 |
| w11 | 9 | -0.083399 | 9.003 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | -0.078229 | 0.499 |
| w14 | 14 | -0.207079 | 4.97 |
| w15 | 14 | -0.141895 | -4.158 |
| w16 | 17 | -0.107639 | 10.421 |
| w17 | 6 | 0.049479 | -1.164 |
| w18 | 0 | None | 0.0 |
| w19 | 6 | -0.1025 | -3.871 |
| w20 | 0 | -0.00988 | 0.0 |
| w21 | 2 | -0.242398 | -2.271 |
| w22 | 7 | 0.012274 | -1.045 |
| w23 | 0 | -0.033048 | 0.0 |
| w24 | 9 | -0.072515 | -2.707 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | 0.076692 | 7.19 |
| w27 | 6 | -0.11299 | 10.013 |
| w28 | 7 | 0.115172 | 5.065 |
| w29 | 9 | 0.09887 | 7.72 |
| w30 | 10 | -0.230583 | -9.311 |
| w31 | 6 | 0.190805 | 10.414 |
| w32 | 10 | 0.052704 | 20.759 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 0 | -0.055675 | 0.0 |
| w18 | 12 | 0.039065 | 13.085 |
| w19 | 1 | -0.082348 | -2.182 |
| w20 | 3 | -0.104162 | -0.357 |
| w21 | 1 | -0.035599 | -0.957 |
| w22 | 11 | -0.042647 | 7.622 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | -0.091884 | 2.044 |
| w25 | 5 | -0.216266 | 2.316 |
| w26 | 0 | None | 0.0 |
| w27 | 6 | 0.051943 | 26.046 |
| w28 | 3 | -0.069312 | -0.967 |
| w29 | 8 | 0.003127 | -5.011 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 9 | 0.102967 | -5.757 |

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
| w17 | 6 | -0.269361 | -12.11 |
| w18 | 0 | -0.023676 | 0.0 |
| w19 | 2 | -0.014492 | 0.737 |
| w20 | 2 | -0.052799 | -0.952 |
| w21 | 0 | -0.196589 | 0.0 |
| w22 | 6 | 0.107199 | 6.771 |
| w23 | 0 | 0.003185 | 0.0 |
| w24 | 13 | -0.061834 | -6.841 |
| w25 | 4 | 0.056018 | -0.188 |
| w26 | 5 | -0.032007 | -4.187 |
| w27 | 13 | 0.061284 | 13.957 |
| w28 | 1 | -0.099114 | -2.728 |
| w29 | 17 | 0.012906 | -1.489 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 4 | 0.165168 | 10.389 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 3 | -0.07266 | 0.085 |
| w20 | 1 | -0.068634 | -1.537 |
| w21 | 6 | -0.033516 | -2.411 |
| w22 | 18 | -0.052515 | 20.436 |
| w23 | 3 | -0.048344 | -5.633 |
| w24 | 17 | 0.129212 | 114.089 |
| w25 | 4 | -0.119942 | -7.624 |
| w26 | 3 | -0.06957 | -6.488 |
| w27 | 7 | -0.034192 | -0.327 |
| w28 | 0 | None | 0.0 |
| w29 | 7 | 0.004899 | -0.491 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | -0.006126 | -0.697 |
| w32 | 9 | 0.025122 | 7.442 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 7 | -0.156358 | 1.99 |
| w23 | 1 | -0.064819 | -1.975 |
| w24 | 10 | -0.166292 | -0.666 |
| w25 | 9 | -0.164382 | 1.726 |
| w26 | 0 | -0.051579 | 0.0 |
| w27 | 9 | -0.068941 | -0.749 |
| w28 | 1 | -0.150434 | -4.605 |
| w29 | 9 | 0.094135 | 3.437 |
| w30 | 1 | -0.090884 | -1.652 |
| w31 | 1 | -0.062217 | -5.725 |
| w32 | 2 | -0.125805 | -0.704 |

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
| w27 | 11 | 0.077396 | 6.036 |
| w28 | 1 | -0.033309 | -2.002 |
| w29 | 2 | -0.223127 | -6.602 |
| w30 | 2 | 0.077077 | -1.507 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | 0.133702 | 28.814 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 2 | -0.040595 | -1.032 |
| w18 | 2 | 0.170093 | -3.06 |
| w19 | 3 | 0.132908 | 2.819 |
| w20 | 1 | -0.135553 | -3.18 |
| w21 | 0 | -0.212649 | 0.0 |
| w22 | 7 | -0.039237 | -1.234 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | -0.170219 | -1.203 |
| w25 | 7 | 0.053014 | 2.987 |
| w26 | 0 | None | 0.0 |
| w27 | 9 | -0.024783 | 1.939 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | 0.004061 | -1.681 |
| w30 | 1 | -0.119434 | -6.573 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.126209 | -3.315 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 6 | 0.087666 | 0.575 |
| w18 | 5 | -0.069108 | -3.424 |
| w19 | 2 | -0.020607 | -1.012 |
| w20 | 0 | None | 0.0 |
| w21 | 1 | -0.273999 | -3.924 |
| w22 | 11 | -0.053302 | 26.761 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | -0.150439 | 4.338 |
| w25 | 12 | 0.070257 | 17.426 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | -0.063491 | 7.862 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.030528 | 1.702 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.039739 | -1.274 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 1 | -0.044037 | -0.456 |
| w29 | 2 | 0.023948 | 0.797 |
| w30 | 3 | 0.026939 | -3.813 |
| w31 | 3 | 0.108711 | -0.509 |
| w32 | 5 | -0.096609 | -1.269 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 3 | 0.308028 | 11.163 |
| w15 | 8 | -0.033619 | 3.952 |
| w16 | 13 | 0.142089 | 129.237 |
| w17 | 3 | 0.022772 | -2.127 |
| w18 | 0 | 0.019635 | 0.0 |
| w19 | 1 | -0.330092 | -7.117 |
| w20 | 3 | -0.120293 | -12.15 |
| w21 | 5 | 0.208384 | 44.852 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | -0.145945 | -3.536 |
| w24 | 9 | -0.237861 | -6.471 |
| w25 | 6 | -0.011887 | 25.619 |
| w26 | 2 | -0.049294 | -0.172 |
| w27 | 12 | 0.366469 | 40.563 |
| w28 | 1 | -0.075737 | -1.896 |
| w29 | 5 | -0.037459 | -3.776 |
| w30 | 4 | 0.138055 | 1.593 |
| w31 | 2 | 0.0561 | 1.388 |
| w32 | 5 | -0.007673 | -3.653 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 5 | 0.341875 | 58.372 |
| w26 | 9 | 0.044896 | 5.39 |
| w27 | 8 | 0.160467 | 14.294 |
| w28 | 0 | -0.010209 | 0.0 |
| w29 | 7 | 0.107594 | 7.678 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | -0.036601 | -2.533 |
| w32 | 6 | 0.228374 | 5.679 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

