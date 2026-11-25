# Backtest of 058-03_calm-rise-stretch-continuation_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/058-03_calm-rise-stretch-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.049841 | -2.001 |
| w2 | 2 | -0.017087 | -3.683 |
| w3 | 3 | -0.053688 | -27.877 |
| w4 | 19 | 0.002865 | 30.764 |
| w5 | 5 | -0.111997 | -9.893 |
| w6 | 5 | 0.183645 | 34.917 |
| w7 | 7 | -0.047556 | -9.369 |
| w8 | 7 | 0.111014 | 24.665 |
| w9 | 1 | -0.008497 | -0.155 |
| w10 | 14 | -0.036436 | 22.555 |
| w11 | 6 | -0.083322 | -3.075 |
| w12 | 16 | -0.221023 | -13.866 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | -0.058763 | -6.922 |
| w15 | 8 | 0.215958 | 50.182 |
| w16 | 17 | -0.022701 | 0.927 |
| w17 | 22 | 0.016677 | 50.22 |
| w18 | 17 | 0.072859 | 9.761 |
| w19 | 8 | 0.152368 | 39.239 |
| w20 | 0 | None | 0.0 |
| w21 | 18 | 0.115011 | 30.532 |
| w22 | 8 | -0.083303 | -4.351 |
| w23 | 34 | -0.057612 | -4.193 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.077706 | 6.736 |
| w2 | 1 | -0.151407 | -1.208 |
| w3 | 3 | -0.071015 | -3.186 |
| w4 | 38 | -0.106467 | 15.644 |
| w5 | 3 | -0.207128 | -12.014 |
| w6 | 6 | 0.122927 | 28.59 |
| w7 | 2 | -0.064064 | -0.526 |
| w8 | 21 | -0.059452 | -0.951 |
| w9 | 3 | -0.052397 | -2.97 |
| w10 | 22 | 0.156142 | 67.167 |
| w11 | 13 | -0.082066 | 5.965 |
| w12 | 32 | -0.048172 | -7.314 |
| w13 | 3 | -0.09324 | -8.781 |
| w14 | 2 | -0.03115 | -5.141 |
| w15 | 15 | 0.189015 | 50.798 |
| w16 | 9 | 0.085902 | 52.806 |
| w17 | 8 | 0.100407 | 35.088 |
| w18 | 10 | 0.012222 | 6.013 |
| w19 | 11 | 0.210336 | 63.805 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.115039 | -4.507 |
| w23 | 19 | 0.007126 | 38.38 |
| w24 | 4 | -0.023676 | -9.443 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.013523 | -4.096 |
| w2 | 3 | -0.00311 | -0.854 |
| w3 | 11 | -0.187821 | -33.471 |
| w4 | 25 | -0.006346 | -2.031 |
| w5 | 3 | -0.045748 | -8.425 |
| w6 | 20 | -0.131555 | -13.515 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | -0.058283 | 3.151 |
| w9 | 0 | None | 0.0 |
| w10 | 7 | 0.028967 | 18.215 |
| w11 | 4 | 0.058677 | 7.776 |
| w12 | 15 | -0.077855 | -9.794 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 9 | 0.025541 | 3.625 |
| w16 | 15 | -0.006312 | 5.498 |
| w17 | 5 | -0.041487 | 0.733 |
| w18 | 6 | -0.043228 | -3.993 |
| w19 | 2 | -0.032938 | 1.43 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | 0.029693 | -7.528 |
| w22 | 0 | None | 0.0 |
| w23 | 17 | -0.112921 | -19.032 |
| w24 | 4 | -0.030992 | -1.087 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.038478 | -1.658 |
| w2 | 1 | -0.038559 | -1.432 |
| w3 | 4 | -0.249798 | -3.475 |
| w4 | 17 | 0.013418 | 3.458 |
| w5 | 3 | -0.042426 | -3.757 |
| w6 | 19 | -0.08578 | -0.671 |
| w7 | 0 | None | 0.0 |
| w8 | 28 | 0.03393 | 19.028 |
| w9 | 0 | None | 0.0 |
| w10 | 29 | -0.021735 | 17.729 |
| w11 | 10 | 0.030834 | 18.263 |
| w12 | 3 | -0.192293 | -8.853 |
| w14 | 0 | -0.016079 | 0.0 |
| w15 | 11 | 0.136627 | 19.809 |
| w16 | 20 | -0.025122 | 7.415 |
| w17 | 23 | -0.008307 | 15.858 |
| w18 | 9 | -0.028308 | -3.836 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | -0.013975 | 9.364 |
| w21 | 5 | 0.296256 | 19.308 |
| w22 | 6 | -0.117021 | -6.627 |
| w23 | 5 | 0.223041 | 44.443 |
| w24 | 6 | -0.190213 | -9.253 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.008743 | -1.444 |
| w2 | 0 | -0.012982 | 0.0 |
| w3 | 0 | -0.111171 | 0.0 |
| w4 | 0 | -0.054679 | 0.0 |
| w5 | 0 | 0.008835 | 0.0 |
| w6 | 8 | 0.107163 | 22.445 |
| w8 | 1 | -0.048735 | -8.397 |
| w9 | 5 | -0.110277 | -6.548 |
| w10 | 10 | 0.179853 | 36.7 |
| w11 | 0 | None | 0.0 |
| w12 | 13 | -0.080511 | -11.048 |
| w14 | 4 | -0.075205 | -4.276 |
| w15 | 5 | -0.066554 | -4.516 |
| w16 | 5 | 0.032815 | 4.657 |
| w17 | 2 | 0.236464 | 117.605 |
| w18 | 6 | -0.000908 | 7.655 |
| w19 | 2 | -0.210484 | -7.121 |
| w20 | 0 | None | 0.0 |
| w21 | 1 | 0.193441 | 120.306 |
| w22 | 1 | -0.097721 | -4.287 |
| w23 | 9 | 0.064716 | 9.81 |
| w24 | 2 | -0.013897 | 0.703 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.142897 | -3.885 |
| w2 | 3 | -0.048703 | -7.273 |
| w3 | 1 | -0.029488 | -1.04 |
| w4 | 17 | -0.065257 | -12.949 |
| w5 | 0 | -0.025972 | 0.0 |
| w6 | 22 | -0.1093 | -3.194 |
| w7 | 4 | -0.07091 | -3.35 |
| w8 | 11 | 0.127122 | 21.628 |
| w9 | 0 | None | 0.0 |
| w10 | 30 | 0.063386 | 39.695 |
| w11 | 14 | 0.001791 | 12.469 |
| w12 | 14 | -0.154289 | -23.311 |
| w13 | 0 | None | 0.0 |
| w14 | 2 | -0.04886 | -10.098 |
| w15 | 20 | 0.061085 | 19.576 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.079719 | 6.254 |
| w18 | 6 | -0.021965 | -5.459 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | -0.099932 | -16.238 |
| w22 | 1 | -0.099117 | -1.833 |
| w23 | 13 | -0.008912 | -0.153 |
| w24 | 8 | -0.091227 | 25.933 |

