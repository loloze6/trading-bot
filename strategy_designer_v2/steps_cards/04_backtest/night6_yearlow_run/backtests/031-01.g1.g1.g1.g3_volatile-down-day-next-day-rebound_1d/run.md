# Backtest of 031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound_1d

- Plan: `../../../../03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.03568 | 0.947 |
| w2 | 11 | 0.142372 | 7.572 |
| w3 | 7 | 0.276057 | 12.846 |
| w4 | 3 | 0.080841 | 2.777 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | 0.05864 | 1.356 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 24 | 0.03061 | 5.542 |
| w12 | 0 | None | 0.0 |
| w13 | 24 | -0.01135 | -4.686 |
| w14 | 5 | -0.000919 | -1.023 |
| w15 | 23 | -0.011881 | 3.132 |
| w16 | 10 | 0.339215 | 18.793 |
| w17 | 6 | 0.016785 | 4.785 |
| w18 | 27 | 0.159408 | 17.128 |
| w19 | 28 | 0.131427 | 22.317 |
| w20 | 14 | 0.126481 | 7.984 |
| w21 | 5 | 0.042077 | 3.122 |
| w22 | 14 | 0.117254 | 7.52 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | -0.09108 | -5.111 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 24 | 0.166655 | 18.88 |
| w3 | 7 | 0.002205 | -3.413 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | 0.14654 | 8.28 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.133158 | 6.035 |
| w9 | 2 | -0.006392 | -2.074 |
| w10 | 0 | None | 0.0 |
| w11 | 11 | 0.141075 | 12.47 |
| w12 | 0 | None | 0.0 |
| w13 | 14 | -0.088148 | -7.441 |
| w14 | 16 | 0.127814 | 9.022 |
| w15 | 1 | 0.121535 | 5.123 |
| w16 | 19 | 0.094627 | 5.987 |
| w17 | 10 | 0.11501 | 12.65 |
| w18 | 21 | 0.097195 | 11.258 |
| w19 | 27 | -0.015586 | 4.208 |
| w20 | 17 | 0.199511 | 17.743 |
| w21 | 9 | -0.037216 | -1.366 |
| w22 | 19 | 0.139329 | 6.686 |
| w23 | 11 | 0.086891 | 10.356 |
| w24 | 4 | -0.062507 | -2.305 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 14 | 0.10476 | 5.501 |
| w3 | 8 | 0.358104 | 21.141 |
| w4 | 4 | 0.120807 | 3.872 |
| w5 | 12 | 0.033479 | -0.499 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 17 | 0.017282 | 4.091 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 14 | 0.0713 | 7.127 |
| w12 | 6 | 0.004208 | -1.001 |
| w13 | 2 | 0.022242 | 0.252 |
| w14 | 1 | 0.021154 | 0.356 |
| w15 | 7 | 0.200467 | 12.567 |
| w16 | 15 | 0.093899 | 1.284 |
| w17 | 22 | 0.089722 | 13.897 |
| w18 | 17 | 0.177844 | 13.003 |
| w19 | 21 | 0.099131 | 12.863 |
| w20 | 6 | 0.051931 | 0.712 |
| w21 | 18 | -0.002405 | 2.966 |
| w22 | 16 | -0.14327 | -14.453 |
| w23 | 0 | None | 0.0 |
| w24 | 16 | -0.10931 | -8.765 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.014589 | -0.055 |
| w2 | 17 | 0.098299 | 3.912 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 27 | -0.003719 | 14.54 |
| w12 | 0 | None | 0.0 |
| w14 | 6 | -0.037512 | -4.979 |
| w15 | 7 | 0.026253 | 1.199 |
| w16 | 24 | 0.04288 | -3.554 |
| w17 | 6 | 0.168564 | 9.735 |
| w18 | 22 | 0.255671 | 31.733 |
| w19 | 39 | 0.244306 | 32.101 |
| w20 | 9 | 0.038838 | 3.056 |
| w21 | 9 | 0.066937 | 3.623 |
| w22 | 1 | 0.044359 | 1.298 |
| w23 | 17 | -0.203386 | -19.588 |
| w24 | 16 | -0.051025 | -1.661 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=385. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | 0.212137 | 0.0 |
| w4 | 0 | 0.154136 | 0.0 |
| w5 | 4 | -0.018057 | -0.304 |
| w6 | 1 | 0.197334 | 6.679 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 21 | 0.009989 | 9.903 |
| w12 | 0 | None | 0.0 |
| w14 | 3 | 0.067844 | 1.527 |
| w15 | 8 | -0.008599 | -0.768 |
| w16 | 21 | 0.06241 | 0.62 |
| w17 | 18 | -0.066911 | -7.8 |
| w18 | 8 | 0.07277 | 1.777 |
| w19 | 21 | 0.104152 | 6.782 |
| w20 | 12 | -0.070238 | -6.485 |
| w21 | 12 | -0.020861 | 2.874 |
| w22 | 15 | 0.094458 | 7.112 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=385. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=385. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.195876 | 0.0 |
| w2 | 9 | 0.125395 | 6.846 |
| w3 | 6 | 0.032599 | 0.255 |
| w4 | 0 | None | 0.0 |
| w5 | 4 | 0.20776 | 12.396 |
| w6 | 1 | -0.001902 | -0.066 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 4 | 0.127903 | 2.991 |
| w10 | 4 | 0.009309 | 1.13 |
| w11 | 22 | 0.01565 | 9.836 |
| w12 | 8 | -0.022301 | -0.875 |
| w13 | 11 | -0.012572 | -1.345 |
| w14 | 5 | -0.00056 | -2.8 |
| w15 | 8 | 0.124336 | 3.484 |
| w16 | 19 | 0.027403 | 3.433 |
| w17 | 15 | 0.028987 | 0.316 |
| w18 | 22 | 0.236422 | 23.386 |
| w19 | 32 | 0.073234 | 1.709 |
| w20 | 6 | 0.068564 | 1.598 |
| w21 | 20 | -0.025961 | 1.326 |
| w22 | 18 | 0.074682 | 4.323 |
| w23 | 2 | 0.08338 | 2.039 |
| w24 | 30 | -0.070147 | 5.074 |

