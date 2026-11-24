# Backtest of 031-01_extreme-rise-partly-reverses_1d

- Plan: `../../../../03_test_plan/night6_longreversal_run/plans/031-01_extreme-rise-partly-reverses_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 10 | 0.11054 | -34.065 |
| w5 | 3 | -0.018976 | -15.695 |
| w6 | 7 | 0.059224 | -28.474 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.052259 | 1.12 |
| w9 | 1 | 0.014625 | 8.118 |
| w10 | 4 | 0.12033 | -25.601 |
| w11 | 20 | -0.051728 | -54.276 |
| w12 | 6 | 0.012222 | -4.685 |
| w13 | 4 | 0.032675 | 14.165 |
| w14 | 0 | None | 0.0 |
| w15 | 21 | -0.112462 | -67.271 |
| w16 | 1 | 0.041813 | 20.3 |
| w17 | 7 | -0.109923 | -59.719 |
| w18 | 5 | 0.011236 | 20.819 |
| w19 | 20 | 0.142229 | -73.849 |
| w20 | 4 | -0.078173 | -10.431 |
| w21 | 5 | 0.02977 | -31.522 |
| w22 | 8 | 0.004043 | -4.124 |
| w23 | 8 | -0.010217 | -17.746 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | 0.146318 | 18.806 |
| w4 | 5 | 0.042272 | -19.545 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.043862 | -22.332 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | -0.017811 | -20.064 |
| w9 | 0 | None | 0.0 |
| w10 | 11 | 0.071849 | -68.491 |
| w11 | 21 | 0.038639 | -70.648 |
| w12 | 5 | 0.049234 | -10.706 |
| w13 | 6 | 0.047733 | -1.747 |
| w14 | 0 | None | 0.0 |
| w15 | 14 | -0.094619 | -55.695 |
| w16 | 4 | 0.137951 | 47.383 |
| w17 | 7 | 0.248394 | -20.185 |
| w18 | 4 | 0.058159 | 7.74 |
| w19 | 21 | 0.081471 | -53.369 |
| w20 | 4 | 0.007568 | -13.166 |
| w21 | 4 | 0.093834 | 4.978 |
| w22 | 3 | 0.049437 | 16.102 |
| w23 | 20 | 0.008288 | -54.044 |
| w24 | 7 | 0.002072 | 11.21 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.101115 | 8.388 |
| w4 | 11 | -0.051177 | -19.782 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.080654 | -38.064 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.287531 | 15.065 |
| w11 | 15 | 0.122688 | -42.134 |
| w12 | 4 | 0.023906 | -5.736 |
| w13 | 7 | 0.060357 | 4.81 |
| w14 | 0 | None | 0.0 |
| w15 | 13 | -0.150686 | -34.425 |
| w16 | 3 | 0.074501 | 21.415 |
| w17 | 2 | -0.016016 | -37.118 |
| w18 | 5 | -0.068741 | 16.63 |
| w19 | 2 | 0.188247 | 23.137 |
| w20 | 0 | None | 0.0 |
| w21 | 6 | 0.057337 | -14.0 |
| w22 | 5 | 0.00038 | 4.666 |
| w23 | 2 | 0.073215 | -1.293 |
| w24 | 2 | 0.038983 | 17.477 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.141349 | 16.762 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | 0.149402 | 5.847 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.159071 | 12.518 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | 0.180227 | -3.769 |
| w11 | 14 | -0.023611 | -56.995 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 8 | 0.009249 | -34.034 |
| w16 | 7 | 0.1437 | 52.114 |
| w17 | 10 | -0.056864 | -44.857 |
| w18 | 2 | 0.040834 | 22.816 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | 0.085674 | 5.788 |
| w21 | 1 | None | -0.127 |
| w22 | 4 | 0.136067 | 8.98 |
| w23 | 10 | -0.046297 | -24.17 |
| w24 | 6 | 0.131543 | -15.254 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | 0.022129 | 0.0 |
| w4 | 0 | 0.072755 | 0.0 |
| w5 | 0 | 0.142002 | 0.0 |
| w6 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | 0.184564 | 14.031 |
| w11 | 10 | -0.021976 | -66.548 |
| w12 | 2 | 0.009723 | -1.746 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.199666 | 34.577 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.087321 | 31.294 |
| w18 | 5 | 0.167752 | 24.595 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 11 | -0.145629 | -76.635 |
| w22 | 8 | -0.021356 | -8.177 |
| w23 | 1 | 0.096662 | 4.066 |
| w24 | 0 | None | 0.0 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.108275 | 15.571 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.228606 | 31.078 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 8 | 0.130409 | -53.867 |
| w11 | 12 | 0.116882 | -50.077 |
| w12 | 3 | 0.096428 | 5.371 |
| w14 | 0 | None | 0.0 |
| w15 | 7 | -0.091257 | -7.762 |
| w16 | 7 | 0.206802 | 11.364 |
| w17 | 1 | 0.139885 | 9.438 |
| w18 | 2 | -0.022596 | 14.634 |
| w19 | 1 | 0.057888 | 21.286 |
| w20 | 3 | 0.046255 | -22.107 |
| w21 | 11 | 0.062631 | -55.115 |
| w22 | 1 | 0.120731 | 23.711 |
| w23 | 1 | 0.148408 | 17.304 |
| w24 | 17 | -0.032864 | -95.032 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

