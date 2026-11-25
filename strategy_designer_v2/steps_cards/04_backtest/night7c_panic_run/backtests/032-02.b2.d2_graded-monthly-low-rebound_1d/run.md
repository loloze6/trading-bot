# Backtest of 032-02.b2.d2_graded-monthly-low-rebound_1d

- Plan: `../../../../03_test_plan/night7c_panic_run/plans/032-02.b2.d2_graded-monthly-low-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.041068 | 1.306 |
| w2 | 6 | -0.10668 | -16.901 |
| w3 | 2 | 0.30617 | 11.133 |
| w4 | 1 | -0.039951 | -0.905 |
| w5 | 4 | 0.146456 | 8.422 |
| w6 | 0 | None | 0.0 |
| w7 | 5 | 0.142187 | 6.104 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.006237 | -0.407 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.138186 | 6.282 |
| w13 | 3 | 0.07065 | 3.029 |
| w14 | 6 | 0.020241 | -2.061 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.134428 | 5.908 |
| w17 | 1 | 0.05905 | 2.938 |
| w18 | 2 | 0.131001 | 6.542 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | 0.077502 | 5.738 |
| w21 | 1 | -0.002471 | 0.285 |
| w22 | 1 | -0.105976 | -5.942 |
| w23 | 2 | 0.061918 | 3.005 |
| w24 | 3 | 0.012637 | -0.399 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.143528 | -8.748 |
| w2 | 5 | -0.071444 | -14.068 |
| w3 | 3 | 0.365126 | 16.258 |
| w4 | 1 | -0.031666 | -0.668 |
| w5 | 2 | -0.005192 | -0.94 |
| w6 | 1 | 0.019879 | 1.257 |
| w7 | 7 | 0.133885 | 4.24 |
| w8 | 1 | -0.03611 | -0.559 |
| w9 | 2 | 0.190465 | 9.073 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.244059 | 1.547 |
| w13 | 4 | 0.141837 | 7.05 |
| w14 | 7 | 0.014525 | -1.515 |
| w15 | 5 | -0.096663 | -8.73 |
| w16 | 2 | 0.232387 | 14.161 |
| w17 | 1 | 0.098442 | 4.321 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.095945 | -8.807 |
| w21 | 1 | 0.051606 | 1.494 |
| w22 | 3 | 0.043218 | 1.21 |
| w23 | 1 | -0.084234 | -2.08 |
| w24 | 4 | 0.082493 | 4.177 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.013016 | -0.183 |
| w2 | 3 | 0.006127 | -0.558 |
| w3 | 0 | None | 0.0 |
| w4 | 1 | -0.256504 | -19.019 |
| w5 | 5 | -0.066835 | -5.772 |
| w6 | 0 | None | 0.0 |
| w7 | 9 | 0.050096 | -1.436 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | 0.124216 | 5.113 |
| w10 | 1 | 0.011011 | 0.452 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.019333 | 0.498 |
| w13 | 1 | -0.086562 | -2.946 |
| w14 | 6 | 0.022245 | -0.776 |
| w15 | 2 | -0.027429 | -2.169 |
| w16 | 3 | 0.231457 | 9.994 |
| w17 | 2 | 0.092128 | 6.778 |
| w18 | 1 | 0.169854 | 6.588 |
| w19 | 1 | 0.035557 | 1.798 |
| w20 | 4 | 0.132437 | 7.721 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | 0.072171 | 3.242 |
| w23 | 1 | -0.006615 | -0.107 |
| w24 | 5 | 0.102137 | 4.562 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.110737 | -5.035 |
| w2 | 3 | -0.199478 | -15.22 |
| w3 | 2 | 0.233487 | 8.256 |
| w4 | 4 | 0.138288 | 7.239 |
| w5 | 6 | -0.028862 | -8.508 |
| w6 | 0 | None | 0.0 |
| w7 | 9 | 0.075485 | 2.14 |
| w8 | 0 | None | 0.0 |
| w9 | 5 | 0.24239 | 15.317 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.142949 | 6.332 |
| w14 | 7 | -0.086737 | -9.772 |
| w15 | 2 | -0.026561 | -2.131 |
| w16 | 3 | 0.122665 | 9.725 |
| w17 | 1 | 0.114735 | 4.94 |
| w18 | 1 | 0.499806 | 21.759 |
| w19 | 5 | 0.327397 | 40.587 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | 0.080922 | 6.833 |
| w22 | 1 | 0.165377 | 5.097 |
| w23 | 4 | 0.067607 | 2.631 |
| w24 | 0 | None | 0.0 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.004774 | -1.403 |
| w2 | 1 | -0.121942 | -7.392 |
| w3 | 0 | 0.034108 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | -0.006828 | -0.094 |
| w6 | 0 | None | 0.0 |
| w8 | 2 | 0.015853 | 0.987 |
| w9 | 4 | 0.185662 | 13.595 |
| w10 | 2 | 0.057621 | 2.668 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.123324 | 1.913 |
| w14 | 3 | -0.012424 | -0.911 |
| w15 | 3 | 0.005776 | 0.659 |
| w16 | 2 | 0.22698 | 12.847 |
| w17 | 3 | 0.254194 | 19.928 |
| w18 | 2 | 0.249764 | 9.091 |
| w19 | 1 | -0.307497 | -9.328 |
| w20 | 1 | 0.069378 | 4.544 |
| w21 | 1 | 0.016047 | 2.338 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.065988 | 2.385 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.123061 | -7.611 |
| w2 | 3 | 0.033976 | 0.804 |
| w3 | 4 | 0.036483 | -1.321 |
| w4 | 2 | -0.184683 | -11.225 |
| w5 | 6 | 0.018829 | -0.229 |
| w6 | 2 | 0.048649 | 1.014 |
| w7 | 5 | 0.081417 | 3.102 |
| w8 | 2 | -0.018865 | -0.447 |
| w9 | 3 | 0.008762 | -0.904 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.100905 | 5.029 |
| w14 | 6 | 0.008685 | -3.488 |
| w15 | 6 | -0.023123 | -6.394 |
| w16 | 3 | 0.02 | 1.519 |
| w17 | 3 | 0.167343 | 10.531 |
| w18 | 1 | 0.274456 | 11.22 |
| w19 | 3 | -0.052246 | -8.254 |
| w20 | 2 | -0.013027 | -0.798 |
| w21 | 2 | 0.010433 | 1.178 |
| w22 | 3 | -0.06965 | -4.594 |
| w23 | 2 | 0.096854 | 3.936 |
| w24 | 1 | -0.036693 | -0.591 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

