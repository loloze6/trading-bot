# Backtest of 058-02.b1_calm-range-bottom-keeps-falling_1d

- Plan: `../../../../03_test_plan/night8_choppycalm_run/plans/058-02.b1_calm-range-bottom-keeps-falling_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.018165 | 1.635 |
| w2 | 12 | -0.015892 | 23.46 |
| w3 | 5 | -0.005087 | 2.589 |
| w4 | 2 | -0.050808 | -4.706 |
| w5 | 27 | -0.068159 | 9.055 |
| w6 | 4 | -0.024187 | -5.605 |
| w7 | 26 | 0.027598 | 13.5 |
| w8 | 9 | -0.080226 | -9.194 |
| w9 | 5 | 0.054298 | 5.048 |
| w10 | 13 | -0.04743 | -3.746 |
| w11 | 5 | 0.005274 | -2.866 |
| w12 | 1 | 0.19493 | 4.685 |
| w13 | 3 | -0.028489 | -11.283 |
| w14 | 16 | 0.029574 | 17.522 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | 0.168063 | 25.498 |
| w17 | 4 | -0.002457 | -4.077 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 19 | 0.107374 | 11.526 |
| w21 | 8 | -0.01745 | -9.77 |
| w22 | 18 | 0.02412 | 6.454 |
| w23 | 15 | 0.013074 | -6.291 |
| w24 | 16 | -0.131929 | -3.596 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.064803 | -0.64 |
| w2 | 5 | 0.159378 | 25.053 |
| w3 | 6 | -0.046143 | -1.31 |
| w4 | 5 | -0.102047 | -13.012 |
| w5 | 31 | -0.002804 | 16.391 |
| w6 | 5 | -0.008119 | -5.069 |
| w7 | 8 | -0.073554 | -0.616 |
| w8 | 11 | 0.087098 | 2.559 |
| w9 | 5 | 0.097564 | 3.077 |
| w10 | 5 | -0.026324 | -3.589 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.016921 | -0.732 |
| w13 | 1 | 0.057662 | 5.107 |
| w14 | 1 | 0.180469 | 5.215 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.024155 | -4.439 |
| w18 | 2 | -0.068301 | -1.472 |
| w19 | 0 | None | 0.0 |
| w20 | 11 | 0.104592 | 8.131 |
| w21 | 17 | -0.127423 | -30.574 |
| w22 | 1 | 0.00539 | -3.833 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.146341 | -7.073 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.012371 | 10.187 |
| w2 | 13 | -0.075919 | 11.277 |
| w3 | 14 | 0.002902 | -10.384 |
| w4 | 9 | 0.159528 | -0.541 |
| w5 | 16 | 0.170129 | 25.449 |
| w6 | 29 | -0.19501 | -31.303 |
| w7 | 14 | -0.038118 | 4.398 |
| w8 | 2 | -0.04074 | -1.213 |
| w9 | 0 | None | 0.0 |
| w10 | 23 | -0.019818 | -15.979 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.107839 | -3.307 |
| w13 | 4 | 0.020258 | 1.936 |
| w14 | 11 | 0.026165 | 17.293 |
| w15 | 2 | 0.214259 | -3.948 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 6 | -0.034061 | -9.969 |
| w20 | 4 | 0.08277 | 8.942 |
| w21 | 18 | -0.015632 | -18.956 |
| w22 | 0 | None | 0.0 |
| w23 | 12 | 0.121656 | 2.552 |
| w24 | 4 | -0.021962 | -6.623 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.083281 | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 18 | -0.089792 | -6.004 |
| w4 | 23 | -0.031963 | -16.101 |
| w5 | 39 | -0.070496 | -4.112 |
| w6 | 4 | 0.024884 | -3.756 |
| w7 | 15 | 0.130746 | 11.498 |
| w8 | 14 | -0.115262 | -10.451 |
| w9 | 10 | 0.116156 | 23.118 |
| w10 | 12 | -0.011963 | -5.42 |
| w11 | 0 | None | 0.0 |
| w12 | 22 | -0.124906 | 2.22 |
| w14 | 17 | -0.055103 | -0.445 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | -0.053914 | 0.0 |
| w19 | 3 | 0.136541 | 12.445 |
| w20 | 6 | 0.126616 | 5.123 |
| w21 | 16 | 0.080907 | 7.678 |
| w22 | 7 | 0.223927 | 3.837 |
| w23 | 10 | 0.098806 | 29.919 |
| w24 | 6 | -0.021986 | -4.802 |

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
| w1 | 13 | -0.008454 | 7.096 |
| w2 | 0 | -0.024607 | 0.0 |
| w3 | 0 | -0.068407 | 0.0 |
| w4 | 0 | -0.067256 | 0.0 |
| w5 | 12 | 0.01118 | -1.099 |
| w6 | 6 | -0.124913 | -12.764 |
| w8 | 28 | -0.032703 | -8.949 |
| w9 | 10 | 0.04196 | 8.636 |
| w10 | 11 | 0.085112 | 6.022 |
| w11 | 0 | None | 0.0 |
| w12 | 17 | -0.040612 | 10.201 |
| w14 | 1 | 0.123197 | 4.988 |
| w15 | 10 | -0.044349 | -9.721 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.030625 | -6.765 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 11 | -0.006503 | -4.416 |
| w21 | 6 | -0.005449 | -8.844 |
| w22 | 0 | None | 0.0 |
| w23 | 21 | -0.013428 | -13.018 |
| w24 | 5 | -0.045329 | -2.218 |

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
| w1 | 8 | 0.041373 | 2.779 |
| w2 | 7 | -0.062295 | -3.125 |
| w3 | 13 | -0.142991 | -6.924 |
| w4 | 16 | -0.03903 | -3.84 |
| w5 | 22 | 0.088582 | 15.818 |
| w6 | 13 | -0.136011 | -22.517 |
| w7 | 2 | -0.141246 | -6.026 |
| w8 | 6 | -0.171729 | -7.877 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | 0.032525 | -0.77 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.017187 | 1.367 |
| w13 | 0 | None | 0.0 |
| w14 | 3 | 0.089327 | 18.783 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.067023 | -8.487 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.002693 | 1.651 |
| w21 | 5 | -0.003853 | 0.339 |
| w22 | 2 | 0.042239 | -3.149 |
| w23 | 11 | -0.108517 | -4.932 |
| w24 | 0 | 0.011454 | 0.0 |

