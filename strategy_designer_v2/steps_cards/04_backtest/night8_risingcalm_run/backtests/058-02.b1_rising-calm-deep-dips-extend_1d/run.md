# Backtest of 058-02.b1_rising-calm-deep-dips-extend_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/058-02.b1_rising-calm-deep-dips-extend_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.040545 | 1.342 |
| w2 | 5 | 0.171735 | 13.492 |
| w3 | 0 | None | 0.0 |
| w4 | 33 | 0.084418 | -33.445 |
| w5 | 23 | 0.042168 | 24.633 |
| w6 | 5 | 0.155726 | -0.37 |
| w7 | 8 | -0.009963 | 6.392 |
| w8 | 13 | -0.032113 | -19.21 |
| w9 | 1 | 0.008497 | 0.12 |
| w10 | 29 | -0.020902 | -16.09 |
| w11 | 12 | 0.067847 | 6.778 |
| w12 | 34 | -0.049582 | 6.414 |
| w13 | 0 | None | 0.0 |
| w14 | 2 | -0.045823 | 2.158 |
| w15 | 9 | -0.146637 | -22.912 |
| w16 | 27 | 0.011755 | 1.41 |
| w17 | 29 | 0.085391 | -32.713 |
| w18 | 15 | -0.133739 | -18.184 |
| w19 | 10 | -0.023868 | -18.795 |
| w20 | 0 | None | 0.0 |
| w21 | 15 | 0.111148 | -1.158 |
| w22 | 6 | 0.037643 | -0.123 |
| w23 | 50 | 0.070521 | 8.591 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.018515 | 9.808 |
| w2 | 2 | 0.124254 | 8.435 |
| w3 | 1 | 0.188445 | 6.492 |
| w4 | 52 | -0.005347 | -26.919 |
| w5 | 7 | -0.020556 | 16.505 |
| w6 | 12 | -0.176117 | -15.596 |
| w7 | 19 | 0.000367 | 11.542 |
| w8 | 36 | -0.117479 | -28.674 |
| w9 | 0 | None | 0.0 |
| w10 | 42 | -0.064701 | -45.592 |
| w11 | 15 | 0.005379 | -23.026 |
| w12 | 39 | -0.051812 | -7.105 |
| w13 | 2 | 0.091156 | 3.338 |
| w14 | 2 | 0.001122 | 13.794 |
| w15 | 28 | -0.068479 | -24.828 |
| w16 | 12 | -0.021293 | -16.89 |
| w17 | 11 | -0.118593 | -25.715 |
| w18 | 10 | -0.09843 | -8.668 |
| w19 | 17 | -0.167997 | -24.344 |
| w20 | 7 | 0.003561 | 14.78 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.04115 | 1.48 |
| w23 | 29 | 0.108703 | -15.775 |
| w24 | 9 | 0.093559 | 15.037 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.020724 | 6.01 |
| w2 | 6 | 0.088571 | 8.917 |
| w3 | 20 | 0.09851 | 19.208 |
| w4 | 29 | -0.012629 | -7.037 |
| w5 | 6 | -0.00657 | 11.427 |
| w6 | 15 | 0.104329 | 9.827 |
| w7 | 0 | None | 0.0 |
| w8 | 20 | -0.134892 | -32.587 |
| w9 | 0 | None | 0.0 |
| w10 | 21 | -0.172591 | -16.982 |
| w11 | 6 | -0.143654 | -19.409 |
| w12 | 20 | 0.118605 | 1.861 |
| w13 | 3 | -0.073904 | 6.178 |
| w14 | 0 | None | 0.0 |
| w15 | 25 | 0.069345 | 5.166 |
| w16 | 17 | -0.022143 | -3.588 |
| w17 | 4 | -0.008717 | -11.928 |
| w18 | 7 | -0.045778 | -1.107 |
| w19 | 3 | 0.162659 | 1.462 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.03179 | 0.276 |
| w22 | 0 | None | 0.0 |
| w23 | 31 | -0.078642 | -1.423 |
| w24 | 11 | -0.08184 | -1.565 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.018778 | -0.637 |
| w2 | 10 | -0.063035 | -0.492 |
| w3 | 5 | -0.188094 | -7.139 |
| w4 | 22 | 0.037543 | -5.574 |
| w5 | 13 | 0.205904 | 15.375 |
| w6 | 25 | -0.02166 | -23.059 |
| w7 | 0 | None | 0.0 |
| w8 | 24 | -0.043897 | -26.685 |
| w9 | 0 | None | 0.0 |
| w10 | 40 | -0.200431 | -43.589 |
| w11 | 10 | -0.098239 | -28.473 |
| w12 | 0 | -0.008212 | 0.0 |
| w14 | 6 | -0.045535 | -1.021 |
| w15 | 16 | 0.038536 | -22.065 |
| w16 | 12 | 0.051953 | -2.657 |
| w17 | 37 | -0.156789 | -30.419 |
| w18 | 5 | -0.001072 | 6.59 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | -0.145072 | -17.792 |
| w21 | 2 | 0.017523 | 0.117 |
| w22 | 4 | -0.003116 | 7.177 |
| w23 | 14 | -0.093305 | -22.709 |
| w24 | 7 | -0.036574 | 2.632 |

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
| w1 | 10 | 0.020656 | 4.882 |
| w2 | 0 | 0.189529 | 0.0 |
| w3 | 0 | 0.057291 | 0.0 |
| w4 | 0 | 0.014422 | 0.0 |
| w5 | 6 | -0.018705 | -41.162 |
| w6 | 13 | 0.069623 | 4.807 |
| w8 | 4 | -0.072093 | 3.326 |
| w9 | 7 | 0.065676 | 4.124 |
| w10 | 23 | -0.105275 | -8.075 |
| w11 | 0 | None | 0.0 |
| w12 | 29 | 0.009665 | 27.338 |
| w14 | 12 | -0.015775 | -1.819 |
| w15 | 16 | 0.081952 | 10.238 |
| w16 | 4 | -0.044686 | -8.115 |
| w17 | 5 | 0.076998 | -68.599 |
| w18 | 11 | -0.072599 | -5.688 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | 0.004505 | -2.653 |
| w22 | 4 | 0.054163 | 10.209 |
| w23 | 22 | 0.004206 | 5.076 |
| w24 | 4 | -0.128117 | -3.89 |

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
| w1 | 11 | 0.103073 | 19.414 |
| w2 | 5 | 0.059713 | 16.19 |
| w3 | 1 | 0.040273 | 2.895 |
| w4 | 13 | 0.181224 | 9.081 |
| w5 | 4 | 0.113515 | 14.336 |
| w6 | 19 | -0.043772 | -5.406 |
| w7 | 5 | 0.013026 | 9.56 |
| w8 | 19 | -0.005285 | 0.055 |
| w9 | 0 | None | 0.0 |
| w10 | 47 | -0.230307 | -50.397 |
| w11 | 11 | 0.045265 | -12.723 |
| w12 | 16 | 0.061276 | -23.739 |
| w13 | 0 | None | 0.0 |
| w14 | 4 | -0.006123 | 16.394 |
| w15 | 30 | -0.091969 | -17.837 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | -0.335031 | -10.496 |
| w18 | 7 | -0.048603 | -5.937 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 7 | 0.073959 | -9.734 |
| w22 | 3 | 0.082074 | 6.502 |
| w23 | 14 | 0.002494 | -12.477 |
| w24 | 7 | -0.052306 | -36.857 |

