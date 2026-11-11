# Backtest of 002-02_sma-death-cross-downward-drift_1d

- Plan: `../../../../03_test_plan/full_data_run/plans/002-02_sma-death-cross-downward-drift_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.127464 | -11.709 |
| w2 | 34 | -0.149865 | 35.112 |
| w3 | 8 | -0.033565 | 5.712 |
| w4 | 4 | -0.150572 | -19.529 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.072409 | -8.428 |
| w7 | 6 | -0.161987 | -6.564 |
| w8 | 16 | 0.082729 | -35.026 |
| w9 | 3 | 0.018395 | 3.407 |
| w10 | 7 | -0.051026 | -13.378 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.017672 | 0.292 |
| w13 | 1 | -0.110574 | -2.157 |
| w14 | 16 | -0.112039 | 15.687 |
| w15 | 0 | None | 0.0 |
| w16 | 15 | -0.128512 | -49.162 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.177259 | -16.779 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | 0.000278 | 0.0 |
| w21 | 2 | 0.010509 | -6.985 |
| w22 | 1 | -0.122166 | -2.437 |
| w23 | 2 | -0.116945 | -2.966 |
| w24 | 7 | -0.04108 | 0.382 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.116551 | -4.568 |
| w2 | 41 | -0.189261 | -42.184 |
| w3 | 5 | -0.026037 | 9.305 |
| w4 | 4 | -0.15096 | -16.999 |
| w5 | 0 | None | 0.0 |
| w6 | 9 | -0.038462 | -18.197 |
| w7 | 8 | 0.001782 | 46.824 |
| w8 | 12 | 0.060759 | -14.419 |
| w9 | 5 | 0.07525 | 18.425 |
| w10 | 3 | 0.096409 | -3.396 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 1 | -0.10601 | -5.557 |
| w14 | 43 | -0.08338 | 33.307 |
| w15 | 0 | None | 0.0 |
| w16 | 11 | -0.116317 | -54.587 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | -0.140138 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.021911 | 0.131 |
| w21 | 11 | -0.084516 | -36.551 |
| w22 | 17 | -0.06797 | -8.433 |
| w23 | 14 | -0.039467 | -60.779 |
| w24 | 3 | -0.028233 | 0.538 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.098321 | -4.124 |
| w2 | 37 | -0.084886 | 22.758 |
| w3 | 6 | 0.022954 | -10.813 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | 0.017026 | 1.849 |
| w6 | 20 | -0.040509 | -33.17 |
| w7 | 12 | -0.060464 | 31.796 |
| w8 | 12 | 0.002437 | -45.446 |
| w9 | 8 | 0.027877 | 27.09 |
| w10 | 8 | -0.066367 | -22.696 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.112849 | -5.398 |
| w13 | 0 | 0.000382 | 0.0 |
| w14 | 24 | -0.088329 | 51.906 |
| w15 | 0 | None | 0.0 |
| w16 | 12 | -0.158415 | -54.759 |
| w17 | 0 | -0.047816 | 0.0 |
| w18 | 2 | -0.095193 | -11.447 |
| w19 | 2 | 0.048444 | -1.502 |
| w20 | 13 | -0.032572 | -4.898 |
| w21 | 9 | 0.046558 | -30.465 |
| w22 | 3 | -0.051069 | -4.665 |
| w23 | 5 | -0.05215 | -16.733 |
| w24 | 7 | 0.007989 | 6.83 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 54 | -0.051769 | -57.817 |
| w2 | 16 | -0.125874 | -36.449 |
| w3 | 5 | 0.004647 | 1.893 |
| w4 | 0 | -0.059311 | 0.0 |
| w5 | 11 | -0.242903 | -18.324 |
| w6 | 17 | -0.086255 | -23.538 |
| w7 | 15 | -0.142041 | -9.913 |
| w8 | 15 | -0.001018 | -35.738 |
| w9 | 10 | -0.054324 | 11.027 |
| w10 | 4 | 0.038023 | -4.968 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.159807 | -13.081 |
| w14 | 21 | -0.14699 | 38.924 |
| w15 | 0 | 0.012666 | 0.0 |
| w16 | 14 | -0.145448 | -54.528 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | -0.095139 | -9.055 |
| w19 | 25 | -0.036619 | -11.812 |
| w20 | 15 | -0.124432 | -44.242 |
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
| w1 | 40 | -0.17012 | -45.246 |
| w2 | 34 | -0.100416 | 39.449 |
| w3 | 9 | -0.143689 | -35.424 |
| w4 | 2 | -0.198285 | -8.555 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.125173 | -5.284 |
| w8 | 5 | -0.082102 | 4.682 |
| w9 | 18 | -0.162535 | 0.989 |
| w10 | 11 | -0.074849 | -23.744 |
| w11 | 0 | -0.096671 | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 16 | -0.163773 | -73.604 |
| w15 | 10 | -0.125294 | -24.058 |
| w16 | 23 | -0.155304 | -60.957 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | -0.207203 | -22.307 |
| w19 | 4 | -0.178017 | -10.93 |
| w20 | 28 | -0.060864 | -41.592 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | -0.215636 | 0.0 |
| w24 | 9 | 0.017369 | 20.596 |

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
| w1 | 17 | -0.240026 | -60.644 |
| w2 | 46 | -0.053745 | 1.554 |
| w3 | 19 | -0.033074 | 24.106 |
| w4 | 5 | -0.153547 | -13.663 |
| w5 | 12 | -0.123632 | 6.673 |
| w6 | 7 | -0.066913 | -19.799 |
| w7 | 23 | -0.16971 | -4.949 |
| w8 | 10 | 0.005918 | -9.794 |
| w9 | 25 | 0.014567 | 51.792 |
| w10 | 2 | 0.054839 | -1.983 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.082371 | -11.641 |
| w13 | 7 | -0.156173 | -38.738 |
| w14 | 26 | -0.205829 | 63.512 |
| w15 | 3 | 0.000655 | -0.232 |
| w16 | 14 | -0.213324 | -68.843 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | -0.099523 | -18.835 |
| w19 | 17 | -0.227647 | -49.826 |
| w20 | 20 | -0.037987 | -48.972 |
| w21 | 0 | None | 0.0 |
| w22 | 7 | -0.117959 | -16.359 |
| w23 | 5 | -0.13413 | -20.245 |
| w24 | 0 | None | 0.0 |

