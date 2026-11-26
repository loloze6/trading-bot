# Backtest of 058-01.g1_thin-volume-deep-fall-continues_1d

- Plan: `../../../../03_test_plan/night8_fallingcalm_run/plans/058-01.g1_thin-volume-deep-fall-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.018629 | 5.053 |
| w2 | 3 | 0.183843 | 28.691 |
| w3 | 15 | 0.012977 | -14.255 |
| w4 | 3 | -0.001021 | -0.96 |
| w5 | 10 | -0.073218 | -9.694 |
| w6 | 2 | 0.101162 | 3.252 |
| w7 | 10 | -0.008908 | 2.553 |
| w8 | 4 | 0.059785 | 2.523 |
| w9 | 31 | -0.139348 | -16.949 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.034784 | -0.809 |
| w12 | 7 | -0.012122 | 0.153 |
| w13 | 6 | -0.011899 | -0.068 |
| w14 | 8 | 0.165364 | 25.45 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.097575 | -4.045 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | -0.081251 | -5.662 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.022724 | -7.428 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.149852 | 9.487 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.0077 | 4.607 |
| w2 | 2 | -0.088467 | 7.566 |
| w3 | 13 | -0.00635 | -0.488 |
| w4 | 4 | -0.07675 | -4.009 |
| w5 | 9 | -0.04661 | -1.97 |
| w6 | 17 | 0.034561 | -4.012 |
| w7 | 23 | 0.036832 | 27.851 |
| w8 | 0 | None | 0.0 |
| w9 | 29 | -0.073856 | -4.923 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.02259 | 0.651 |
| w13 | 8 | 0.123548 | 5.512 |
| w14 | 14 | 0.110112 | 35.602 |
| w15 | 14 | 0.061141 | 9.195 |
| w16 | 3 | -0.041544 | -5.535 |
| w17 | 4 | -0.057552 | -3.313 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.003487 | -0.632 |
| w22 | 4 | -0.007848 | 3.908 |
| w23 | 0 | None | 0.0 |
| w24 | 13 | 0.053694 | 6.533 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | -0.059724 | 4.149 |
| w2 | 3 | 0.113188 | 6.872 |
| w3 | 10 | 0.023501 | 0.239 |
| w4 | 5 | -0.127667 | -11.116 |
| w5 | 4 | -0.075769 | -0.101 |
| w6 | 9 | 0.090282 | 6.766 |
| w7 | 21 | -0.046445 | 12.845 |
| w8 | 0 | None | 0.0 |
| w9 | 29 | -0.108258 | 3.889 |
| w10 | 6 | -0.021403 | -1.863 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | -0.004665 | -0.47 |
| w13 | 9 | -0.040964 | -4.284 |
| w14 | 9 | 0.102274 | 18.143 |
| w15 | 12 | 0.075353 | 6.277 |
| w16 | 2 | -0.05573 | -2.937 |
| w17 | 7 | 0.000133 | -6.423 |
| w18 | 8 | 0.031761 | -1.125 |
| w19 | 2 | -0.110343 | -10.47 |
| w20 | 17 | -0.000977 | 3.99 |
| w21 | 6 | -0.02107 | -3.348 |
| w22 | 1 | 0.127037 | 11.477 |
| w23 | 0 | -0.116672 | 0.0 |
| w24 | 16 | -0.038528 | -2.812 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.111254 | -4.278 |
| w2 | 0 | None | 0.0 |
| w3 | 12 | -0.117444 | -4.221 |
| w4 | 7 | -0.266405 | -10.079 |
| w5 | 9 | -0.124746 | -9.139 |
| w6 | 1 | -0.006437 | -1.933 |
| w8 | 7 | 0.061231 | 2.87 |
| w9 | 39 | -0.096658 | 2.055 |
| w10 | 0 | -0.308113 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 15 | -0.060293 | -5.251 |
| w14 | 6 | 0.095226 | 29.077 |
| w15 | 5 | 0.023031 | 3.627 |
| w16 | 2 | -0.125738 | -15.767 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | -0.045513 | -2.139 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | -0.100516 | -3.78 |
| w21 | 7 | -0.122406 | -6.483 |
| w22 | 4 | -0.112322 | -4.511 |
| w23 | 7 | 0.05567 | 3.853 |
| w24 | 0 | None | 0.0 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 483 warm-up bars -- required_bars=493. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=493. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 21 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.057056 | 8.698 |
| w2 | 7 | -0.071743 | 22.223 |
| w3 | 0 | 0.027035 | 0.0 |
| w4 | 0 | -0.007204 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 7 | -0.082964 | -3.445 |
| w8 | 17 | -0.01608 | -2.401 |
| w9 | 21 | 0.070995 | 26.323 |
| w10 | 4 | -0.108294 | -9.871 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | -0.060879 | -2.811 |
| w15 | 6 | 0.052773 | 17.933 |
| w16 | 5 | -0.126399 | -14.693 |
| w17 | 4 | -0.059446 | -3.295 |
| w18 | 7 | 0.038384 | 1.709 |
| w19 | 13 | -0.089203 | -11.369 |
| w20 | 15 | 0.072629 | 11.187 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.068813 | -1.204 |
| w23 | 0 | -0.020124 | 0.0 |
| w24 | 24 | -0.062762 | 7.556 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=493. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=493. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 470 warm-up bars -- required_bars=493. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.0268 | 1.956 |
| w2 | 6 | -0.161799 | -7.982 |
| w3 | 15 | 0.022088 | 8.702 |
| w4 | 11 | -0.179236 | -12.455 |
| w5 | 18 | -0.00099 | 15.507 |
| w6 | 9 | -0.054336 | -8.804 |
| w7 | 15 | -0.069978 | -9.621 |
| w8 | 10 | 0.028241 | 0.488 |
| w9 | 24 | -0.112909 | -10.969 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | -0.077525 | -5.243 |
| w14 | 21 | 0.029997 | 10.058 |
| w15 | 4 | 0.075968 | 17.469 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.047198 | -4.929 |
| w18 | 7 | -0.066334 | -3.625 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | 0.014511 | -6.639 |
| w21 | 6 | 0.013864 | 0.878 |
| w22 | 2 | -0.180561 | -1.401 |
| w23 | 7 | -0.094888 | -5.144 |
| w24 | 0 | None | 0.0 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=493. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

