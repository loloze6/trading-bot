# Backtest of 031-02.b1.b2_flat-day-after-strong-rise_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-02.b1.b2_flat-day-after-strong-rise_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | 0.02564 | 19.582 |
| w3 | 9 | -0.003685 | 32.548 |
| w4 | 3 | -0.134336 | 7.407 |
| w5 | 2 | 0.037582 | 6.772 |
| w6 | 2 | 0.032087 | 63.159 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 6 | 0.068966 | 47.012 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.00321 | -1.52 |
| w13 | 4 | -0.020895 | -3.798 |
| w14 | 2 | 0.064697 | 8.068 |
| w15 | 8 | -0.073168 | 28.81 |
| w16 | 2 | 0.041584 | -7.778 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | 0.028207 | -11.58 |
| w20 | 3 | 0.034211 | 0.001 |
| w21 | 1 | -0.07464 | -3.497 |
| w22 | 7 | -0.041599 | 14.229 |
| w23 | 0 | 0.019975 | 0.0 |
| w24 | 1 | 0.0417 | 40.513 |
| w25 | 5 | -0.045828 | -1.625 |
| w26 | 0 | 0.015628 | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | -0.099529 | 0.0 |
| w30 | 4 | 0.027463 | 0.103 |
| w31 | 2 | -0.081535 | 2.748 |
| w32 | 0 | None | 0.0 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.060867 | 19.701 |
| w2 | 6 | -0.029195 | -13.355 |
| w3 | 2 | 0.027783 | -13.336 |
| w4 | 4 | -0.093484 | -5.863 |
| w5 | 6 | 0.170563 | 15.176 |
| w6 | 4 | -0.164819 | -16.477 |
| w7 | 1 | -0.019202 | -1.37 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | -0.119562 | -3.877 |
| w10 | 2 | 0.013383 | -3.871 |
| w11 | 4 | -0.084073 | 14.562 |
| w12 | 2 | 0.14409 | 3.204 |
| w13 | 8 | 0.002957 | 3.81 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.133921 | -7.89 |
| w16 | 5 | 0.092063 | -3.863 |
| w17 | 4 | 0.00859 | -3.504 |
| w18 | 6 | 0.123018 | -21.884 |
| w19 | 1 | -0.118538 | -5.291 |
| w20 | 4 | 0.144471 | 2.873 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | -0.010128 | 10.84 |
| w23 | 1 | -0.039709 | -2.86 |
| w24 | 4 | -0.106649 | 1.762 |
| w25 | 1 | 0.150209 | 34.634 |
| w26 | 1 | -0.012447 | -0.414 |
| w27 | 2 | -0.006307 | -9.331 |
| w28 | 3 | 0.043543 | 4.689 |
| w29 | 4 | 0.118821 | 20.286 |
| w30 | 2 | 0.005353 | -22.099 |
| w31 | 4 | -0.06286 | -3.535 |
| w32 | 2 | -0.045117 | -12.8 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 6 | -0.015018 | 22.452 |
| w7 | 4 | 0.014152 | 10.993 |
| w8 | 0 | None | 0.0 |
| w9 | 5 | 0.032965 | -3.103 |
| w10 | 2 | 0.070633 | -1.724 |
| w11 | 1 | -0.24341 | -2.953 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | -0.012441 | -0.11 |
| w14 | 2 | 0.309387 | 47.469 |
| w15 | 3 | 0.066199 | 144.849 |
| w16 | 8 | -0.038904 | 14.13 |
| w17 | 3 | -0.072598 | 0.489 |
| w18 | 7 | 0.03372 | -2.737 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.130017 | 0.165 |
| w21 | 1 | -0.088983 | -0.388 |
| w22 | 4 | -0.069257 | 7.999 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | -0.044426 | 35.758 |
| w25 | 4 | -0.053786 | -9.669 |
| w26 | 3 | 0.067639 | 3.699 |
| w27 | 5 | 0.104672 | 95.858 |
| w28 | 2 | 0.088792 | 2.119 |
| w29 | 1 | 0.08488 | 42.099 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 4 | 0.062338 | -13.902 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 3 | -0.01317 | 31.276 |
| w8 | 3 | -0.093868 | -15.938 |
| w9 | 3 | 0.01998 | -10.771 |
| w10 | 0 | None | 0.0 |
| w11 | 5 | -0.045191 | 12.132 |
| w12 | 3 | -0.059721 | -30.94 |
| w13 | 6 | -0.022114 | 42.888 |
| w14 | 2 | 0.020501 | -1.67 |
| w15 | 6 | 0.049016 | 15.757 |
| w16 | 5 | -0.11391 | -14.575 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | -0.034274 | 0.0 |
| w19 | 3 | -0.01691 | -0.799 |
| w20 | 3 | 0.148564 | 16.813 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | 0.055444 | 21.434 |
| w23 | 2 | -0.004436 | -2.251 |
| w24 | 4 | 0.200085 | -2.357 |
| w25 | 4 | -0.09854 | 51.94 |
| w26 | 1 | -0.17708 | -8.248 |
| w27 | 2 | 0.027075 | 2.992 |
| w28 | 6 | 0.451736 | 0.722 |
| w29 | 4 | -0.045047 | 5.939 |
| w30 | 2 | -0.148159 | 1.321 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.019777 | -9.163 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.088628 | 89.769 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 8 | 0.049206 | 132.053 |
| w5 | 8 | -0.127963 | 10.029 |
| w6 | 2 | -0.033698 | -1.94 |
| w7 | 4 | 0.041084 | 30.427 |
| w8 | 0 | 0.060934 | 0.0 |
| w9 | 2 | -0.184618 | 0.253 |
| w10 | 2 | 0.115786 | 0.596 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.035961 | 6.58 |
| w13 | 6 | 0.038103 | 19.005 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.048405 | 0.648 |
| w16 | 6 | -0.153627 | 6.876 |
| w17 | 2 | 0.074965 | -14.716 |
| w18 | 2 | -0.056454 | 1.023 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.008317 | -0.269 |
| w22 | 2 | 0.040774 | 5.499 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.031558 | 7.644 |
| w25 | 4 | 0.098932 | 20.259 |
| w26 | 0 | 0.031017 | 0.0 |
| w27 | 0 | -0.031967 | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | 0.04505 | 3.161 |
| w30 | 2 | 0.064612 | -1.268 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 6 | -0.039502 | 6.509 |
| w11 | 1 | -0.200224 | -6.443 |
| w12 | 2 | 0.089299 | 2.706 |
| w13 | 7 | 0.010586 | 25.835 |
| w14 | 4 | -0.166911 | 27.326 |
| w15 | 0 | None | 0.0 |
| w16 | 7 | -0.086888 | 17.991 |
| w17 | 7 | -0.073178 | 44.942 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.000987 | -3.806 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | -0.084649 | 28.239 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.007453 | -7.772 |
| w25 | 2 | 0.090046 | 12.429 |
| w26 | 2 | 0.06539 | -0.658 |
| w27 | 7 | 0.149371 | 43.358 |
| w28 | 0 | -0.014306 | 0.0 |
| w29 | 5 | 0.002995 | 15.978 |
| w30 | 2 | 0.103595 | -6.186 |
| w31 | 4 | -0.120518 | -9.91 |
| w32 | 3 | -0.041966 | -12.651 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 4 | 0.104981 | -4.098 |
| w13 | 0 | None | 0.0 |
| w14 | 8 | -0.011438 | 71.719 |
| w15 | 1 | -0.152775 | -7.488 |
| w16 | 7 | 0.098697 | 47.153 |
| w17 | 5 | 0.062415 | 18.558 |
| w18 | 2 | -0.056747 | 8.146 |
| w19 | 2 | 0.065337 | -6.556 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.178795 | -4.011 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.051191 | -0.949 |
| w24 | 10 | 0.06199 | 43.923 |
| w25 | 2 | 0.061824 | 16.88 |
| w26 | 1 | -0.015359 | -2.503 |
| w27 | 2 | 0.058645 | -2.371 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.003637 | -17.337 |
| w30 | 2 | 0.079377 | -3.366 |
| w31 | 0 | None | 0.0 |
| w32 | 7 | 0.005916 | 4.837 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 2 | -0.071865 | -1.888 |
| w16 | 7 | 0.181302 | 19.003 |
| w17 | 2 | -0.000313 | -3.92 |
| w18 | 5 | 0.126166 | -10.848 |
| w19 | 4 | 0.089192 | 0.765 |
| w20 | 2 | 0.03214 | 1.132 |
| w21 | 5 | 0.038944 | -11.371 |
| w22 | 4 | 0.057444 | 3.77 |
| w23 | 0 | 0.099234 | 0.0 |
| w24 | 6 | -0.087408 | 52.49 |
| w25 | 3 | -0.024587 | 53.227 |
| w26 | 4 | -0.071604 | -11.219 |
| w27 | 4 | 0.166368 | 65.528 |
| w28 | 0 | 0.084194 | 0.0 |
| w29 | 4 | 0.372313 | 23.751 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | -0.048421 | -6.082 |
| w32 | 4 | 0.197833 | -16.376 |

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
| w15 | 3 | 0.217945 | -10.283 |
| w16 | 5 | 0.129619 | 22.293 |
| w17 | 3 | 0.012403 | 0.949 |
| w18 | 2 | -0.096592 | -1.068 |
| w19 | 3 | 0.10686 | -15.933 |
| w20 | 2 | 0.024469 | -1.073 |
| w21 | 2 | -0.035918 | 2.622 |
| w22 | 4 | -0.110486 | -5.427 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.051462 | 7.419 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | 0.217769 | 6.679 |
| w27 | 1 | 0.072673 | 35.969 |
| w28 | 1 | -0.088174 | -1.48 |
| w29 | 4 | 0.007225 | 5.418 |
| w30 | 4 | 0.031545 | 1.473 |
| w31 | 6 | -0.148513 | -5.238 |
| w32 | 4 | -0.000949 | -7.559 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 7 | -0.015778 | -2.933 |
| w17 | 2 | 0.072413 | 7.253 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | -0.088728 | -6.457 |
| w20 | 2 | 0.085481 | 6.168 |
| w21 | 1 | -0.195549 | -6.186 |
| w22 | 5 | 0.076944 | -1.948 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.084851 | 9.556 |
| w25 | 4 | 0.016721 | 25.501 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | 0.1147 | -1.889 |
| w29 | 5 | 0.090822 | -6.928 |
| w30 | 2 | 0.018489 | -11.035 |
| w31 | 2 | 0.078403 | -4.246 |
| w32 | 1 | -0.113422 | -2.548 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 2 | -0.01577 | -6.099 |
| w21 | 3 | 0.11069 | -33.165 |
| w22 | 7 | 0.027156 | -18.657 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | 0.197782 | 95.378 |
| w25 | 2 | 0.085 | 1.789 |
| w26 | 3 | -0.101904 | -1.363 |
| w27 | 2 | 0.06134 | -5.013 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | 0.09613 | 17.087 |
| w30 | 0 | None | 0.0 |
| w31 | 4 | -0.060561 | -6.182 |
| w32 | 2 | -0.094783 | 8.779 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 4 | 0.070396 | 19.445 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | -0.092914 | 83.597 |
| w25 | 4 | 0.141197 | 75.673 |
| w26 | 2 | -0.022097 | -1.394 |
| w27 | 5 | 0.061918 | 2.734 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.080086 | -6.526 |
| w30 | 2 | 0.055588 | -16.518 |
| w31 | 4 | -0.030346 | 2.387 |
| w32 | 4 | 0.019749 | 1.841 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 6 | 0.185039 | 40.106 |
| w25 | 0 | -0.070492 | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 9 | -0.079554 | 48.024 |
| w28 | 2 | 0.015011 | -0.203 |
| w29 | 0 | -0.146398 | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 6 | -0.115441 | -12.407 |
| w32 | 0 | None | 0.0 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 10 | -0.047041 | 4.744 |
| w6 | 2 | 0.137671 | -4.937 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.052003 | 4.618 |
| w9 | 0 | None | 0.0 |
| w10 | 6 | -0.105429 | 0.763 |
| w11 | 3 | -0.082777 | -11.475 |
| w12 | 2 | 0.095295 | 1.142 |
| w13 | 6 | 0.035676 | 29.104 |
| w14 | 5 | 0.042045 | 25.58 |
| w15 | 3 | -0.122426 | -0.31 |
| w16 | 4 | 0.136505 | -5.698 |
| w17 | 5 | 0.016705 | -5.832 |
| w18 | 3 | -0.031857 | -11.42 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.02333 | -2.717 |
| w22 | 2 | 0.068825 | 2.171 |
| w23 | 4 | 0.015742 | 5.771 |
| w24 | 5 | -0.029187 | -22.439 |
| w25 | 0 | None | 0.0 |
| w26 | 6 | -0.036338 | 4.466 |
| w27 | 6 | -0.062746 | -0.295 |
| w28 | 2 | 0.051494 | -2.118 |
| w29 | 6 | -0.133282 | -6.163 |
| w30 | 8 | 0.137367 | 41.993 |
| w31 | 2 | 0.183142 | 0.367 |
| w32 | 5 | 0.282124 | 50.269 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 5 | -0.105121 | 32.818 |
| w6 | 7 | 0.188309 | 53.389 |
| w7 | 2 | -0.121027 | -4.08 |
| w8 | 2 | 0.234641 | 6.066 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | -0.114391 | -2.52 |
| w11 | 2 | 0.042507 | -17.434 |
| w12 | 3 | -0.05842 | -3.529 |
| w13 | 2 | -0.018833 | 7.408 |
| w14 | 5 | 0.099197 | 40.794 |
| w15 | 5 | 0.023756 | -5.54 |
| w16 | 9 | 0.037734 | -3.968 |
| w17 | 2 | -0.010667 | 7.209 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | -0.070974 | 1.432 |
| w20 | 5 | -0.006166 | 6.803 |
| w21 | 2 | -0.324108 | -17.605 |
| w22 | 4 | 0.078621 | 1.398 |
| w23 | 2 | 0.193956 | 2.272 |
| w24 | 7 | -0.022452 | 3.443 |
| w25 | 6 | 0.087834 | -8.12 |
| w26 | 3 | 0.011467 | -1.82 |
| w27 | 8 | 0.07657 | 15.719 |
| w28 | 2 | -0.087898 | -0.065 |
| w29 | 2 | -0.059377 | 1.298 |
| w30 | 8 | 0.110667 | 9.979 |
| w31 | 0 | -0.234341 | 0.0 |
| w32 | 7 | -0.090591 | 23.24 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | 0.142008 | 5.784 |
| w18 | 5 | -0.121595 | -14.772 |
| w19 | 2 | -0.083013 | -8.495 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.088655 | 1.915 |
| w22 | 4 | -0.178239 | 0.96 |
| w23 | 2 | -0.043553 | -8.119 |
| w24 | 7 | 0.061283 | 28.035 |
| w25 | 3 | -0.043913 | 31.534 |
| w26 | 3 | -0.04014 | -7.186 |
| w27 | 7 | 0.051801 | 65.149 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | -0.071991 | -9.416 |
| w30 | 2 | 0.025575 | -0.759 |
| w31 | 0 | 0.003227 | 0.0 |
| w32 | 6 | -0.124372 | 33.186 |

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
| w17 | 4 | 0.122923 | -5.085 |
| w18 | 2 | -0.010726 | 1.051 |
| w19 | 6 | -0.051704 | -9.968 |
| w20 | 4 | 0.156578 | 12.471 |
| w21 | 5 | -0.2252 | -25.595 |
| w22 | 2 | 0.175721 | 4.667 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.068286 | -7.03 |
| w25 | 2 | 0.024915 | 26.786 |
| w26 | 0 | None | 0.0 |
| w27 | 4 | 0.029711 | 16.902 |
| w28 | 2 | -0.00637 | -1.33 |
| w29 | 7 | 0.015696 | 4.981 |
| w30 | 0 | None | 0.0 |
| w31 | 3 | -0.149665 | -10.911 |
| w32 | 4 | 0.115184 | -2.906 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 1 | -0.073126 | -2.78 |
| w20 | 2 | -0.060429 | 4.666 |
| w21 | 4 | 0.010698 | -19.531 |
| w22 | 11 | -0.005002 | 130.348 |
| w23 | 2 | -0.095693 | -11.259 |
| w24 | 5 | 0.197005 | 43.2 |
| w25 | 1 | -0.113024 | -17.19 |
| w26 | 4 | -0.080225 | -26.38 |
| w27 | 4 | -0.022925 | 2.903 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.026452 | -3.549 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | -0.12046 | -13.023 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 8 | 0.102473 | 53.671 |
| w23 | 0 | 0.070406 | 0.0 |
| w24 | 6 | -0.10114 | 10.018 |
| w25 | 4 | -0.059301 | 0.021 |
| w26 | 0 | None | 0.0 |
| w27 | 4 | 0.058311 | -4.413 |
| w28 | 1 | -0.010904 | -0.072 |
| w29 | 2 | 0.072386 | 1.091 |
| w30 | 0 | None | 0.0 |
| w31 | 6 | 0.078986 | 6.71 |
| w32 | 5 | 0.139759 | -11.779 |

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
| w27 | 4 | -0.077208 | 23.47 |
| w28 | 3 | -0.003738 | -1.196 |
| w29 | 4 | 0.05761 | -2.493 |
| w30 | 2 | 0.119861 | -4.938 |
| w31 | 6 | -0.178964 | -20.68 |
| w32 | 3 | 0.134736 | 16.6 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 2 | 0.017071 | 2.929 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | -0.011855 | -11.906 |
| w20 | 0 | None | 0.0 |
| w21 | 8 | -0.019218 | -28.93 |
| w22 | 7 | -0.127491 | 9.501 |
| w23 | 2 | 0.088304 | 2.433 |
| w24 | 6 | -0.118168 | 30.78 |
| w25 | 3 | 0.019212 | 18.173 |
| w26 | 4 | -0.05436 | -8.664 |
| w27 | 2 | 0.216571 | 20.587 |
| w28 | 0 | -0.037989 | 0.0 |
| w29 | 6 | -0.065742 | -7.517 |
| w30 | 2 | -0.134431 | 11.821 |
| w31 | 2 | 0.004951 | 0.768 |
| w32 | 0 | None | 0.0 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 0 | None | 0.0 |
| w18 | 2 | 0.002526 | -0.295 |
| w19 | 1 | -0.128676 | -17.005 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | -0.27825 | -27.343 |
| w22 | 5 | -0.022982 | 33.537 |
| w23 | 2 | 0.113843 | 4.619 |
| w24 | 3 | 0.21571 | 41.31 |
| w25 | 2 | -0.007921 | 11.057 |
| w26 | 2 | -0.087011 | 3.381 |
| w27 | 6 | 0.15253 | 5.873 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | 0.201384 | 9.323 |
| w30 | 1 | -0.080454 | -14.547 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | 0.06704 | -8.863 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 4 | 0.073456 | -11.463 |
| w29 | 2 | 0.021726 | 1.275 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | 0.107051 | 14.789 |
| w32 | 4 | -0.061509 | -4.132 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 0 | -0.043787 | 0.0 |
| w15 | 3 | 0.317991 | 10.675 |
| w16 | 3 | -0.036704 | -3.2 |
| w17 | 2 | 0.041473 | -0.574 |
| w18 | 5 | -0.021536 | -8.424 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | 0.193681 | -0.809 |
| w21 | 1 | -0.045555 | 2.606 |
| w22 | 1 | -0.06598 | -6.056 |
| w23 | 4 | 0.043262 | 17.689 |
| w24 | 2 | 0.025023 | 2.717 |
| w25 | 6 | 0.212614 | 49.782 |
| w26 | 2 | -0.050975 | 7.438 |
| w27 | 4 | 0.044419 | 16.746 |
| w28 | 1 | -0.018374 | -3.179 |
| w29 | 5 | -0.081311 | -1.283 |
| w30 | 2 | 0.050468 | 6.105 |
| w31 | 8 | -0.113835 | -4.483 |
| w32 | 4 | 0.016427 | -19.723 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 4 | 0.018827 | 16.252 |
| w26 | 2 | -0.060007 | 18.596 |
| w27 | 7 | -0.087601 | -19.771 |
| w28 | 2 | -0.005168 | 0.287 |
| w29 | 6 | 0.020181 | -0.438 |
| w30 | 2 | 0.04753 | 2.102 |
| w31 | 6 | -0.10057 | 2.886 |
| w32 | 3 | 0.015237 | -14.505 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

