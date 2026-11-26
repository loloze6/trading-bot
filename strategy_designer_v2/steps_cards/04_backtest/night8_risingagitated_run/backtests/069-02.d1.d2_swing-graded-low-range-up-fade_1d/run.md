# Backtest of 069-02.d1.d2_swing-graded-low-range-up-fade_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/069-02.d1.d2_swing-graded-low-range-up-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.033076 | -0.464 |
| w2 | 4 | 0.145254 | 10.757 |
| w3 | 5 | -0.069984 | -5.664 |
| w4 | 1 | 0.016555 | -0.059 |
| w5 | 2 | 0.103601 | 2.162 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | 0.079504 | 0.138 |
| w8 | 3 | 0.029929 | 0.204 |
| w9 | 4 | 0.124034 | 6.555 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | -0.056626 | -1.565 |
| w14 | 7 | -0.074682 | -4.572 |
| w15 | 1 | None | -0.023 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | 0.026968 | 0.788 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.088966 | 3.316 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.103706 | 2.158 |
| w2 | 2 | -0.009102 | -2.102 |
| w3 | 3 | -0.050242 | -3.2 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | -0.139094 | -1.107 |
| w6 | 1 | -0.048034 | -2.705 |
| w7 | 11 | 0.089874 | 6.459 |
| w8 | 1 | 0.034848 | 1.014 |
| w9 | 1 | 0.168635 | 2.201 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | -0.050983 | -1.291 |
| w14 | 13 | 0.092646 | 15.705 |
| w15 | 3 | -0.025642 | -0.906 |
| w16 | 2 | -0.041673 | -4.217 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.084839 | -2.35 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | -0.018805 | -0.651 |
| w21 | 1 | -0.02018 | -0.491 |
| w22 | 5 | -0.073793 | -4.04 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | -0.036813 | -0.711 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.054519 | 0.996 |
| w2 | 2 | 0.015583 | 2.435 |
| w3 | 2 | 0.006691 | -0.247 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | -0.0413 | -2.066 |
| w6 | 2 | -0.008847 | -0.703 |
| w7 | 12 | 0.125237 | 4.167 |
| w8 | 1 | 0.053295 | 1.39 |
| w9 | 9 | -0.03224 | -0.957 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | -0.060326 | -0.177 |
| w14 | 10 | -0.066438 | -4.747 |
| w15 | 6 | -0.02321 | -1.514 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | -0.133746 | -4.416 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | 0.053823 | 2.146 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | -0.049084 | -1.309 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.007717 | -0.976 |
| w2 | 4 | 0.060681 | 3.059 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | -0.117316 | -5.345 |
| w6 | 0 | None | 0.0 |
| w8 | 2 | -0.024724 | -1.394 |
| w9 | 9 | 0.080737 | 4.72 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.02944 | -0.808 |
| w14 | 10 | 0.106637 | 15.624 |
| w15 | 1 | 0.020482 | 0.33 |
| w16 | 2 | 0.066453 | 2.205 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | -0.012259 | -0.179 |
| w19 | 2 | -0.004666 | -0.969 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

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
| w1 | 4 | 0.031631 | 0.638 |
| w2 | 3 | 0.008899 | 12.223 |
| w3 | 0 | 0.045724 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | -0.043281 | 0.0 |
| w8 | 4 | 0.022213 | 0.911 |
| w9 | 2 | 0.101737 | 2.503 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | -0.04136 | -1.726 |
| w12 | 0 | None | 0.0 |
| w15 | 1 | -0.066589 | -2.097 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | 0.1889 | 3.655 |
| w19 | 2 | -0.006089 | -0.131 |
| w20 | 0 | None | 0.0 |
| w21 | 1 | 0.034997 | 0.759 |
| w22 | 1 | -0.05006 | -0.62 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.064372 | 1.243 |

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
| w1 | 3 | -0.049709 | -0.938 |
| w2 | 6 | 0.247188 | 14.686 |
| w3 | 3 | 0.021587 | 0.832 |
| w4 | 1 | -0.034646 | -0.435 |
| w5 | 3 | 0.256042 | 7.86 |
| w6 | 1 | -0.013853 | -0.347 |
| w7 | 8 | 0.003283 | 0.451 |
| w8 | 6 | 0.093347 | 1.711 |
| w9 | 8 | -0.04916 | -2.029 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 10 | -0.042077 | -0.788 |
| w15 | 8 | 0.042527 | 2.355 |
| w16 | 3 | -0.032031 | -5.288 |
| w17 | 2 | 0.047917 | 1.143 |
| w18 | 2 | -0.048234 | -1.758 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.018595 | -0.432 |
| w21 | 0 | None | 0.0 |
| w22 | 5 | -0.16385 | -5.221 |
| w23 | 2 | -0.118022 | -1.851 |
| w24 | 0 | None | 0.0 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=486. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

