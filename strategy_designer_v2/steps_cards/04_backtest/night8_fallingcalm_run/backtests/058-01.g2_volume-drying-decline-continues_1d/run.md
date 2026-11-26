# Backtest of 058-01.g2_volume-drying-decline-continues_1d

- Plan: `../../../../03_test_plan/night8_fallingcalm_run/plans/058-01.g2_volume-drying-decline-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.1537 | 28.107 |
| w2 | 6 | 0.085969 | 10.683 |
| w3 | 10 | 0.016667 | -3.586 |
| w4 | 1 | 0.008967 | -2.62 |
| w5 | 6 | -0.033691 | -4.033 |
| w6 | 1 | 0.112639 | -0.04 |
| w7 | 7 | 0.081066 | 3.93 |
| w8 | 3 | 0.065302 | 1.227 |
| w9 | 14 | -0.070731 | -4.692 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.034784 | -2.784 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | -0.099211 | -3.439 |
| w14 | 7 | -0.021874 | 6.354 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | -0.056267 | -12.039 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.071939 | -2.913 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.022724 | -0.93 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | -0.017811 | -0.247 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.191551 | 31.059 |
| w2 | 2 | -0.088467 | 2.741 |
| w3 | 15 | -0.059014 | -17.463 |
| w4 | 1 | -0.053496 | -5.013 |
| w5 | 7 | -0.027599 | 0.578 |
| w6 | 8 | -0.007263 | 0.04 |
| w7 | 14 | 0.127085 | 38.222 |
| w8 | 0 | None | 0.0 |
| w9 | 7 | 0.00178 | 9.985 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 8 | 0.162854 | 20.058 |
| w14 | 9 | 0.005072 | 9.609 |
| w15 | 7 | 0.08259 | 10.977 |
| w16 | 1 | -0.02107 | -1.693 |
| w17 | 4 | -0.056728 | -15.706 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.028423 | -0.861 |
| w22 | 2 | -0.010475 | -0.743 |
| w23 | 0 | None | 0.0 |
| w24 | 16 | -0.033575 | 5.245 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.001199 | 2.305 |
| w2 | 2 | -0.125107 | -8.3 |
| w3 | 5 | 0.00736 | -0.999 |
| w4 | 4 | -0.104658 | -6.679 |
| w5 | 4 | -0.106187 | 0.757 |
| w6 | 10 | 0.00812 | 1.527 |
| w7 | 17 | 0.137694 | 36.928 |
| w8 | 0 | None | 0.0 |
| w9 | 24 | -0.027071 | 15.984 |
| w10 | 9 | -0.075902 | -0.693 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.030176 | 1.035 |
| w13 | 17 | -0.028144 | -6.515 |
| w14 | 7 | 0.098806 | 28.45 |
| w15 | 4 | 0.089954 | 13.583 |
| w16 | 1 | -0.055033 | -11.92 |
| w17 | 4 | -0.01986 | -6.708 |
| w18 | 9 | 0.013859 | -6.63 |
| w19 | 0 | None | 0.0 |
| w20 | 9 | -0.071025 | 0.514 |
| w21 | 4 | -0.038173 | -5.383 |
| w22 | 3 | 0.145166 | 8.449 |
| w23 | 2 | -0.116672 | -3.529 |
| w24 | 9 | -0.020957 | -2.114 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.033194 | -7.803 |
| w2 | 0 | None | 0.0 |
| w3 | 11 | 0.005844 | -0.495 |
| w4 | 0 | -0.041797 | 0.0 |
| w5 | 8 | -0.173574 | -5.178 |
| w6 | 0 | -0.013728 | 0.0 |
| w7 | 16 | 0.10991 | 26.576 |
| w8 | 2 | 0.087342 | 2.25 |
| w9 | 19 | -0.174605 | -6.903 |
| w10 | 2 | -0.308113 | -1.246 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.111354 | -1.851 |
| w14 | 4 | -0.013223 | 7.859 |
| w15 | 5 | 0.006189 | 11.55 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.050433 | -6.724 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.208402 | -1.661 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | -0.147562 | -12.769 |
| w23 | 1 | 0.08545 | 0.875 |
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
| w1 | 15 | 0.056764 | 25.971 |
| w2 | 2 | 0.037999 | 8.815 |
| w3 | 0 | 0.061139 | 0.0 |
| w4 | 0 | -0.001171 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | 0.001267 | -5.361 |
| w8 | 9 | -0.054713 | -3.459 |
| w9 | 21 | 0.09768 | 11.032 |
| w10 | 3 | -0.138875 | -6.386 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.066695 | 2.221 |
| w14 | 3 | -0.093274 | -0.812 |
| w15 | 12 | 0.066712 | 14.645 |
| w16 | 3 | -0.144137 | -8.432 |
| w17 | 4 | -0.049765 | -7.206 |
| w18 | 8 | 0.01845 | -0.523 |
| w19 | 5 | -0.074112 | -3.245 |
| w20 | 9 | 0.026042 | 3.827 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.071581 | -3.091 |
| w23 | 2 | -0.020124 | -3.686 |
| w24 | 21 | 0.023742 | 16.099 |

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
| w1 | 12 | 0.03245 | -2.367 |
| w2 | 4 | -0.143236 | -2.887 |
| w3 | 13 | 0.000247 | 17.5 |
| w4 | 5 | -0.09104 | -8.207 |
| w5 | 12 | -0.075496 | 1.394 |
| w6 | 7 | -0.060398 | -2.201 |
| w7 | 8 | -0.049128 | -3.54 |
| w8 | 7 | 0.013607 | -3.719 |
| w9 | 8 | -0.163723 | -14.996 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.070984 | -9.246 |
| w13 | 10 | 0.102089 | 19.782 |
| w14 | 16 | -0.077709 | 2.029 |
| w15 | 7 | 0.054354 | 12.399 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | -0.008149 | -12.672 |
| w18 | 4 | -0.067298 | -3.52 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | -0.062758 | -1.638 |
| w21 | 7 | -0.051877 | -16.637 |
| w22 | 0 | None | 0.0 |
| w23 | 4 | 0.064795 | 1.738 |
| w24 | 0 | None | 0.0 |

