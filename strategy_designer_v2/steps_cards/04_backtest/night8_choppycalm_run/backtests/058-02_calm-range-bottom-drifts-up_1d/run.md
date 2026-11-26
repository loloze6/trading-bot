# Backtest of 058-02_calm-range-bottom-drifts-up_1d

- Plan: `../../../../03_test_plan/night8_choppycalm_run/plans/058-02_calm-range-bottom-drifts-up_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.018165 | -3.087 |
| w2 | 11 | 0.015892 | -22.791 |
| w3 | 5 | 0.005087 | -3.923 |
| w4 | 1 | 0.050808 | 4.693 |
| w5 | 26 | 0.068159 | -14.515 |
| w6 | 4 | 0.024187 | 5.564 |
| w7 | 24 | -0.027598 | -13.914 |
| w8 | 9 | 0.080226 | 8.795 |
| w9 | 5 | -0.054298 | -5.086 |
| w10 | 13 | 0.04743 | 3.493 |
| w11 | 5 | -0.005274 | 1.833 |
| w12 | 1 | -0.19493 | -4.764 |
| w13 | 3 | 0.028489 | 11.606 |
| w14 | 16 | -0.029574 | -20.584 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | -0.168063 | -25.542 |
| w17 | 4 | 0.002457 | 4.028 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 15 | -0.107374 | -12.185 |
| w21 | 7 | 0.01745 | 9.912 |
| w22 | 17 | -0.02412 | -10.997 |
| w23 | 12 | -0.013074 | 4.128 |
| w24 | 12 | 0.131929 | 1.469 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.064803 | -0.417 |
| w2 | 7 | -0.159378 | -22.287 |
| w3 | 6 | 0.046143 | 1.125 |
| w4 | 4 | 0.102047 | 13.192 |
| w5 | 33 | 0.002804 | -18.077 |
| w6 | 4 | 0.008119 | 3.962 |
| w7 | 8 | 0.073554 | 0.188 |
| w8 | 11 | -0.087098 | -3.015 |
| w9 | 5 | -0.097564 | -3.363 |
| w10 | 5 | 0.026324 | 3.516 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.016921 | 0.683 |
| w13 | 1 | -0.057662 | -5.133 |
| w14 | 1 | -0.180469 | -5.255 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | 0.024155 | 4.493 |
| w18 | 2 | 0.068301 | 1.47 |
| w19 | 0 | None | 0.0 |
| w20 | 12 | -0.104592 | -8.438 |
| w21 | 17 | 0.127423 | 38.321 |
| w22 | 1 | -0.00539 | 3.758 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.146341 | 7.134 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.012371 | -10.633 |
| w2 | 11 | 0.075919 | -13.389 |
| w3 | 14 | -0.002902 | 9.296 |
| w4 | 10 | -0.159528 | -0.614 |
| w5 | 16 | -0.170129 | -23.226 |
| w6 | 23 | 0.19501 | 37.408 |
| w7 | 15 | 0.038118 | -4.502 |
| w8 | 2 | 0.04074 | 1.187 |
| w9 | 0 | None | 0.0 |
| w10 | 21 | 0.019818 | 15.503 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.107839 | 3.281 |
| w13 | 4 | -0.020258 | -2.178 |
| w14 | 11 | -0.026165 | -16.411 |
| w15 | 2 | -0.214259 | 3.844 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 6 | 0.034061 | 10.16 |
| w20 | 4 | -0.08277 | -9.805 |
| w21 | 13 | 0.015632 | 19.882 |
| w22 | 0 | None | 0.0 |
| w23 | 12 | -0.121656 | -3.671 |
| w24 | 5 | 0.021962 | 6.138 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.083281 | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 20 | 0.089792 | 4.118 |
| w4 | 22 | 0.031963 | 11.396 |
| w5 | 37 | 0.070496 | -5.483 |
| w6 | 4 | -0.024884 | 2.81 |
| w7 | 15 | -0.130746 | -11.882 |
| w8 | 14 | 0.115262 | 10.307 |
| w9 | 11 | -0.116156 | -21.295 |
| w10 | 11 | 0.011963 | 4.594 |
| w11 | 0 | None | 0.0 |
| w12 | 19 | 0.124906 | -5.169 |
| w14 | 18 | 0.055103 | -2.443 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | 0.053914 | 0.0 |
| w19 | 4 | -0.136541 | -12.357 |
| w20 | 6 | -0.126616 | -6.377 |
| w21 | 16 | -0.080907 | -12.093 |
| w22 | 7 | -0.223927 | -4.623 |
| w23 | 10 | -0.098806 | -25.843 |
| w24 | 6 | 0.021986 | 4.612 |

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
| w1 | 11 | 0.008454 | -7.716 |
| w2 | 0 | 0.024607 | 0.0 |
| w3 | 0 | 0.068407 | 0.0 |
| w4 | 0 | 0.067256 | 0.0 |
| w5 | 11 | -0.01118 | 0.328 |
| w6 | 5 | 0.124913 | 11.809 |
| w8 | 24 | 0.032703 | 5.067 |
| w9 | 10 | -0.04196 | -8.752 |
| w10 | 10 | -0.085112 | -7.052 |
| w11 | 0 | None | 0.0 |
| w12 | 15 | 0.040612 | -11.53 |
| w14 | 1 | -0.123197 | -5.023 |
| w15 | 10 | 0.044349 | 9.466 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.030625 | 6.641 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 10 | 0.006503 | 2.452 |
| w21 | 6 | 0.005449 | 9.043 |
| w22 | 0 | None | 0.0 |
| w23 | 21 | 0.013428 | 12.339 |
| w24 | 5 | 0.045329 | 1.759 |

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
| w1 | 8 | -0.041373 | -4.106 |
| w2 | 7 | 0.062295 | 2.171 |
| w3 | 13 | 0.142991 | 4.943 |
| w4 | 15 | 0.03903 | 0.09 |
| w5 | 22 | -0.088582 | -15.948 |
| w6 | 9 | 0.136011 | 24.659 |
| w7 | 2 | 0.141246 | 6.14 |
| w8 | 6 | 0.171729 | 7.37 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | -0.032525 | 0.651 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.017187 | -1.493 |
| w13 | 0 | None | 0.0 |
| w14 | 3 | -0.089327 | -18.361 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.067023 | 8.103 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | 0.002693 | -2.048 |
| w21 | 5 | 0.003853 | -0.688 |
| w22 | 2 | -0.042239 | 3.076 |
| w23 | 10 | 0.108517 | 4.09 |
| w24 | 0 | -0.011454 | 0.0 |

