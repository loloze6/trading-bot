# Backtest of 058-03.e1_calm-rise-stretch-ten-days_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/058-03.e1_calm-rise-stretch-ten-days_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.049841 | -8.542 |
| w2 | 2 | -0.017087 | -4.423 |
| w3 | 3 | -0.053688 | -31.853 |
| w4 | 15 | 0.002865 | 28.746 |
| w5 | 5 | -0.111997 | -8.378 |
| w6 | 4 | 0.183645 | 38.362 |
| w7 | 7 | -0.047556 | -18.59 |
| w8 | 7 | 0.111014 | 32.215 |
| w9 | 1 | -0.008497 | -3.013 |
| w10 | 15 | -0.036436 | 19.848 |
| w11 | 4 | -0.083322 | -9.982 |
| w12 | 12 | -0.221023 | -16.014 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | -0.058763 | -9.023 |
| w15 | 8 | 0.215958 | 47.405 |
| w16 | 9 | -0.022701 | 4.661 |
| w17 | 20 | 0.016677 | 66.76 |
| w18 | 10 | 0.072859 | 15.839 |
| w19 | 8 | 0.152368 | 51.054 |
| w20 | 0 | None | 0.0 |
| w21 | 19 | 0.115011 | 53.19 |
| w22 | 5 | -0.083303 | -1.139 |
| w23 | 27 | -0.057612 | -7.656 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.077706 | 6.462 |
| w2 | 1 | -0.151407 | -1.981 |
| w3 | 3 | -0.071015 | -8.467 |
| w4 | 21 | -0.106467 | 31.357 |
| w5 | 3 | -0.207128 | -13.256 |
| w6 | 6 | 0.122927 | 27.541 |
| w7 | 1 | -0.064064 | -0.975 |
| w8 | 18 | -0.059452 | 0.393 |
| w9 | 2 | -0.052397 | -3.282 |
| w10 | 17 | 0.156142 | 71.123 |
| w11 | 9 | -0.082066 | 16.723 |
| w12 | 14 | -0.048172 | -6.847 |
| w13 | 3 | -0.09324 | -9.844 |
| w14 | 2 | -0.03115 | -14.768 |
| w15 | 14 | 0.189015 | 38.541 |
| w16 | 5 | 0.085902 | 56.763 |
| w17 | 11 | 0.100407 | 33.744 |
| w18 | 7 | 0.012222 | 8.294 |
| w19 | 12 | 0.210336 | 53.709 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.115039 | -2.859 |
| w23 | 18 | 0.007126 | 42.481 |
| w24 | 5 | -0.023676 | -10.244 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.013523 | -3.343 |
| w2 | 4 | -0.00311 | -3.716 |
| w3 | 8 | -0.187821 | -29.65 |
| w4 | 16 | -0.006346 | -1.087 |
| w5 | 3 | -0.045748 | -4.631 |
| w6 | 15 | -0.131555 | -14.498 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | -0.058283 | 13.009 |
| w9 | 0 | None | 0.0 |
| w10 | 7 | 0.028967 | 11.866 |
| w11 | 4 | 0.058677 | 13.019 |
| w12 | 15 | -0.077855 | -12.068 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 6 | 0.025541 | 5.048 |
| w16 | 10 | -0.006312 | 15.8 |
| w17 | 5 | -0.041487 | 17.231 |
| w18 | 3 | -0.043228 | -5.295 |
| w19 | 2 | -0.032938 | 31.191 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | 0.029693 | -4.819 |
| w22 | 0 | None | 0.0 |
| w23 | 13 | -0.112921 | -12.749 |
| w24 | 4 | -0.030992 | -2.842 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.038478 | -4.829 |
| w2 | 1 | -0.038559 | -2.766 |
| w3 | 4 | -0.249798 | -5.388 |
| w4 | 14 | 0.013418 | 6.008 |
| w5 | 3 | -0.042426 | -7.452 |
| w6 | 16 | -0.08578 | -7.837 |
| w7 | 0 | None | 0.0 |
| w8 | 21 | 0.03393 | 22.027 |
| w9 | 0 | None | 0.0 |
| w10 | 23 | -0.021735 | 36.829 |
| w11 | 11 | 0.030834 | 22.576 |
| w12 | 3 | -0.192293 | -15.698 |
| w14 | 0 | -0.016079 | 0.0 |
| w15 | 11 | 0.136627 | 13.529 |
| w16 | 10 | -0.025122 | 10.167 |
| w17 | 10 | -0.008307 | 25.101 |
| w18 | 7 | -0.028308 | -0.187 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.013975 | 3.234 |
| w21 | 5 | 0.296256 | 7.724 |
| w22 | 5 | -0.117021 | -8.256 |
| w23 | 5 | 0.223041 | 44.608 |
| w24 | 6 | -0.190213 | -9.045 |

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
| w1 | 2 | -0.008743 | -2.394 |
| w2 | 0 | -0.012982 | 0.0 |
| w3 | 0 | -0.111171 | 0.0 |
| w4 | 0 | -0.054679 | 0.0 |
| w5 | 0 | 0.008835 | 0.0 |
| w6 | 6 | 0.107163 | 3.966 |
| w8 | 2 | -0.048735 | -9.734 |
| w9 | 2 | -0.110277 | -5.834 |
| w10 | 9 | 0.179853 | 50.64 |
| w11 | 0 | None | 0.0 |
| w12 | 13 | -0.080511 | -18.535 |
| w14 | 4 | -0.075205 | -4.833 |
| w15 | 4 | -0.066554 | -6.81 |
| w16 | 3 | 0.032815 | 6.33 |
| w17 | 2 | 0.236464 | 164.445 |
| w18 | 5 | -0.000908 | 10.163 |
| w19 | 2 | -0.210484 | 3.857 |
| w20 | 0 | None | 0.0 |
| w21 | 1 | 0.193441 | 150.946 |
| w22 | 1 | -0.097721 | -5.077 |
| w23 | 9 | 0.064716 | 13.941 |
| w24 | 2 | -0.013897 | 0.484 |

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
| w1 | 2 | -0.142897 | -4.396 |
| w2 | 3 | -0.048703 | -8.542 |
| w3 | 1 | -0.029488 | -3.217 |
| w4 | 14 | -0.065257 | -9.888 |
| w5 | 0 | -0.025972 | 0.0 |
| w6 | 14 | -0.1093 | 2.039 |
| w7 | 3 | -0.07091 | -11.169 |
| w8 | 11 | 0.127122 | 18.984 |
| w9 | 0 | None | 0.0 |
| w10 | 20 | 0.063386 | 51.563 |
| w11 | 10 | 0.001791 | 12.585 |
| w12 | 12 | -0.154289 | -0.542 |
| w13 | 0 | None | 0.0 |
| w14 | 2 | -0.04886 | -22.729 |
| w15 | 17 | 0.061085 | 14.898 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.079719 | 10.791 |
| w18 | 2 | -0.021965 | -4.984 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | -0.099932 | -3.57 |
| w22 | 1 | -0.099117 | -6.387 |
| w23 | 12 | -0.008912 | -3.241 |
| w24 | 3 | -0.091227 | 146.311 |

