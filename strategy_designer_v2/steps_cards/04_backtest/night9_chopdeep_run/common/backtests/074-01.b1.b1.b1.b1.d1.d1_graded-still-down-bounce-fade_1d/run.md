# Backtest of 074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d

- Plan: `../../../../../03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.026456 | -0.638 |
| w2 | 5 | 0.056522 | 0.993 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 14 | 0.121418 | 7.468 |
| w8 | 8 | 0.150043 | 10.147 |
| w9 | 18 | 0.184396 | 37.631 |
| w10 | 8 | 0.077519 | 0.754 |
| w11 | 1 | None | -0.019 |
| w12 | 20 | -0.008056 | 0.773 |
| w13 | 10 | 0.113488 | 5.719 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 14 | 0.224162 | 21.165 |
| w18 | 5 | -0.025329 | -1.499 |
| w19 | 13 | -0.069346 | -6.105 |
| w20 | 15 | 0.095536 | 10.802 |
| w21 | 18 | 0.080019 | 5.612 |
| w22 | 1 | 0.006236 | -0.06 |
| w23 | 5 | -0.075896 | -4.8 |
| w24 | 4 | -0.041212 | -4.332 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | -0.037205 | -2.703 |
| w27 | 0 | None | 0.0 |
| w28 | 7 | 0.115576 | 6.151 |
| w29 | 0 | None | 0.0 |
| w30 | 10 | 0.02376 | 2.203 |
| w31 | 15 | 0.045119 | 5.997 |
| w32 | 9 | 0.038635 | 1.319 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.029198 | -1.475 |
| w2 | 7 | 0.035482 | 0.886 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.039415 | -4.353 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.007811 | -0.257 |
| w7 | 14 | 0.040856 | 2.39 |
| w8 | 18 | 0.225263 | 24.415 |
| w9 | 18 | 0.228056 | 33.537 |
| w10 | 3 | 0.124804 | 2.302 |
| w11 | 9 | 0.03562 | 1.274 |
| w12 | 20 | -0.003646 | 0.314 |
| w13 | 10 | 0.095202 | 3.262 |
| w14 | 3 | -0.005582 | -0.886 |
| w15 | 3 | 0.040045 | 0.425 |
| w16 | 0 | None | 0.0 |
| w17 | 10 | 0.057252 | 1.273 |
| w18 | 3 | 0.072183 | 1.181 |
| w19 | 17 | 0.02146 | 1.622 |
| w20 | 17 | 0.084135 | 12.318 |
| w21 | 5 | 0.048195 | 1.038 |
| w22 | 0 | None | 0.0 |
| w23 | 6 | -0.055577 | -2.43 |
| w24 | 14 | -0.050059 | -3.877 |
| w25 | 0 | None | 0.0 |
| w26 | 17 | 0.049553 | 4.528 |
| w27 | 3 | -0.012792 | -1.386 |
| w28 | 11 | 0.09349 | 6.607 |
| w29 | 1 | -0.08089 | -1.282 |
| w30 | 14 | -0.042897 | -2.171 |
| w31 | 20 | -0.046905 | -1.797 |
| w32 | 9 | 0.044202 | 2.905 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 2 | -0.013354 | -1.673 |
| w7 | 9 | -0.035308 | -1.863 |
| w8 | 20 | -0.024481 | 1.386 |
| w9 | 10 | 0.040397 | 1.25 |
| w10 | 12 | 0.046577 | 1.235 |
| w11 | 12 | -0.039862 | -4.018 |
| w12 | 14 | 0.11527 | 11.014 |
| w13 | 8 | 0.159622 | 7.778 |
| w14 | 4 | 0.029577 | 0.453 |
| w15 | 2 | 0.005979 | 0.101 |
| w16 | 5 | 0.024246 | -0.507 |
| w17 | 13 | 0.109619 | 5.201 |
| w18 | 8 | 0.019219 | 1.837 |
| w19 | 16 | 0.016696 | 1.523 |
| w20 | 6 | 0.0244 | 11.462 |
| w21 | 9 | 0.014278 | 0.153 |
| w22 | 1 | 0.038604 | 0.54 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.045427 | -3.326 |
| w25 | 10 | 0.045683 | 3.013 |
| w26 | 10 | 0.1166 | 9.57 |
| w27 | 2 | 0.084301 | 3.47 |
| w28 | 7 | 0.067317 | 2.117 |
| w29 | 0 | None | 0.0 |
| w30 | 22 | -0.078142 | -5.166 |
| w31 | 14 | 0.054876 | 4.252 |
| w32 | 17 | 0.050686 | 2.371 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 10 | 0.122498 | 6.516 |
| w8 | 15 | 0.025721 | 0.555 |
| w9 | 22 | 0.025005 | 2.863 |
| w10 | 9 | 0.081693 | 1.265 |
| w11 | 10 | 0.024455 | -1.206 |
| w12 | 13 | 0.03106 | -0.634 |
| w13 | 7 | 0.09822 | 3.878 |
| w14 | 4 | -0.004623 | -1.501 |
| w15 | 4 | 0.02362 | -0.032 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.095548 | 3.51 |
| w18 | 8 | -0.025438 | -1.616 |
| w19 | 18 | -0.009642 | -2.594 |
| w20 | 21 | 0.160484 | 17.889 |
| w21 | 11 | -0.046404 | -3.458 |
| w22 | 4 | -0.02266 | -1.654 |
| w23 | 4 | 0.059226 | 2.769 |
| w24 | 5 | 0.035405 | -0.086 |
| w25 | 0 | None | 0.0 |
| w26 | 18 | 0.14523 | 11.19 |
| w27 | 2 | -0.150331 | -4.606 |
| w28 | 23 | -0.041183 | -6.87 |
| w29 | 0 | None | 0.0 |
| w30 | 8 | 0.043957 | 0.524 |
| w31 | 11 | -0.113076 | -9.643 |
| w32 | 15 | 0.167521 | 25.271 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 5 | -0.048649 | -2.018 |
| w3 | 15 | 0.014431 | 4.588 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | 0.020381 | -0.144 |
| w6 | 0 | None | 0.0 |
| w7 | 10 | 0.063791 | 3.92 |
| w8 | 18 | 0.107013 | 13.201 |
| w9 | 22 | 0.173391 | 33.713 |
| w10 | 3 | 0.206107 | 3.356 |
| w11 | 9 | 0.009026 | -0.081 |
| w12 | 17 | 0.027986 | 3.378 |
| w13 | 8 | 0.03154 | -0.025 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.047453 | -1.659 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | 0.084139 | 2.192 |
| w18 | 1 | 0.020562 | 0.612 |
| w19 | 12 | -0.108051 | -7.5 |
| w20 | 17 | -0.037612 | -3.376 |
| w21 | 14 | 0.013278 | 0.662 |
| w22 | 1 | -0.02418 | -0.143 |
| w23 | 4 | -0.060712 | -2.061 |
| w24 | 9 | -0.017046 | -5.371 |
| w25 | 0 | None | 0.0 |
| w26 | 13 | 0.075112 | 6.245 |
| w27 | 5 | -0.043492 | -3.073 |
| w28 | 17 | 0.079641 | 10.144 |
| w29 | 0 | None | 0.0 |
| w30 | 16 | -0.067849 | -3.249 |
| w31 | 15 | -0.006414 | 1.593 |
| w32 | 10 | 0.025226 | 0.781 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 1 | 0.07901 | 0.831 |
| w11 | 13 | -0.08281 | -6.494 |
| w12 | 15 | 0.032463 | 2.234 |
| w13 | 5 | 0.142082 | 5.363 |
| w14 | 0 | None | 0.0 |
| w15 | 9 | -0.02603 | -5.015 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.055514 | 0.908 |
| w18 | 19 | 0.09347 | 14.363 |
| w19 | 17 | 0.01374 | 0.874 |
| w20 | 19 | -0.01482 | -0.521 |
| w21 | 24 | -0.029579 | -2.442 |
| w22 | 1 | -0.029478 | -0.555 |
| w23 | 11 | 0.105789 | 10.962 |
| w24 | 8 | 0.031111 | -3.093 |
| w25 | 3 | -0.018899 | -0.874 |
| w26 | 17 | 0.155638 | 14.262 |
| w27 | 4 | -0.039586 | -4.925 |
| w28 | 16 | -0.064626 | -13.095 |
| w29 | 7 | 0.024841 | -0.578 |
| w30 | 17 | -0.08488 | -3.574 |
| w31 | 16 | -0.077393 | -6.253 |
| w32 | 10 | -0.008537 | -1.057 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 9 | 0.032002 | -1.837 |
| w13 | 9 | 0.033801 | 2.946 |
| w14 | 3 | -0.041555 | -4.179 |
| w15 | 9 | -0.05064 | -4.648 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.13816 | 5.771 |
| w18 | 8 | 0.06089 | 2.063 |
| w19 | 13 | 0.078324 | 4.562 |
| w20 | 16 | 0.089478 | 9.86 |
| w21 | 11 | 0.101099 | 5.293 |
| w22 | 11 | 0.058971 | 0.362 |
| w23 | 18 | -0.09636 | -8.247 |
| w24 | 12 | -0.05648 | -15.221 |
| w25 | 6 | 0.001726 | -1.43 |
| w26 | 21 | -0.053488 | -3.683 |
| w27 | 4 | -0.030274 | -2.675 |
| w28 | 16 | -0.043313 | -4.104 |
| w29 | 1 | -0.11181 | -1.585 |
| w30 | 25 | -0.028651 | -1.613 |
| w31 | 12 | -0.051574 | -5.142 |
| w32 | 9 | -0.025827 | -2.614 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 8 | -0.039081 | -3.126 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | -0.017512 | -1.671 |
| w18 | 6 | 0.08855 | 4.73 |
| w19 | 28 | 0.004638 | 4.661 |
| w20 | 21 | -0.073505 | -8.719 |
| w21 | 12 | 0.075214 | 4.594 |
| w22 | 8 | -0.150259 | -8.921 |
| w23 | 23 | -0.054267 | -1.836 |
| w24 | 9 | -0.047108 | -10.587 |
| w25 | 4 | -0.058513 | -3.55 |
| w26 | 20 | 0.057959 | 3.234 |
| w27 | 5 | 0.028174 | -1.307 |
| w28 | 19 | -0.006053 | -0.939 |
| w29 | 5 | -0.178795 | -8.682 |
| w30 | 21 | -0.010999 | 1.884 |
| w31 | 18 | -0.105383 | -12.492 |
| w32 | 13 | -0.035519 | -3.861 |

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
| w15 | 4 | -0.052125 | -2.985 |
| w16 | 1 | -0.010493 | -0.659 |
| w17 | 13 | -0.055555 | -3.082 |
| w18 | 6 | 0.052249 | 2.239 |
| w19 | 13 | 0.057006 | 3.685 |
| w20 | 3 | -0.076732 | -2.609 |
| w21 | 13 | 0.041097 | 2.235 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 4 | 0.063904 | 1.638 |
| w26 | 1 | -0.07441 | -1.329 |
| w27 | 0 | None | 0.0 |
| w28 | 4 | -0.001536 | -0.882 |
| w29 | 0 | None | 0.0 |
| w30 | 13 | 0.027091 | 1.537 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 1 | -0.120467 | -5.708 |
| w17 | 15 | 0.213 | 12.374 |
| w18 | 5 | 0.022039 | -0.266 |
| w19 | 15 | -0.035402 | -2.906 |
| w20 | 20 | -0.01522 | -1.129 |
| w21 | 22 | -0.01754 | -3.829 |
| w22 | 2 | -0.001572 | -0.562 |
| w23 | 16 | -0.069481 | -5.71 |
| w24 | 12 | -0.021638 | -15.475 |
| w25 | 3 | -0.009912 | -1.32 |
| w26 | 18 | -0.179489 | -15.423 |
| w27 | 6 | -0.011864 | -4.653 |
| w28 | 16 | 0.019531 | 1.059 |
| w29 | 6 | -0.081508 | -3.826 |
| w30 | 17 | -0.098966 | -5.416 |
| w31 | 19 | -0.078027 | -4.719 |
| w32 | 15 | 0.154803 | 11.906 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 19 | 0.117021 | 19.939 |
| w21 | 20 | 0.132181 | 10.439 |
| w22 | 5 | -0.026412 | -2.416 |
| w23 | 17 | -0.015706 | 0.633 |
| w24 | 11 | 0.047597 | -4.703 |
| w25 | 5 | 0.082822 | 2.762 |
| w26 | 19 | 0.011432 | -1.117 |
| w27 | 4 | -0.096277 | -4.03 |
| w28 | 22 | 0.072301 | 7.69 |
| w29 | 4 | -0.067426 | -2.018 |
| w30 | 14 | -0.139496 | -7.458 |
| w31 | 13 | -0.069707 | -3.767 |
| w32 | 13 | -0.091277 | -5.765 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 8 | 0.034999 | 0.319 |
| w23 | 19 | -0.039338 | -1.442 |
| w24 | 15 | 0.067542 | -4.299 |
| w25 | 2 | -0.162276 | -7.818 |
| w26 | 12 | -0.006153 | -0.603 |
| w27 | 5 | 0.028751 | 0.137 |
| w28 | 22 | -0.013776 | 0.823 |
| w29 | 4 | -0.039822 | -1.683 |
| w30 | 16 | -0.261553 | -21.928 |
| w31 | 11 | 0.000964 | 0.176 |
| w32 | 8 | 0.077276 | 2.131 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 12 | 0.007316 | -3.086 |
| w25 | 4 | 0.013238 | -0.139 |
| w26 | 21 | -0.086406 | -8.668 |
| w27 | 0 | None | 0.0 |
| w28 | 17 | 0.07915 | 6.116 |
| w29 | 3 | -0.062165 | -1.999 |
| w30 | 21 | -0.01529 | 2.474 |
| w31 | 12 | -0.01389 | 0.285 |
| w32 | 10 | -0.037736 | -1.913 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 3 | -0.014166 | -1.575 |
| w6 | 1 | -0.080217 | -2.252 |
| w7 | 11 | 0.01417 | 0.686 |
| w8 | 16 | -0.081628 | -6.183 |
| w9 | 18 | 0.142141 | 17.606 |
| w10 | 15 | 0.132577 | 2.406 |
| w11 | 9 | 0.069896 | 3.343 |
| w12 | 26 | -0.061017 | -4.907 |
| w13 | 6 | 0.085389 | 2.157 |
| w14 | 0 | None | 0.0 |
| w15 | 8 | 0.054008 | 2.079 |
| w16 | 0 | None | 0.0 |
| w17 | 12 | 0.123384 | 7.004 |
| w18 | 1 | -0.051567 | -1.342 |
| w19 | 12 | -0.138494 | -11.669 |
| w20 | 18 | 0.07637 | 5.512 |
| w21 | 19 | -0.046042 | -2.702 |
| w22 | 9 | -0.029935 | -2.415 |
| w23 | 14 | 0.058303 | 7.535 |
| w24 | 8 | -0.061819 | -4.211 |
| w25 | 8 | -0.114507 | -6.532 |
| w26 | 7 | -0.033408 | -4.766 |
| w27 | 2 | -0.077289 | -3.12 |
| w28 | 11 | -0.092872 | -6.92 |
| w29 | 7 | 0.031149 | 0.95 |
| w30 | 0 | None | 0.0 |
| w31 | 18 | -0.090933 | -6.55 |
| w32 | 2 | -0.00828 | -0.457 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.016137 | -0.118 |
| w7 | 15 | 0.162146 | 9.676 |
| w8 | 26 | 0.037363 | 3.407 |
| w9 | 22 | 0.242206 | 41.988 |
| w10 | 6 | 0.043205 | 0.254 |
| w11 | 6 | 0.0364 | 0.772 |
| w12 | 17 | -0.084641 | -6.384 |
| w13 | 7 | 0.122665 | 4.899 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.040572 | 1.35 |
| w18 | 9 | 0.045648 | 2.432 |
| w19 | 11 | 0.087767 | 4.435 |
| w20 | 14 | -0.052803 | -5.931 |
| w21 | 6 | 0.060377 | 1.927 |
| w22 | 3 | -0.206705 | -8.638 |
| w23 | 4 | -0.101114 | -7.297 |
| w24 | 6 | -0.069969 | -5.152 |
| w25 | 11 | 0.008389 | -1.878 |
| w26 | 2 | 0.065676 | 1.23 |
| w27 | 2 | -0.008139 | -1.352 |
| w28 | 0 | None | 0.0 |
| w29 | 6 | -0.082909 | -8.954 |
| w30 | 1 | -0.00673 | -0.479 |
| w31 | 14 | 0.006539 | 0.037 |
| w32 | 7 | 0.022323 | -0.257 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 10 | 0.159632 | 6.926 |
| w18 | 0 | None | 0.0 |
| w19 | 15 | 0.011599 | 1.835 |
| w20 | 12 | -0.098291 | -9.564 |
| w21 | 21 | 0.018775 | -0.597 |
| w22 | 4 | -0.012227 | -1.541 |
| w23 | 13 | 0.113168 | 11.513 |
| w24 | 8 | -0.028044 | -4.527 |
| w25 | 9 | 0.028132 | 0.581 |
| w26 | 17 | 0.057311 | 8.742 |
| w27 | 4 | -0.035307 | -5.322 |
| w28 | 13 | 0.014509 | 0.047 |
| w29 | 4 | -0.0445 | -2.076 |
| w30 | 21 | -0.097863 | -6.978 |
| w31 | 19 | -0.058291 | -2.996 |
| w32 | 7 | -0.056473 | -6.388 |

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
| w17 | 8 | 0.10696 | 4.368 |
| w18 | 16 | 0.070288 | 9.121 |
| w19 | 11 | 0.030699 | 1.962 |
| w20 | 11 | -0.028757 | -2.079 |
| w21 | 18 | 0.12362 | 8.729 |
| w22 | 7 | 0.014328 | -0.543 |
| w23 | 11 | 0.095597 | 9.866 |
| w24 | 5 | 0.001864 | -3.411 |
| w25 | 5 | -0.057066 | -1.792 |
| w26 | 5 | -0.080848 | -5.145 |
| w27 | 0 | None | 0.0 |
| w28 | 18 | 0.130255 | 12.141 |
| w29 | 0 | None | 0.0 |
| w30 | 18 | -0.110723 | -6.989 |
| w31 | 19 | -0.100489 | -8.123 |
| w32 | 9 | 0.107599 | 4.96 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 14 | 0.015287 | 2.421 |
| w20 | 17 | 0.145767 | 18.59 |
| w21 | 6 | 0.052369 | 1.553 |
| w22 | 0 | -0.012228 | 0.0 |
| w23 | 2 | 0.041654 | 1.071 |
| w24 | 6 | 0.010861 | -6.06 |
| w25 | 7 | 0.000799 | -0.536 |
| w26 | 13 | 0.055819 | 2.601 |
| w27 | 4 | 0.016086 | -0.229 |
| w28 | 20 | -0.020445 | -1.741 |
| w29 | 3 | -0.147005 | -5.514 |
| w30 | 20 | 0.040309 | 7.162 |
| w31 | 20 | -0.037828 | -3.818 |
| w32 | 3 | -0.172991 | -12.135 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 3 | 0.030188 | 0.039 |
| w23 | 15 | 0.191811 | 11.747 |
| w24 | 12 | -0.021598 | -9.597 |
| w25 | 3 | 0.039743 | 1.272 |
| w26 | 16 | 0.093354 | 6.951 |
| w27 | 5 | 0.00298 | -1.269 |
| w28 | 14 | 0.165987 | 12.724 |
| w29 | 7 | -0.24166 | -11.852 |
| w30 | 18 | -0.04978 | -2.955 |
| w31 | 18 | 0.032971 | 2.941 |
| w32 | 6 | -0.045672 | -4.07 |

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
| w27 | 4 | 0.036401 | -0.664 |
| w28 | 15 | 0.072837 | 5.749 |
| w29 | 3 | -0.069792 | -2.409 |
| w30 | 22 | -0.01349 | 3.535 |
| w31 | 19 | -0.08245 | -4.673 |
| w32 | 3 | -0.242198 | -8.136 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 10 | -0.118779 | -5.323 |
| w18 | 15 | 0.032691 | 3.935 |
| w19 | 19 | 0.033077 | 3.341 |
| w20 | 20 | 0.113462 | 14.767 |
| w21 | 16 | 0.024488 | 1.81 |
| w22 | 2 | 0.035801 | 0.452 |
| w23 | 13 | -0.046617 | -4.0 |
| w24 | 12 | -0.050042 | -13.895 |
| w25 | 2 | 0.058171 | 0.591 |
| w26 | 16 | 0.141117 | 11.072 |
| w27 | 4 | -0.009324 | -1.196 |
| w28 | 19 | -0.068397 | -4.792 |
| w29 | 4 | -0.058684 | -2.246 |
| w30 | 19 | -0.151831 | -18.581 |
| w31 | 19 | -0.006689 | -1.166 |
| w32 | 13 | -0.066638 | -8.904 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 19 | 0.188019 | 14.866 |
| w18 | 4 | -0.100606 | -3.427 |
| w19 | 20 | 0.070247 | 5.683 |
| w20 | 21 | 0.070763 | 6.556 |
| w21 | 15 | 0.050706 | 3.709 |
| w22 | 3 | 0.028042 | 0.329 |
| w23 | 15 | -0.017733 | -1.951 |
| w24 | 14 | -0.025553 | -12.744 |
| w25 | 0 | None | 0.0 |
| w26 | 21 | 0.064043 | 5.233 |
| w27 | 5 | -0.006979 | -1.732 |
| w28 | 19 | 0.096824 | 9.438 |
| w29 | 4 | -0.02487 | -1.243 |
| w30 | 29 | -0.037446 | 1.417 |
| w31 | 20 | -0.01391 | -1.865 |
| w32 | 14 | 0.05464 | 3.82 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 17 | 0.098151 | 8.363 |
| w29 | 2 | -0.167721 | -3.035 |
| w30 | 10 | -0.001491 | 1.094 |
| w31 | 12 | 0.020887 | 0.231 |
| w32 | 17 | 0.137022 | 8.257 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 0 | None | 0.0 |
| w15 | 16 | 0.051303 | 0.87 |
| w16 | 0 | None | 0.0 |
| w17 | 10 | -0.181009 | -10.516 |
| w18 | 7 | 0.069275 | 4.904 |
| w19 | 15 | 0.005569 | 1.05 |
| w20 | 18 | -0.060619 | -4.496 |
| w21 | 12 | -0.027265 | -3.963 |
| w22 | 5 | -0.159419 | -8.105 |
| w23 | 10 | 0.128036 | 9.265 |
| w24 | 8 | -0.006158 | -2.887 |
| w25 | 2 | -0.025412 | -1.44 |
| w26 | 19 | -0.054866 | -4.244 |
| w27 | 4 | -0.01876 | -3.047 |
| w28 | 21 | 0.065384 | 8.09 |
| w29 | 4 | -0.148432 | -6.893 |
| w30 | 17 | -0.030525 | 0.235 |
| w31 | 12 | -0.011361 | -1.18 |
| w32 | 15 | -0.141576 | -10.554 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 6 | -0.012503 | -3.865 |
| w26 | 8 | 0.078912 | 3.018 |
| w27 | 5 | -0.029464 | -3.467 |
| w28 | 23 | 0.069339 | 7.038 |
| w29 | 1 | -0.038296 | -0.986 |
| w30 | 24 | -0.046318 | -0.304 |
| w31 | 13 | 0.018955 | -0.298 |
| w32 | 8 | -0.054787 | -4.957 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

