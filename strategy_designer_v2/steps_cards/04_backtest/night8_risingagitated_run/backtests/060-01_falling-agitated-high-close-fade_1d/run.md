# Backtest of 060-01_falling-agitated-high-close-fade_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/060-01_falling-agitated-high-close-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.122 | 5.961 |
| w2 | 57 | -0.048373 | 6.3 |
| w3 | 38 | -0.004869 | 2.717 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.039872 | -4.501 |
| w7 | 0 | None | 0.0 |
| w8 | 15 | 0.145611 | 5.502 |
| w9 | 19 | 0.034016 | 5.6 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.00811 | 0.629 |
| w13 | 43 | 0.007668 | 1.729 |
| w14 | 39 | 0.106904 | 22.715 |
| w15 | 5 | 0.0464 | 0.73 |
| w16 | 40 | -0.003897 | -6.152 |
| w17 | 0 | None | 0.0 |
| w18 | 64 | 0.05094 | 7.28 |
| w19 | 0 | None | 0.0 |
| w20 | 17 | -0.057872 | -5.171 |
| w21 | 0 | None | 0.0 |
| w22 | 42 | 0.060089 | 6.58 |
| w23 | 0 | None | 0.0 |
| w24 | 28 | 0.018634 | 6.353 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.056825 | 6.841 |
| w2 | 70 | -0.122258 | -8.921 |
| w3 | 16 | -0.055802 | -5.138 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 20 | 0.062236 | 2.075 |
| w9 | 18 | 0.027297 | 2.912 |
| w10 | 2 | 0.028507 | 0.034 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 62 | -0.053074 | 0.99 |
| w15 | 14 | 0.086229 | 6.418 |
| w16 | 38 | -0.038683 | -11.403 |
| w17 | 3 | -0.003239 | -0.718 |
| w18 | 23 | -0.029754 | -7.7 |
| w19 | 1 | None | -0.014 |
| w20 | 50 | 0.067443 | 16.105 |
| w21 | 20 | 0.00467 | -4.658 |
| w22 | 63 | 0.144591 | 44.861 |
| w23 | 5 | -0.052266 | -6.987 |
| w24 | 22 | -0.138253 | -12.263 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 58 | 0.035176 | 16.197 |
| w3 | 1 | -0.393083 | -4.923 |
| w4 | 2 | -0.045578 | -0.76 |
| w5 | 20 | -0.010439 | -0.685 |
| w6 | 5 | -0.142118 | -7.38 |
| w7 | 0 | None | 0.0 |
| w8 | 17 | 0.030096 | -4.882 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.024725 | 1.549 |
| w13 | 18 | -0.145389 | -11.629 |
| w14 | 44 | -0.021421 | 0.806 |
| w15 | 18 | 0.026632 | 1.029 |
| w16 | 32 | 0.068651 | 4.393 |
| w17 | 8 | 0.027167 | -0.919 |
| w18 | 36 | -0.048996 | -5.052 |
| w19 | 1 | 0.045338 | 2.489 |
| w20 | 50 | -0.061758 | -4.086 |
| w21 | 1 | -0.047127 | -0.95 |
| w22 | 37 | 0.030577 | 3.773 |
| w23 | 4 | 0.025688 | 0.813 |
| w24 | 42 | -0.057307 | -5.661 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.071361 | -10.91 |
| w2 | 43 | -0.080165 | -13.892 |
| w3 | 5 | -0.005553 | -1.361 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 8 | -0.018714 | -4.362 |
| w7 | 0 | None | 0.0 |
| w8 | 18 | 0.105333 | 3.586 |
| w9 | 2 | 0.021599 | 1.166 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 41 | 0.097775 | 20.568 |
| w15 | 7 | -0.00596 | -0.871 |
| w16 | 38 | -0.003232 | -6.993 |
| w17 | 0 | None | 0.0 |
| w18 | 34 | 0.035048 | 0.695 |
| w19 | 41 | -0.118395 | -16.915 |
| w20 | 5 | -0.031999 | -3.404 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 12 | -0.136456 | -16.765 |
| w24 | 11 | -0.035971 | -8.935 |

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
| w1 | 4 | 0.057517 | 3.289 |
| w2 | 25 | 0.125455 | 24.242 |
| w3 | 0 | -0.032881 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.072797 | -3.777 |
| w8 | 8 | -0.006812 | -0.283 |
| w9 | 11 | -0.059636 | -4.21 |
| w10 | 0 | None | 0.0 |
| w11 | 19 | -0.022312 | -11.725 |
| w12 | 0 | None | 0.0 |
| w14 | 11 | 0.063156 | 6.198 |
| w15 | 8 | 0.058004 | 5.395 |
| w16 | 43 | 0.047149 | 1.569 |
| w17 | 3 | 0.007888 | 1.71 |
| w18 | 27 | 0.06931 | 6.15 |
| w19 | 15 | -0.031651 | -3.334 |
| w20 | 12 | -0.050606 | -11.425 |
| w21 | 6 | 0.094964 | 5.731 |
| w22 | 37 | 0.07496 | 5.798 |
| w23 | 0 | None | 0.0 |
| w24 | 23 | -0.069361 | -5.133 |

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
| w1 | 0 | -0.021729 | 0.0 |
| w2 | 52 | 0.081232 | 20.037 |
| w3 | 23 | -0.109529 | -11.98 |
| w4 | 14 | 0.029823 | 1.327 |
| w5 | 21 | -0.154386 | -13.709 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | 0.063448 | 0.382 |
| w8 | 16 | 0.190575 | 8.445 |
| w9 | 41 | -0.05732 | -4.386 |
| w10 | 3 | 0.024864 | 0.057 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 18 | 0.094306 | 7.415 |
| w14 | 32 | 0.075219 | 16.07 |
| w15 | 12 | 0.0684 | 4.778 |
| w16 | 46 | -0.053097 | -22.697 |
| w17 | 15 | -0.00655 | -1.294 |
| w18 | 34 | 0.020509 | 0.23 |
| w19 | 50 | -0.067201 | -9.975 |
| w20 | 17 | -0.073198 | -15.655 |
| w21 | 13 | 0.007242 | -5.003 |
| w22 | 53 | -0.108781 | -13.805 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

