# Backtest of 002-03_price-cross-above-long-sma.b1_cross-with-rising-average_1d

- Plan: `../../../03_test_plan/plans/002-03_price-cross-above-long-sma.b1_cross-with-rising-average_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 4 | -0.1088 | 1.504 |
| w5 | 8 | 0.023469 | -8.791 |
| w6 | 9 | -0.072245 | 12.691 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | -0.071991 | -16.062 |
| w10 | 9 | -0.019896 | 24.916 |
| w11 | 6 | 0.064743 | 85.025 |
| w12 | 5 | -0.155223 | -7.885 |
| w13 | 8 | -0.125976 | -15.587 |
| w14 | 0 | None | 0.0 |
| w15 | 10 | -0.136848 | 10.61 |
| w16 | 0 | None | 0.0 |
| w17 | 13 | 0.185724 | 285.896 |
| w18 | 4 | -0.231741 | -23.982 |
| w19 | 9 | -0.043189 | 48.496 |
| w20 | 8 | 0.027918 | 0.421 |
| w21 | 6 | -0.11117 | 0.176 |
| w22 | 13 | -0.146771 | -26.304 |
| w23 | 10 | -0.003559 | 3.168 |
| w24 | 9 | -0.028383 | -15.483 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.09626 | -2.784 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 8 | -0.135582 | -1.943 |
| w5 | 11 | 0.026927 | -6.483 |
| w6 | 5 | -0.032503 | 3.707 |
| w7 | 2 | 0.007551 | -1.608 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | -0.033352 | -0.746 |
| w10 | 10 | 0.078808 | 102.22 |
| w11 | 5 | -0.054139 | 132.681 |
| w12 | 3 | -0.009787 | -1.827 |
| w13 | 7 | -0.102876 | -4.569 |
| w14 | 0 | None | 0.0 |
| w15 | 10 | -0.170855 | -14.152 |
| w16 | 3 | -0.25049 | -17.876 |
| w17 | 10 | -0.157387 | 30.194 |
| w18 | 8 | -0.096522 | -3.701 |
| w19 | 10 | -0.080747 | 23.244 |
| w20 | 7 | 0.0712 | 3.719 |
| w21 | 3 | -0.067505 | -1.462 |
| w22 | 0 | -0.056837 | 0.0 |
| w23 | 8 | -0.05196 | 7.722 |
| w24 | 4 | -0.062714 | -30.623 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | -0.083469 | 0.0 |
| w4 | 8 | -0.245029 | -5.702 |
| w5 | 9 | -0.093737 | -13.178 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | 0.004716 | -0.458 |
| w8 | 3 | -0.133725 | -2.357 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | 0.075273 | 0.0 |
| w11 | 3 | -0.048632 | 62.998 |
| w12 | 0 | -0.071041 | 0.0 |
| w13 | 12 | -0.0763 | -9.29 |
| w14 | 0 | None | 0.0 |
| w15 | 12 | -0.039742 | -9.964 |
| w16 | 0 | None | 0.0 |
| w17 | 10 | 0.132699 | 85.917 |
| w18 | 5 | -0.108259 | -24.391 |
| w19 | 10 | -0.075453 | -6.793 |
| w20 | 2 | 0.02776 | -1.106 |
| w21 | 7 | -0.098357 | -8.115 |
| w22 | 1 | -0.009057 | -11.447 |
| w23 | 3 | -0.076606 | -1.902 |
| w24 | 7 | -0.130179 | -13.568 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 13 | -0.091127 | -11.137 |
| w5 | 13 | -0.025517 | -6.427 |
| w6 | 9 | -0.109967 | -5.745 |
| w7 | 1 | 0.015332 | -0.03 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | -0.119668 | -3.321 |
| w10 | 13 | 0.038197 | 38.897 |
| w11 | 9 | -0.156717 | 103.419 |
| w12 | 1 | -0.130885 | -4.234 |
| w14 | 0 | None | 0.0 |
| w15 | 8 | -0.13674 | -12.528 |
| w16 | 0 | -0.060489 | 0.0 |
| w17 | 10 | 0.015991 | 55.662 |
| w18 | 8 | -0.200452 | -36.41 |
| w19 | 2 | -0.15026 | -27.033 |
| w20 | 4 | 0.015896 | 2.964 |
| w21 | 23 | -0.157704 | -30.193 |
| w22 | 16 | -0.093296 | 23.39 |
| w23 | 14 | 0.024189 | -1.88 |
| w24 | 9 | -0.06681 | 15.163 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 364 prefetch bars (<date> to <date>) -- required_bars=275. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 10 | -0.105704 | -4.569 |
| w5 | 13 | -0.008643 | 57.03 |
| w6 | 12 | -0.174258 | -7.348 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 5 | -0.056708 | -2.436 |
| w11 | 15 | -0.058339 | 76.534 |
| w12 | 6 | -0.084692 | -9.892 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.153066 | -8.454 |
| w16 | 0 | None | 0.0 |
| w17 | 13 | -0.040732 | 41.473 |
| w18 | 10 | -0.105575 | -13.815 |
| w19 | 7 | -0.134701 | -13.469 |
| w20 | 3 | -0.06441 | -1.586 |
| w21 | 8 | 0.09517 | 91.555 |
| w22 | 8 | -0.012991 | -0.753 |
| w23 | 3 | -0.048648 | -0.16 |
| w24 | 4 | -0.087587 | -6.18 |

- w7 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 347 prefetch bars (<date> to <date>) -- required_bars=275. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 228 prefetch bars (<date> to <date>) -- required_bars=275. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.156555 | -21.089 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | -0.211954 | -1.245 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 11 | 0.004293 | 38.677 |
| w11 | 13 | -0.174223 | 72.471 |
| w12 | 2 | -0.122876 | -2.87 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | -0.194464 | -11.827 |
| w16 | 1 | -0.025228 | -0.008 |
| w17 | 18 | -0.169971 | -23.426 |
| w18 | 10 | -0.143197 | -42.341 |
| w19 | 7 | -0.141458 | -10.432 |
| w20 | 7 | -0.055204 | -0.59 |
| w21 | 18 | -0.015271 | 42.752 |
| w22 | 4 | -0.09485 | -17.518 |
| w23 | 3 | -0.078913 | -2.01 |
| w24 | 13 | 0.060025 | 308.066 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 429 prefetch bars (<date> to <date>) -- required_bars=275. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

