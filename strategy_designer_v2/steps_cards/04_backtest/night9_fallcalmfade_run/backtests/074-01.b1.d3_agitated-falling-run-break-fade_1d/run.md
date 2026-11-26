# Backtest of 074-01.b1.d3_agitated-falling-run-break-fade_1d

- Plan: `../../../../03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d3_agitated-falling-run-break-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.129417 | 7.577 |
| w2 | 6 | 0.096467 | 10.42 |
| w3 | 7 | -0.023993 | -1.689 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.048728 | -2.415 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.184781 | 0.257 |
| w9 | 5 | -0.050425 | -2.749 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 6 | 0.157398 | 9.972 |
| w14 | 5 | 0.041795 | 5.447 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | -0.056963 | -1.712 |
| w17 | 0 | None | 0.0 |
| w18 | 10 | 0.193958 | 13.379 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.046079 | 2.154 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | -0.003261 | -1.001 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | -0.005852 | 0.351 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.101709 | -5.443 |
| w2 | 8 | 0.028974 | 3.227 |
| w3 | 6 | -0.039793 | -2.072 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | 0.150911 | 3.456 |
| w9 | 2 | 0.068615 | 2.992 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 14 | 0.15625 | 25.324 |
| w15 | 1 | -0.018847 | -0.488 |
| w16 | 4 | -0.059701 | -2.109 |
| w17 | 1 | -0.029217 | -0.498 |
| w18 | 4 | 0.030545 | 0.912 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.049243 | 5.435 |
| w21 | 3 | -0.005199 | -1.022 |
| w22 | 11 | 0.253045 | 27.466 |
| w23 | 1 | 0.023113 | 0.02 |
| w24 | 4 | -0.017591 | -0.552 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 8 | 0.011937 | 3.856 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | -0.059777 | -2.753 |
| w6 | 1 | -0.135216 | -3.605 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.122608 | 2.499 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | 0.013205 | 0.353 |
| w14 | 8 | 0.113404 | 9.207 |
| w15 | 2 | -0.060661 | -2.637 |
| w16 | 3 | 0.126021 | 4.943 |
| w17 | 0 | None | 0.0 |
| w18 | 9 | -0.001129 | -0.152 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | 0.144271 | 10.771 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | 0.04485 | 3.122 |
| w23 | 1 | 0.031273 | 0.168 |
| w24 | 10 | -0.066917 | -5.265 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.109755 | 6.717 |
| w2 | 6 | -0.037427 | -4.361 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.082713 | -1.74 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.063085 | 0.393 |
| w9 | 1 | 0.09161 | 3.409 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 7 | 0.072397 | 4.869 |
| w15 | 2 | 0.037852 | 0.421 |
| w16 | 4 | 0.035334 | 0.759 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.050501 | -2.246 |
| w19 | 7 | -0.009981 | -0.312 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | -0.327986 | -22.027 |
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
| w1 | 1 | 0.0449 | 0.31 |
| w2 | 1 | -0.020579 | 18.026 |
| w3 | 0 | 0.00473 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.013003 | -0.804 |
| w8 | 1 | 0.061173 | 0.338 |
| w9 | 0 | 0.086999 | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | -0.029333 | -0.472 |
| w12 | 0 | None | 0.0 |
| w14 | 3 | 0.030831 | 1.122 |
| w15 | 2 | -0.047053 | -2.645 |
| w16 | 5 | 0.106409 | 4.872 |
| w17 | 0 | None | 0.0 |
| w18 | 5 | 0.055433 | 2.207 |
| w19 | 2 | 0.000438 | -0.562 |
| w20 | 1 | 0.105114 | 1.441 |
| w21 | 1 | 0.112248 | 5.774 |
| w22 | 4 | 0.075744 | 2.995 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | 0.003118 | 0.341 |

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
| w2 | 6 | 0.335737 | 27.048 |
| w3 | 4 | -0.112621 | -4.907 |
| w4 | 2 | 0.014916 | 0.104 |
| w5 | 1 | -0.370947 | -5.237 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.145 | 0.209 |
| w9 | 8 | 0.104377 | 7.496 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | 0.096081 | 2.364 |
| w14 | 5 | 0.191349 | 12.139 |
| w15 | 3 | 0.071732 | 2.166 |
| w16 | 6 | 0.112761 | 5.158 |
| w17 | 1 | 0.051212 | 1.114 |
| w18 | 6 | 0.15358 | 5.835 |
| w19 | 9 | -0.1081 | -10.304 |
| w20 | 5 | 0.074305 | 4.576 |
| w21 | 1 | 0.02023 | 0.14 |
| w22 | 8 | 0.029037 | 2.204 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

