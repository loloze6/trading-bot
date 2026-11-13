# Backtest of N2-01_weekday-of-coming-bar_1d_oos

- Plan: `../../../../03_test_plan/overnight_run/plans_oos/N2-01_weekday-of-coming-bar_1d_oos.md`
- Config: `config.json` (a copy of the plan's config)
- Data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- ADAUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.002075 | -12.892 |
| w2 | 16 | 0.049759 | 3.705 |
| w3 | 18 | 0.092335 | 3.177 |
| w4 | 10 | -0.03876 | -3.605 |
| w5 | 0 | None | 0.0 |
| w6 | 6 | -0.058009 | -1.874 |
| w7 | 13 | -0.060818 | -8.552 |
| w8 | 10 | 0.047661 | 0.539 |
| w9 | 17 | -0.022948 | 4.261 |
| w10 | 3 | 0.00051 | 0.442 |
| w11 | 1 | -0.012053 | 0.083 |
| w12 | 0 | None | 0.0 |

- AVAXUSD: 10 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w3 | 2 | 0.001208 | -0.579 |
| w4 | 1 | -0.017446 | -0.2 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | 0.031916 | 6.498 |
| w7 | 17 | -0.025202 | -12.787 |
| w8 | 15 | -0.021428 | -6.94 |
| w9 | 9 | -0.057011 | -4.004 |
| w10 | 0 | 0.070098 | 0.0 |
| w11 | 15 | 0.078309 | 12.485 |
| w12 | 17 | 0.070041 | 3.446 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 11 prefetch bars (<date> to <date>) -- required_bars=228. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w2 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 131 prefetch bars (<date> to <date>) -- required_bars=228. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.074204 | -6.153 |
| w2 | 10 | -0.096321 | -9.487 |
| w3 | 12 | 0.017578 | 8.264 |
| w4 | 17 | 0.04128 | 9.514 |
| w5 | 7 | -0.20878 | -14.014 |
| w6 | 12 | -0.044219 | -1.975 |
| w7 | 9 | -0.052981 | -9.036 |
| w8 | 14 | 0.119219 | 9.033 |
| w9 | 17 | 0.062206 | 48.974 |
| w10 | 17 | 0.028512 | -4.274 |
| w11 | 18 | -0.027866 | -5.312 |
| w12 | 11 | -0.030959 | -6.417 |

- LINKUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.001807 | -11.886 |
| w2 | 14 | -0.063117 | -15.332 |
| w3 | 7 | -0.105068 | -9.855 |
| w4 | 10 | -0.027486 | -1.341 |
| w5 | 0 | -0.288302 | 0.0 |
| w6 | 4 | -0.056864 | -3.786 |
| w7 | 16 | -0.077826 | -15.177 |
| w8 | 7 | -0.004919 | -1.969 |
| w9 | 15 | -0.001242 | 4.028 |
| w10 | 3 | -0.00574 | -0.051 |
| w11 | 3 | 0.006762 | 0.457 |
| w12 | 15 | 0.040727 | -1.31 |

- SOLUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 11 | 0.087148 | 12.02 |
| w3 | 18 | 0.00218 | -21.07 |
| w4 | 17 | -0.089677 | -11.045 |
| w5 | 3 | -0.202007 | -6.433 |
| w6 | 2 | -0.077113 | -2.747 |
| w7 | 10 | -0.033473 | -2.151 |
| w8 | 3 | -0.056519 | -2.1 |
| w9 | 14 | -0.020096 | 0.745 |
| w10 | 14 | -0.009902 | -6.418 |
| w11 | 13 | -0.009671 | -1.159 |
| w12 | 0 | -0.127594 | 0.0 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 198 prefetch bars (<date> to <date>) -- required_bars=228. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- TRXUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.006912 | -5.806 |
| w2 | 4 | -0.089438 | -4.354 |
| w3 | 13 | 0.076867 | 0.891 |
| w4 | 10 | 0.015449 | 0.419 |
| w5 | 15 | 0.018304 | -0.304 |
| w6 | 18 | 0.052886 | 6.808 |
| w7 | 17 | 0.05057 | 1.707 |
| w8 | 16 | -0.030978 | -1.502 |
| w9 | 10 | 0.005437 | 4.65 |
| w10 | 0 | None | 0.0 |
| w11 | 8 | -0.126651 | -1.581 |
| w12 | 0 | -0.290184 | 0.0 |

- UNIUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.042438 | -12.181 |
| w2 | 2 | -0.122875 | -5.485 |
| w3 | 3 | -0.111252 | -3.324 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.049773 | -2.928 |
| w7 | 12 | -0.012008 | -4.177 |
| w8 | 13 | 0.021988 | 1.835 |
| w9 | 17 | 0.026899 | 29.914 |
| w10 | 7 | -0.010057 | -3.73 |
| w11 | 15 | -0.044171 | -3.838 |
| w12 | 8 | 0.071018 | 7.187 |

- AAVEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.048279 | -9.309 |
| w2 | 0 | -0.147749 | 0.0 |
| w3 | 0 | -0.000563 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | -0.060322 | 0.0 |
| w8 | 5 | -0.00653 | 0.629 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 3 | 0.028662 | 0.654 |
| w12 | 8 | 0.00555 | -1.829 |

- INJUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 3 | -0.043353 | -7.737 |
| w3 | 1 | -0.039065 | 0.061 |
| w4 | 1 | -0.12044 | -3.255 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 4 | -0.111617 | -1.509 |
| w8 | 1 | -0.059439 | -0.37 |
| w9 | 1 | -0.173412 | -1.578 |
| w10 | 0 | None | 0.0 |
| w11 | 13 | -0.032833 | -3.777 |
| w12 | 14 | -0.027168 | -11.665 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 144 prefetch bars (<date> to <date>) -- required_bars=228. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

