# Backtest of 061-01.g1.d1.d2.d1_calm-outsized-rise-continues_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1.d2.d1_calm-outsized-rise-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.065731 | -6.14 |
| w2 | 2 | -0.160188 | -8.961 |
| w3 | 6 | 0.019794 | -9.066 |
| w4 | 2 | 0.164233 | 12.471 |
| w5 | 6 | -0.034012 | -5.275 |
| w6 | 6 | -0.090622 | 2.565 |
| w7 | 6 | 0.044275 | 1.323 |
| w8 | 7 | -0.160385 | -0.653 |
| w9 | 4 | -0.089879 | -1.784 |
| w10 | 6 | 0.170097 | 7.464 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 1 | -0.130214 | -0.557 |
| w14 | 2 | 0.01971 | -0.194 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.048799 | 2.659 |
| w17 | 4 | 0.022364 | 6.614 |
| w18 | 2 | 0.160686 | 2.767 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.008455 | -2.741 |
| w21 | 6 | -0.025452 | 3.754 |
| w22 | 6 | -0.1485 | -7.195 |
| w23 | 6 | 0.136931 | 4.285 |
| w24 | 4 | 0.140077 | 7.438 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.014287 | 0.0 |
| w2 | 3 | -0.106879 | -2.551 |
| w3 | 6 | 0.010062 | -9.091 |
| w4 | 4 | -0.042371 | 6.488 |
| w5 | 5 | -0.035684 | 0.366 |
| w6 | 6 | -0.032492 | 1.01 |
| w7 | 1 | -0.112578 | 0.648 |
| w8 | 0 | None | 0.0 |
| w9 | 4 | 0.00145 | -3.423 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | -0.004185 | -0.046 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.010654 | 1.287 |
| w17 | 5 | 0.034627 | 0.36 |
| w18 | 2 | 0.048405 | 3.233 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | -0.111605 | -0.073 |
| w21 | 5 | -0.076169 | -5.107 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.127603 | 2.733 |
| w24 | 2 | 0.025795 | 2.598 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.066392 | -3.246 |
| w2 | 6 | -0.082757 | -9.202 |
| w3 | 6 | -0.009953 | 8.252 |
| w4 | 4 | 0.128661 | 1.053 |
| w5 | 7 | 0.103402 | -0.938 |
| w6 | 7 | 0.041961 | 5.016 |
| w7 | 2 | -0.04132 | 0.96 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.077579 | 0.205 |
| w10 | 9 | -0.021392 | 0.34 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.040856 | 1.91 |
| w13 | 1 | -0.143956 | -1.484 |
| w14 | 2 | -0.039668 | -1.694 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | -0.044289 | -0.733 |
| w17 | 3 | -0.022756 | -2.898 |
| w18 | 2 | -0.034004 | 1.505 |
| w19 | 6 | 0.091974 | 6.375 |
| w20 | 5 | 0.007738 | -5.255 |
| w21 | 6 | 0.034434 | 2.544 |
| w22 | 0 | None | 0.0 |
| w23 | 10 | 0.037786 | 7.728 |
| w24 | 3 | -0.228099 | -6.381 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.073052 | -4.155 |
| w2 | 4 | -0.040896 | -0.698 |
| w3 | 6 | 0.041896 | -1.97 |
| w4 | 7 | -0.011272 | -0.851 |
| w5 | 10 | 0.118517 | -2.98 |
| w6 | 6 | 0.076784 | 0.079 |
| w7 | 6 | -0.036555 | -1.118 |
| w8 | 7 | -0.065709 | -0.4 |
| w9 | 2 | -0.163816 | -5.087 |
| w10 | 2 | -0.09204 | 0.337 |
| w11 | 0 | None | 0.0 |
| w12 | 9 | 0.017834 | -5.22 |
| w14 | 6 | 0.066636 | -5.528 |
| w15 | 0 | None | 0.0 |
| w16 | 3 | -0.078413 | -1.16 |
| w17 | 0 | None | 0.0 |
| w18 | 7 | 0.058343 | 3.208 |
| w19 | 1 | -0.017154 | -5.862 |
| w20 | 4 | -0.035466 | -4.208 |
| w21 | 6 | 0.026925 | 1.578 |
| w22 | 4 | 0.002479 | 3.701 |
| w23 | 5 | -0.031405 | -4.696 |
| w24 | 2 | 0.042574 | -0.241 |

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
| w1 | 9 | 0.000433 | -0.98 |
| w2 | 0 | -0.001692 | 0.0 |
| w3 | 0 | 0.083024 | 0.0 |
| w4 | 0 | -0.007941 | 0.0 |
| w5 | 0 | -0.039237 | 0.0 |
| w6 | 1 | -0.011613 | 3.657 |
| w8 | 6 | -0.064748 | -1.296 |
| w9 | 1 | -0.096732 | -4.738 |
| w10 | 1 | -0.050335 | -1.201 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.033099 | 1.716 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.305107 | 5.497 |
| w16 | 1 | -0.018224 | -0.224 |
| w17 | 4 | 0.004038 | 6.404 |
| w18 | 2 | -0.00822 | 8.927 |
| w19 | 7 | 0.012558 | -1.345 |
| w20 | 1 | -0.10051 | -0.488 |
| w21 | 7 | -0.004684 | 21.13 |
| w22 | 0 | None | 0.0 |
| w23 | 7 | 0.112134 | 8.122 |
| w24 | 3 | -0.035066 | -0.088 |

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
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.1336 | -2.183 |
| w4 | 5 | -0.198647 | -0.635 |
| w5 | 2 | -0.00179 | -0.746 |
| w6 | 4 | -0.120445 | -2.531 |
| w7 | 2 | 0.036208 | -0.151 |
| w8 | 8 | -0.19354 | 1.049 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | 0.070421 | 3.324 |
| w13 | 0 | None | 0.0 |
| w14 | 4 | 0.017155 | 1.432 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | 0.047013 | 3.207 |
| w18 | 2 | -0.016903 | 2.293 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.114322 | -4.965 |
| w21 | 6 | -0.01211 | 2.605 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | 0.100835 | -0.24 |
| w24 | 0 | None | 0.0 |

