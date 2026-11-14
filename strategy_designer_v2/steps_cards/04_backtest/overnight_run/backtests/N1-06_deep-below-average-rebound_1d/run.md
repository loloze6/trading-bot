# Backtest of N1-06_deep-below-average-rebound_1d

- Plan: `../../../../03_test_plan/overnight_run/plans/N1-06_deep-below-average-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.275662 | 24.986 |
| w2 | 35 | 0.093363 | -44.617 |
| w3 | 7 | 0.145948 | 4.189 |
| w4 | 0 | 0.024149 | 0.0 |
| w5 | 0 | 0.128592 | 0.0 |
| w6 | 0 | 0.034392 | 0.0 |
| w7 | 2 | 0.172882 | 2.927 |
| w8 | 10 | -0.062414 | 4.008 |
| w9 | 0 | 0.13782 | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | 0.172965 | 0.0 |
| w13 | 0 | 0.118383 | 0.0 |
| w14 | 21 | 0.061424 | -30.078 |
| w15 | 0 | None | 0.0 |
| w16 | 16 | 0.18645 | 105.68 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | 0.155252 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | 0.294613 | 0.0 |
| w21 | 0 | 0.067505 | 0.0 |
| w22 | 0 | 0.259434 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 18 | 0.103801 | 3.607 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.234517 | 6.554 |
| w2 | 27 | 0.041395 | -45.755 |
| w3 | 4 | 0.132353 | -0.184 |
| w4 | 0 | 0.078461 | 0.0 |
| w5 | 0 | 0.090057 | 0.0 |
| w6 | 4 | 0.011709 | 6.802 |
| w7 | 8 | 0.030559 | -10.993 |
| w8 | 2 | -0.005995 | 0.874 |
| w9 | 6 | 0.050957 | 0.03 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | 0.088198 | 0.0 |
| w14 | 19 | 0.061 | -49.974 |
| w15 | 0 | -0.003772 | 0.0 |
| w16 | 14 | 0.258802 | 90.352 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | 0.104601 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.16077 | 3.227 |
| w21 | 6 | 0.093857 | 9.831 |
| w22 | 18 | 0.097588 | -14.891 |
| w23 | 2 | 0.141335 | 26.545 |
| w24 | 0 | 0.169404 | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | 0.146747 | -3.544 |
| w2 | 20 | 0.034234 | -47.211 |
| w3 | 0 | 0.040181 | 0.0 |
| w4 | 0 | 0.25146 | 0.0 |
| w5 | 6 | 0.007398 | -0.937 |
| w6 | 24 | 0.075105 | 22.404 |
| w7 | 8 | 0.078433 | -2.746 |
| w8 | 2 | 0.03179 | 8.682 |
| w9 | 3 | 0.082673 | 2.055 |
| w10 | 0 | 0.123639 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.108181 | 1.402 |
| w13 | 0 | 0.115534 | 0.0 |
| w14 | 13 | 0.166156 | -16.658 |
| w15 | 0 | -0.034602 | 0.0 |
| w16 | 9 | 0.312402 | 68.121 |
| w17 | 0 | 0.07269 | 0.0 |
| w18 | 0 | 0.113579 | 0.0 |
| w19 | 2 | 0.079556 | 1.777 |
| w20 | 28 | 0.18183 | 27.553 |
| w21 | 9 | 0.008594 | 12.751 |
| w22 | 2 | 0.111987 | 3.697 |
| w23 | 0 | 0.10861 | 0.0 |
| w24 | 18 | 0.102024 | 8.976 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | 0.102095 | 30.595 |
| w2 | 28 | 0.101731 | 30.359 |
| w3 | 11 | 0.295952 | 15.292 |
| w4 | 2 | 0.168063 | 1.598 |
| w5 | 22 | 0.15864 | 18.927 |
| w6 | 16 | 0.067581 | 9.059 |
| w7 | 8 | 0.130152 | 9.376 |
| w8 | 5 | 0.023437 | 10.337 |
| w9 | 8 | 0.149935 | -0.14 |
| w10 | 0 | 0.308387 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 13 | 0.079725 | 14.76 |
| w14 | 12 | 0.111359 | -17.583 |
| w15 | 0 | 0.010976 | 0.0 |
| w16 | 9 | 0.201804 | 97.892 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | 0.078295 | 0.0 |
| w19 | 34 | 0.176808 | 69.016 |
| w20 | 8 | 0.141507 | 14.373 |
| w21 | 2 | 0.171659 | 2.144 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | 0.178689 | 0.0 |
| w24 | 0 | 0.077057 | 0.0 |

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
| w1 | 37 | 0.147755 | 30.117 |
| w2 | 18 | -0.010019 | -66.943 |
| w3 | 3 | 0.128436 | 9.536 |
| w4 | 2 | 0.242461 | 2.532 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | 0.094329 | 0.0 |
| w8 | 7 | 0.330728 | 8.187 |
| w9 | 27 | 0.119869 | 2.596 |
| w10 | 2 | 0.076855 | 4.377 |
| w11 | 0 | 0.048861 | 0.0 |
| w12 | 2 | 0.138472 | 3.355 |
| w14 | 6 | 0.101391 | 29.793 |
| w15 | 7 | 0.031254 | 5.744 |
| w16 | 17 | 0.200593 | 110.473 |
| w17 | 0 | 0.003415 | 0.0 |
| w18 | 0 | 0.106973 | 0.0 |
| w19 | 11 | 0.124955 | 15.172 |
| w20 | 24 | 0.065261 | 20.547 |
| w21 | 0 | -0.006188 | 0.0 |
| w22 | 0 | 0.228857 | 0.0 |
| w23 | 0 | 0.11573 | 0.0 |
| w24 | 20 | 0.093999 | 3.718 |

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
| w1 | 28 | 0.122699 | 54.794 |
| w2 | 40 | 0.128435 | -40.142 |
| w3 | 11 | 0.182913 | 2.068 |
| w4 | 2 | 0.213925 | 2.777 |
| w5 | 21 | 0.186227 | 24.547 |
| w6 | 4 | 0.07858 | 6.256 |
| w7 | 13 | 0.133276 | 7.095 |
| w8 | 3 | -0.0223 | -0.82 |
| w9 | 17 | 0.177864 | -5.164 |
| w10 | 0 | 0.096762 | 0.0 |
| w11 | 0 | 0.022409 | 0.0 |
| w12 | 0 | 0.061418 | 0.0 |
| w13 | 4 | 0.096898 | 10.666 |
| w14 | 17 | 0.134644 | -24.414 |
| w15 | 2 | -0.04053 | -1.917 |
| w16 | 5 | 0.151287 | 22.62 |
| w17 | 0 | 0.198969 | 0.0 |
| w18 | 0 | 0.097197 | 0.0 |
| w19 | 31 | 0.191761 | 42.753 |
| w20 | 20 | 0.079912 | 34.852 |
| w21 | 0 | 0.026103 | 0.0 |
| w22 | 2 | 0.244752 | 4.953 |
| w23 | 0 | 0.233453 | 0.0 |
| w24 | 0 | None | 0.0 |

