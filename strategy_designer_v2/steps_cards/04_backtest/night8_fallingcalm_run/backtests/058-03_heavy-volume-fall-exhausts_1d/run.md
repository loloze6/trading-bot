# Backtest of 058-03_heavy-volume-fall-exhausts_1d

- Plan: `../../../../03_test_plan/night8_fallingcalm_run/plans/058-03_heavy-volume-fall-exhausts_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.031032 | 13.692 |
| w2 | 6 | 0.175698 | 23.619 |
| w3 | 10 | -0.050538 | -0.894 |
| w4 | 1 | 0.008432 | -2.62 |
| w5 | 5 | -0.01366 | -2.366 |
| w6 | 3 | 0.100568 | 4.66 |
| w7 | 8 | -0.041856 | -2.598 |
| w8 | 1 | 0.06869 | 0.459 |
| w9 | 19 | -0.149404 | -17.647 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.034784 | -2.797 |
| w12 | 4 | 0.018583 | 3.683 |
| w13 | 8 | 0.01789 | 1.351 |
| w14 | 5 | 0.068843 | 30.845 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | -0.057464 | -8.824 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.083692 | -6.826 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.022724 | -1.814 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | -0.189135 | -2.48 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.107294 | 17.055 |
| w2 | 2 | -0.088467 | 3.845 |
| w3 | 9 | -0.029065 | -5.531 |
| w4 | 1 | -0.054046 | -5.073 |
| w5 | 7 | -0.025142 | -3.871 |
| w6 | 8 | 0.059239 | -2.407 |
| w7 | 10 | 0.111972 | 23.318 |
| w8 | 0 | None | 0.0 |
| w9 | 12 | -0.051733 | -2.81 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.040388 | 2.117 |
| w13 | 9 | 0.195114 | 20.256 |
| w14 | 10 | 0.046687 | 6.127 |
| w15 | 4 | 0.097226 | 15.392 |
| w16 | 6 | -0.030731 | -22.585 |
| w17 | 4 | -0.056041 | -5.573 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.030662 | -1.922 |
| w22 | 4 | -0.008203 | -5.081 |
| w23 | 0 | None | 0.0 |
| w24 | 9 | -0.044543 | 0.188 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.067373 | -3.514 |
| w2 | 3 | 0.047889 | 9.284 |
| w3 | 4 | 0.015736 | 0.042 |
| w4 | 4 | -0.11043 | -5.982 |
| w5 | 4 | -0.10143 | 1.184 |
| w6 | 11 | -0.008661 | 1.968 |
| w7 | 12 | -0.0121 | 40.222 |
| w8 | 0 | None | 0.0 |
| w9 | 17 | 0.005944 | 14.988 |
| w10 | 10 | -0.047902 | -1.628 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.007874 | 0.684 |
| w13 | 8 | -0.113016 | -9.507 |
| w14 | 14 | 0.083237 | 33.297 |
| w15 | 5 | -0.095587 | -0.759 |
| w16 | 1 | -0.054991 | -10.914 |
| w17 | 4 | -0.034912 | -2.757 |
| w18 | 9 | -0.020429 | -12.695 |
| w19 | 2 | 0.110343 | 9.235 |
| w20 | 12 | -0.00724 | 6.178 |
| w21 | 4 | -0.035906 | -4.567 |
| w22 | 2 | -0.039891 | -3.549 |
| w23 | 2 | -0.116672 | -3.555 |
| w24 | 11 | -0.010831 | -4.436 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.172134 | -10.086 |
| w2 | 0 | None | 0.0 |
| w3 | 12 | -0.009822 | -0.058 |
| w4 | 6 | -0.255632 | -12.351 |
| w5 | 6 | -0.108339 | -6.408 |
| w6 | 5 | -0.01682 | -5.177 |
| w7 | 19 | -0.030614 | 12.658 |
| w8 | 1 | 0.083804 | 0.93 |
| w9 | 19 | -0.072025 | 7.321 |
| w10 | 2 | 0.308113 | 0.358 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | -0.071508 | -2.18 |
| w14 | 10 | 0.028825 | 19.025 |
| w15 | 6 | 0.042548 | 10.578 |
| w16 | 2 | -0.156037 | -18.872 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.05156 | -3.853 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | 0.044598 | 0.0 |
| w21 | 4 | -0.058676 | -4.317 |
| w22 | 4 | -0.152447 | -13.509 |
| w23 | 6 | 0.105632 | 15.923 |
| w24 | 0 | None | 0.0 |

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
| w1 | 10 | -0.014758 | -1.164 |
| w2 | 2 | 0.067657 | 8.588 |
| w3 | 0 | 0.051383 | 0.0 |
| w4 | 0 | -0.004762 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | -0.007918 | -2.481 |
| w8 | 11 | 0.071948 | 3.667 |
| w9 | 15 | -0.032808 | -7.239 |
| w10 | 3 | -0.138058 | -25.92 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.024565 | -0.634 |
| w14 | 6 | -0.167383 | -25.01 |
| w15 | 8 | 0.055088 | 3.162 |
| w16 | 3 | -0.129826 | -7.119 |
| w17 | 4 | -0.037244 | -11.536 |
| w18 | 5 | -0.020834 | -12.093 |
| w19 | 7 | -0.00173 | 1.342 |
| w20 | 8 | 0.095857 | 22.538 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.069 | -0.536 |
| w23 | 2 | -0.020124 | -3.064 |
| w24 | 18 | 0.027151 | 26.574 |

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
| w1 | 10 | -0.142161 | -12.277 |
| w2 | 5 | -0.135558 | -12.146 |
| w3 | 10 | 0.078929 | 35.308 |
| w4 | 3 | -0.092898 | -9.758 |
| w5 | 12 | 0.016097 | 8.399 |
| w6 | 6 | -0.067972 | -6.657 |
| w7 | 16 | -0.111005 | -18.31 |
| w8 | 14 | -0.03415 | -5.202 |
| w9 | 17 | -0.095152 | -9.562 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.079902 | -6.226 |
| w14 | 14 | -0.118304 | 8.877 |
| w15 | 8 | 0.059649 | 7.244 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | 0.022983 | -7.846 |
| w18 | 5 | -0.074926 | -4.953 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.040401 | -1.846 |
| w21 | 5 | -0.095125 | -26.271 |
| w22 | 0 | -0.180561 | 0.0 |
| w23 | 5 | -0.007666 | -3.546 |
| w24 | 0 | None | 0.0 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

