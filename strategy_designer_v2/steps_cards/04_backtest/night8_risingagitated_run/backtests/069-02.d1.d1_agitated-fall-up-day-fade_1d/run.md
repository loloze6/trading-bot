# Backtest of 069-02.d1.d1_agitated-fall-up-day-fade_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/069-02.d1.d1_agitated-fall-up-day-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.13055 | 2.867 |
| w2 | 23 | 0.097979 | 17.08 |
| w3 | 17 | -0.014016 | -0.707 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.033933 | -2.473 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | 0.205097 | 5.687 |
| w9 | 9 | 0.054338 | 5.15 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.027418 | 1.221 |
| w13 | 15 | 0.085283 | 6.393 |
| w14 | 17 | 0.069908 | 12.984 |
| w15 | 1 | None | -0.036 |
| w16 | 16 | 0.018531 | -1.573 |
| w17 | 0 | None | 0.0 |
| w18 | 27 | 0.182621 | 24.235 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | -0.014367 | -1.149 |
| w21 | 0 | None | 0.0 |
| w22 | 16 | 0.053466 | 2.05 |
| w23 | 0 | None | 0.0 |
| w24 | 9 | 0.012532 | 2.166 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.050684 | -2.024 |
| w2 | 22 | 0.019018 | 7.046 |
| w3 | 7 | 0.009207 | 0.72 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.083294 | 1.588 |
| w9 | 5 | 0.040416 | 2.513 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 29 | 0.063845 | 12.04 |
| w15 | 6 | 0.064967 | 5.276 |
| w16 | 12 | 0.014135 | -2.989 |
| w17 | 1 | -0.020634 | -1.093 |
| w18 | 14 | -0.01228 | -3.284 |
| w19 | 0 | None | 0.0 |
| w20 | 17 | 0.112191 | 13.924 |
| w21 | 10 | -0.01031 | -3.305 |
| w22 | 21 | 0.10523 | 20.939 |
| w23 | 1 | 0.034929 | 0.018 |
| w24 | 12 | -0.046696 | -1.822 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 24 | 0.09866 | 15.559 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 8 | -0.052578 | -6.858 |
| w6 | 3 | -0.198365 | -6.72 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.074212 | -0.14 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.100399 | 6.465 |
| w13 | 5 | 0.034611 | 0.906 |
| w14 | 16 | -0.018766 | 0.111 |
| w15 | 6 | 0.046303 | 2.486 |
| w16 | 12 | 0.126427 | 6.805 |
| w17 | 2 | 0.050767 | 1.356 |
| w18 | 15 | 0.050698 | 3.863 |
| w19 | 0 | None | 0.0 |
| w20 | 19 | -0.074378 | -7.229 |
| w21 | 0 | None | 0.0 |
| w22 | 15 | 0.078507 | 7.715 |
| w23 | 1 | 0.031273 | 0.085 |
| w24 | 14 | -0.053775 | -4.92 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.070635 | -8.598 |
| w2 | 18 | -0.012307 | -6.079 |
| w3 | 3 | 0.015751 | 0.068 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | -0.104505 | -3.525 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.067183 | 0.993 |
| w9 | 2 | 0.045308 | 2.334 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 20 | 0.042051 | 6.219 |
| w15 | 3 | -0.014387 | -1.902 |
| w16 | 16 | 0.081152 | 1.778 |
| w17 | 0 | None | 0.0 |
| w18 | 14 | -0.000398 | -0.39 |
| w19 | 20 | -0.022862 | -5.984 |
| w20 | 2 | 0.043073 | 0.397 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | -0.285696 | -14.775 |
| w24 | 5 | -0.027576 | -2.699 |

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
| w1 | 2 | 0.101907 | 1.182 |
| w2 | 1 | 0.076229 | 16.414 |
| w3 | 0 | -0.03007 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.063103 | -3.758 |
| w8 | 3 | -0.002248 | -0.066 |
| w9 | 5 | -0.029057 | -1.218 |
| w10 | 0 | None | 0.0 |
| w11 | 10 | -0.184538 | -21.413 |
| w12 | 0 | None | 0.0 |
| w14 | 4 | 0.013212 | 0.285 |
| w15 | 4 | 0.011419 | 0.783 |
| w16 | 16 | 0.20047 | 10.58 |
| w17 | 0 | None | 0.0 |
| w18 | 12 | 0.13346 | 10.843 |
| w19 | 3 | 0.018838 | 0.053 |
| w20 | 8 | -0.00647 | -3.898 |
| w21 | 2 | 0.084574 | 6.002 |
| w22 | 15 | 0.091557 | 5.216 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | -0.069917 | -4.772 |

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
| w1 | 0 | None | 0.0 |
| w2 | 23 | 0.225488 | 27.819 |
| w3 | 9 | -0.054361 | -2.533 |
| w4 | 5 | 0.023064 | -0.17 |
| w5 | 9 | -0.129994 | -7.85 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.255746 | 4.558 |
| w9 | 13 | 0.011295 | 2.097 |
| w10 | 1 | -0.015115 | -0.159 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | 0.084713 | 3.325 |
| w14 | 15 | 0.002536 | 1.703 |
| w15 | 4 | 0.12182 | 7.847 |
| w16 | 20 | -0.002164 | -7.68 |
| w17 | 6 | -0.038282 | -2.318 |
| w18 | 16 | 0.079607 | 6.65 |
| w19 | 18 | -0.090584 | -10.664 |
| w20 | 7 | 0.022264 | -0.573 |
| w21 | 3 | 0.017658 | -0.321 |
| w22 | 23 | -0.121191 | -12.319 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

