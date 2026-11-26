# Backtest of 058-02.b2_calm-range-position-continues_1d

- Plan: `../../../../03_test_plan/night8_choppycalm_run/plans/058-02.b2_calm-range-position-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.059759 | -16.758 |
| w2 | 15 | -0.003971 | 9.146 |
| w3 | 16 | -0.020236 | -20.461 |
| w4 | 8 | 0.092554 | 24.676 |
| w5 | 36 | 0.021468 | 20.362 |
| w6 | 17 | -0.114538 | -1.505 |
| w7 | 36 | 0.054458 | 5.705 |
| w8 | 22 | -0.088267 | -12.425 |
| w9 | 12 | -0.07182 | -0.077 |
| w10 | 19 | 0.195726 | 17.882 |
| w11 | 5 | 0.005274 | -2.866 |
| w12 | 2 | 0.185636 | 4.336 |
| w13 | 8 | -0.009038 | -8.62 |
| w14 | 22 | 0.035739 | 12.796 |
| w15 | 0 | None | 0.0 |
| w16 | 8 | 0.012464 | 38.166 |
| w17 | 16 | 0.060667 | 22.745 |
| w18 | 5 | 0.100148 | 23.992 |
| w19 | 0 | None | 0.0 |
| w20 | 22 | 0.1274 | 17.067 |
| w21 | 17 | -0.099616 | -8.347 |
| w22 | 25 | -0.01175 | 1.916 |
| w23 | 28 | 0.127263 | 10.912 |
| w24 | 30 | -0.047628 | -7.407 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.053963 | 2.342 |
| w2 | 5 | 0.159378 | 25.053 |
| w3 | 14 | -0.051494 | -19.883 |
| w4 | 18 | 0.091788 | 13.963 |
| w5 | 51 | -0.052927 | 0.366 |
| w6 | 13 | 0.016191 | 0.268 |
| w7 | 9 | -0.069951 | -2.039 |
| w8 | 13 | 0.132904 | -1.423 |
| w9 | 16 | 0.005705 | 1.498 |
| w10 | 6 | -0.126981 | -4.629 |
| w11 | 0 | None | 0.0 |
| w12 | 7 | 0.023595 | 0.984 |
| w13 | 1 | 0.057662 | 5.107 |
| w14 | 5 | 0.070424 | -4.879 |
| w15 | 1 | -0.057183 | -1.334 |
| w16 | 5 | -0.010855 | 4.58 |
| w17 | 12 | -0.028126 | 7.867 |
| w18 | 9 | 0.079785 | 19.184 |
| w19 | 0 | None | 0.0 |
| w20 | 13 | 0.125963 | 8.141 |
| w21 | 23 | -0.137168 | -37.326 |
| w22 | 1 | 0.00539 | -3.833 |
| w23 | 2 | 0.102045 | 28.512 |
| w24 | 5 | -0.207489 | -10.63 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.036808 | -9.17 |
| w2 | 22 | -0.066367 | 12.507 |
| w3 | 23 | 0.063562 | 4.835 |
| w4 | 17 | 0.044239 | -7.047 |
| w5 | 28 | 0.133003 | 16.246 |
| w6 | 37 | -0.10815 | -31.656 |
| w7 | 15 | -0.078231 | -4.33 |
| w8 | 3 | 0.038039 | -1.219 |
| w9 | 7 | -0.020075 | -6.967 |
| w10 | 32 | -0.075241 | -22.85 |
| w11 | 0 | None | 0.0 |
| w12 | 13 | 0.062075 | 10.256 |
| w13 | 4 | 0.020258 | 1.936 |
| w14 | 14 | 0.005447 | 8.74 |
| w15 | 2 | 0.214259 | -3.948 |
| w16 | 2 | -0.020698 | -1.012 |
| w17 | 7 | -0.065726 | -3.34 |
| w18 | 6 | 0.028069 | 20.671 |
| w19 | 15 | 0.031901 | 24.034 |
| w20 | 13 | 0.041322 | -8.079 |
| w21 | 29 | -0.046343 | -21.71 |
| w22 | 0 | None | 0.0 |
| w23 | 24 | 0.114389 | 23.591 |
| w24 | 19 | -0.145641 | -38.713 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.099997 | -19.514 |
| w2 | 5 | 0.003478 | -0.994 |
| w3 | 35 | -0.081448 | -10.212 |
| w4 | 41 | -0.102981 | -12.965 |
| w5 | 50 | 0.044541 | 12.26 |
| w6 | 30 | -0.00714 | -1.7 |
| w7 | 19 | 0.097347 | 9.578 |
| w8 | 20 | -0.127616 | -13.366 |
| w9 | 15 | 0.00994 | -5.51 |
| w10 | 21 | -0.075315 | -9.337 |
| w11 | 0 | None | 0.0 |
| w12 | 27 | -0.127404 | -6.059 |
| w14 | 23 | -0.097929 | -21.179 |
| w15 | 0 | None | 0.0 |
| w16 | 7 | -0.015963 | -2.019 |
| w17 | 2 | 0.133098 | 7.063 |
| w18 | 13 | 0.037221 | 9.921 |
| w19 | 3 | 0.136541 | 12.445 |
| w20 | 10 | 0.053062 | 5.254 |
| w21 | 38 | 0.029961 | -3.112 |
| w22 | 17 | 0.119245 | 32.37 |
| w23 | 17 | 0.08881 | 29.548 |
| w24 | 9 | -0.036681 | -8.389 |

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
| w1 | 26 | -0.043723 | 3.662 |
| w2 | 0 | -0.046431 | 0.0 |
| w3 | 0 | -0.044065 | 0.0 |
| w4 | 0 | -0.045157 | 0.0 |
| w5 | 16 | -0.015174 | -8.499 |
| w6 | 13 | -0.003013 | -3.77 |
| w8 | 34 | -0.014267 | -14.049 |
| w9 | 16 | -0.008463 | -10.014 |
| w10 | 28 | 0.020539 | 26.972 |
| w11 | 0 | None | 0.0 |
| w12 | 26 | -0.112775 | -11.037 |
| w14 | 1 | 0.123197 | 4.988 |
| w15 | 11 | 0.091947 | -9.444 |
| w16 | 2 | -0.008015 | -0.667 |
| w17 | 14 | 0.001463 | 18.446 |
| w18 | 2 | 0.1572 | 33.477 |
| w19 | 13 | 0.002659 | -3.212 |
| w20 | 11 | -0.022782 | -4.416 |
| w21 | 15 | -0.051823 | 3.015 |
| w22 | 1 | -0.021052 | -1.692 |
| w23 | 32 | 0.059336 | 11.933 |
| w24 | 15 | -0.05412 | -13.603 |

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
| w1 | 8 | 0.041373 | 2.779 |
| w2 | 10 | -0.059105 | -12.122 |
| w3 | 16 | -0.139642 | -21.907 |
| w4 | 20 | -0.129105 | 6.982 |
| w5 | 24 | 0.058549 | 14.038 |
| w6 | 24 | -0.103196 | -29.341 |
| w7 | 5 | -0.065279 | -11.563 |
| w8 | 19 | -0.13853 | -10.186 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | 0.017134 | -0.77 |
| w11 | 0 | None | 0.0 |
| w12 | 15 | 0.033711 | 13.226 |
| w13 | 0 | None | 0.0 |
| w14 | 10 | 0.105208 | 17.693 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 10 | -0.053897 | -1.808 |
| w18 | 6 | 0.039045 | 16.257 |
| w19 | 0 | None | 0.0 |
| w20 | 10 | -0.135386 | -5.521 |
| w21 | 9 | -0.043727 | 0.617 |
| w22 | 2 | 0.042239 | -3.149 |
| w23 | 22 | -0.0944 | -3.866 |
| w24 | 2 | 0.001154 | 3.964 |

