# Backtest of 061-01.g1.d1.d2.d2_calm-large-breakout-continues_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1.d2.d2_calm-large-breakout-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.020313 | -20.913 |
| w2 | 2 | 0.01394 | -2.626 |
| w3 | 8 | 0.037726 | -40.999 |
| w4 | 3 | 0.145526 | 41.203 |
| w5 | 5 | 0.083538 | 4.143 |
| w6 | 6 | -0.036591 | 27.709 |
| w7 | 2 | 0.24591 | 6.659 |
| w8 | 4 | -0.198146 | -6.16 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | 0.311386 | 26.525 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 3 | -0.094869 | -0.709 |
| w14 | 3 | 0.002784 | -2.41 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | -0.048263 | 8.797 |
| w17 | 7 | 0.078134 | 23.316 |
| w18 | 3 | 0.162523 | 16.379 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | -0.02314 | -7.886 |
| w22 | 2 | -0.080441 | -5.618 |
| w23 | 1 | 0.218978 | 15.217 |
| w24 | 8 | 0.073968 | -1.015 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | 0.010052 | -37.349 |
| w4 | 3 | -0.010062 | 25.219 |
| w5 | 6 | -0.06431 | -1.914 |
| w6 | 8 | 0.016303 | 4.498 |
| w7 | 1 | -0.026394 | -2.887 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.03611 | -6.212 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | -0.004185 | -0.184 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | -0.019622 | -0.631 |
| w17 | 6 | 0.04438 | -1.002 |
| w18 | 4 | 0.05724 | 19.538 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.080889 | -15.856 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | 0.127603 | 11.054 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.040548 | -3.488 |
| w2 | 2 | 0.048488 | 0.434 |
| w3 | 3 | 0.026569 | 24.323 |
| w4 | 4 | -0.205143 | -9.291 |
| w5 | 2 | 0.036281 | -4.768 |
| w6 | 4 | -0.025266 | 3.269 |
| w7 | 1 | -0.058273 | -8.037 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | 0.063447 | 0.926 |
| w10 | 2 | -0.063883 | -3.988 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.034699 | 9.716 |
| w13 | 0 | None | 0.0 |
| w14 | 2 | -0.044842 | -6.698 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | -0.044289 | -3.664 |
| w17 | 5 | -0.002674 | -8.001 |
| w18 | 3 | -0.012409 | 11.083 |
| w19 | 6 | 0.076806 | 18.934 |
| w20 | 2 | -0.012457 | -0.424 |
| w21 | 6 | -0.04144 | -12.982 |
| w22 | 0 | None | 0.0 |
| w23 | 9 | 0.08953 | 39.836 |
| w24 | 4 | -0.339827 | -30.386 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.073052 | -16.62 |
| w2 | 4 | -0.040896 | -2.789 |
| w3 | 11 | -0.027949 | -30.788 |
| w4 | 6 | 0.013064 | 0.863 |
| w5 | 6 | 0.107416 | 8.031 |
| w6 | 10 | 0.006692 | 1.622 |
| w7 | 3 | -0.01066 | 0.257 |
| w8 | 5 | -0.148932 | -4.313 |
| w9 | 2 | -0.15505 | -16.255 |
| w10 | 3 | -0.123811 | -1.833 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.014627 | -6.479 |
| w14 | 5 | -0.011266 | -21.766 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | -0.082105 | -4.756 |
| w17 | 0 | None | 0.0 |
| w18 | 9 | 0.038913 | -0.096 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.061223 | -1.845 |
| w21 | 3 | -0.023764 | -11.698 |
| w22 | 7 | 0.117333 | 16.592 |
| w23 | 6 | -0.023786 | -3.99 |
| w24 | 2 | -0.082352 | -5.306 |

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
| w1 | 5 | 0.037111 | -1.191 |
| w2 | 0 | -0.069324 | 0.0 |
| w3 | 0 | -0.012343 | 0.0 |
| w4 | 0 | -0.060453 | 0.0 |
| w5 | 0 | -0.034124 | 0.0 |
| w6 | 2 | 0.0413 | -1.171 |
| w8 | 3 | -0.082487 | -0.276 |
| w9 | 2 | -0.096732 | -18.791 |
| w10 | 4 | -0.072488 | 4.116 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.089884 | -3.65 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | 0.500358 | 17.581 |
| w16 | 1 | -0.018224 | -0.897 |
| w17 | 8 | -0.018464 | 14.56 |
| w18 | 2 | 0.097163 | 38.358 |
| w19 | 5 | 0.026412 | 7.306 |
| w20 | 0 | None | 0.0 |
| w21 | 9 | -0.044874 | 48.699 |
| w22 | 2 | -0.000196 | -0.886 |
| w23 | 7 | 0.161595 | 46.451 |
| w24 | 2 | 0.003267 | -0.386 |

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
| w2 | 1 | -0.018687 | -2.295 |
| w3 | 1 | -0.029387 | -1.268 |
| w4 | 4 | 0.01752 | -2.388 |
| w5 | 2 | -0.02794 | -10.231 |
| w6 | 3 | -0.061628 | -10.677 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | -0.149046 | -4.221 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | 0.095874 | 11.874 |
| w13 | 0 | None | 0.0 |
| w14 | 2 | -0.011498 | -1.543 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.045258 | -2.17 |
| w18 | 3 | -0.026884 | 8.448 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.080716 | -3.711 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | -0.093834 | -4.183 |
| w24 | 0 | None | 0.0 |

