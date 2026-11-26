# Backtest of 031-03_up-streak-length-continuation_1d

- Plan: `../../../../03_test_plan/night6_streak_run/plans/031-03_up-streak-length-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | -0.010997 | -21.863 |
| w2 | 40 | -0.033143 | -32.749 |
| w3 | 41 | 0.004921 | -30.557 |
| w4 | 35 | 0.138663 | 124.1 |
| w5 | 39 | 0.00125 | -8.417 |
| w6 | 40 | 0.009462 | 113.463 |
| w7 | 40 | 0.138423 | -14.905 |
| w8 | 39 | -0.07777 | 48.454 |
| w9 | 44 | -0.019001 | -32.426 |
| w10 | 28 | -0.141563 | 36.871 |
| w11 | 35 | -0.048354 | 63.219 |
| w12 | 45 | -0.041023 | -19.372 |
| w13 | 31 | -0.042785 | -4.109 |
| w14 | 43 | -0.01901 | -61.672 |
| w15 | 36 | 0.163199 | 72.138 |
| w16 | 43 | -0.092943 | -8.425 |
| w17 | 38 | 0.071014 | 194.082 |
| w18 | 33 | -0.07526 | -18.301 |
| w19 | 33 | 0.053282 | 63.168 |
| w20 | 43 | -0.036202 | -13.419 |
| w21 | 46 | 0.005919 | 61.405 |
| w22 | 38 | -0.086016 | -22.578 |
| w23 | 33 | 0.005715 | 10.153 |
| w24 | 49 | 0.024537 | -37.551 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | 0.047863 | -25.079 |
| w2 | 39 | -0.004648 | -25.587 |
| w3 | 25 | -0.045 | -21.464 |
| w4 | 31 | 0.024717 | 53.756 |
| w5 | 42 | -0.058814 | -12.144 |
| w6 | 35 | 0.007949 | 62.589 |
| w7 | 31 | 0.088495 | -30.998 |
| w8 | 26 | -0.154172 | 12.514 |
| w9 | 37 | 0.009647 | -5.201 |
| w10 | 41 | 0.063709 | 113.503 |
| w11 | 40 | -0.094122 | 93.117 |
| w12 | 39 | -0.056105 | -7.302 |
| w13 | 30 | 0.141459 | 19.67 |
| w14 | 19 | -0.033226 | -25.586 |
| w15 | 36 | 0.068429 | 25.626 |
| w16 | 39 | -0.047288 | 23.846 |
| w17 | 37 | -0.017428 | 35.962 |
| w18 | 46 | -0.04728 | 21.218 |
| w19 | 36 | -0.017878 | 43.084 |
| w20 | 41 | -0.05087 | -13.508 |
| w21 | 49 | -0.017224 | 56.144 |
| w22 | 30 | -0.143901 | -56.877 |
| w23 | 38 | 0.000705 | 130.44 |
| w24 | 32 | 0.092351 | -32.984 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.087123 | -22.128 |
| w2 | 35 | -0.074716 | -34.551 |
| w3 | 38 | 0.018599 | 36.837 |
| w4 | 40 | -0.042933 | 11.485 |
| w5 | 33 | 0.079715 | -16.557 |
| w6 | 45 | 0.023718 | 7.178 |
| w7 | 31 | -0.063393 | -40.573 |
| w8 | 33 | 0.009191 | 70.588 |
| w9 | 42 | -0.054733 | -32.781 |
| w10 | 34 | -0.260659 | 36.572 |
| w11 | 46 | 0.053865 | 57.606 |
| w12 | 45 | 0.045757 | -12.187 |
| w13 | 22 | -0.135606 | -15.077 |
| w14 | 23 | -0.105787 | -55.965 |
| w15 | 30 | 0.012145 | -21.729 |
| w16 | 33 | -0.094918 | 11.601 |
| w17 | 38 | -0.05863 | 95.295 |
| w18 | 27 | -0.098728 | -6.741 |
| w19 | 50 | -0.028568 | 29.562 |
| w20 | 33 | 0.00678 | -30.821 |
| w21 | 53 | -0.144615 | 23.939 |
| w22 | 43 | 0.05027 | -13.865 |
| w23 | 39 | -0.073007 | 13.391 |
| w24 | 44 | -0.113754 | -48.942 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | -0.059026 | -6.853 |
| w2 | 35 | -0.066785 | -3.388 |
| w3 | 40 | -0.165062 | -22.809 |
| w4 | 33 | -0.148811 | -2.684 |
| w5 | 36 | 0.09939 | -19.67 |
| w6 | 46 | -0.09629 | 10.491 |
| w7 | 24 | -0.063884 | -19.359 |
| w8 | 26 | -0.192886 | 32.259 |
| w9 | 39 | -0.017093 | -32.595 |
| w10 | 32 | -0.173847 | 50.234 |
| w11 | 33 | -0.045559 | 96.809 |
| w12 | 46 | -0.090572 | -33.88 |
| w14 | 23 | -0.195528 | -60.627 |
| w15 | 32 | 0.0578 | 21.261 |
| w16 | 29 | -0.061938 | 40.247 |
| w17 | 32 | -0.215735 | 50.117 |
| w18 | 33 | -0.120475 | -14.917 |
| w19 | 45 | -0.036666 | -58.018 |
| w20 | 44 | -0.096696 | 21.973 |
| w21 | 41 | -0.016397 | 28.407 |
| w22 | 39 | 0.004099 | 27.526 |
| w23 | 50 | 0.034985 | -22.662 |
| w24 | 47 | -0.012845 | 31.495 |

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
| w1 | 33 | 0.067386 | -11.107 |
| w2 | 15 | -0.075882 | -36.66 |
| w3 | 0 | -0.096472 | 0.0 |
| w4 | 0 | -0.170171 | 0.0 |
| w5 | 2 | -0.077063 | -5.41 |
| w6 | 47 | 0.030807 | 42.53 |
| w8 | 34 | -0.216637 | -19.514 |
| w9 | 40 | -0.001493 | -13.999 |
| w10 | 31 | -0.055015 | 42.237 |
| w11 | 33 | -0.065893 | 144.068 |
| w12 | 28 | -0.113366 | -21.897 |
| w14 | 31 | 0.148901 | 19.858 |
| w15 | 37 | 0.076012 | -15.361 |
| w16 | 29 | -0.058049 | -15.908 |
| w17 | 32 | 0.041659 | 145.162 |
| w18 | 28 | -0.155972 | 17.817 |
| w19 | 26 | -0.127355 | -11.667 |
| w20 | 40 | 0.02709 | -2.765 |
| w21 | 34 | 0.195291 | 293.065 |
| w22 | 39 | -0.026849 | -16.373 |
| w23 | 47 | 0.046784 | 8.077 |
| w24 | 34 | -0.020718 | -40.29 |

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
| w1 | 38 | 0.001474 | 9.57 |
| w2 | 37 | -0.007432 | -26.131 |
| w3 | 41 | -0.029251 | -35.282 |
| w4 | 34 | -0.041795 | -7.563 |
| w5 | 47 | -3.6e-05 | -47.649 |
| w6 | 51 | -0.061236 | 6.034 |
| w7 | 33 | 0.02172 | -32.211 |
| w8 | 26 | -0.162315 | 12.433 |
| w9 | 36 | 0.08665 | -15.628 |
| w10 | 33 | -0.125334 | 34.325 |
| w11 | 36 | 0.149217 | 113.431 |
| w12 | 40 | 0.045118 | 12.124 |
| w14 | 40 | -0.036047 | -51.633 |
| w15 | 32 | -0.059114 | -13.554 |
| w16 | 33 | 0.021532 | 28.559 |
| w17 | 31 | -0.062234 | 1.141 |
| w18 | 36 | -0.134128 | -11.686 |
| w19 | 32 | 0.031538 | -2.607 |
| w20 | 36 | 0.038952 | 24.855 |
| w21 | 41 | 0.088024 | 80.447 |
| w22 | 31 | 0.016663 | -26.93 |
| w23 | 36 | 0.038376 | 1.789 |
| w24 | 46 | 0.125065 | 382.45 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

