# Backtest of 013-06_breakout-volume-drives-continuation_1d

- Plan: `../../../../03_test_plan/night_013_run/plans/013-06_breakout-volume-drives-continuation_1d.md`
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
| w5 | 4 | -0.161856 | -10.302 |
| w6 | 12 | 0.063043 | 15.194 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | -0.15217 | -10.769 |
| w11 | 16 | 0.056648 | 13.479 |
| w12 | 2 | -0.059875 | -3.564 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 11 | -0.026768 | 0.213 |
| w16 | 0 | None | 0.0 |
| w17 | 23 | 0.08263 | 43.06 |
| w18 | 0 | None | 0.0 |
| w19 | 18 | -0.016048 | 1.327 |
| w20 | 0 | None | 0.0 |
| w21 | 16 | 0.027053 | 13.527 |
| w22 | 1 | -0.080441 | -1.834 |
| w23 | 10 | -0.084305 | -6.855 |
| w24 | 2 | -0.066516 | -4.09 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | -0.009158 | 0.506 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 5 | 0.100952 | 23.974 |
| w11 | 19 | 0.125362 | 48.134 |
| w12 | 7 | -0.003913 | -0.451 |
| w13 | 5 | 0.179986 | 18.836 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 11 | 0.026663 | 9.393 |
| w18 | 7 | -0.010507 | 1.257 |
| w19 | 16 | 0.021731 | 5.519 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 4 | 0.004629 | 4.634 |
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
| w11 | 12 | 0.075543 | 11.943 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | 0.014186 | 0.452 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | -0.013636 | -1.348 |
| w18 | 2 | -0.045331 | -3.105 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | 0.076686 | 8.342 |
| w22 | 1 | -0.165165 | -3.386 |
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
| w11 | 13 | -0.19368 | -18.403 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 17 | -0.178597 | -17.772 |
| w18 | 3 | 0.01877 | 1.129 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | -0.172479 | -3.895 |
| w21 | 2 | -0.372398 | -21.342 |
| w22 | 6 | 0.060506 | 6.237 |
| w23 | 10 | 0.108683 | 14.255 |
| w24 | 3 | 0.002178 | 0.776 |

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
| w11 | 4 | 0.008384 | 4.027 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.002444 | -1.444 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 5 | 0.463405 | 114.87 |
| w22 | 2 | 0.043846 | 1.32 |
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
| w10 | 3 | 0.041073 | 5.312 |
| w11 | 13 | -0.009397 | 7.368 |
| w12 | 0 | None | 0.0 |
| w13 | 1 | -0.10006 | -2.927 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | 0.064365 | 4.309 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | 0.184351 | 13.48 |
| w21 | 6 | 0.10707 | 17.57 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 13 | 0.073732 | 24.221 |

