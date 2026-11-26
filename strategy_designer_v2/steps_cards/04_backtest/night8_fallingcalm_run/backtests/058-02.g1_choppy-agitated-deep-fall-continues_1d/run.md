# Backtest of 058-02.g1_choppy-agitated-deep-fall-continues_1d

- Plan: `../../../../03_test_plan/night8_fallingcalm_run/plans/058-02.g1_choppy-agitated-deep-fall-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.061827 | -3.159 |
| w2 | 0 | None | 0.0 |
| w3 | 5 | 0.101956 | 4.095 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | -0.051231 | -0.106 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.08783 | -2.724 |
| w13 | 3 | 0.089469 | 2.501 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | 0.003199 | -3.112 |
| w16 | 3 | 0.337286 | 22.501 |
| w17 | 9 | -0.005959 | -3.5 |
| w18 | 3 | -0.018472 | 0.534 |
| w19 | 10 | -0.025183 | -7.518 |
| w20 | 15 | -0.039561 | -6.847 |
| w21 | 6 | -0.162047 | -3.47 |
| w22 | 2 | 0.22522 | 11.242 |
| w23 | 0 | None | 0.0 |
| w24 | 13 | -0.013348 | 2.872 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 12 | 0.039663 | -0.042 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | 0.030308 | 1.936 |
| w9 | 3 | 0.052998 | -1.79 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.056385 | -1.38 |
| w13 | 0 | 0.024651 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 6 | -0.027025 | 0.695 |
| w16 | 1 | 0.135025 | 5.962 |
| w17 | 6 | -0.044752 | -2.235 |
| w18 | 5 | 0.040602 | 1.769 |
| w19 | 10 | -0.025234 | -1.067 |
| w20 | 4 | -0.08816 | -5.216 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | -0.159179 | 0.209 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.086419 | -0.243 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 6 | 0.03088 | 1.948 |
| w4 | 12 | -0.132937 | -7.186 |
| w5 | 7 | -0.39961 | -22.419 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 5 | -0.000664 | -0.615 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.03577 | 2.321 |
| w13 | 2 | -0.131628 | -0.337 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | -0.027531 | 0.333 |
| w16 | 1 | 0.408361 | 13.231 |
| w17 | 7 | 0.044721 | -0.422 |
| w18 | 8 | 0.160601 | 3.269 |
| w19 | 16 | 0.014738 | -6.894 |
| w20 | 11 | 0.054142 | 6.044 |
| w21 | 2 | -0.14539 | -4.304 |
| w22 | 4 | 0.060271 | -0.248 |
| w23 | 0 | -0.033865 | 0.0 |
| w24 | 3 | -0.086612 | 5.396 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.01431 | -0.522 |
| w2 | 11 | 0.090981 | -1.452 |
| w3 | 11 | -0.05468 | -4.625 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 6 | -0.078701 | -7.071 |
| w12 | 5 | -0.228787 | -7.383 |
| w14 | 0 | None | 0.0 |
| w15 | 11 | -0.054475 | -5.229 |
| w16 | 3 | 0.353826 | 27.168 |
| w17 | 0 | None | 0.0 |
| w18 | 13 | -0.086155 | -8.118 |
| w19 | 35 | -0.035284 | 0.883 |
| w20 | 4 | -0.036637 | -3.796 |
| w21 | 9 | -0.01834 | -4.941 |
| w22 | 8 | -0.062788 | -4.265 |
| w23 | 2 | 0.198666 | 6.097 |
| w24 | 2 | 0.004362 | -0.339 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 483 warm-up bars -- required_bars=486. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=486. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 21 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | -0.114656 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | -0.011514 | 0.0 |
| w6 | 0 | 0.071784 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | 0.00511 | 2.903 |
| w10 | 0 | None | 0.0 |
| w11 | 6 | -0.024441 | -7.42 |
| w12 | 0 | None | 0.0 |
| w15 | 2 | -0.021169 | 5.755 |
| w16 | 3 | 0.261896 | 26.133 |
| w17 | 8 | -0.099697 | -4.139 |
| w18 | 1 | 0.113588 | 1.074 |
| w19 | 11 | 0.054443 | 5.543 |
| w20 | 2 | -0.281929 | -6.64 |
| w21 | 12 | 0.065612 | 2.829 |
| w22 | 4 | -0.247005 | -4.242 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.081857 | 1.022 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=486. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=486. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 470 warm-up bars -- required_bars=486. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | None | -0.046 |
| w2 | 2 | -0.098618 | 0.06 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | -0.023098 | -0.018 |
| w6 | 4 | -0.041475 | -2.806 |
| w7 | 1 | 0.028086 | 0.423 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | 0.264663 | 3.421 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | -0.031353 | -3.2 |
| w12 | 8 | -0.051692 | -5.283 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | 0.024685 | 2.881 |
| w16 | 0 | None | 0.0 |
| w17 | 10 | -0.018394 | -0.532 |
| w18 | 6 | -0.114005 | -4.392 |
| w19 | 5 | 0.015573 | 9.849 |
| w20 | 6 | 0.075079 | 10.178 |
| w21 | 5 | 0.053399 | -1.021 |
| w22 | 15 | 0.04905 | -1.267 |
| w23 | 1 | -0.006431 | -0.233 |
| w24 | 0 | None | 0.0 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=486. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

