# Backtest of 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends_1d

- Plan: `../../../../03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.164223 | 7.326 |
| w2 | 3 | 0.100586 | 10.203 |
| w3 | 3 | 0.210266 | 2.27 |
| w4 | 44 | -0.03123 | -38.772 |
| w5 | 56 | -0.097634 | -17.321 |
| w6 | 38 | -0.21495 | -32.049 |
| w7 | 3 | -0.056149 | -1.911 |
| w8 | 18 | -0.111141 | -47.995 |
| w9 | 9 | -0.118008 | -3.706 |
| w10 | 46 | 0.059266 | -21.729 |
| w11 | 53 | -0.019569 | 24.712 |
| w12 | 45 | 0.004223 | -3.98 |
| w13 | 15 | -0.014244 | -5.736 |
| w14 | 11 | 0.004929 | -5.801 |
| w15 | 54 | -0.007187 | 38.589 |
| w16 | 12 | -0.105491 | -15.328 |
| w17 | 50 | -0.014366 | -50.905 |
| w18 | 17 | -0.091455 | -17.525 |
| w19 | 59 | -0.100801 | -24.14 |
| w20 | 27 | -0.183524 | -19.063 |
| w21 | 34 | -0.163302 | -14.653 |
| w22 | 15 | 0.004619 | -4.472 |
| w23 | 66 | -0.045298 | -15.912 |
| w24 | 21 | -0.102279 | -9.583 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.073584 | -11.704 |
| w2 | 4 | 0.129828 | -3.551 |
| w3 | 10 | 0.043313 | 1.713 |
| w4 | 20 | 0.029234 | -37.147 |
| w5 | 25 | -0.067541 | -7.412 |
| w6 | 29 | 0.088019 | -23.498 |
| w7 | 9 | -0.069981 | -5.211 |
| w8 | 17 | -0.02268 | -17.747 |
| w9 | 2 | 0.015259 | -0.655 |
| w10 | 42 | -0.052259 | -37.568 |
| w11 | 59 | -0.15739 | -36.812 |
| w12 | 69 | -0.084769 | -13.627 |
| w13 | 41 | 0.083716 | 25.9 |
| w14 | 0 | None | 0.0 |
| w15 | 48 | -0.201767 | -32.871 |
| w16 | 39 | 0.118212 | 24.14 |
| w17 | 54 | -0.048579 | -7.748 |
| w18 | 38 | 0.131702 | 11.73 |
| w19 | 50 | -0.131984 | -28.45 |
| w20 | 22 | -0.120581 | -18.016 |
| w21 | 36 | -0.08976 | 8.082 |
| w22 | 15 | 0.002684 | 5.078 |
| w23 | 32 | -0.101755 | 12.897 |
| w24 | 30 | -0.101946 | -7.001 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 40 | 0.009764 | 3.835 |
| w4 | 64 | -0.128151 | -55.333 |
| w5 | 21 | 0.101221 | 22.039 |
| w6 | 18 | 0.249115 | 19.32 |
| w7 | 3 | -0.014819 | -2.383 |
| w8 | 20 | -0.121087 | -34.125 |
| w9 | 0 | None | 0.0 |
| w10 | 37 | 0.04641 | -18.316 |
| w11 | 64 | -0.022213 | 7.422 |
| w12 | 36 | 0.106342 | 7.309 |
| w13 | 22 | -0.097427 | -4.588 |
| w14 | 0 | None | 0.0 |
| w15 | 41 | 0.084393 | 18.844 |
| w16 | 30 | 0.131794 | 19.545 |
| w17 | 48 | -0.120721 | -37.27 |
| w18 | 21 | -0.150519 | -30.373 |
| w19 | 49 | -0.01346 | -30.876 |
| w20 | 17 | 0.131067 | 1.235 |
| w21 | 40 | -0.140102 | -59.195 |
| w22 | 29 | -0.093529 | 1.133 |
| w23 | 30 | 0.027903 | 0.562 |
| w24 | 26 | 0.068584 | 1.863 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.027923 | -5.861 |
| w2 | 19 | 0.237736 | 12.596 |
| w3 | 28 | 0.134338 | 13.209 |
| w4 | 43 | 0.017944 | -15.797 |
| w5 | 30 | 0.056318 | 9.945 |
| w6 | 40 | 0.108807 | -0.241 |
| w8 | 18 | -0.127014 | -39.178 |
| w9 | 0 | None | 0.0 |
| w10 | 22 | -0.051194 | -44.449 |
| w11 | 66 | -0.03443 | -13.106 |
| w12 | 40 | -0.134813 | -9.322 |
| w14 | 10 | 0.106418 | 11.42 |
| w15 | 43 | 0.004053 | -5.34 |
| w16 | 37 | 0.094991 | 26.924 |
| w17 | 46 | 0.077255 | -10.138 |
| w18 | 31 | -0.073827 | 11.369 |
| w19 | 8 | 0.08578 | 54.049 |
| w20 | 52 | 0.110463 | 2.927 |
| w21 | 34 | 0.12604 | -19.195 |
| w22 | 64 | 0.089518 | -6.984 |
| w23 | 42 | -0.19405 | -63.607 |
| w24 | 42 | -0.069037 | 22.688 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 483 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 21 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.151008 | 11.137 |
| w2 | 2 | 0.219552 | -2.548 |
| w3 | 0 | -0.112844 | 0.0 |
| w4 | 0 | 0.070974 | 0.0 |
| w5 | 0 | 0.041256 | 0.0 |
| w6 | 23 | 0.104952 | 10.009 |
| w8 | 8 | 0.122451 | 15.005 |
| w9 | 4 | 0.121809 | 5.762 |
| w10 | 33 | -0.0906 | -32.047 |
| w11 | 35 | 0.003251 | -46.459 |
| w12 | 17 | 0.042218 | -5.243 |
| w15 | 27 | -0.087911 | -31.687 |
| w16 | 16 | -0.055241 | -25.025 |
| w17 | 32 | 0.132282 | -52.743 |
| w18 | 32 | -0.0707 | 7.258 |
| w19 | 27 | 0.073626 | 7.285 |
| w20 | 21 | 0.051662 | -6.187 |
| w21 | 36 | -0.012479 | -8.763 |
| w22 | 42 | -0.051923 | -1.027 |
| w23 | 36 | 0.042006 | 16.742 |
| w24 | 24 | -0.045083 | -1.056 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 470 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.100205 | -17.437 |
| w2 | 5 | 0.099998 | -0.805 |
| w3 | 6 | -0.116874 | -12.848 |
| w4 | 7 | 0.054981 | -0.091 |
| w5 | 0 | None | 0.0 |
| w6 | 34 | 0.153557 | 11.506 |
| w7 | 2 | 0.007327 | -3.942 |
| w8 | 16 | -0.13649 | -30.165 |
| w9 | 0 | None | 0.0 |
| w10 | 46 | -0.17205 | -13.332 |
| w11 | 59 | -0.028382 | -50.422 |
| w12 | 50 | 0.015628 | 17.706 |
| w14 | 0 | None | 0.0 |
| w15 | 35 | -0.114728 | -7.006 |
| w16 | 43 | 0.121254 | 53.37 |
| w17 | 38 | -0.013464 | -21.493 |
| w18 | 23 | -0.017334 | -6.107 |
| w19 | 16 | -0.046748 | -19.271 |
| w20 | 38 | -0.087218 | -17.651 |
| w21 | 56 | -0.077825 | -7.713 |
| w22 | 18 | 0.067922 | 1.816 |
| w23 | 39 | -0.058865 | 1.998 |
| w24 | 47 | -0.051106 | -33.837 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

