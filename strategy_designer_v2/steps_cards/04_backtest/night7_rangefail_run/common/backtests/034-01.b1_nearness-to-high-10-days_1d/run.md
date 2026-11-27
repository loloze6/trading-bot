# Backtest of 034-01.b1_nearness-to-high-10-days_1d

- Plan: `../../../../../03_test_plan/night7_rangefail_run/plans/034-01.b1_nearness-to-high-10-days_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.190261 | 4.321 |
| w2 | 21 | 0.213062 | 34.085 |
| w3 | 22 | 0.021136 | 61.426 |
| w4 | 29 | 0.058203 | -28.923 |
| w5 | 34 | 0.027637 | 56.017 |
| w6 | 25 | 0.176938 | 74.468 |
| w7 | 3 | -0.045887 | 1.466 |
| w8 | 4 | -0.031394 | -6.153 |
| w9 | 1 | -0.062283 | -5.177 |
| w10 | 13 | 0.10381 | 21.014 |
| w11 | 33 | 0.003187 | 2.44 |
| w12 | 1 | -0.008497 | -3.587 |
| w13 | 8 | -0.004024 | 6.59 |
| w14 | 23 | -0.247198 | 1.87 |
| w15 | 16 | 0.077716 | 81.575 |
| w16 | 32 | 0.077955 | 9.034 |
| w17 | 4 | 0.018235 | 7.209 |
| w18 | 16 | 0.070938 | 6.362 |
| w19 | 5 | 0.0781 | 0.968 |
| w20 | 2 | 0.020465 | -3.566 |
| w21 | 3 | -0.018033 | -12.754 |
| w22 | 24 | -0.036281 | 30.623 |
| w23 | 14 | -0.054469 | 1.53 |
| w24 | 18 | 0.009935 | 34.307 |
| w25 | 30 | -0.004126 | 25.107 |
| w26 | 0 | None | 0.0 |
| w27 | 18 | 0.058298 | 34.971 |
| w28 | 10 | -0.096644 | -4.287 |
| w29 | 24 | -0.011385 | -3.116 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | -0.03775 | 1.36 |
| w32 | 7 | 0.139619 | 16.268 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.046503 | -4.404 |
| w2 | 15 | 0.119862 | -16.771 |
| w3 | 3 | -0.138777 | -5.822 |
| w4 | 11 | -0.06402 | 5.944 |
| w5 | 32 | 0.019954 | 14.088 |
| w6 | 21 | 0.153693 | 71.002 |
| w7 | 5 | -0.015407 | -1.653 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 17 | 0.019796 | 22.442 |
| w11 | 19 | 0.041638 | 3.381 |
| w12 | 0 | None | 0.0 |
| w13 | 10 | 0.074857 | 10.238 |
| w14 | 16 | -0.103693 | 4.723 |
| w15 | 15 | 0.003582 | 8.989 |
| w16 | 27 | 0.041325 | -0.488 |
| w17 | 5 | 0.001956 | -10.119 |
| w18 | 18 | 0.096362 | 0.96 |
| w19 | 3 | -0.007483 | -1.957 |
| w20 | 1 | 0.02938 | -1.763 |
| w21 | 14 | -0.020477 | -9.726 |
| w22 | 14 | 0.000346 | 9.666 |
| w23 | 8 | -0.090588 | -4.128 |
| w24 | 14 | -0.047028 | -10.234 |
| w25 | 10 | -0.097145 | -3.033 |
| w26 | 0 | None | 0.0 |
| w27 | 13 | -0.01437 | 21.279 |
| w28 | 10 | -0.141898 | -5.26 |
| w29 | 14 | -0.074551 | -4.648 |
| w30 | 4 | -0.115685 | -1.955 |
| w31 | 1 | -0.019916 | -1.172 |
| w32 | 7 | -0.146229 | -22.047 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 22 | 0.190733 | 46.086 |
| w7 | 7 | 0.070288 | -0.912 |
| w8 | 2 | -0.021343 | -1.657 |
| w9 | 15 | -0.073646 | -3.527 |
| w10 | 3 | -0.15187 | -7.876 |
| w11 | 12 | 0.043108 | -2.397 |
| w12 | 5 | -0.106119 | -3.31 |
| w13 | 6 | 0.142798 | 16.955 |
| w14 | 16 | 0.086571 | 12.136 |
| w15 | 14 | 0.286899 | 143.013 |
| w16 | 19 | 0.071801 | 24.006 |
| w17 | 8 | -0.123803 | 7.389 |
| w18 | 14 | 0.00182 | -4.79 |
| w19 | 5 | 0.017461 | -1.85 |
| w20 | 2 | 0.013341 | -1.773 |
| w21 | 14 | -0.021513 | 8.884 |
| w22 | 15 | -0.155542 | 3.88 |
| w23 | 7 | -0.025578 | -0.621 |
| w24 | 15 | 0.084321 | 6.328 |
| w25 | 6 | -0.207659 | 0.022 |
| w26 | 7 | -0.109008 | -1.305 |
| w27 | 12 | 0.369572 | 112.547 |
| w28 | 9 | 0.00746 | 2.062 |
| w29 | 17 | -0.067305 | 1.447 |
| w30 | 4 | -0.079625 | -2.39 |
| w31 | 0 | None | 0.0 |
| w32 | 3 | 0.208331 | 4.912 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 7 | -0.084022 | 3.223 |
| w8 | 11 | 0.016929 | 0.714 |
| w9 | 1 | -0.059742 | -13.579 |
| w10 | 9 | 0.158599 | 23.037 |
| w11 | 18 | -0.076165 | -2.87 |
| w12 | 0 | None | 0.0 |
| w13 | 9 | 0.05947 | 3.564 |
| w14 | 14 | -0.102023 | -1.72 |
| w15 | 11 | -0.049392 | -1.472 |
| w16 | 30 | 0.096836 | 22.145 |
| w17 | 6 | -0.075687 | -4.798 |
| w18 | 12 | -0.037784 | -7.076 |
| w19 | 4 | -0.027354 | -1.951 |
| w20 | 2 | -0.000842 | -2.21 |
| w21 | 7 | -0.192322 | -7.946 |
| w22 | 18 | 0.017772 | 10.717 |
| w23 | 12 | 0.228494 | 52.212 |
| w24 | 12 | -0.137685 | -8.18 |
| w25 | 15 | 0.137068 | 15.721 |
| w26 | 4 | 0.059183 | -1.163 |
| w27 | 14 | 0.070341 | 12.421 |
| w28 | 4 | -0.093305 | 0.361 |
| w29 | 27 | -0.272466 | 5.622 |
| w30 | 7 | -0.109715 | -3.892 |
| w31 | 4 | 0.090501 | 1.131 |
| w32 | 3 | 0.201708 | 6.067 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | 0.184653 | 94.479 |
| w2 | 13 | 0.02089 | -2.587 |
| w3 | 6 | -0.007642 | 5.496 |
| w4 | 24 | 0.146474 | 161.323 |
| w5 | 18 | 0.179492 | 68.413 |
| w6 | 21 | 0.114381 | 28.097 |
| w7 | 9 | 0.086551 | 3.118 |
| w8 | 6 | -0.082787 | -1.589 |
| w9 | 1 | -0.034572 | -4.011 |
| w10 | 18 | -0.083121 | 0.671 |
| w11 | 16 | 0.083617 | 22.447 |
| w12 | 2 | -0.043994 | -1.293 |
| w13 | 10 | 0.161654 | 24.007 |
| w14 | 21 | -0.046085 | 30.477 |
| w15 | 21 | -0.017248 | 6.778 |
| w16 | 26 | -0.002086 | 27.317 |
| w17 | 15 | -0.009029 | 1.308 |
| w18 | 19 | -0.079245 | -3.515 |
| w19 | 9 | 0.093028 | 2.378 |
| w20 | 3 | -0.000109 | -2.794 |
| w21 | 6 | -0.053878 | -6.137 |
| w22 | 19 | -0.045024 | 7.062 |
| w23 | 5 | -0.159544 | -3.841 |
| w24 | 17 | -0.122369 | 6.103 |
| w25 | 18 | 0.092109 | 20.289 |
| w26 | 9 | -0.038396 | -1.485 |
| w27 | 10 | 0.052772 | 10.35 |
| w28 | 3 | -0.148577 | 0.235 |
| w29 | 25 | -0.010098 | 19.454 |
| w30 | 9 | -0.064505 | -3.921 |
| w31 | 3 | -0.074898 | -0.179 |
| w32 | 7 | 0.168893 | 18.082 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 16 | 0.081176 | 25.221 |
| w11 | 10 | -0.017764 | -0.439 |
| w12 | 0 | None | 0.0 |
| w13 | 8 | 0.12031 | 14.46 |
| w14 | 20 | -0.028626 | 21.175 |
| w15 | 14 | 0.051872 | 22.086 |
| w16 | 35 | 0.138606 | 42.579 |
| w17 | 15 | 0.029639 | 28.815 |
| w18 | 7 | -0.086773 | -1.042 |
| w19 | 4 | 0.019479 | -3.75 |
| w20 | 4 | 0.049156 | -3.503 |
| w21 | 1 | -0.053787 | -2.412 |
| w22 | 11 | 0.022457 | -2.933 |
| w23 | 6 | 0.047756 | 1.629 |
| w24 | 12 | 0.121129 | 72.133 |
| w25 | 12 | 0.000771 | 3.275 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | 0.33293 | 81.586 |
| w28 | 10 | -0.223662 | -6.835 |
| w29 | 16 | -0.096403 | -4.435 |
| w30 | 8 | -0.11934 | -1.782 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | 0.022853 | -5.519 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 18 | -0.066627 | -2.527 |
| w13 | 8 | -0.066522 | -10.539 |
| w14 | 26 | 0.040635 | 26.27 |
| w15 | 11 | 0.083714 | 4.598 |
| w16 | 24 | 0.032058 | 20.003 |
| w17 | 11 | 0.032512 | 12.855 |
| w18 | 13 | -0.163914 | 10.382 |
| w19 | 11 | -0.183227 | -7.654 |
| w20 | 9 | -0.01898 | -1.741 |
| w21 | 10 | -0.003378 | -2.785 |
| w22 | 9 | -0.026423 | 9.333 |
| w23 | 0 | None | 0.0 |
| w24 | 14 | -0.185164 | 15.452 |
| w25 | 7 | 0.096328 | 4.708 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | 0.161601 | 34.14 |
| w28 | 4 | -0.215647 | -0.936 |
| w29 | 7 | -0.010232 | -1.123 |
| w30 | 0 | -0.058284 | 0.0 |
| w31 | 3 | -0.018936 | -3.627 |
| w32 | 5 | 0.023057 | -4.509 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 8 | 0.057403 | 2.87 |
| w16 | 22 | 0.090211 | 34.31 |
| w17 | 8 | -0.114674 | 0.466 |
| w18 | 19 | -0.106501 | 20.715 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.002299 | -3.23 |
| w21 | 7 | 0.017753 | -17.266 |
| w22 | 6 | 0.029847 | 2.911 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | -0.02169 | 35.562 |
| w25 | 8 | 0.096708 | 6.427 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | 0.184151 | 58.651 |
| w28 | 5 | -0.107492 | -2.194 |
| w29 | 14 | -0.104425 | -3.649 |
| w30 | 2 | -0.075831 | -1.136 |
| w31 | 3 | -0.1666 | -5.732 |
| w32 | 7 | -0.053645 | -4.995 |

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
| w15 | 14 | -0.109345 | -7.458 |
| w16 | 25 | 0.003984 | 39.042 |
| w17 | 10 | -0.009709 | 5.444 |
| w18 | 14 | -0.083501 | -2.781 |
| w19 | 6 | 0.074236 | -4.499 |
| w20 | 9 | -0.037204 | -0.944 |
| w21 | 0 | None | 0.0 |
| w22 | 14 | -0.094216 | 16.75 |
| w23 | 22 | -0.081249 | -16.369 |
| w24 | 25 | -0.111074 | -8.406 |
| w25 | 15 | 0.168725 | 21.293 |
| w26 | 8 | 0.187733 | -20.786 |
| w27 | 21 | 0.092316 | 49.244 |
| w28 | 9 | -0.126457 | -0.327 |
| w29 | 25 | -0.077191 | 17.579 |
| w30 | 4 | -0.001174 | -3.139 |
| w31 | 8 | -0.044716 | -4.861 |
| w32 | 14 | 0.134257 | -19.739 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 31 | 0.025286 | 29.231 |
| w17 | 7 | -0.042377 | -9.853 |
| w18 | 15 | -0.034892 | 5.756 |
| w19 | 4 | 0.049505 | 1.389 |
| w20 | 1 | -0.037772 | -5.197 |
| w21 | 1 | -0.08487 | -4.563 |
| w22 | 12 | -0.080262 | -1.764 |
| w23 | 2 | 0.035365 | 3.237 |
| w24 | 12 | -0.053878 | 24.522 |
| w25 | 12 | 0.025529 | 4.857 |
| w26 | 0 | None | 0.0 |
| w27 | 7 | 0.19088 | 27.57 |
| w28 | 5 | -0.258076 | 0.011 |
| w29 | 7 | -0.026223 | -0.546 |
| w30 | 7 | -0.149036 | 0.156 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 5 | 0.075802 | -0.078 |
| w21 | 2 | 0.043067 | -1.304 |
| w22 | 14 | -0.019844 | -0.803 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | 0.209013 | 74.503 |
| w25 | 16 | 0.081539 | 8.805 |
| w26 | 0 | None | 0.0 |
| w27 | 17 | 0.009905 | -9.07 |
| w28 | 6 | -0.195033 | -0.578 |
| w29 | 13 | -0.186031 | -11.117 |
| w30 | 14 | 0.170097 | -0.089 |
| w31 | 2 | 0.019669 | -0.451 |
| w32 | 2 | 0.058387 | -2.095 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 10 | -0.077985 | 1.732 |
| w23 | 1 | 0.028862 | 4.028 |
| w24 | 13 | 0.079609 | 13.825 |
| w25 | 16 | 0.04436 | 25.793 |
| w26 | 8 | -0.030184 | 5.706 |
| w27 | 15 | 0.092049 | 7.937 |
| w28 | 3 | -0.195172 | 0.186 |
| w29 | 11 | -0.062145 | -5.501 |
| w30 | 7 | -0.07424 | -10.471 |
| w31 | 8 | -0.037661 | -3.296 |
| w32 | 17 | 0.049071 | 16.695 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 12 | -0.127758 | -9.999 |
| w25 | 15 | -0.000928 | 7.724 |
| w26 | 1 | -0.114195 | -2.747 |
| w27 | 33 | 0.007777 | 1.143 |
| w28 | 7 | 0.020558 | 5.143 |
| w29 | 12 | -0.023586 | -2.149 |
| w30 | 2 | -0.066404 | -2.095 |
| w31 | 1 | 0.010791 | -2.063 |
| w32 | 7 | 0.098779 | -6.287 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 18 | 0.271451 | 57.422 |
| w6 | 19 | 0.06655 | 15.696 |
| w7 | 9 | 0.005413 | 1.67 |
| w8 | 7 | 0.041529 | -1.891 |
| w9 | 1 | -0.047768 | -6.749 |
| w10 | 7 | 0.17528 | 6.411 |
| w11 | 18 | 0.071257 | 16.064 |
| w12 | 0 | None | 0.0 |
| w13 | 6 | 0.181903 | 15.173 |
| w14 | 18 | -0.151718 | 15.287 |
| w15 | 6 | -0.060229 | -1.313 |
| w16 | 31 | 0.047362 | 11.817 |
| w17 | 9 | 0.090949 | -9.363 |
| w18 | 16 | 0.021553 | -2.776 |
| w19 | 9 | 0.060913 | 4.992 |
| w20 | 4 | 0.053821 | -0.593 |
| w21 | 1 | -0.029239 | -1.953 |
| w22 | 9 | 0.0351 | -0.059 |
| w23 | 3 | 0.029958 | 3.215 |
| w24 | 13 | -0.115121 | 0.195 |
| w25 | 10 | 0.10109 | 2.684 |
| w26 | 12 | 0.15069 | 13.292 |
| w27 | 13 | -0.029436 | 1.366 |
| w28 | 4 | -0.071703 | 0.761 |
| w29 | 14 | 0.041859 | -8.216 |
| w30 | 21 | 0.115491 | 142.376 |
| w31 | 6 | 0.063954 | 0.875 |
| w32 | 24 | 0.086982 | 36.365 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 27 | 0.107459 | 45.047 |
| w6 | 18 | 0.038346 | 32.152 |
| w7 | 6 | -0.08706 | 3.924 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | -0.061984 | -1.415 |
| w10 | 13 | 0.026341 | 14.412 |
| w11 | 22 | -0.050362 | -5.644 |
| w12 | 0 | None | 0.0 |
| w13 | 10 | 0.043028 | 8.073 |
| w14 | 25 | -0.227956 | 18.943 |
| w15 | 24 | -0.128363 | 11.655 |
| w16 | 25 | -0.046472 | 17.134 |
| w17 | 8 | 0.155151 | -0.69 |
| w18 | 11 | -0.001888 | -4.357 |
| w19 | 9 | 0.012924 | -0.667 |
| w20 | 4 | 0.026777 | 0.605 |
| w21 | 5 | -0.156467 | -0.459 |
| w22 | 13 | 0.045249 | 13.009 |
| w23 | 6 | 0.100665 | 2.633 |
| w24 | 18 | -0.091938 | -14.551 |
| w25 | 0 | -0.077008 | 0.0 |
| w26 | 11 | -0.00027 | 5.121 |
| w27 | 8 | -0.121451 | 9.245 |
| w28 | 18 | -0.058438 | 3.254 |
| w29 | 17 | 0.160743 | 5.58 |
| w30 | 19 | -0.221655 | -5.424 |
| w31 | 9 | 0.172538 | -8.607 |
| w32 | 15 | 0.031662 | 26.307 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 9 | -0.267012 | -5.642 |
| w18 | 22 | -0.074859 | -7.494 |
| w19 | 5 | -0.08978 | -3.184 |
| w20 | 7 | -0.109944 | -4.995 |
| w21 | 2 | -0.004697 | 0.087 |
| w22 | 16 | -0.015821 | 9.922 |
| w23 | 0 | None | 0.0 |
| w24 | 10 | -0.086361 | -1.866 |
| w25 | 7 | 0.027044 | 10.815 |
| w26 | 1 | -0.075027 | -1.531 |
| w27 | 15 | 0.147484 | 47.56 |
| w28 | 13 | -0.035023 | 0.899 |
| w29 | 19 | -0.080468 | -2.489 |
| w30 | 3 | -0.116598 | -2.413 |
| w31 | 0 | None | 0.0 |
| w32 | 9 | 0.084715 | 0.052 |

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
| w17 | 11 | -0.148523 | -13.091 |
| w18 | 4 | -0.109423 | -6.299 |
| w19 | 6 | 0.050464 | -3.263 |
| w20 | 7 | 0.00448 | 0.201 |
| w21 | 6 | -0.09238 | -13.599 |
| w22 | 14 | 0.028291 | 11.637 |
| w23 | 6 | 0.111085 | 1.271 |
| w24 | 20 | -0.17503 | -6.901 |
| w25 | 10 | 0.053336 | -0.466 |
| w26 | 12 | -0.013826 | -11.714 |
| w27 | 25 | -0.040897 | -0.905 |
| w28 | 10 | -0.084268 | 0.309 |
| w29 | 26 | 0.016965 | -7.798 |
| w30 | 0 | -0.107821 | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 9 | 0.101072 | 6.064 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 3 | -0.021249 | -1.238 |
| w20 | 4 | -0.13163 | -4.234 |
| w21 | 13 | -0.034901 | -12.586 |
| w22 | 25 | -0.026167 | 52.949 |
| w23 | 17 | -0.069513 | -7.779 |
| w24 | 22 | 0.137119 | 105.257 |
| w25 | 19 | -0.172039 | -4.086 |
| w26 | 3 | -0.085367 | -11.666 |
| w27 | 16 | 0.109277 | -4.11 |
| w28 | 4 | -0.193063 | -1.192 |
| w29 | 17 | -0.024887 | 0.901 |
| w30 | 5 | -0.025173 | -1.673 |
| w31 | 2 | -0.006095 | -1.493 |
| w32 | 14 | 0.071229 | 20.126 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 17 | -0.032998 | 3.883 |
| w23 | 2 | -0.088535 | -1.558 |
| w24 | 14 | -0.200318 | 5.574 |
| w25 | 20 | -0.040743 | -6.846 |
| w26 | 6 | -0.108584 | -4.944 |
| w27 | 11 | -0.049793 | 3.227 |
| w28 | 13 | -0.222893 | -8.222 |
| w29 | 16 | -0.038764 | -13.986 |
| w30 | 7 | -0.178794 | -3.938 |
| w31 | 2 | -0.18023 | -3.164 |
| w32 | 9 | 0.032422 | -16.831 |

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
| w27 | 11 | 0.128041 | 20.768 |
| w28 | 6 | 0.006061 | -0.328 |
| w29 | 16 | -0.179956 | -13.738 |
| w30 | 6 | -0.008433 | -7.364 |
| w31 | 0 | -0.128754 | 0.0 |
| w32 | 14 | 0.005643 | 11.971 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 8 | 0.172932 | 5.47 |
| w18 | 7 | 0.107016 | -1.869 |
| w19 | 3 | 0.039942 | -3.037 |
| w20 | 4 | -0.07133 | -4.259 |
| w21 | 4 | -0.100497 | -8.368 |
| w22 | 17 | -0.037973 | 0.291 |
| w23 | 1 | 0.055738 | 4.037 |
| w24 | 17 | -0.131613 | 18.334 |
| w25 | 16 | 0.113293 | 18.488 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | 0.112867 | 22.67 |
| w28 | 4 | -0.272856 | -0.257 |
| w29 | 6 | -0.077402 | -4.086 |
| w30 | 1 | -0.150538 | -7.008 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | 0.004022 | -4.258 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 7 | 0.071565 | 4.124 |
| w18 | 13 | -0.06555 | 2.341 |
| w19 | 2 | -0.012663 | -4.727 |
| w20 | 2 | 0.003628 | -4.32 |
| w21 | 5 | -0.083732 | -6.988 |
| w22 | 16 | 0.032885 | 46.504 |
| w23 | 1 | -0.132311 | -1.947 |
| w24 | 11 | -0.111936 | 20.86 |
| w25 | 16 | 0.157907 | 39.439 |
| w26 | 1 | 0.130783 | 3.43 |
| w27 | 11 | 0.094985 | 22.701 |
| w28 | 5 | -0.276413 | -0.127 |
| w29 | 11 | -0.015902 | -0.527 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.05836 | -9.606 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 4 | -0.012401 | -4.461 |
| w29 | 11 | -0.025029 | -1.401 |
| w30 | 6 | -0.03283 | -5.479 |
| w31 | 7 | 0.028862 | -0.77 |
| w32 | 6 | -0.021294 | -5.513 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 16 | 0.06815 | -0.398 |
| w15 | 11 | 0.084776 | 0.003 |
| w16 | 20 | -0.007956 | 42.643 |
| w17 | 9 | -0.0312 | -0.446 |
| w18 | 7 | 0.063895 | -2.936 |
| w19 | 2 | -0.390248 | -9.793 |
| w20 | 4 | -0.026177 | -10.209 |
| w21 | 12 | 0.177364 | 30.649 |
| w22 | 4 | 0.007797 | 2.335 |
| w23 | 5 | -0.039431 | -1.753 |
| w24 | 14 | -0.085362 | 7.636 |
| w25 | 18 | 0.085408 | 23.218 |
| w26 | 3 | -0.068272 | -0.284 |
| w27 | 14 | 0.315406 | 77.284 |
| w28 | 5 | -0.202426 | -1.667 |
| w29 | 12 | -0.035105 | -5.365 |
| w30 | 7 | 0.066679 | -0.991 |
| w31 | 2 | 0.0561 | 1.491 |
| w32 | 9 | 0.020313 | -3.857 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 10 | 0.236552 | 73.769 |
| w26 | 15 | 0.0705 | 6.851 |
| w27 | 15 | 0.116886 | -26.034 |
| w28 | 5 | -0.082725 | -0.234 |
| w29 | 18 | 0.066872 | -11.939 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | -0.088708 | -5.26 |
| w32 | 9 | 0.19536 | 0.902 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

