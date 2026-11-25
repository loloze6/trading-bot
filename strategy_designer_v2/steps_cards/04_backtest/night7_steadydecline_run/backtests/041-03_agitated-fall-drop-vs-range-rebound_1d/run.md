# Backtest of 041-03_agitated-fall-drop-vs-range-rebound_1d

- Plan: `../../../../03_test_plan/night7_steadydecline_run/plans/041-03_agitated-fall-drop-vs-range-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.049017 | -6.041 |
| w2 | 27 | 0.089122 | 0.358 |
| w3 | 21 | 0.206077 | 21.421 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.09751 | 5.213 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.047282 | 2.125 |
| w9 | 11 | -0.067391 | -9.984 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.092316 | 4.104 |
| w13 | 22 | 0.088228 | 11.054 |
| w14 | 21 | 0.216974 | 22.305 |
| w15 | 5 | -0.078786 | -4.272 |
| w16 | 18 | 0.264185 | 27.982 |
| w17 | 0 | None | 0.0 |
| w18 | 38 | 0.130078 | 17.537 |
| w19 | 0 | None | 0.0 |
| w20 | 12 | 0.114433 | 8.134 |
| w21 | 0 | None | 0.0 |
| w22 | 21 | 0.207989 | 29.52 |
| w23 | 0 | None | 0.0 |
| w24 | 22 | 0.04819 | -0.337 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.165904 | -18.504 |
| w2 | 36 | 0.016675 | -12.899 |
| w3 | 13 | 0.258042 | 22.104 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 13 | 0.16333 | 13.715 |
| w9 | 11 | 0.075828 | 5.098 |
| w10 | 2 | 0.122215 | 2.562 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 41 | 0.191706 | 22.33 |
| w15 | 7 | -0.00908 | -1.288 |
| w16 | 20 | 0.221258 | 27.069 |
| w17 | 1 | -0.006609 | 0.037 |
| w18 | 12 | 0.033635 | 5.312 |
| w19 | 1 | None | -0.057 |
| w20 | 25 | 0.152217 | 5.669 |
| w21 | 9 | 0.006392 | 2.055 |
| w22 | 39 | 0.066331 | -5.449 |
| w23 | 3 | 0.075447 | 2.819 |
| w24 | 12 | 0.151331 | 9.71 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 31 | 0.074658 | 2.825 |
| w3 | 1 | 0.393083 | 19.101 |
| w4 | 2 | 0.074385 | 3.102 |
| w5 | 8 | 0.000762 | -2.474 |
| w6 | 1 | 0.066606 | 2.334 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.000725 | 2.447 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.063497 | 3.529 |
| w13 | 7 | 0.080505 | 5.156 |
| w14 | 29 | 0.181561 | 17.664 |
| w15 | 12 | 0.118061 | 11.953 |
| w16 | 18 | 0.302506 | 33.419 |
| w17 | 3 | 0.051073 | 4.458 |
| w18 | 22 | 0.145506 | 12.565 |
| w19 | 1 | -0.041622 | -1.042 |
| w20 | 22 | 0.095106 | 3.597 |
| w21 | 1 | 0.047127 | 2.174 |
| w22 | 24 | 0.115644 | 11.523 |
| w23 | 3 | 0.081896 | 6.001 |
| w24 | 27 | -0.034777 | -9.935 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.06974 | -12.599 |
| w2 | 25 | 0.011332 | -4.613 |
| w3 | 2 | 0.148825 | 8.022 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.004642 | -0.159 |
| w7 | 0 | None | 0.0 |
| w8 | 12 | 0.090462 | 4.385 |
| w9 | 2 | 0.032662 | 0.53 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 28 | 0.129242 | 7.5 |
| w15 | 4 | 0.08815 | 4.183 |
| w16 | 19 | 0.254535 | 27.459 |
| w17 | 0 | None | 0.0 |
| w18 | 21 | 0.201608 | 24.219 |
| w19 | 23 | 0.272766 | 34.965 |
| w20 | 2 | 0.253207 | 10.783 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 7 | 0.011053 | -0.127 |
| w24 | 3 | 0.014481 | 1.014 |

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
| w1 | 4 | 0.130986 | 6.576 |
| w2 | 0 | -0.035959 | 0.0 |
| w3 | 0 | 0.031369 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.043222 | 1.56 |
| w8 | 4 | 0.101666 | 4.268 |
| w9 | 6 | 0.090833 | 5.501 |
| w10 | 0 | None | 0.0 |
| w11 | 8 | 0.024625 | 6.106 |
| w12 | 0 | None | 0.0 |
| w14 | 8 | -0.007928 | -1.176 |
| w15 | 6 | 0.015843 | 0.758 |
| w16 | 22 | 0.2477 | 43.345 |
| w17 | 3 | -0.011939 | -1.795 |
| w18 | 14 | 0.034206 | 2.179 |
| w19 | 12 | -0.041432 | -8.769 |
| w20 | 5 | 0.037188 | 4.779 |
| w21 | 5 | -0.020317 | 3.248 |
| w22 | 23 | 0.100586 | 11.82 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | 0.04892 | 0.273 |

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
| w1 | 1 | 0.021729 | 0.965 |
| w2 | 32 | 0.080923 | 1.942 |
| w3 | 10 | 0.19466 | 15.161 |
| w4 | 6 | -0.033936 | -2.119 |
| w5 | 12 | 0.084131 | 7.434 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | -0.063448 | -2.051 |
| w8 | 9 | 0.166543 | 5.483 |
| w9 | 24 | 0.108135 | 5.91 |
| w10 | 3 | -0.04842 | 2.01 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 10 | 0.086173 | 5.56 |
| w14 | 22 | 0.159338 | 12.982 |
| w15 | 10 | -0.05213 | -6.009 |
| w16 | 23 | 0.130354 | 20.912 |
| w17 | 9 | 0.203334 | 18.209 |
| w18 | 23 | 0.131417 | 14.895 |
| w19 | 34 | 0.086241 | 4.95 |
| w20 | 12 | 0.089477 | 11.505 |
| w21 | 6 | -0.012335 | 0.494 |
| w22 | 29 | -0.004517 | -7.323 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

