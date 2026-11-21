# Backtest of 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h

- Plan: `../../../../03_test_plan/hold2_rerun_run/plans/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.015117 | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 23 | -0.037254 | 30.023 |
| w5 | 29 | 0.023745 | 5.129 |
| w6 | 26 | -0.00145 | 29.944 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | -0.041861 | -1.755 |
| w9 | 18 | -0.020356 | -18.775 |
| w10 | 28 | 0.014276 | 41.02 |
| w11 | 42 | -0.016694 | 35.733 |
| w12 | 20 | 0.018442 | 12.3 |
| w13 | 12 | 0.001089 | -16.053 |
| w14 | 0 | None | 0.0 |
| w15 | 50 | 0.014928 | 61.992 |
| w16 | 2 | -0.017617 | -6.014 |
| w17 | 43 | 0.034893 | 185.201 |
| w18 | 8 | -0.044551 | -24.072 |
| w19 | 56 | 0.012621 | 30.316 |
| w20 | 27 | -0.010226 | -18.013 |
| w21 | 22 | 0.015439 | 53.562 |
| w22 | 22 | -0.008889 | -8.64 |
| w23 | 29 | -0.00575 | -12.376 |
| w24 | 16 | -0.009957 | -9.301 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.018615 | -7.861 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 12 | -0.03699 | 15.394 |
| w5 | 28 | -0.017516 | -15.699 |
| w6 | 6 | -0.015077 | 10.305 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.00883 | -3.821 |
| w9 | 0 | -0.009824 | 0.0 |
| w10 | 34 | 0.031672 | 107.915 |
| w11 | 41 | -0.014237 | 106.649 |
| w12 | 36 | -0.006334 | -11.566 |
| w13 | 9 | -0.013436 | 2.822 |
| w14 | 0 | None | 0.0 |
| w15 | 35 | 0.014846 | 13.023 |
| w16 | 13 | -0.001125 | 1.425 |
| w17 | 34 | 0.008173 | 51.658 |
| w18 | 31 | 0.003759 | 3.938 |
| w19 | 40 | 0.027677 | 39.842 |
| w20 | 36 | 0.010562 | -23.394 |
| w21 | 3 | -0.021037 | -9.672 |
| w22 | 11 | -0.017926 | -18.923 |
| w23 | 26 | 0.01259 | 47.334 |
| w24 | 19 | -0.030998 | -18.746 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.023229 | -4.101 |
| w2 | 0 | None | 0.0 |
| w3 | 10 | -0.005062 | -3.527 |
| w4 | 34 | -0.007397 | -7.564 |
| w5 | 18 | 0.008473 | -9.029 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 17 | -0.007094 | 13.393 |
| w9 | 0 | None | 0.0 |
| w10 | 5 | -0.035518 | -3.663 |
| w11 | 44 | -0.019804 | 36.754 |
| w12 | 9 | -0.022779 | -22.347 |
| w13 | 0 | 2.9e-05 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 23 | 0.007934 | 6.998 |
| w16 | 6 | -0.013602 | -10.255 |
| w17 | 30 | 0.00777 | 46.65 |
| w18 | 13 | -0.019152 | -25.008 |
| w19 | 19 | -0.000808 | 19.435 |
| w20 | 14 | -0.006896 | -7.678 |
| w21 | 13 | 0.0135 | 21.324 |
| w22 | 10 | -0.031754 | -9.662 |
| w23 | 5 | -0.020984 | -9.181 |
| w24 | 21 | -0.054949 | -41.872 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.033526 | -6.481 |
| w2 | 8 | -0.009822 | -25.183 |
| w3 | 0 | None | 0.0 |
| w4 | 19 | -0.006277 | 0.92 |
| w5 | 14 | -0.023281 | -14.469 |
| w6 | 7 | -0.04525 | -6.629 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 7 | -0.02499 | -21.289 |
| w10 | 27 | -0.009444 | 41.271 |
| w11 | 40 | -0.004098 | 61.297 |
| w12 | 0 | None | 0.0 |
| w13 | 6 | -0.008006 | -11.531 |
| w14 | 0 | None | 0.0 |
| w15 | 40 | -0.012003 | -15.407 |
| w16 | 13 | -0.007681 | -12.628 |
| w17 | 22 | -0.008863 | 51.245 |
| w18 | 9 | -0.014519 | -18.373 |
| w19 | 16 | -0.010188 | -33.61 |
| w20 | 19 | -0.039895 | -9.747 |
| w21 | 26 | -0.027741 | -15.986 |
| w22 | 23 | -0.01383 | 31.667 |
| w23 | 23 | 0.008915 | -5.548 |
| w24 | 14 | -0.0193 | 40.258 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 5 | -0.01683 | -6.71 |
| w4 | 11 | -0.003517 | -0.537 |
| w5 | 24 | 0.015534 | 33.039 |
| w6 | 19 | -0.0484 | -19.346 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | -0.005391 | 1.223 |
| w11 | 33 | -0.007654 | 112.871 |
| w12 | 22 | -0.027925 | -24.916 |
| w13 | 11 | -0.005574 | -15.872 |
| w14 | 0 | None | 0.0 |
| w15 | 11 | -0.030883 | -25.245 |
| w16 | 0 | None | 0.0 |
| w17 | 17 | 0.036504 | 171.341 |
| w18 | 15 | -0.012818 | -10.269 |
| w19 | 14 | -0.018416 | -19.596 |
| w20 | 7 | -0.007963 | -4.768 |
| w21 | 33 | 0.063442 | 225.939 |
| w22 | 34 | 0.001424 | -8.991 |
| w23 | 19 | -0.022638 | -23.515 |
| w24 | 15 | -0.030275 | -14.537 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.020116 | -1.397 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.050181 | -23.434 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 17 | 0.011086 | 54.819 |
| w11 | 46 | -0.014488 | 65.532 |
| w12 | 8 | 0.008931 | -11.689 |
| w13 | 3 | -0.015354 | -0.932 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.006928 | -0.573 |
| w16 | 12 | -0.008285 | 1.735 |
| w17 | 26 | -0.008083 | -9.818 |
| w18 | 10 | -0.019663 | -26.568 |
| w19 | 11 | -0.000954 | -10.974 |
| w20 | 9 | -0.013785 | -12.239 |
| w21 | 21 | -0.00412 | 76.522 |
| w22 | 14 | -0.025639 | -6.464 |
| w23 | 18 | -0.018501 | -13.72 |
| w24 | 35 | 0.02045 | 380.473 |

- ADAUSD: 20 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 6 | -0.021099 | 1.944 |
| w5 | 6 | -0.012388 | -20.489 |
| w6 | 19 | 0.023254 | 37.527 |
| w9 | 0 | None | 0.0 |
| w10 | 37 | 0.016491 | 47.86 |
| w11 | 35 | 0.006973 | 128.958 |
| w12 | 16 | -0.010024 | -15.178 |
| w15 | 15 | -0.01877 | -10.769 |
| w16 | 12 | -0.015138 | -17.559 |
| w17 | 28 | 0.008709 | 42.424 |
| w18 | 47 | 0.015065 | 61.097 |
| w19 | 17 | 0.0127 | 11.185 |
| w20 | 3 | -0.012384 | -3.688 |
| w21 | 17 | 0.02301 | 30.323 |
| w22 | 17 | -0.02154 | -20.799 |
| w23 | 5 | -0.032111 | -13.732 |
| w24 | 12 | -0.015898 | -16.633 |

- w7 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ADAUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w8 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 2174 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ADAUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 15 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 7 | -0.02301 | -5.639 |
| w4 | 13 | -0.011988 | -3.032 |
| w5 | 0 | None | 0.0 |
| w6 | 11 | 0.001747 | 12.352 |
| w11 | 46 | 0.03398 | 934.843 |
| w12 | 2 | 0.006548 | -2.752 |
| w18 | 31 | 0.018312 | 16.733 |
| w19 | 25 | 0.032544 | 103.049 |
| w20 | 12 | -0.010188 | -8.603 |
| w21 | 19 | 0.043213 | 60.214 |
| w22 | 9 | -0.009717 | -12.584 |
| w23 | 7 | -0.018053 | -7.489 |
| w24 | 10 | 0.000957 | 6.877 |

- w7 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for DOGEUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w8 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for DOGEUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w9 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w10 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 1710 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for DOGEUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w14 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for DOGEUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w15 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for DOGEUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w16 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 63 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w17 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 3982 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- LINKUSD: 16 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 17 | -0.026023 | -9.402 |
| w5 | 3 | -0.01909 | -4.341 |
| w6 | 32 | 0.019091 | 58.889 |
| w11 | 30 | -0.02993 | 69.474 |
| w12 | 11 | 0.002527 | -15.012 |
| w17 | 31 | -0.001232 | -0.894 |
| w18 | 11 | -0.017655 | -16.299 |
| w19 | 25 | 0.002418 | -9.562 |
| w20 | 4 | -0.014972 | 4.344 |
| w21 | 9 | 0.009444 | 11.423 |
| w22 | 10 | -0.021096 | -15.921 |
| w23 | 18 | -0.006601 | 4.735 |
| w24 | 10 | -0.026732 | -11.138 |

- w7 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for LINKUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w8 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for LINKUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w9 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w10 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 4775 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for LINKUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w14 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for LINKUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w15 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for LINKUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w16 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 2021 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- TRXUSD: 15 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 25 | -0.016416 | -25.51 |
| w3 | 0 | None | 0.0 |
| w4 | 18 | -0.026767 | -14.919 |
| w5 | 28 | -0.009657 | 0.982 |
| w6 | 68 | -0.007819 | 51.729 |
| w11 | 37 | -0.01951 | 110.25 |
| w12 | 16 | -0.022502 | -10.086 |
| w18 | 13 | -0.033969 | -18.757 |
| w19 | 40 | 0.015584 | 38.034 |
| w20 | 53 | 0.011618 | 12.606 |
| w21 | 53 | 0.014902 | 117.638 |
| w22 | 33 | -0.038624 | -7.304 |
| w23 | 34 | -0.002996 | 54.261 |
| w24 | 13 | -0.011984 | -16.327 |

- w7 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TRXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w8 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TRXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w9 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TRXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w10 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 1045 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TRXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w14 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TRXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w15 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TRXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w16 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w17 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 3624 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- UNIUSD: 13 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 5 | -0.062864 | -16.544 |
| w4 | 13 | -0.03148 | -18.79 |
| w5 | 2 | -0.023579 | -15.392 |
| w6 | 15 | -0.00545 | 5.696 |
| w12 | 0 | None | 0.0 |
| w19 | 33 | 0.024679 | 36.491 |
| w20 | 18 | 0.029639 | 14.387 |
| w21 | 9 | 0.023515 | 50.087 |
| w22 | 10 | -0.014555 | -11.78 |
| w23 | 11 | -0.02001 | -13.11 |
| w24 | 1 | -0.019055 | -1.84 |

- w7 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for UNIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w8 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for UNIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w9 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for UNIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w10 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for UNIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w11 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 1820 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for UNIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w14 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for UNIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w15 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for UNIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w16 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for UNIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w17 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w18 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 4698 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- AAVEUSD: 13 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 17 | -0.02335 | -16.508 |
| w5 | 0 | None | 0.0 |
| w6 | 10 | -0.021885 | 27.929 |
| w12 | 8 | -0.016097 | -18.641 |
| w19 | 39 | 0.008787 | -22.042 |
| w20 | 5 | -0.013128 | -2.694 |
| w21 | 24 | -0.007527 | 122.382 |
| w22 | 11 | -0.015606 | -15.371 |
| w23 | 22 | -0.0101 | 2.359 |
| w24 | 2 | -0.021512 | -1.619 |

- w7 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AAVEUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w8 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AAVEUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w9 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AAVEUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w10 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AAVEUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w11 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 382 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AAVEUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w14 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AAVEUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w15 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AAVEUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w16 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AAVEUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w17 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w18 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 3259 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- AVAXUSD: 10 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w3 | 0 | None | 0.0 |
| w4 | 16 | -0.004881 | -7.276 |
| w5 | 0 | None | 0.0 |
| w6 | 13 | -0.001649 | 28.583 |
| w19 | 15 | 0.021287 | 21.796 |
| w20 | 12 | 0.001626 | -2.907 |
| w21 | 11 | 0.019374 | 16.991 |
| w22 | 9 | -0.017773 | -9.18 |
| w23 | 7 | -0.004094 | -2.196 |
| w24 | 16 | 0.025736 | 7.943 |

- w1 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 249 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w2 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 3129 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w7 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AVAXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w8 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AVAXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w9 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AVAXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w10 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AVAXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w11 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AVAXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w12 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AVAXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w14 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AVAXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w15 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AVAXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w16 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AVAXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w17 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AVAXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w18 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for AVAXUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- SOLUSD: 11 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.031611 | -8.081 |
| w5 | 10 | -0.038925 | -19.556 |
| w6 | 32 | 0.015554 | 118.002 |
| w19 | 35 | 0.016868 | 31.702 |
| w20 | 33 | 0.006904 | 0.579 |
| w21 | 9 | 0.003947 | 32.654 |
| w22 | 11 | 0.003331 | -8.008 |
| w23 | 7 | -0.003522 | 0.579 |
| w24 | 10 | 0.001974 | -1.612 |

- w1 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 4702 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w7 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SOLUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w8 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SOLUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w9 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SOLUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w10 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SOLUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w11 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SOLUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w12 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 1774 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SOLUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w14 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SOLUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w15 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SOLUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w16 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SOLUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w17 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SOLUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w18 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- INJUSD: 11 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 23 | -0.016153 | 35.97 |
| w5 | 30 | 0.000181 | -10.812 |
| w6 | 40 | 0.032813 | 237.747 |
| w19 | 20 | -0.001089 | -6.33 |
| w20 | 4 | -0.021684 | -0.088 |
| w21 | 4 | -0.011359 | -11.593 |
| w22 | 10 | -0.014135 | -9.364 |
| w23 | 9 | -0.023969 | -11.64 |
| w24 | 9 | -0.019525 | -11.654 |

- w1 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 3106 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w7 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for INJUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w8 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for INJUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w9 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for INJUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w10 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for INJUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w11 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for INJUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w12 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 463 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for INJUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w14 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for INJUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w15 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for INJUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w16 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for INJUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w17 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for INJUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w18 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=4920. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

