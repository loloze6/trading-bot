# Backtest of 061-01_choppy-agitated-strong-close-fade_1d

- Plan: `../../../../03_test_plan/night9_chopagishort_run/plans/061-01_choppy-agitated-strong-close-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.077255 | 3.105 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | 0.18301 | 8.506 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | -0.068355 | -1.51 |
| w10 | 2 | -0.001712 | -0.88 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.258611 | -8.4 |
| w13 | 1 | 0.061537 | -0.446 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | 0.061218 | 1.431 |
| w16 | 3 | 0.384208 | 33.728 |
| w17 | 2 | 0.071185 | 1.513 |
| w18 | 1 | 0.255317 | 11.99 |
| w19 | 7 | 0.041463 | -5.227 |
| w20 | 16 | 0.07384 | 10.632 |
| w21 | 4 | 0.115178 | 9.867 |
| w22 | 6 | 0.140095 | 14.27 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | 0.078463 | 1.524 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 3 | -0.036871 | -1.983 |
| w3 | 4 | 0.120811 | 2.761 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | 0.065189 | 11.987 |
| w10 | 1 | 0.025048 | 0.376 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.041299 | -1.911 |
| w13 | 1 | 0.024651 | 2.556 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.084247 | -1.116 |
| w16 | 4 | 0.112645 | 5.608 |
| w17 | 1 | 0.04126 | 1.175 |
| w18 | 3 | 0.144116 | 5.531 |
| w19 | 7 | -0.016598 | -2.436 |
| w20 | 3 | -0.017219 | 0.251 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | 0.008822 | 0.6 |
| w23 | 2 | -0.120412 | -12.518 |
| w24 | 2 | 0.061486 | 9.996 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 5 | -0.006514 | 0.873 |
| w4 | 8 | -0.156808 | -9.253 |
| w5 | 5 | -0.017317 | -3.971 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | -0.099292 | -3.864 |
| w13 | 3 | -0.086467 | -1.658 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | 0.014689 | 1.159 |
| w17 | 1 | 0.029328 | -2.291 |
| w18 | 2 | 0.02722 | -2.714 |
| w19 | 5 | 0.030183 | -6.15 |
| w20 | 2 | 0.11214 | 2.947 |
| w21 | 3 | 0.046017 | 5.529 |
| w22 | 4 | 0.05144 | -5.266 |
| w23 | 1 | -0.03265 | -2.539 |
| w24 | 2 | -0.086596 | 5.532 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.101006 | 10.451 |
| w2 | 5 | 0.13793 | 8.866 |
| w3 | 8 | -0.017977 | 1.295 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | -0.072213 | -5.734 |
| w14 | 2 | -0.08398 | -3.836 |
| w15 | 5 | 0.143793 | 10.525 |
| w16 | 2 | -0.120614 | -5.567 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.016177 | -0.855 |
| w19 | 14 | 0.178348 | 26.975 |
| w20 | 7 | 0.042264 | 3.804 |
| w21 | 7 | 0.017149 | -0.447 |
| w22 | 5 | 0.102587 | 1.158 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

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
| w1 | 2 | -0.01126 | 0.998 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.011782 | -0.042 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | 0.060049 | 2.865 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | -0.089666 | -6.047 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | 0.07106 | 4.179 |
| w16 | 6 | 0.054505 | 8.961 |
| w17 | 2 | -0.038753 | -3.022 |
| w18 | 1 | 0.10316 | 2.193 |
| w19 | 7 | -0.010905 | 3.194 |
| w20 | 4 | -0.345787 | -31.039 |
| w21 | 4 | 0.049462 | -0.552 |
| w22 | 6 | 0.000265 | -6.202 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

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
| w1 | 4 | 0.010438 | -11.56 |
| w2 | 1 | 0.034495 | 2.088 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 5 | 0.097176 | 12.461 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | 0.088808 | 5.484 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | 0.264663 | 17.884 |
| w10 | 1 | 0.084245 | 2.386 |
| w11 | 0 | None | 0.0 |
| w12 | 7 | -0.012839 | -4.48 |
| w13 | 1 | 0.006856 | 0.693 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.055261 | 2.035 |
| w16 | 2 | -0.173097 | -30.685 |
| w17 | 8 | -0.023343 | -5.049 |
| w18 | 2 | 0.111366 | 2.371 |
| w19 | 6 | -0.0619 | 4.35 |
| w20 | 2 | -0.038908 | -4.687 |
| w21 | 2 | -0.044192 | -2.082 |
| w22 | 6 | -0.08386 | -0.62 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.005767 | -5.808 |

