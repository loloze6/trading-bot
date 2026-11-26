# Backtest of 062-01_choppy-calm-fall-continues_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/062-01_choppy-calm-fall-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.01134 | 5.733 |
| w2 | 14 | -0.053731 | 25.212 |
| w3 | 9 | -0.193812 | -0.124 |
| w4 | 2 | -0.050808 | -5.632 |
| w5 | 30 | 0.024534 | 15.091 |
| w6 | 7 | 0.017848 | -14.796 |
| w7 | 24 | 0.079209 | 19.776 |
| w8 | 18 | -0.11433 | -18.39 |
| w9 | 10 | 0.255274 | 18.874 |
| w10 | 11 | -0.015837 | -1.27 |
| w11 | 5 | 0.050877 | -0.877 |
| w12 | 2 | 0.116077 | 5.94 |
| w13 | 5 | 0.025168 | -3.546 |
| w14 | 19 | 0.034872 | 20.77 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.055321 | 0.5 |
| w17 | 6 | -0.008651 | -9.84 |
| w18 | 4 | -0.056241 | -5.893 |
| w19 | 0 | None | 0.0 |
| w20 | 13 | 0.097408 | 10.588 |
| w21 | 10 | -0.057983 | -17.089 |
| w22 | 21 | -0.028302 | -4.334 |
| w23 | 19 | -0.104566 | -10.982 |
| w24 | 8 | -0.011863 | 3.155 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.031764 | 4.307 |
| w2 | 5 | 0.21341 | 28.495 |
| w3 | 8 | -0.102962 | 1.059 |
| w4 | 8 | -0.117734 | -17.318 |
| w5 | 35 | 0.044518 | 10.643 |
| w6 | 1 | 0.037866 | 8.697 |
| w7 | 10 | -0.010574 | 3.441 |
| w8 | 7 | 0.069481 | 1.598 |
| w9 | 9 | 0.257827 | 9.884 |
| w10 | 6 | -0.039661 | -13.24 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.075038 | -3.232 |
| w13 | 0 | 0.057662 | 0.0 |
| w14 | 3 | 0.13747 | 13.993 |
| w15 | 0 | 0.095893 | 0.0 |
| w16 | 2 | -0.051592 | -5.499 |
| w17 | 7 | 0.045797 | -4.938 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | 0.064571 | 6.712 |
| w21 | 17 | -0.052874 | -35.208 |
| w22 | 2 | -0.020489 | -5.466 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.055937 | -5.815 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.006747 | 16.045 |
| w2 | 13 | -0.119178 | 11.183 |
| w3 | 15 | 0.048412 | -17.437 |
| w4 | 9 | 0.119242 | -7.641 |
| w5 | 23 | 0.145104 | 18.86 |
| w6 | 16 | -0.12708 | -21.807 |
| w7 | 9 | -0.03899 | 10.213 |
| w8 | 2 | -0.021575 | -0.969 |
| w9 | 0 | None | 0.0 |
| w10 | 19 | -0.012048 | -0.074 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | -0.142865 | -5.523 |
| w13 | 0 | -0.038038 | 0.0 |
| w14 | 14 | 0.009793 | 23.906 |
| w15 | 2 | 0.214259 | -8.5 |
| w16 | 0 | 0.018901 | 0.0 |
| w17 | 2 | 0.053117 | -4.381 |
| w18 | 2 | -0.069023 | -5.67 |
| w19 | 12 | 0.091259 | 6.36 |
| w20 | 5 | 0.03682 | 6.533 |
| w21 | 11 | -0.003444 | -18.118 |
| w22 | 0 | None | 0.0 |
| w23 | 16 | -0.064085 | -5.011 |
| w24 | 5 | 0.017982 | -5.564 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | -0.097357 | 0.0 |
| w3 | 15 | -0.131076 | -11.351 |
| w4 | 25 | -0.101938 | -12.089 |
| w5 | 38 | -0.051761 | 0.126 |
| w6 | 13 | 0.0834 | -7.056 |
| w7 | 5 | 0.073277 | 6.718 |
| w8 | 13 | -0.081326 | -11.261 |
| w9 | 7 | 0.028209 | 6.899 |
| w10 | 12 | -0.063441 | -12.679 |
| w11 | 0 | None | 0.0 |
| w12 | 26 | -0.112554 | 5.297 |
| w14 | 13 | -0.022945 | 10.355 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | -0.016794 | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 6 | -0.105421 | -13.33 |
| w19 | 3 | 0.121168 | 20.352 |
| w20 | 7 | 0.135803 | 2.336 |
| w21 | 21 | 0.089125 | 2.653 |
| w22 | 14 | 0.05433 | -4.799 |
| w23 | 12 | 0.051874 | 23.257 |
| w24 | 5 | 0.040668 | -0.527 |

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
| w1 | 13 | -0.012298 | 13.287 |
| w2 | 0 | -0.076623 | 0.0 |
| w3 | 0 | -0.146848 | 0.0 |
| w4 | 0 | -0.058439 | 0.0 |
| w5 | 9 | -0.020358 | -0.81 |
| w6 | 1 | 0.017465 | 0.656 |
| w8 | 31 | -0.017728 | -13.425 |
| w9 | 13 | -0.016124 | 3.52 |
| w10 | 21 | 0.049614 | 5.291 |
| w11 | 0 | None | 0.0 |
| w12 | 15 | -0.066771 | 9.98 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.024502 | -9.579 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | -0.007153 | -8.323 |
| w18 | 0 | None | 0.0 |
| w19 | 4 | 0.023106 | 3.201 |
| w20 | 12 | -0.012965 | -5.3 |
| w21 | 11 | 0.032381 | -13.91 |
| w22 | 0 | None | 0.0 |
| w23 | 28 | -0.099541 | -18.981 |
| w24 | 5 | 0.116138 | 1.547 |

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
| w1 | 5 | 0.130193 | 10.118 |
| w2 | 8 | -0.037389 | 1.056 |
| w3 | 9 | 0.0231 | 0.719 |
| w4 | 21 | -0.042893 | -6.281 |
| w5 | 12 | 0.058982 | 13.707 |
| w6 | 10 | -0.159893 | -11.841 |
| w7 | 2 | -0.139592 | -4.615 |
| w8 | 7 | -0.108261 | -6.773 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | -0.01773 | 0.315 |
| w11 | 0 | None | 0.0 |
| w12 | 8 | -0.092608 | -5.734 |
| w13 | 0 | None | 0.0 |
| w14 | 3 | 0.129205 | 35.086 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.073588 | -8.367 |
| w18 | 0 | -0.095896 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | -0.10818 | 4.022 |
| w21 | 7 | -0.037286 | -1.195 |
| w22 | 0 | None | 0.0 |
| w23 | 7 | 0.063237 | 0.12 |
| w24 | 4 | 0.00477 | -7.814 |

