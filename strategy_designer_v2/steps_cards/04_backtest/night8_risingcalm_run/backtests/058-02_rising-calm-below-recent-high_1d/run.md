# Backtest of 058-02_rising-calm-below-recent-high_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/058-02_rising-calm-below-recent-high_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.040545 | -1.509 |
| w2 | 6 | -0.171735 | -13.662 |
| w3 | 0 | None | 0.0 |
| w4 | 29 | -0.084418 | 31.959 |
| w5 | 23 | -0.042168 | -24.344 |
| w6 | 6 | -0.155726 | -1.303 |
| w7 | 8 | 0.009963 | -6.492 |
| w8 | 13 | 0.032113 | 21.111 |
| w9 | 1 | -0.008497 | -0.135 |
| w10 | 24 | 0.020902 | 14.604 |
| w11 | 12 | -0.067847 | -7.932 |
| w12 | 31 | 0.049582 | -9.947 |
| w13 | 0 | None | 0.0 |
| w14 | 2 | 0.045823 | -2.184 |
| w15 | 6 | 0.146637 | 24.634 |
| w16 | 22 | -0.011755 | -6.474 |
| w17 | 23 | -0.085391 | 27.609 |
| w18 | 16 | 0.133739 | 18.557 |
| w19 | 8 | 0.023868 | 20.99 |
| w20 | 0 | None | 0.0 |
| w21 | 13 | -0.111148 | -1.27 |
| w22 | 7 | -0.037643 | -0.522 |
| w23 | 43 | -0.070521 | -14.438 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.018515 | -10.213 |
| w2 | 2 | -0.124254 | -8.628 |
| w3 | 1 | -0.188445 | -6.539 |
| w4 | 45 | 0.005347 | 20.547 |
| w5 | 4 | 0.020556 | -16.798 |
| w6 | 7 | 0.176117 | 15.35 |
| w7 | 20 | -0.000367 | -11.174 |
| w8 | 33 | 0.117479 | 33.675 |
| w9 | 0 | None | 0.0 |
| w10 | 38 | 0.064701 | 66.266 |
| w11 | 14 | -0.005379 | 26.947 |
| w12 | 37 | 0.051812 | -1.433 |
| w13 | 3 | -0.091156 | -7.383 |
| w14 | 2 | -0.001122 | -13.797 |
| w15 | 27 | 0.068479 | 23.084 |
| w16 | 12 | 0.021293 | 19.127 |
| w17 | 8 | 0.118593 | 30.44 |
| w18 | 10 | 0.09843 | 8.822 |
| w19 | 14 | 0.167997 | 26.713 |
| w20 | 7 | -0.003561 | -14.258 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.04115 | -1.504 |
| w23 | 26 | -0.108703 | 13.672 |
| w24 | 10 | -0.093559 | -14.716 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.020724 | -6.384 |
| w2 | 6 | -0.088571 | -9.507 |
| w3 | 21 | -0.09851 | -19.357 |
| w4 | 27 | 0.012629 | -1.203 |
| w5 | 7 | 0.00657 | -12.833 |
| w6 | 14 | -0.104329 | -11.954 |
| w7 | 0 | None | 0.0 |
| w8 | 20 | 0.134892 | 36.395 |
| w9 | 0 | None | 0.0 |
| w10 | 22 | 0.172591 | 15.751 |
| w11 | 6 | 0.143654 | 22.169 |
| w12 | 19 | -0.118605 | -8.893 |
| w13 | 3 | 0.073904 | -6.198 |
| w14 | 0 | None | 0.0 |
| w15 | 25 | -0.069345 | -8.253 |
| w16 | 16 | 0.022143 | -1.754 |
| w17 | 4 | 0.008717 | 12.325 |
| w18 | 6 | 0.045778 | 0.215 |
| w19 | 4 | -0.162659 | -2.38 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.03179 | -0.539 |
| w22 | 0 | None | 0.0 |
| w23 | 24 | 0.078642 | -3.308 |
| w24 | 10 | 0.08184 | 0.897 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.018778 | -1.855 |
| w2 | 10 | 0.063035 | -2.699 |
| w3 | 3 | 0.188094 | 5.94 |
| w4 | 19 | -0.037543 | -3.688 |
| w5 | 14 | -0.205904 | -17.562 |
| w6 | 20 | 0.02166 | 16.144 |
| w7 | 0 | None | 0.0 |
| w8 | 23 | 0.043897 | 25.829 |
| w9 | 0 | None | 0.0 |
| w10 | 31 | 0.200431 | 56.377 |
| w11 | 8 | 0.098239 | 34.032 |
| w12 | 0 | 0.008212 | 0.0 |
| w14 | 6 | 0.045535 | 0.153 |
| w15 | 13 | -0.038536 | 10.547 |
| w16 | 13 | -0.051953 | -1.431 |
| w17 | 31 | 0.156789 | 29.278 |
| w18 | 5 | 0.001072 | -7.135 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.145072 | 14.943 |
| w21 | 2 | -0.017523 | -0.186 |
| w22 | 4 | 0.003116 | -8.341 |
| w23 | 11 | 0.093305 | 25.558 |
| w24 | 6 | 0.036574 | -5.493 |

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
| w1 | 10 | -0.020656 | -5.33 |
| w2 | 0 | -0.189529 | 0.0 |
| w3 | 0 | -0.057291 | 0.0 |
| w4 | 0 | -0.014422 | 0.0 |
| w5 | 6 | 0.018705 | 30.327 |
| w6 | 15 | -0.069623 | -6.828 |
| w8 | 3 | 0.072093 | -4.811 |
| w9 | 8 | -0.065676 | -4.752 |
| w10 | 21 | 0.105275 | 6.642 |
| w11 | 0 | None | 0.0 |
| w12 | 27 | -0.009665 | -23.607 |
| w14 | 12 | 0.015775 | 1.124 |
| w15 | 16 | -0.081952 | -10.995 |
| w16 | 4 | 0.044686 | 7.934 |
| w17 | 3 | -0.076998 | 97.587 |
| w18 | 10 | 0.072599 | 4.295 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | -0.004505 | 2.451 |
| w22 | 4 | -0.054163 | -11.686 |
| w23 | 21 | -0.004206 | -9.489 |
| w24 | 4 | 0.128117 | 3.594 |

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
| w1 | 11 | -0.103073 | -18.583 |
| w2 | 5 | -0.059713 | -15.44 |
| w3 | 1 | -0.040273 | -2.952 |
| w4 | 12 | -0.181224 | -11.75 |
| w5 | 5 | -0.113515 | -14.293 |
| w6 | 15 | 0.043772 | 1.303 |
| w7 | 5 | -0.013026 | -11.171 |
| w8 | 16 | 0.005285 | -3.52 |
| w9 | 0 | None | 0.0 |
| w10 | 45 | 0.230307 | 81.257 |
| w11 | 11 | -0.045265 | 11.052 |
| w12 | 15 | -0.061276 | 21.475 |
| w13 | 0 | None | 0.0 |
| w14 | 5 | 0.006123 | -17.974 |
| w15 | 27 | 0.091969 | 10.269 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.335031 | 9.68 |
| w18 | 7 | 0.048603 | 3.771 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 6 | -0.073959 | 6.902 |
| w22 | 3 | -0.082074 | -6.699 |
| w23 | 14 | -0.002494 | 11.724 |
| w24 | 4 | 0.052306 | 46.701 |

