# Backtest of 013-05_longer-stall-bigger-breakout_1d

- Plan: `../../../../03_test_plan/night_013_run/plans/013-05_longer-stall-bigger-breakout_1d.md`
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
| w5 | 4 | -0.167632 | -13.908 |
| w6 | 7 | 0.096666 | 22.753 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | -0.088262 | -7.345 |
| w11 | 10 | 0.047621 | 22.817 |
| w12 | 2 | -0.043586 | -1.31 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | 0.076813 | 18.811 |
| w16 | 0 | None | 0.0 |
| w17 | 12 | 0.095602 | 60.721 |
| w18 | 0 | None | 0.0 |
| w19 | 9 | 0.067755 | 21.46 |
| w20 | 0 | None | 0.0 |
| w21 | 8 | -0.02858 | 5.109 |
| w22 | 1 | -0.080441 | -2.52 |
| w23 | 6 | -0.063201 | -6.1 |
| w24 | 1 | -0.042878 | -3.189 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.016007 | 1.034 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | 0.096957 | 23.464 |
| w11 | 14 | 0.031941 | 49.848 |
| w12 | 4 | 0.001012 | -0.074 |
| w13 | 2 | 0.178856 | 25.828 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | 0.012625 | 8.398 |
| w18 | 3 | 0.031733 | 6.736 |
| w19 | 9 | 0.029437 | 11.434 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | 0.002627 | 4.524 |
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
| w11 | 6 | 0.101845 | 24.588 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | 0.011707 | 0.576 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | -0.020014 | -1.836 |
| w18 | 2 | -0.071595 | -6.025 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.064322 | 7.822 |
| w22 | 1 | -0.165165 | -5.859 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 1 | -0.26066 | -12.346 |
| w11 | 10 | -0.157739 | -12.32 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 11 | -0.21528 | -26.776 |
| w18 | 2 | -0.040476 | -4.565 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | -0.172479 | -2.476 |
| w21 | 2 | -0.462719 | -11.055 |
| w22 | 4 | -0.044372 | -0.685 |
| w23 | 5 | 0.182509 | 22.617 |
| w24 | 2 | 0.035414 | 2.694 |

- w7 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 483 prefetch bars (<date> to <date>) -- required_bars=531. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 364 prefetch bars (<date> to <date>) -- required_bars=531. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 21 of 24 windows run.

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
| w11 | 3 | 0.040224 | 7.125 |
| w12 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.002444 | -1.444 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | 0.495939 | 134.436 |
| w22 | 1 | 0.033791 | 2.199 |
| w23 | 2 | -0.019477 | -0.335 |
| w24 | 0 | None | 0.0 |

- w7 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 347 prefetch bars (<date> to <date>) -- required_bars=531. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 228 prefetch bars (<date> to <date>) -- required_bars=531. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 470 prefetch bars (<date> to <date>) -- required_bars=531. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

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
| w10 | 2 | 0.129277 | 13.324 |
| w11 | 6 | 0.056213 | 20.259 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | 0.053801 | 5.044 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.134071 | 14.844 |
| w21 | 4 | 0.109201 | 14.133 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | 0.0189 | 14.818 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 429 prefetch bars (<date> to <date>) -- required_bars=531. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

