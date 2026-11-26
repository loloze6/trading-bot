# Backtest of 032-02_low-range-decline-continues-more_1d

- Plan: `../../../../03_test_plan/night7c_steadydecline_run/plans/032-02_low-range-decline-continues-more_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.05286 | 1.599 |
| w2 | 12 | 0.094334 | 48.18 |
| w3 | 17 | -0.030626 | -9.25 |
| w4 | 11 | 0.012191 | -36.966 |
| w5 | 7 | 0.094327 | 12.496 |
| w6 | 3 | 0.004508 | -7.841 |
| w7 | 13 | -0.097645 | -18.026 |
| w8 | 12 | 0.020254 | -12.634 |
| w9 | 7 | -0.093688 | 5.039 |
| w10 | 11 | 0.017854 | -6.756 |
| w11 | 8 | -0.025745 | -8.075 |
| w12 | 8 | 0.055728 | 8.241 |
| w13 | 10 | -0.090009 | -11.725 |
| w14 | 20 | -0.012332 | 71.024 |
| w15 | 8 | -0.048291 | -3.064 |
| w16 | 3 | 0.080614 | 10.452 |
| w17 | 1 | 0.188172 | 5.284 |
| w18 | 9 | 0.025709 | 7.039 |
| w19 | 12 | 0.037898 | -10.437 |
| w20 | 9 | -0.114829 | -15.629 |
| w21 | 9 | -0.000229 | -9.309 |
| w22 | 18 | -0.132954 | -14.128 |
| w23 | 17 | -0.026385 | -17.087 |
| w24 | 13 | 0.036044 | 9.092 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.017402 | 20.304 |
| w2 | 11 | 0.19606 | 79.8 |
| w3 | 16 | -0.05621 | -15.354 |
| w4 | 13 | -0.104519 | -19.15 |
| w5 | 16 | -0.044034 | 10.844 |
| w6 | 5 | 0.028456 | -2.974 |
| w7 | 12 | 0.035945 | 68.772 |
| w8 | 13 | -0.085463 | -21.487 |
| w9 | 16 | -0.112694 | -4.298 |
| w10 | 8 | -0.074108 | -32.317 |
| w11 | 6 | 0.016365 | -4.21 |
| w12 | 17 | -0.13047 | -15.745 |
| w13 | 13 | 0.023117 | -7.093 |
| w14 | 18 | -0.051718 | 35.237 |
| w15 | 7 | 0.076168 | -0.253 |
| w16 | 5 | -0.008128 | -6.967 |
| w17 | 9 | -0.023872 | -2.651 |
| w18 | 11 | 0.01593 | -10.791 |
| w19 | 7 | 0.033996 | -6.12 |
| w20 | 12 | -0.058071 | -2.507 |
| w21 | 15 | -0.124163 | -47.222 |
| w22 | 10 | -0.061346 | 34.053 |
| w23 | 7 | -0.050667 | -14.806 |
| w24 | 10 | -0.03076 | 7.971 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.049297 | 11.636 |
| w2 | 16 | 0.050397 | 14.55 |
| w3 | 17 | -0.143268 | -40.375 |
| w4 | 7 | 0.001116 | -2.728 |
| w5 | 8 | -0.059283 | -6.134 |
| w6 | 23 | -0.208813 | -21.84 |
| w7 | 9 | 0.043168 | 71.011 |
| w8 | 8 | -0.11999 | -17.328 |
| w9 | 11 | -0.062493 | 11.452 |
| w10 | 18 | -0.118241 | -17.089 |
| w11 | 8 | -0.101992 | -9.981 |
| w12 | 16 | 0.0015 | -3.381 |
| w13 | 6 | -0.046555 | -7.387 |
| w14 | 24 | -0.147657 | 37.31 |
| w15 | 3 | 0.069684 | -0.08 |
| w16 | 5 | -0.01673 | -10.952 |
| w17 | 5 | 0.095342 | -4.609 |
| w18 | 14 | -0.052498 | -10.236 |
| w19 | 13 | 0.016481 | -3.187 |
| w20 | 20 | -0.185449 | 4.335 |
| w21 | 10 | -0.064314 | -24.585 |
| w22 | 13 | -0.048123 | 0.934 |
| w23 | 13 | -0.043366 | -16.274 |
| w24 | 12 | -0.100599 | 0.135 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.061071 | -19.869 |
| w2 | 11 | -0.009349 | 5.923 |
| w3 | 12 | -0.079017 | -9.569 |
| w4 | 5 | -0.001014 | -3.439 |
| w5 | 16 | 0.0135 | 2.748 |
| w6 | 7 | -0.071079 | -7.371 |
| w7 | 13 | 0.007873 | 12.57 |
| w8 | 9 | -0.03291 | -9.498 |
| w9 | 8 | -0.082015 | 6.267 |
| w10 | 9 | -0.131463 | -10.929 |
| w11 | 9 | 0.05049 | -8.577 |
| w12 | 13 | -0.125057 | -13.52 |
| w14 | 13 | -0.006538 | 64.635 |
| w15 | 12 | -0.039849 | 1.544 |
| w16 | 3 | -0.070827 | -14.676 |
| w17 | 9 | -0.212144 | -18.354 |
| w18 | 8 | 0.000422 | 1.06 |
| w19 | 8 | -0.135043 | -0.976 |
| w20 | 13 | -0.042878 | -13.625 |
| w21 | 6 | 0.033033 | -1.918 |
| w22 | 17 | -0.106573 | -20.855 |
| w23 | 7 | 0.073457 | 11.326 |
| w24 | 15 | -0.115137 | -13.48 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.0977 | -12.809 |
| w2 | 5 | 0.060645 | 54.338 |
| w3 | 0 | 0.0654 | 0.0 |
| w4 | 0 | -0.120179 | 0.0 |
| w5 | 1 | -0.140306 | 1.693 |
| w6 | 16 | -0.113724 | -17.138 |
| w8 | 11 | -0.106732 | -4.548 |
| w9 | 12 | -0.008688 | 8.104 |
| w10 | 7 | -0.035057 | -19.124 |
| w11 | 7 | 0.041855 | -10.681 |
| w12 | 12 | -0.005886 | 15.749 |
| w14 | 17 | -0.033381 | -11.5 |
| w15 | 11 | 0.000383 | 2.342 |
| w16 | 4 | -0.029446 | -7.198 |
| w17 | 9 | 0.037424 | -3.629 |
| w18 | 12 | -0.018763 | -6.954 |
| w19 | 10 | 0.000253 | 5.408 |
| w20 | 17 | 0.04563 | -2.234 |
| w21 | 10 | 0.159567 | -4.811 |
| w22 | 12 | -0.100739 | -4.339 |
| w23 | 13 | 0.035966 | -24.292 |
| w24 | 16 | 0.019704 | 31.462 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.039805 | -15.181 |
| w2 | 13 | -0.050612 | 9.941 |
| w3 | 11 | -0.001649 | 28.926 |
| w4 | 13 | -0.159895 | -18.543 |
| w5 | 9 | 0.080877 | 16.242 |
| w6 | 8 | -0.081705 | -16.918 |
| w7 | 10 | -0.026825 | 2.54 |
| w8 | 15 | -0.055621 | -21.181 |
| w9 | 12 | -0.14795 | 5.827 |
| w10 | 6 | -0.062027 | -8.792 |
| w11 | 8 | -0.037634 | -15.794 |
| w12 | 11 | -0.033327 | -17.183 |
| w14 | 16 | -0.104162 | 29.744 |
| w15 | 5 | -0.020455 | -5.486 |
| w16 | 6 | -0.031782 | -16.534 |
| w17 | 13 | -0.114018 | -17.273 |
| w18 | 12 | -0.053149 | -9.924 |
| w19 | 5 | 0.032127 | 3.487 |
| w20 | 2 | 0.013259 | -3.194 |
| w21 | 6 | 0.015427 | -8.999 |
| w22 | 11 | -0.251215 | -21.625 |
| w23 | 13 | -0.093086 | -25.78 |
| w24 | 2 | 0.031077 | -2.251 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

