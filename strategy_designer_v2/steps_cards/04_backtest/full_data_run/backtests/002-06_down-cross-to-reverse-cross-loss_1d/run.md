# Backtest of 002-06_down-cross-to-reverse-cross-loss_1d

- Plan: `../../../../03_test_plan/full_data_run/plans/002-06_down-cross-to-reverse-cross-loss_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.127464 | -5.64 |
| w2 | 15 | -0.149865 | 26.716 |
| w3 | 5 | -0.033565 | 7.543 |
| w4 | 6 | -0.150572 | -20.707 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.072409 | -10.446 |
| w7 | 2 | -0.161987 | 2.602 |
| w8 | 13 | 0.082729 | -26.558 |
| w9 | 2 | 0.018395 | 0.683 |
| w10 | 7 | -0.051026 | -3.74 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.017672 | 0.444 |
| w13 | 1 | -0.110574 | -0.864 |
| w14 | 9 | -0.112039 | 30.234 |
| w15 | 0 | None | 0.0 |
| w16 | 11 | -0.128512 | -21.156 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.177259 | -7.529 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | 0.000278 | 0.0 |
| w21 | 2 | 0.010509 | -3.349 |
| w22 | 1 | -0.122166 | -1.488 |
| w23 | 2 | -0.116945 | -1.849 |
| w24 | 8 | -0.04108 | 1.077 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.116551 | -2.511 |
| w2 | 14 | -0.189261 | 3.384 |
| w3 | 5 | -0.026037 | 1.597 |
| w4 | 3 | -0.15096 | -8.046 |
| w5 | 0 | None | 0.0 |
| w6 | 11 | -0.038462 | -20.705 |
| w7 | 6 | 0.001782 | 15.539 |
| w8 | 7 | 0.060759 | -2.492 |
| w9 | 5 | 0.07525 | 11.383 |
| w10 | 3 | 0.096409 | -3.832 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.10601 | -2.22 |
| w14 | 13 | -0.08338 | 35.054 |
| w15 | 0 | None | 0.0 |
| w16 | 9 | -0.116317 | -35.219 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | -0.140138 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.021911 | 0.102 |
| w21 | 11 | -0.084516 | -25.664 |
| w22 | 10 | -0.06797 | 1.316 |
| w23 | 11 | -0.039467 | -27.971 |
| w24 | 3 | -0.028233 | -0.278 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.098321 | 8.605 |
| w2 | 9 | -0.084886 | 27.339 |
| w3 | 5 | 0.022954 | -1.797 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | 0.017026 | 1.52 |
| w6 | 18 | -0.040509 | -27.805 |
| w7 | 6 | -0.060464 | 13.5 |
| w8 | 6 | 0.002437 | -16.813 |
| w9 | 5 | 0.027877 | 16.046 |
| w10 | 9 | -0.066367 | -19.525 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.112849 | -4.345 |
| w13 | 0 | 0.000382 | 0.0 |
| w14 | 6 | -0.088329 | 40.997 |
| w15 | 0 | None | 0.0 |
| w16 | 12 | -0.158415 | -29.753 |
| w17 | 0 | -0.047816 | 0.0 |
| w18 | 2 | -0.095193 | -3.379 |
| w19 | 2 | 0.048444 | -4.746 |
| w20 | 7 | -0.032572 | 3.262 |
| w21 | 10 | 0.046558 | -22.12 |
| w22 | 3 | -0.051069 | -1.888 |
| w23 | 4 | -0.05215 | -8.456 |
| w24 | 7 | 0.007989 | 3.663 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.051769 | -9.732 |
| w2 | 12 | -0.125874 | -10.982 |
| w3 | 6 | 0.004647 | 1.385 |
| w4 | 0 | -0.059311 | 0.0 |
| w5 | 14 | -0.242903 | -23.219 |
| w6 | 20 | -0.086255 | -28.527 |
| w7 | 6 | -0.142041 | -2.258 |
| w8 | 8 | -0.001018 | -17.064 |
| w9 | 8 | -0.054324 | 8.517 |
| w10 | 4 | 0.038023 | -1.812 |
| w11 | 0 | None | 0.0 |
| w12 | 8 | -0.159807 | -8.047 |
| w14 | 7 | -0.14699 | 30.514 |
| w15 | 0 | 0.012666 | 0.0 |
| w16 | 11 | -0.145448 | -31.692 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.095139 | -3.377 |
| w19 | 13 | -0.036619 | 4.48 |
| w20 | 11 | -0.124432 | -30.168 |
| w21 | 0 | -0.121697 | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | -0.003585 | 0.0 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 364 prefetch bars (<date> to <date>) -- required_bars=250. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.17012 | -12.855 |
| w2 | 13 | -0.100416 | 30.498 |
| w3 | 8 | -0.143689 | -24.196 |
| w4 | 1 | -0.198285 | -6.008 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.125173 | -8.403 |
| w8 | 6 | -0.082102 | 0.426 |
| w9 | 13 | -0.162535 | 4.277 |
| w10 | 12 | -0.074849 | -21.4 |
| w11 | 0 | -0.096671 | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 12 | -0.163773 | -23.169 |
| w15 | 7 | -0.125294 | -12.674 |
| w16 | 17 | -0.155304 | -37.618 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.207203 | -9.455 |
| w19 | 4 | -0.178017 | -9.172 |
| w20 | 31 | -0.060864 | -29.681 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | -0.215636 | 0.0 |
| w24 | 8 | 0.017369 | 10.256 |

- w7 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 347 prefetch bars (<date> to <date>) -- required_bars=250. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 228 prefetch bars (<date> to <date>) -- required_bars=250. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.240026 | -23.323 |
| w2 | 14 | -0.053745 | 7.411 |
| w3 | 6 | -0.033074 | 20.048 |
| w4 | 4 | -0.153547 | -2.861 |
| w5 | 10 | -0.123632 | 9.287 |
| w6 | 8 | -0.066913 | -18.017 |
| w7 | 4 | -0.16971 | 9.841 |
| w8 | 9 | 0.005918 | -14.965 |
| w9 | 12 | 0.014567 | 25.338 |
| w10 | 2 | 0.054839 | -4.884 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.082371 | -5.489 |
| w13 | 5 | -0.156173 | -14.773 |
| w14 | 5 | -0.205829 | 37.521 |
| w15 | 3 | 0.000655 | -2.966 |
| w16 | 9 | -0.213324 | -40.148 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | -0.099523 | -7.74 |
| w19 | 13 | -0.227647 | -24.2 |
| w20 | 19 | -0.037987 | -27.795 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.117959 | -1.877 |
| w23 | 4 | -0.13413 | -7.474 |
| w24 | 0 | None | 0.0 |

