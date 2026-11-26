# Backtest of 058-01.b2_quiet-volume-calm-fall-continues_1d

- Plan: `../../../../03_test_plan/night8_fallingcalm_run/plans/058-01.b2_quiet-volume-calm-fall-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.018202 | 13.937 |
| w2 | 4 | 0.196825 | 27.887 |
| w3 | 7 | -0.050629 | -1.512 |
| w4 | 1 | 0.008662 | -2.478 |
| w5 | 4 | -0.01484 | -2.689 |
| w6 | 3 | 0.100568 | 4.66 |
| w7 | 6 | -0.042459 | -0.359 |
| w8 | 1 | 0.072199 | 0.36 |
| w9 | 18 | -0.141427 | -13.663 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.034784 | -2.763 |
| w12 | 4 | 0.018003 | 3.997 |
| w13 | 0 | None | 0.0 |
| w14 | 5 | 0.073259 | 31.446 |
| w15 | 0 | None | 0.0 |
| w16 | 3 | -0.056499 | -9.79 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.083692 | -6.826 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.022724 | -2.012 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | 0.011164 | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.091365 | 18.673 |
| w2 | 2 | -0.088467 | 4.435 |
| w3 | 7 | -0.027953 | -4.653 |
| w4 | 1 | -0.054169 | -4.763 |
| w5 | 7 | -0.027775 | -3.992 |
| w6 | 8 | 0.057262 | -2.156 |
| w7 | 11 | 0.098279 | 23.841 |
| w8 | 0 | None | 0.0 |
| w9 | 12 | -0.047042 | -1.857 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.040214 | 2.189 |
| w13 | 7 | 0.189577 | 18.082 |
| w14 | 7 | 0.039674 | 7.151 |
| w15 | 5 | 0.092625 | 13.6 |
| w16 | 5 | -0.03093 | -23.282 |
| w17 | 4 | -0.055713 | -4.995 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.030826 | -1.594 |
| w22 | 0 | 0.026501 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.002142 | -0.082 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | -0.07565 | -3.534 |
| w2 | 3 | 0.080816 | 12.297 |
| w3 | 4 | 0.015177 | 0.729 |
| w4 | 4 | -0.112295 | -5.777 |
| w5 | 2 | -0.115725 | 0.73 |
| w6 | 11 | -0.014153 | 2.511 |
| w7 | 12 | -0.014005 | 33.596 |
| w8 | 0 | None | 0.0 |
| w9 | 15 | 0.002733 | 13.107 |
| w10 | 10 | -0.046278 | -1.646 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.008648 | 0.686 |
| w13 | 6 | -0.113347 | -7.232 |
| w14 | 14 | 0.084745 | 34.37 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | -0.054726 | -11.352 |
| w17 | 4 | -0.033639 | -2.571 |
| w18 | 9 | -0.022477 | -9.297 |
| w19 | 0 | None | 0.0 |
| w20 | 12 | -0.000299 | 7.114 |
| w21 | 4 | -0.036142 | -4.159 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.116672 | -3.201 |
| w24 | 7 | -0.035684 | -3.482 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.176574 | -9.065 |
| w2 | 0 | None | 0.0 |
| w3 | 10 | -0.013916 | 0.322 |
| w4 | 6 | -0.256467 | -11.676 |
| w5 | 6 | -0.108661 | -7.055 |
| w6 | 5 | -0.017525 | -5.633 |
| w8 | 3 | 0.084423 | 0.194 |
| w9 | 22 | -0.062184 | 10.551 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.009576 | -1.566 |
| w14 | 7 | 0.028014 | 21.274 |
| w15 | 6 | 0.044473 | 8.984 |
| w16 | 2 | -0.156606 | -21.541 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | -0.051712 | -3.43 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | -0.055313 | -3.537 |
| w22 | 4 | -0.151994 | -12.195 |
| w23 | 4 | 0.091475 | 13.94 |
| w24 | 0 | None | 0.0 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 483 warm-up bars -- required_bars=494. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=494. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 21 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.017005 | -1.305 |
| w2 | 2 | 0.078085 | 10.946 |
| w3 | 0 | 0.052646 | 0.0 |
| w4 | 0 | -0.003635 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | -0.005663 | -2.221 |
| w8 | 6 | -0.013442 | -0.081 |
| w9 | 10 | -0.055194 | -5.678 |
| w10 | 3 | -0.143415 | -23.301 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.023759 | -0.556 |
| w15 | 2 | 0.063943 | 2.894 |
| w16 | 3 | -0.131432 | -6.113 |
| w17 | 4 | -0.037631 | -11.082 |
| w18 | 5 | -0.020834 | -12.093 |
| w19 | 0 | -0.082526 | 0.0 |
| w20 | 7 | 0.10413 | 22.073 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.068155 | -0.419 |
| w23 | 2 | -0.020124 | -2.512 |
| w24 | 16 | 0.035324 | 27.502 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=494. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=494. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 470 warm-up bars -- required_bars=494. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.205019 | -6.93 |
| w2 | 5 | -0.135558 | -12.146 |
| w3 | 10 | 0.07955 | 35.383 |
| w4 | 3 | -0.095595 | -9.772 |
| w5 | 12 | 0.04757 | 17.287 |
| w6 | 6 | -0.067588 | -5.318 |
| w7 | 14 | -0.109109 | -17.483 |
| w8 | 13 | -0.028429 | -5.327 |
| w9 | 10 | -0.075731 | -5.553 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.082317 | -5.395 |
| w14 | 14 | -0.107692 | 10.123 |
| w15 | 8 | 0.058993 | 6.928 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.00707 | -7.557 |
| w18 | 4 | -0.07476 | -3.648 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.046977 | -1.857 |
| w21 | 5 | -0.095026 | -21.728 |
| w22 | 0 | -0.180561 | 0.0 |
| w23 | 6 | -0.01103 | -3.248 |
| w24 | 0 | None | 0.0 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=494. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

