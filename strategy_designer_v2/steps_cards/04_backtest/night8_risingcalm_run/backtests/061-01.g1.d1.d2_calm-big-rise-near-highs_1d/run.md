# Backtest of 061-01.g1.d1.d2_calm-big-rise-near-highs_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1.d2_calm-big-rise-near-highs_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.04829 | -26.119 |
| w2 | 7 | -0.122083 | -27.171 |
| w3 | 10 | 0.049318 | -42.029 |
| w4 | 3 | 0.140884 | 39.706 |
| w5 | 23 | 0.019133 | -6.095 |
| w6 | 10 | -0.023714 | 32.303 |
| w7 | 17 | 0.084542 | 2.735 |
| w8 | 16 | -0.053267 | 2.384 |
| w9 | 9 | -0.093905 | -13.935 |
| w10 | 9 | 0.252679 | 27.778 |
| w11 | 1 | -0.108515 | -2.554 |
| w12 | 2 | 0.003457 | -0.63 |
| w13 | 8 | -0.030495 | 3.435 |
| w14 | 15 | 0.033596 | -9.753 |
| w15 | 0 | None | 0.0 |
| w16 | 5 | -0.051112 | 8.921 |
| w17 | 8 | 0.069786 | 32.597 |
| w18 | 2 | 0.162607 | 16.227 |
| w19 | 0 | None | 0.0 |
| w20 | 11 | 0.038768 | -0.704 |
| w21 | 9 | -0.076461 | 9.079 |
| w22 | 19 | -0.012461 | -13.735 |
| w23 | 11 | 0.14408 | 14.848 |
| w24 | 22 | 0.054129 | -4.955 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.013598 | -2.248 |
| w2 | 4 | -0.113679 | -6.505 |
| w3 | 10 | 0.051877 | -37.22 |
| w4 | 5 | 0.023263 | 27.215 |
| w5 | 22 | -0.110348 | -7.671 |
| w6 | 14 | 0.014694 | 5.264 |
| w7 | 6 | -0.040581 | -8.182 |
| w8 | 5 | 0.069098 | -1.302 |
| w9 | 11 | 0.008113 | 2.222 |
| w10 | 5 | -0.037229 | 7.882 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.045146 | -1.596 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | -0.004185 | -0.184 |
| w15 | 0 | None | 0.0 |
| w16 | 3 | -0.017383 | 2.892 |
| w17 | 11 | 0.01469 | 9.808 |
| w18 | 6 | 0.054124 | 21.724 |
| w19 | 0 | None | 0.0 |
| w20 | 8 | -0.016905 | 4.292 |
| w21 | 13 | -0.027687 | -0.887 |
| w22 | 2 | 0.013053 | 1.073 |
| w23 | 1 | 0.127603 | 11.054 |
| w24 | 3 | 0.000121 | 3.959 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.055425 | -12.798 |
| w2 | 11 | -0.039462 | -17.973 |
| w3 | 12 | 0.023859 | 30.654 |
| w4 | 8 | -0.113942 | -3.02 |
| w5 | 15 | 0.04312 | -10.925 |
| w6 | 25 | 0.138874 | 30.453 |
| w7 | 5 | -0.054676 | -11.16 |
| w8 | 3 | 0.057978 | 0.45 |
| w9 | 5 | -0.024502 | -6.426 |
| w10 | 19 | -0.105632 | 12.717 |
| w11 | 0 | None | 0.0 |
| w12 | 9 | 0.039687 | 10.939 |
| w13 | 2 | -0.163349 | -5.871 |
| w14 | 5 | -0.039296 | -8.878 |
| w15 | 0 | -0.214259 | 0.0 |
| w16 | 1 | -0.044289 | -4.03 |
| w17 | 6 | -0.009554 | -6.685 |
| w18 | 4 | -0.013132 | 10.859 |
| w19 | 12 | 0.07746 | 23.892 |
| w20 | 11 | -0.057228 | -20.664 |
| w21 | 15 | -0.024334 | 8.581 |
| w22 | 0 | None | 0.0 |
| w23 | 14 | 0.078906 | 27.586 |
| w24 | 10 | -0.217566 | -24.189 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.084716 | -19.613 |
| w2 | 4 | -0.040896 | -2.789 |
| w3 | 21 | 0.009835 | -12.649 |
| w4 | 27 | -0.202617 | -3.153 |
| w5 | 32 | 0.1421 | -5.436 |
| w6 | 19 | 0.018733 | -5.552 |
| w7 | 11 | -0.052866 | -8.03 |
| w8 | 13 | -0.056056 | 1.936 |
| w9 | 7 | -0.186073 | -19.218 |
| w10 | 11 | -0.102021 | 6.79 |
| w11 | 0 | None | 0.0 |
| w12 | 18 | 0.010589 | -18.992 |
| w14 | 9 | -0.057524 | -28.573 |
| w15 | 0 | None | 0.0 |
| w16 | 5 | -0.09065 | 4.173 |
| w17 | 0 | 0.133098 | 0.0 |
| w18 | 9 | 0.044115 | 9.218 |
| w19 | 2 | -0.017154 | -13.275 |
| w20 | 8 | 0.028839 | -1.162 |
| w21 | 21 | -0.016873 | 10.554 |
| w22 | 12 | 0.064494 | 30.654 |
| w23 | 6 | -0.034531 | -12.571 |
| w24 | 5 | 0.044184 | 0.653 |

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
| w1 | 14 | -0.000514 | -0.378 |
| w2 | 0 | -0.035668 | 0.0 |
| w3 | 0 | 0.017207 | 0.0 |
| w4 | 0 | -0.043714 | 0.0 |
| w5 | 5 | -0.047981 | -3.938 |
| w6 | 7 | 0.060183 | 31.695 |
| w8 | 15 | 0.019978 | -1.291 |
| w9 | 7 | -0.090732 | -19.433 |
| w10 | 17 | -0.053386 | -0.462 |
| w11 | 0 | None | 0.0 |
| w12 | 10 | -0.130076 | -10.798 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.313499 | 21.074 |
| w16 | 1 | -0.018224 | -0.897 |
| w17 | 12 | -0.008759 | 27.121 |
| w18 | 2 | 0.110223 | 38.62 |
| w19 | 9 | 0.041757 | -13.366 |
| w20 | 6 | -0.137239 | -17.381 |
| w21 | 10 | -0.031896 | 65.877 |
| w22 | 1 | -0.006203 | -1.298 |
| w23 | 22 | 0.101345 | 40.555 |
| w24 | 12 | -0.00099 | -13.382 |

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
| w1 | 1 | -0.027057 | -0.682 |
| w2 | 5 | -0.000906 | -4.06 |
| w3 | 12 | -0.074865 | -7.696 |
| w4 | 15 | -0.172633 | -2.711 |
| w5 | 18 | -0.051453 | -12.13 |
| w6 | 16 | -0.011808 | -9.772 |
| w7 | 5 | 0.141597 | 3.464 |
| w8 | 18 | -0.113952 | 5.961 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.109888 | -0.927 |
| w11 | 0 | None | 0.0 |
| w12 | 10 | 0.074791 | 12.121 |
| w13 | 0 | None | 0.0 |
| w14 | 7 | 0.067744 | 2.495 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | 0.04914 | 13.032 |
| w18 | 2 | -0.015822 | 8.813 |
| w19 | 0 | None | 0.0 |
| w20 | 8 | -0.130864 | -18.618 |
| w21 | 6 | -0.020453 | 4.746 |
| w22 | 0 | None | 0.0 |
| w23 | 12 | 0.067911 | 3.2 |
| w24 | 2 | 0.019073 | 2.516 |

