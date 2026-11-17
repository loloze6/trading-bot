# Backtest of 013-06_breakout-volume-drives-continuation_1d

- Plan: `../../../../03_test_plan/volume_run/plans/013-06_breakout-volume-drives-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 4 | -0.161974 | -10.322 |
| w6 | 12 | 0.062869 | 15.138 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | -0.151952 | -10.757 |
| w11 | 16 | 0.05609 | 13.415 |
| w12 | 2 | -0.059305 | -3.562 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 11 | -0.026605 | 0.237 |
| w16 | 0 | None | 0.0 |
| w17 | 23 | 0.082498 | 42.962 |
| w18 | 0 | None | 0.0 |
| w19 | 18 | -0.015536 | 1.465 |
| w20 | 0 | None | 0.0 |
| w21 | 16 | 0.027267 | 13.548 |
| w22 | 1 | -0.080441 | -1.843 |
| w23 | 10 | -0.084914 | -6.903 |
| w24 | 2 | -0.066137 | -4.098 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | -0.009662 | 0.478 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 5 | 0.100167 | 23.953 |
| w11 | 19 | 0.123345 | 47.522 |
| w12 | 7 | -0.003877 | -0.447 |
| w13 | 5 | 0.180326 | 18.747 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 11 | 0.026052 | 9.291 |
| w18 | 7 | -0.010374 | 1.257 |
| w19 | 16 | 0.021851 | 5.592 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 4 | 0.004406 | 4.647 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | -0.09825 | -5.589 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 12 | 0.075145 | 11.931 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 6 | 0.001417 | -0.3 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | -0.014699 | -1.395 |
| w18 | 2 | -0.045577 | -3.125 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | 0.076581 | 8.337 |
| w22 | 1 | -0.165165 | -3.418 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 1 | -0.26066 | -12.346 |
| w11 | 13 | -0.192577 | -18.329 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 17 | -0.178439 | -17.757 |
| w18 | 3 | 0.018419 | 1.109 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | -0.172479 | -3.932 |
| w21 | 2 | -0.373582 | -21.459 |
| w22 | 6 | 0.059629 | 6.191 |
| w23 | 10 | 0.10979 | 14.468 |
| w24 | 3 | 0.002564 | 0.791 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 364 prefetch bars (<date> to <date>) -- required_bars=366. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | -0.139679 | -6.262 |
| w6 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | 0.009016 | 4.102 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.002444 | -1.444 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 5 | 0.464362 | 115.196 |
| w22 | 2 | 0.04377 | 1.355 |
| w23 | 2 | -0.042974 | -2.738 |
| w24 | 0 | None | 0.0 |

- w7 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 347 prefetch bars (<date> to <date>) -- required_bars=366. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 228 prefetch bars (<date> to <date>) -- required_bars=366. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | 0.040337 | 5.247 |
| w11 | 13 | -0.008191 | 7.584 |
| w12 | 0 | None | 0.0 |
| w13 | 1 | -0.10006 | -2.919 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | 0.064242 | 4.289 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | 0.184489 | 13.49 |
| w21 | 6 | 0.107021 | 17.568 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 14 | 0.072566 | 25.07 |

