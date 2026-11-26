# Backtest of 058-01_rising-calm-dip-rebound_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/058-01_rising-calm-dip-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.046187 | -0.052 |
| w2 | 6 | -0.175053 | -8.785 |
| w3 | 0 | None | 0.0 |
| w4 | 28 | -0.075779 | 25.211 |
| w5 | 21 | -0.022188 | -15.52 |
| w6 | 2 | -0.132618 | 0.166 |
| w7 | 4 | 0.028393 | -3.529 |
| w8 | 7 | 0.027257 | 7.977 |
| w9 | 0 | None | 0.0 |
| w10 | 21 | 0.050749 | 8.549 |
| w11 | 9 | -0.081796 | -7.091 |
| w12 | 27 | 0.05205 | -6.036 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | 0.054674 | 0.0 |
| w16 | 14 | -0.005892 | -3.718 |
| w17 | 14 | -0.232645 | 0.063 |
| w18 | 10 | 0.139931 | 5.7 |
| w19 | 5 | 0.020774 | 21.308 |
| w20 | 0 | None | 0.0 |
| w21 | 10 | -0.084445 | 8.036 |
| w22 | 6 | 0.017705 | 1.708 |
| w23 | 26 | 0.004738 | -5.455 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.026377 | -5.95 |
| w2 | 2 | -0.082461 | -3.943 |
| w3 | 0 | -0.18194 | 0.0 |
| w4 | 35 | -0.026751 | 29.529 |
| w5 | 10 | 0.04115 | -10.034 |
| w6 | 6 | 0.195739 | 2.201 |
| w7 | 16 | 0.061253 | -11.253 |
| w8 | 19 | 0.110824 | 20.121 |
| w9 | 0 | None | 0.0 |
| w10 | 23 | 0.01944 | 12.68 |
| w11 | 10 | -0.002623 | 14.66 |
| w12 | 30 | 0.06121 | 12.432 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | 0.004187 | -9.694 |
| w15 | 12 | 0.099403 | 1.113 |
| w16 | 4 | -0.034551 | 2.867 |
| w17 | 5 | 0.090825 | 7.584 |
| w18 | 12 | 0.097913 | 10.524 |
| w19 | 2 | 0.057479 | 12.787 |
| w20 | 1 | -0.028873 | -3.044 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 27 | -0.052974 | 8.605 |
| w24 | 9 | -0.153624 | -8.297 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.019551 | -1.901 |
| w2 | 3 | -0.02464 | -5.104 |
| w3 | 14 | -0.029378 | -6.172 |
| w4 | 21 | -0.004303 | -4.255 |
| w5 | 6 | -0.012177 | -6.996 |
| w6 | 10 | -0.054499 | -5.068 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | 0.225547 | 19.057 |
| w9 | 0 | None | 0.0 |
| w10 | 16 | 0.134622 | 4.814 |
| w11 | 3 | 0.098255 | 7.718 |
| w12 | 11 | -0.071558 | 7.486 |
| w13 | 4 | 0.119134 | -3.465 |
| w14 | 0 | None | 0.0 |
| w15 | 16 | 0.044501 | -6.401 |
| w16 | 15 | 0.072513 | 13.586 |
| w17 | 4 | -0.003313 | 8.327 |
| w18 | 6 | 0.055298 | 0.785 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 21 | 0.101074 | 9.419 |
| w24 | 2 | 0.059066 | 0.046 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.050411 | -7.366 |
| w2 | 14 | 0.113138 | 7.217 |
| w3 | 4 | 0.171525 | 7.999 |
| w4 | 19 | 0.008621 | 7.719 |
| w5 | 8 | -0.284938 | -13.417 |
| w6 | 16 | -0.021754 | 7.759 |
| w7 | 0 | None | 0.0 |
| w8 | 19 | 0.01034 | 8.817 |
| w9 | 0 | None | 0.0 |
| w10 | 27 | 0.175876 | 16.024 |
| w11 | 7 | 0.042592 | 13.02 |
| w12 | 0 | None | 0.0 |
| w14 | 6 | 0.003866 | 2.401 |
| w15 | 10 | -0.020906 | 0.186 |
| w16 | 9 | -0.020602 | -5.627 |
| w17 | 22 | 0.113691 | 8.552 |
| w18 | 3 | 0.065915 | -1.448 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.287275 | 19.862 |
| w21 | 0 | -0.017523 | 0.0 |
| w22 | 3 | 0.041581 | -4.944 |
| w23 | 4 | -0.003275 | 8.491 |
| w24 | 2 | 0.038916 | -3.732 |

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
| w1 | 8 | 0.046846 | -6.647 |
| w2 | 0 | -0.157508 | 0.0 |
| w3 | 0 | -0.136009 | 0.0 |
| w4 | 0 | -0.084762 | 0.0 |
| w5 | 5 | -0.119645 | -4.995 |
| w6 | 6 | 0.083064 | 0.635 |
| w8 | 3 | -0.180056 | -4.605 |
| w9 | 6 | -0.010975 | -1.125 |
| w10 | 14 | 0.101367 | 5.801 |
| w11 | 0 | None | 0.0 |
| w12 | 13 | 0.135852 | -5.725 |
| w14 | 9 | 0.043137 | -1.679 |
| w15 | 10 | -0.049769 | -7.522 |
| w16 | 2 | 0.043512 | 3.302 |
| w17 | 1 | -0.123166 | -3.614 |
| w18 | 8 | 0.154035 | 7.997 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | -0.007058 | 2.274 |
| w22 | 3 | 0.004222 | -7.295 |
| w23 | 13 | 0.038501 | -1.973 |
| w24 | 4 | 0.117157 | 1.137 |

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
| w1 | 11 | -0.121345 | -11.901 |
| w2 | 4 | 0.00412 | -5.163 |
| w3 | 0 | None | 0.0 |
| w4 | 6 | -0.158693 | -4.786 |
| w5 | 3 | -0.097757 | -10.813 |
| w6 | 8 | 0.038638 | 7.003 |
| w7 | 6 | -0.065371 | -5.353 |
| w8 | 14 | -0.055134 | -8.456 |
| w9 | 0 | None | 0.0 |
| w10 | 27 | 0.161584 | 26.456 |
| w11 | 6 | 0.04518 | 17.156 |
| w12 | 7 | -0.122801 | 32.412 |
| w13 | 0 | None | 0.0 |
| w14 | 2 | 0.04216 | -14.614 |
| w15 | 14 | 0.015502 | 7.975 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.238087 | 11.18 |
| w18 | 5 | 0.068196 | 8.554 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 5 | -0.108329 | 5.572 |
| w22 | 2 | -0.001575 | -4.579 |
| w23 | 10 | -0.003922 | -0.183 |
| w24 | 2 | 0.062679 | 41.167 |

