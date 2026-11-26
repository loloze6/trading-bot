# Backtest of 058-01.g2.g1.d1.d1_bounce-after-deep-3-day-fall_1d

- Plan: `../../../../03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1.d1.d1_bounce-after-deep-3-day-fall_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.129167 | 7.417 |
| w2 | 16 | 0.095127 | 13.755 |
| w3 | 15 | -0.027023 | -2.273 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.05108 | -2.629 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | 0.029785 | 0.139 |
| w9 | 6 | -0.02495 | -0.61 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.047074 | 0.198 |
| w13 | 11 | 0.119578 | 8.532 |
| w14 | 14 | 0.090255 | 13.159 |
| w15 | 1 | None | -0.034 |
| w16 | 10 | 0.106946 | 5.926 |
| w17 | 0 | None | 0.0 |
| w18 | 21 | 0.177859 | 21.587 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | 0.048015 | 2.4 |
| w21 | 0 | None | 0.0 |
| w22 | 9 | 0.103066 | 6.724 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | -0.034335 | -1.394 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.009301 | -1.088 |
| w2 | 17 | -0.070857 | -9.199 |
| w3 | 9 | 0.009837 | 0.65 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 5 | 0.06583 | 1.019 |
| w9 | 4 | 0.048855 | 2.236 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 19 | 0.059434 | 11.522 |
| w15 | 4 | 0.02622 | 0.691 |
| w16 | 9 | 0.078757 | 2.821 |
| w17 | 1 | -0.018044 | -0.581 |
| w18 | 10 | 0.101603 | 4.393 |
| w19 | 0 | None | 0.0 |
| w20 | 17 | 0.078896 | 9.807 |
| w21 | 6 | -0.049813 | -3.629 |
| w22 | 19 | 0.173948 | 23.209 |
| w23 | 1 | 0.021772 | 0.023 |
| w24 | 9 | -0.077023 | -4.564 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 17 | 0.036336 | 6.162 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 7 | -0.075069 | -5.587 |
| w6 | 2 | -0.136199 | -5.983 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | 0.111978 | 2.776 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.122368 | 2.143 |
| w13 | 2 | 0.012069 | 0.42 |
| w14 | 13 | 0.105251 | 11.386 |
| w15 | 6 | 0.003706 | -0.347 |
| w16 | 9 | 0.166735 | 8.542 |
| w17 | 1 | -0.002557 | -0.175 |
| w18 | 11 | 0.045686 | 2.29 |
| w19 | 0 | None | 0.0 |
| w20 | 14 | 0.089464 | 8.343 |
| w21 | 0 | None | 0.0 |
| w22 | 11 | 0.095359 | 8.648 |
| w23 | 1 | 0.031273 | 0.198 |
| w24 | 14 | -0.058748 | -4.856 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.136545 | 8.499 |
| w2 | 13 | -0.082825 | -9.933 |
| w3 | 2 | 0.027932 | 0.579 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.151857 | -5.516 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | -0.028368 | -1.166 |
| w9 | 2 | 0.048978 | 2.612 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 16 | 0.044852 | 4.034 |
| w15 | 4 | -0.001544 | -0.192 |
| w16 | 10 | 0.109648 | 4.882 |
| w17 | 0 | None | 0.0 |
| w18 | 10 | 0.038988 | 1.786 |
| w19 | 13 | -0.017154 | -4.015 |
| w20 | 2 | 0.063144 | 1.051 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | -0.259516 | -22.249 |
| w24 | 1 | -0.044259 | -0.937 |

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
| w1 | 1 | 0.115594 | 1.853 |
| w2 | 1 | -0.049002 | 18.026 |
| w3 | 0 | -0.064009 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.062689 | -3.953 |
| w8 | 3 | -0.011486 | -0.274 |
| w9 | 2 | 0.046579 | 1.995 |
| w10 | 0 | None | 0.0 |
| w11 | 9 | -0.069993 | -5.285 |
| w12 | 0 | None | 0.0 |
| w14 | 4 | 0.054873 | 2.304 |
| w15 | 4 | -0.027019 | -1.679 |
| w16 | 12 | 0.150833 | 9.591 |
| w17 | 0 | None | 0.0 |
| w18 | 9 | 0.110163 | 6.588 |
| w19 | 3 | 0.003422 | -0.437 |
| w20 | 5 | 0.008923 | -1.52 |
| w21 | 2 | 0.117789 | 7.016 |
| w22 | 9 | 0.078227 | 3.806 |
| w23 | 0 | None | 0.0 |
| w24 | 9 | 0.026426 | 3.178 |

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
| w2 | 16 | 0.242529 | 27.537 |
| w3 | 8 | -0.109303 | -6.499 |
| w4 | 3 | 0.080295 | 1.838 |
| w5 | 6 | -0.093496 | -6.191 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 5 | 0.07343 | 0.979 |
| w9 | 11 | -0.019987 | -1.698 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | 0.084844 | 2.92 |
| w14 | 10 | 0.072927 | 6.798 |
| w15 | 4 | 0.104228 | 3.171 |
| w16 | 12 | 0.037885 | -1.241 |
| w17 | 2 | 0.041194 | 1.148 |
| w18 | 14 | 0.072844 | 5.379 |
| w19 | 13 | -0.105197 | -10.277 |
| w20 | 6 | 0.066757 | 4.228 |
| w21 | 1 | -0.001501 | 0.131 |
| w22 | 13 | -0.112938 | -10.898 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

