# Backtest of 048-01_scaled-up-week-continuation_1d

- Plan: `../../../../../03_test_plan/night7_panic_run/plans/048-01_scaled-up-week-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 51 | -0.025572 | -0.655 |
| w2 | 41 | 0.219634 | 90.316 |
| w3 | 56 | 0.007042 | 58.137 |
| w4 | 37 | 0.022345 | -9.824 |
| w5 | 45 | -0.029718 | 56.114 |
| w6 | 45 | 0.09233 | 92.019 |
| w7 | 35 | -0.009405 | 0.343 |
| w8 | 31 | 0.129862 | 4.876 |
| w9 | 32 | -0.031291 | -13.559 |
| w10 | 35 | 0.05995 | 37.324 |
| w11 | 37 | 0.171479 | 81.286 |
| w12 | 32 | -0.02351 | -12.634 |
| w13 | 48 | 0.029874 | 11.147 |
| w14 | 41 | 0.006184 | 15.715 |
| w15 | 55 | -0.017245 | 60.589 |
| w16 | 48 | 0.044743 | 36.401 |
| w17 | 35 | 0.023728 | -7.467 |
| w18 | 42 | -0.046232 | -13.29 |
| w19 | 27 | -0.0155 | -4.861 |
| w20 | 32 | -0.069743 | -18.151 |
| w21 | 39 | -0.090071 | -17.98 |
| w22 | 37 | 0.138894 | 92.289 |
| w23 | 28 | -0.021598 | -15.012 |
| w24 | 43 | 0.042568 | 45.572 |
| w25 | 41 | 0.093279 | 42.72 |
| w26 | 33 | 0.056203 | 4.605 |
| w27 | 44 | -0.048903 | 21.639 |
| w28 | 38 | -0.036705 | -9.201 |
| w29 | 45 | 0.006972 | 5.135 |
| w30 | 35 | 0.07687 | 3.234 |
| w31 | 48 | 0.032294 | -8.915 |
| w32 | 42 | 0.161294 | 24.926 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 40 | -0.025666 | 10.851 |
| w2 | 39 | 0.038038 | 3.956 |
| w3 | 51 | -0.136466 | -23.968 |
| w4 | 42 | 0.110952 | 73.546 |
| w5 | 44 | -0.007966 | 40.419 |
| w6 | 48 | 0.156227 | 108.785 |
| w7 | 26 | 0.022554 | 8.071 |
| w8 | 33 | -0.005627 | -14.328 |
| w9 | 29 | -0.010877 | -10.143 |
| w10 | 39 | -0.069228 | 15.012 |
| w11 | 35 | -0.002658 | 0.395 |
| w12 | 40 | -0.030427 | -13.722 |
| w13 | 39 | 0.019657 | 16.048 |
| w14 | 42 | 0.002784 | 21.908 |
| w15 | 46 | -0.056098 | 11.746 |
| w16 | 50 | 0.023522 | 23.849 |
| w17 | 37 | 0.086112 | 23.682 |
| w18 | 36 | -0.020894 | -2.796 |
| w19 | 35 | 0.016675 | -3.615 |
| w20 | 36 | -0.074099 | -16.762 |
| w21 | 43 | -0.052688 | -5.538 |
| w22 | 48 | -0.077908 | -8.403 |
| w23 | 27 | -0.032882 | -11.483 |
| w24 | 42 | -0.049962 | -2.07 |
| w25 | 41 | -0.028583 | -0.757 |
| w26 | 27 | -0.016965 | -15.554 |
| w27 | 43 | -0.035781 | 12.435 |
| w28 | 33 | -0.052234 | -12.272 |
| w29 | 29 | 0.056862 | 19.725 |
| w30 | 32 | -0.094401 | -18.874 |
| w31 | 37 | 0.018876 | -12.451 |
| w32 | 35 | 0.082364 | -0.746 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 44 | 0.0683 | 78.455 |
| w7 | 25 | 0.170766 | 24.38 |
| w8 | 29 | -0.06537 | -17.345 |
| w9 | 18 | 0.188763 | 48.645 |
| w10 | 33 | -0.00941 | 1.464 |
| w11 | 39 | 0.060285 | 11.075 |
| w12 | 34 | -0.057577 | -13.403 |
| w13 | 40 | -0.013454 | 2.722 |
| w14 | 33 | 0.170365 | 62.855 |
| w15 | 37 | 0.217403 | 135.1 |
| w16 | 41 | 0.095972 | 86.502 |
| w17 | 27 | 0.119821 | 28.864 |
| w18 | 34 | -0.062827 | -10.068 |
| w19 | 30 | 0.068135 | 3.727 |
| w20 | 20 | -0.036697 | -7.804 |
| w21 | 36 | -0.017534 | 0.632 |
| w22 | 39 | -0.050653 | 5.108 |
| w23 | 26 | -0.020993 | -2.85 |
| w24 | 36 | 0.078884 | 41.474 |
| w25 | 38 | -0.050905 | -18.922 |
| w26 | 32 | 0.134982 | 17.839 |
| w27 | 38 | 0.303154 | 226.046 |
| w28 | 35 | -0.053514 | -3.638 |
| w29 | 35 | 0.110685 | 38.986 |
| w30 | 34 | -0.067274 | -12.728 |
| w31 | 27 | 0.069636 | 7.18 |
| w32 | 35 | 0.136254 | 22.689 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 24 | 0.153791 | 42.307 |
| w8 | 29 | -0.02668 | -12.552 |
| w9 | 24 | 0.103494 | 7.351 |
| w10 | 31 | 0.070173 | 27.514 |
| w11 | 38 | -0.125637 | -16.728 |
| w12 | 37 | 0.031443 | 1.083 |
| w13 | 42 | -0.011062 | 18.37 |
| w14 | 45 | 0.010727 | 10.742 |
| w15 | 37 | -0.144436 | -30.362 |
| w16 | 45 | 0.114066 | 60.54 |
| w17 | 37 | 0.01954 | 12.74 |
| w18 | 38 | -0.057496 | -16.743 |
| w19 | 33 | 0.041509 | -9.518 |
| w20 | 18 | -0.024383 | -7.77 |
| w21 | 42 | -0.0493 | -13.886 |
| w22 | 47 | 0.081652 | 27.527 |
| w23 | 30 | 0.318445 | 93.68 |
| w24 | 30 | -0.10858 | -11.796 |
| w25 | 35 | 0.105577 | 50.127 |
| w26 | 35 | -0.071241 | -18.351 |
| w27 | 50 | -0.102518 | -5.322 |
| w28 | 32 | -0.014504 | -4.527 |
| w29 | 58 | -0.226898 | -27.33 |
| w30 | 45 | -0.124863 | -19.214 |
| w31 | 44 | 0.012726 | -9.402 |
| w32 | 27 | 0.12945 | 7.559 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | 0.121559 | 133.923 |
| w2 | 41 | -0.097027 | -7.822 |
| w3 | 31 | 0.01876 | -11.094 |
| w4 | 45 | 0.062333 | 140.974 |
| w5 | 50 | 0.131198 | 84.696 |
| w6 | 41 | 0.040941 | 45.116 |
| w7 | 33 | 0.124622 | 38.876 |
| w8 | 27 | 0.006246 | -14.035 |
| w9 | 27 | 0.049677 | 2.393 |
| w10 | 34 | 0.026596 | 6.313 |
| w11 | 39 | 0.153219 | 36.595 |
| w12 | 34 | 0.004638 | -4.843 |
| w13 | 49 | 0.010795 | 39.488 |
| w14 | 35 | 0.075182 | 62.966 |
| w15 | 47 | -0.155054 | -13.999 |
| w16 | 52 | 0.043566 | 73.991 |
| w17 | 34 | 0.135002 | 47.32 |
| w18 | 50 | -0.13578 | -10.111 |
| w19 | 34 | 0.079855 | 5.382 |
| w20 | 33 | 0.016879 | -4.188 |
| w21 | 37 | 0.04302 | 5.632 |
| w22 | 40 | 0.037043 | 27.106 |
| w23 | 31 | -0.165775 | -28.669 |
| w24 | 42 | -0.048751 | 10.36 |
| w25 | 29 | 0.123932 | 59.572 |
| w26 | 25 | 0.133481 | 18.647 |
| w27 | 38 | -0.034169 | 0.057 |
| w28 | 29 | -0.07959 | -16.94 |
| w29 | 41 | 0.049244 | 53.444 |
| w30 | 30 | 0.018398 | -8.852 |
| w31 | 38 | 0.012662 | -13.503 |
| w32 | 39 | 0.097271 | 22.564 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 40 | 0.087716 | 50.041 |
| w11 | 32 | -0.071295 | -8.985 |
| w12 | 39 | -0.080538 | -19.728 |
| w13 | 52 | 0.06468 | 33.739 |
| w14 | 35 | 0.080042 | 45.558 |
| w15 | 38 | -0.041738 | 3.664 |
| w16 | 43 | 0.045123 | 70.177 |
| w17 | 49 | 0.018203 | 36.224 |
| w18 | 22 | -0.082507 | -14.902 |
| w19 | 24 | 0.135256 | 15.321 |
| w20 | 31 | -0.053674 | -23.001 |
| w21 | 19 | 0.042172 | -5.732 |
| w22 | 49 | 0.006644 | 16.402 |
| w23 | 31 | -0.143255 | -28.177 |
| w24 | 36 | 0.183411 | 175.505 |
| w25 | 29 | 0.093433 | 7.061 |
| w26 | 25 | -0.033625 | -12.028 |
| w27 | 30 | 0.21906 | 84.572 |
| w28 | 24 | -0.122673 | -16.244 |
| w29 | 32 | 0.049502 | 21.322 |
| w30 | 28 | 0.001535 | -14.062 |
| w31 | 32 | -0.088172 | -15.34 |
| w32 | 27 | 0.047025 | 0.456 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 50 | 0.041972 | 28.101 |
| w13 | 40 | -0.053903 | -19.748 |
| w14 | 50 | 0.028467 | 58.507 |
| w15 | 44 | -0.043831 | -2.282 |
| w16 | 46 | -0.033167 | 16.288 |
| w17 | 49 | 0.008039 | 6.933 |
| w18 | 41 | -0.130575 | -27.023 |
| w19 | 26 | -0.082256 | -11.687 |
| w20 | 39 | -0.069227 | -8.971 |
| w21 | 38 | 0.037936 | 0.897 |
| w22 | 30 | -0.00995 | -0.912 |
| w23 | 26 | -0.132999 | -24.56 |
| w24 | 48 | -0.029559 | 18.977 |
| w25 | 30 | 0.116283 | 12.468 |
| w26 | 29 | -0.035693 | -17.053 |
| w27 | 43 | 0.088447 | 29.33 |
| w28 | 25 | -0.104753 | -18.876 |
| w29 | 35 | -0.092572 | -19.555 |
| w30 | 18 | -0.097145 | -20.921 |
| w31 | 36 | 0.161481 | 20.911 |
| w32 | 37 | -0.104042 | -21.077 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 41 | -0.095508 | -19.697 |
| w16 | 49 | -3e-05 | 35.385 |
| w17 | 41 | -0.095566 | -17.321 |
| w18 | 35 | -0.006813 | 1.187 |
| w19 | 21 | 0.073767 | -6.005 |
| w20 | 29 | -0.127206 | -26.159 |
| w21 | 28 | 0.028586 | -5.908 |
| w22 | 42 | -0.009268 | -6.623 |
| w23 | 28 | -0.016305 | -15.803 |
| w24 | 38 | 0.029836 | 63.313 |
| w25 | 37 | 0.135451 | 21.557 |
| w26 | 33 | 0.070341 | 0.529 |
| w27 | 39 | 0.256986 | 135.873 |
| w28 | 40 | -0.073562 | -10.945 |
| w29 | 32 | 0.072558 | 12.812 |
| w30 | 26 | -0.096671 | -20.597 |
| w31 | 24 | 0.048922 | 2.286 |
| w32 | 30 | -0.103554 | -23.592 |

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
| w15 | 37 | -0.011104 | -4.402 |
| w16 | 54 | 0.041929 | 63.854 |
| w17 | 25 | 0.080965 | 24.09 |
| w18 | 42 | -0.198123 | -27.464 |
| w19 | 37 | 0.022185 | 2.87 |
| w20 | 41 | -0.057626 | -5.913 |
| w21 | 45 | -0.05118 | -11.011 |
| w22 | 38 | 0.006207 | 21.339 |
| w23 | 44 | -0.054277 | -16.435 |
| w24 | 48 | -0.179595 | 3.657 |
| w25 | 48 | 0.135615 | 34.052 |
| w26 | 51 | 0.102105 | 36.363 |
| w27 | 38 | 0.059325 | 96.331 |
| w28 | 47 | -0.17608 | -19.317 |
| w29 | 60 | -0.091219 | 9.871 |
| w30 | 36 | -0.014221 | -11.591 |
| w31 | 56 | -0.019302 | 13.367 |
| w32 | 52 | 0.040516 | 5.475 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 45 | -0.018539 | 21.448 |
| w17 | 35 | 0.024342 | 15.648 |
| w18 | 35 | -0.082671 | -16.605 |
| w19 | 39 | 0.015909 | -8.973 |
| w20 | 31 | -0.046897 | -8.876 |
| w21 | 27 | -0.067316 | -20.575 |
| w22 | 47 | -0.014202 | 11.011 |
| w23 | 26 | -0.068096 | -28.109 |
| w24 | 51 | 0.038603 | 47.521 |
| w25 | 26 | 0.145094 | 25.347 |
| w26 | 31 | -0.051336 | -18.233 |
| w27 | 38 | 0.149527 | 53.516 |
| w28 | 36 | -0.033794 | -8.397 |
| w29 | 25 | -0.020887 | -6.466 |
| w30 | 29 | -0.057334 | -17.676 |
| w31 | 30 | -0.044991 | -11.822 |
| w32 | 32 | 0.006084 | -13.878 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 27 | 0.001792 | -5.541 |
| w21 | 25 | 0.045899 | 2.635 |
| w22 | 44 | 0.08809 | 43.409 |
| w23 | 20 | -0.009436 | -14.795 |
| w24 | 43 | 0.202414 | 162.242 |
| w25 | 32 | 0.025144 | -0.304 |
| w26 | 35 | -0.009475 | -4.94 |
| w27 | 41 | 0.047834 | 29.448 |
| w28 | 33 | -0.066362 | -13.834 |
| w29 | 36 | -0.052892 | -3.631 |
| w30 | 30 | 0.032122 | -2.83 |
| w31 | 37 | -0.01807 | -7.83 |
| w32 | 35 | 0.034301 | -4.2 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 46 | 0.013915 | 18.083 |
| w23 | 29 | 0.085572 | -8.005 |
| w24 | 42 | 0.078301 | 89.043 |
| w25 | 38 | 0.051409 | 39.59 |
| w26 | 25 | 0.029461 | 0.74 |
| w27 | 40 | 0.076551 | 25.765 |
| w28 | 33 | -0.022705 | -8.221 |
| w29 | 33 | -0.033266 | -6.159 |
| w30 | 34 | -0.081525 | -19.202 |
| w31 | 41 | 0.017269 | -5.952 |
| w32 | 31 | 0.04091 | 30.133 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 45 | 0.02474 | 20.821 |
| w25 | 41 | -0.057416 | -8.336 |
| w26 | 27 | -0.027448 | -8.521 |
| w27 | 48 | 0.049972 | 65.67 |
| w28 | 28 | -0.002636 | -2.118 |
| w29 | 39 | -0.019352 | 0.209 |
| w30 | 34 | -0.018539 | -10.788 |
| w31 | 33 | 0.114874 | 8.256 |
| w32 | 29 | 0.090299 | 21.232 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 43 | 0.149442 | 83.548 |
| w6 | 37 | 0.027265 | 23.856 |
| w7 | 27 | 0.078864 | 5.815 |
| w8 | 31 | -0.043131 | -12.48 |
| w9 | 22 | 0.018275 | -7.413 |
| w10 | 36 | 0.103595 | 22.607 |
| w11 | 27 | 0.081915 | 11.79 |
| w12 | 30 | -0.084435 | -20.587 |
| w13 | 45 | 0.11388 | 59.883 |
| w14 | 41 | -0.006781 | 26.172 |
| w15 | 43 | -0.093012 | -22.41 |
| w16 | 40 | 0.145934 | 83.836 |
| w17 | 37 | 0.037171 | 6.078 |
| w18 | 43 | -0.108351 | -19.736 |
| w19 | 36 | 0.024717 | 9.155 |
| w20 | 27 | -0.030228 | -9.892 |
| w21 | 34 | -0.085332 | -14.856 |
| w22 | 43 | -0.15306 | -18.469 |
| w23 | 37 | -0.014788 | -14.039 |
| w24 | 58 | -0.063229 | -4.734 |
| w25 | 42 | 0.108409 | 16.86 |
| w26 | 28 | 0.128862 | 37.695 |
| w27 | 42 | -0.069205 | 13.442 |
| w28 | 40 | -0.075174 | -7.849 |
| w29 | 38 | -0.051726 | -13.415 |
| w30 | 54 | 0.096597 | 135.83 |
| w31 | 25 | 0.047334 | 3.865 |
| w32 | 45 | 0.077013 | 47.883 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 44 | 0.109788 | 127.437 |
| w6 | 41 | 0.092386 | 65.266 |
| w7 | 27 | 0.075776 | 14.259 |
| w8 | 27 | -0.023628 | -6.514 |
| w9 | 26 | -0.014955 | -10.996 |
| w10 | 38 | -0.014175 | 12.277 |
| w11 | 46 | -0.008775 | -2.428 |
| w12 | 36 | -0.03804 | -15.688 |
| w13 | 45 | 0.038176 | 32.146 |
| w14 | 52 | -0.028701 | 31.922 |
| w15 | 52 | -0.108292 | 1.596 |
| w16 | 42 | 0.041677 | 53.857 |
| w17 | 42 | -0.016614 | -12.112 |
| w18 | 37 | -0.12078 | -23.82 |
| w19 | 44 | -0.19378 | -23.084 |
| w20 | 44 | -0.04434 | -15.248 |
| w21 | 53 | -0.138008 | -20.182 |
| w22 | 45 | -0.01053 | 1.756 |
| w23 | 24 | 0.177157 | 17.147 |
| w24 | 50 | -0.036628 | 9.244 |
| w25 | 39 | -0.022598 | -11.822 |
| w26 | 41 | 0.017362 | 16.277 |
| w27 | 40 | -0.071965 | -19.642 |
| w28 | 54 | -0.044904 | 18.896 |
| w29 | 34 | 0.029586 | 2.934 |
| w30 | 52 | -0.143493 | -3.62 |
| w31 | 38 | 0.081475 | 15.764 |
| w32 | 51 | -0.038499 | 20.428 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 52 | -0.020269 | -5.952 |
| w18 | 39 | -0.05288 | -0.399 |
| w19 | 43 | -0.049544 | -19.712 |
| w20 | 32 | -0.102832 | -9.591 |
| w21 | 32 | -0.142794 | -36.881 |
| w22 | 35 | 0.18145 | 50.543 |
| w23 | 31 | -0.072028 | -17.806 |
| w24 | 47 | 0.011952 | 11.458 |
| w25 | 38 | 0.181866 | 30.465 |
| w26 | 32 | 0.000446 | -4.604 |
| w27 | 48 | 0.13326 | 73.643 |
| w28 | 32 | -0.03598 | -7.134 |
| w29 | 35 | 0.039796 | 12.612 |
| w30 | 31 | -0.085019 | -17.601 |
| w31 | 34 | -0.047578 | -10.399 |
| w32 | 35 | -0.045612 | 1.71 |

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
| w17 | 46 | -0.013948 | -3.829 |
| w18 | 40 | 0.001977 | -7.524 |
| w19 | 25 | 0.047292 | 3.107 |
| w20 | 37 | 0.000439 | -5.237 |
| w21 | 31 | -0.035017 | -13.915 |
| w22 | 38 | 0.114054 | 32.585 |
| w23 | 35 | 0.0081 | -11.972 |
| w24 | 47 | -0.090817 | 9.858 |
| w25 | 36 | -0.008893 | -13.173 |
| w26 | 32 | 0.054151 | 32.474 |
| w27 | 45 | -0.075944 | 5.51 |
| w28 | 32 | 0.014559 | -6.456 |
| w29 | 52 | -0.046278 | 8.116 |
| w30 | 31 | -0.109568 | -16.572 |
| w31 | 27 | -0.08376 | -16.19 |
| w32 | 34 | 0.066302 | 19.142 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 31 | 0.075043 | 7.401 |
| w20 | 38 | -0.005715 | -12.124 |
| w21 | 32 | -0.092875 | -17.434 |
| w22 | 49 | 0.046651 | 130.154 |
| w23 | 38 | 0.020888 | -5.451 |
| w24 | 40 | 0.178594 | 212.705 |
| w25 | 34 | -0.142518 | -26.484 |
| w26 | 36 | -0.022516 | -9.089 |
| w27 | 38 | -0.001837 | 5.854 |
| w28 | 28 | -0.058779 | -17.217 |
| w29 | 46 | -0.064209 | -9.47 |
| w30 | 26 | -0.106043 | -21.055 |
| w31 | 46 | -0.022631 | -3.419 |
| w32 | 39 | 0.015708 | 18.484 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 45 | 0.046433 | 26.171 |
| w23 | 33 | -0.105404 | -18.862 |
| w24 | 40 | -0.100269 | -6.381 |
| w25 | 46 | -0.022069 | -14.371 |
| w26 | 30 | 0.058023 | 0.85 |
| w27 | 42 | -0.102731 | -13.6 |
| w28 | 33 | -0.089618 | -19.103 |
| w29 | 24 | 0.082068 | 23.297 |
| w30 | 31 | -0.139742 | -18.85 |
| w31 | 31 | -0.020367 | -4.703 |
| w32 | 40 | 0.212512 | 41.922 |

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
| w27 | 47 | 0.018015 | 27.341 |
| w28 | 34 | -0.173943 | -20.073 |
| w29 | 34 | -0.004877 | -3.258 |
| w30 | 21 | -0.056979 | -16.885 |
| w31 | 41 | -0.04124 | -11.51 |
| w32 | 42 | 0.099369 | 53.285 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 35 | 0.091337 | 8.894 |
| w18 | 30 | -0.050193 | -19.502 |
| w19 | 25 | 0.110134 | 6.049 |
| w20 | 19 | 0.163526 | 21.491 |
| w21 | 32 | -0.055973 | -15.457 |
| w22 | 38 | 0.011098 | 29.381 |
| w23 | 31 | -0.11648 | -22.082 |
| w24 | 46 | -0.028369 | 26.367 |
| w25 | 36 | 0.084309 | 14.102 |
| w26 | 32 | -0.020516 | -12.759 |
| w27 | 47 | 0.06261 | 25.713 |
| w28 | 36 | -0.065771 | -9.126 |
| w29 | 30 | -0.09521 | -22.858 |
| w30 | 36 | 0.022674 | 1.729 |
| w31 | 38 | -0.071024 | -19.692 |
| w32 | 32 | 0.000142 | -10.076 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 33 | 0.033512 | -1.899 |
| w18 | 44 | -0.076613 | -15.394 |
| w19 | 28 | -0.008731 | -8.81 |
| w20 | 29 | -0.055524 | -13.576 |
| w21 | 32 | -0.091113 | -20.571 |
| w22 | 38 | 0.073624 | 76.985 |
| w23 | 35 | -0.13178 | -29.81 |
| w24 | 40 | 0.017745 | 47.338 |
| w25 | 33 | 0.095189 | 44.408 |
| w26 | 39 | 0.040122 | -2.28 |
| w27 | 41 | 0.057063 | 22.578 |
| w28 | 31 | 0.017704 | -8.251 |
| w29 | 30 | -0.036848 | -12.881 |
| w30 | 20 | -0.118177 | -22.393 |
| w31 | 29 | -0.055664 | -15.069 |
| w32 | 26 | 0.115534 | 6.046 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 43 | -0.093536 | -21.603 |
| w29 | 37 | -0.022442 | -3.779 |
| w30 | 31 | 0.003599 | -7.998 |
| w31 | 30 | 0.106194 | 18.172 |
| w32 | 35 | 0.059263 | 12.599 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 31 | 0.080822 | 60.086 |
| w15 | 35 | 0.015665 | 37.204 |
| w16 | 33 | 0.015689 | 259.55 |
| w17 | 24 | 0.048414 | 8.474 |
| w18 | 34 | -0.136765 | -21.865 |
| w19 | 39 | -0.127221 | -19.905 |
| w20 | 31 | -0.026126 | -8.847 |
| w21 | 29 | 0.26712 | 109.551 |
| w22 | 52 | -0.104567 | -0.745 |
| w23 | 46 | -0.082882 | -14.647 |
| w24 | 37 | 0.017269 | 20.356 |
| w25 | 40 | 0.167307 | 69.752 |
| w26 | 33 | -0.002682 | -5.168 |
| w27 | 36 | 0.097725 | 72.564 |
| w28 | 28 | -0.049462 | -13.194 |
| w29 | 34 | 0.067616 | 21.639 |
| w30 | 28 | 0.04189 | -6.379 |
| w31 | 32 | 0.009725 | 7.72 |
| w32 | 32 | 0.083431 | 10.283 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 34 | 0.344569 | 193.214 |
| w26 | 34 | 0.025771 | 1.596 |
| w27 | 31 | 0.100889 | 53.228 |
| w28 | 35 | 0.017207 | -6.978 |
| w29 | 30 | -0.006656 | -3.732 |
| w30 | 29 | -0.043595 | -16.61 |
| w31 | 36 | -0.002286 | 7.977 |
| w32 | 32 | 0.135156 | 20.625 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

