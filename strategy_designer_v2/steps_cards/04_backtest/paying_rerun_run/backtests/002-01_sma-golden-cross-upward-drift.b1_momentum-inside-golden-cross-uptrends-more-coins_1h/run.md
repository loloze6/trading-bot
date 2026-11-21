# Backtest of 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h

- Plan: `../../../../03_test_plan/hold_paying_run/plans/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h.md`
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
| w4 | 23 | -0.037254 | 30.151 |
| w5 | 29 | 0.023745 | 5.297 |
| w6 | 26 | -0.00145 | 30.185 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | -0.041861 | -1.747 |
| w9 | 18 | -0.020356 | -18.696 |
| w10 | 28 | 0.014276 | 41.217 |
| w11 | 42 | -0.016694 | 35.89 |
| w12 | 20 | 0.018442 | 12.379 |
| w13 | 12 | 0.001089 | -16.028 |
| w14 | 0 | None | 0.0 |
| w15 | 50 | 0.014928 | 62.231 |
| w16 | 2 | -0.017617 | -5.998 |
| w17 | 43 | 0.034893 | 185.709 |
| w18 | 8 | -0.044551 | -24.047 |
| w19 | 56 | 0.012621 | 30.666 |
| w20 | 27 | -0.010226 | -17.9 |
| w21 | 22 | 0.015439 | 53.753 |
| w22 | 22 | -0.008889 | -8.519 |
| w23 | 29 | -0.00575 | -12.218 |
| w24 | 16 | -0.009957 | -9.216 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.018615 | -7.844 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 12 | -0.03699 | 15.476 |
| w5 | 28 | -0.017516 | -15.505 |
| w6 | 6 | -0.015077 | 10.366 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.00883 | -3.804 |
| w9 | 0 | -0.009824 | 0.0 |
| w10 | 34 | 0.031672 | 108.286 |
| w11 | 41 | -0.014237 | 106.933 |
| w12 | 36 | -0.006334 | -11.409 |
| w13 | 9 | -0.013436 | 2.843 |
| w14 | 0 | None | 0.0 |
| w15 | 35 | 0.014846 | 13.183 |
| w16 | 13 | -0.001125 | 1.502 |
| w17 | 34 | 0.008173 | 51.885 |
| w18 | 31 | 0.003759 | 4.06 |
| w19 | 40 | 0.027677 | 40.265 |
| w20 | 36 | 0.010562 | -23.228 |
| w21 | 3 | -0.021037 | -9.635 |
| w22 | 11 | -0.017926 | -18.867 |
| w23 | 26 | 0.01259 | 47.517 |
| w24 | 19 | -0.030998 | -18.634 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.023229 | -4.099 |
| w2 | 0 | None | 0.0 |
| w3 | 10 | -0.005062 | -3.511 |
| w4 | 34 | -0.007397 | -7.522 |
| w5 | 18 | 0.008473 | -8.985 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 17 | -0.007094 | 13.417 |
| w9 | 0 | None | 0.0 |
| w10 | 5 | -0.035518 | -3.655 |
| w11 | 44 | -0.019804 | 36.81 |
| w12 | 9 | -0.022779 | -22.334 |
| w13 | 0 | 2.9e-05 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 23 | 0.007934 | 7.023 |
| w16 | 6 | -0.013602 | -10.248 |
| w17 | 30 | 0.00777 | 46.721 |
| w18 | 13 | -0.019152 | -24.999 |
| w19 | 19 | -0.000808 | 19.482 |
| w20 | 14 | -0.006896 | -7.658 |
| w21 | 13 | 0.0135 | 21.355 |
| w22 | 10 | -0.031754 | -9.652 |
| w23 | 5 | -0.020984 | -9.172 |
| w24 | 21 | -0.054949 | -41.837 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.033526 | -6.494 |
| w2 | 8 | -0.009822 | -25.203 |
| w3 | 0 | None | 0.0 |
| w4 | 19 | -0.006277 | 0.759 |
| w5 | 14 | -0.023281 | -14.6 |
| w6 | 7 | -0.04525 | -6.711 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 7 | -0.02499 | -21.32 |
| w10 | 27 | -0.009444 | 41.071 |
| w11 | 40 | -0.004098 | 61.126 |
| w12 | 0 | None | 0.0 |
| w13 | 6 | -0.008006 | -11.542 |
| w14 | 0 | None | 0.0 |
| w15 | 40 | -0.012003 | -15.534 |
| w16 | 13 | -0.007681 | -12.683 |
| w17 | 22 | -0.008863 | 51.085 |
| w18 | 9 | -0.014519 | -18.396 |
| w19 | 16 | -0.010188 | -33.704 |
| w20 | 19 | -0.039895 | -9.887 |
| w21 | 26 | -0.027741 | -16.147 |
| w22 | 23 | -0.01383 | 31.489 |
| w23 | 23 | 0.008915 | -5.671 |
| w24 | 14 | -0.0193 | 40.146 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 5 | -0.01683 | -6.664 |
| w4 | 11 | -0.003517 | -0.463 |
| w5 | 24 | 0.015534 | 33.273 |
| w6 | 19 | -0.0484 | -19.108 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | -0.005391 | 1.283 |
| w11 | 33 | -0.007654 | 113.028 |
| w12 | 22 | -0.027925 | -24.837 |
| w13 | 11 | -0.005574 | -15.847 |
| w14 | 0 | None | 0.0 |
| w15 | 11 | -0.030883 | -25.171 |
| w16 | 0 | None | 0.0 |
| w17 | 17 | 0.036504 | 171.635 |
| w18 | 15 | -0.012818 | -10.226 |
| w19 | 14 | -0.018416 | -19.467 |
| w20 | 7 | -0.007963 | -4.734 |
| w21 | 33 | 0.063442 | 226.613 |
| w22 | 34 | 0.001424 | -8.842 |
| w23 | 19 | -0.022638 | -23.339 |
| w24 | 14 | -0.030275 | -14.43 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.020116 | -1.397 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.050181 | -23.431 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 17 | 0.011086 | 54.827 |
| w11 | 46 | -0.014488 | 65.547 |
| w12 | 8 | 0.008931 | -11.687 |
| w13 | 3 | -0.015354 | -0.931 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.006928 | -0.569 |
| w16 | 12 | -0.008285 | 1.739 |
| w17 | 26 | -0.008083 | -9.811 |
| w18 | 10 | -0.019663 | -26.566 |
| w19 | 11 | -0.000954 | -10.971 |
| w20 | 9 | -0.013785 | -12.237 |
| w21 | 21 | -0.00412 | 76.532 |
| w22 | 14 | -0.025639 | -6.46 |
| w23 | 18 | -0.018501 | -13.713 |
| w24 | 35 | 0.02045 | 380.507 |

- ADAUSD: 20 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 6 | -0.021099 | 1.925 |
| w5 | 6 | -0.012388 | -20.502 |
| w6 | 19 | 0.023254 | 37.481 |
| w9 | 0 | None | 0.0 |
| w10 | 37 | 0.016491 | 47.782 |
| w11 | 35 | 0.006973 | 128.89 |
| w12 | 16 | -0.010024 | -15.201 |
| w15 | 15 | -0.01877 | -10.786 |
| w16 | 12 | -0.015138 | -17.58 |
| w17 | 28 | 0.008709 | 42.36 |
| w18 | 47 | 0.015065 | 61.004 |
| w19 | 17 | 0.0127 | 11.159 |
| w20 | 3 | -0.012384 | -3.692 |
| w21 | 17 | 0.02301 | 30.291 |
| w22 | 17 | -0.02154 | -20.82 |
| w23 | 5 | -0.032111 | -13.743 |
| w24 | 12 | -0.015898 | -16.652 |

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
| w3 | 7 | -0.02301 | -5.61 |
| w4 | 13 | -0.011988 | -2.957 |
| w5 | 0 | None | 0.0 |
| w6 | 11 | 0.001747 | 12.424 |
| w11 | 46 | 0.03398 | 936.062 |
| w12 | 2 | 0.006548 | -2.749 |
| w18 | 31 | 0.018312 | 16.812 |
| w19 | 25 | 0.032544 | 103.274 |
| w20 | 12 | -0.010188 | -8.557 |
| w21 | 19 | 0.043213 | 60.309 |
| w22 | 9 | -0.009717 | -12.54 |
| w23 | 7 | -0.018053 | -7.457 |
| w24 | 10 | 0.000957 | 6.943 |

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
| w4 | 17 | -0.026023 | -9.349 |
| w5 | 3 | -0.01909 | -4.336 |
| w6 | 32 | 0.019091 | 59.02 |
| w11 | 30 | -0.02993 | 69.587 |
| w12 | 11 | 0.002527 | -14.981 |
| w17 | 31 | -0.001232 | -0.84 |
| w18 | 11 | -0.017655 | -16.273 |
| w19 | 25 | 0.002418 | -9.47 |
| w20 | 4 | -0.014972 | 4.351 |
| w21 | 9 | 0.009444 | 11.457 |
| w22 | 10 | -0.021096 | -15.904 |
| w23 | 18 | -0.006601 | 4.782 |
| w24 | 10 | -0.026732 | -11.113 |

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
| w2 | 25 | -0.016416 | -25.43 |
| w3 | 0 | None | 0.0 |
| w4 | 18 | -0.026767 | -14.831 |
| w5 | 28 | -0.009657 | 1.171 |
| w6 | 68 | -0.007819 | 52.241 |
| w11 | 37 | -0.01951 | 110.414 |
| w12 | 16 | -0.022502 | -10.021 |
| w18 | 13 | -0.033969 | -18.742 |
| w19 | 40 | 0.015584 | 38.289 |
| w20 | 53 | 0.011618 | 13.027 |
| w21 | 53 | 0.014902 | 118.175 |
| w22 | 33 | -0.038624 | -7.179 |
| w23 | 34 | -0.002996 | 54.53 |
| w24 | 13 | -0.011984 | -16.248 |

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
| w3 | 5 | -0.062864 | -16.541 |
| w4 | 13 | -0.03148 | -18.784 |
| w5 | 2 | -0.023579 | -15.39 |
| w6 | 15 | -0.00545 | 5.7 |
| w12 | 0 | None | 0.0 |
| w19 | 33 | 0.024679 | 36.502 |
| w20 | 18 | 0.029639 | 14.394 |
| w21 | 9 | 0.023515 | 50.09 |
| w22 | 10 | -0.014555 | -11.779 |
| w23 | 11 | -0.02001 | -13.107 |
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
| w4 | 17 | -0.02335 | -16.529 |
| w5 | 0 | None | 0.0 |
| w6 | 10 | -0.021885 | 27.911 |
| w12 | 8 | -0.016097 | -18.649 |
| w19 | 39 | 0.008787 | -22.079 |
| w20 | 5 | -0.013128 | -2.704 |
| w21 | 24 | -0.007527 | 122.326 |
| w22 | 11 | -0.015606 | -15.378 |
| w23 | 22 | -0.0101 | 2.336 |
| w24 | 2 | -0.021512 | -1.622 |

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
| w4 | 16 | -0.004881 | -7.255 |
| w5 | 0 | None | 0.0 |
| w6 | 13 | -0.001649 | 28.603 |
| w19 | 15 | 0.021287 | 21.815 |
| w20 | 12 | 0.001626 | -2.894 |
| w21 | 11 | 0.019374 | 17.014 |
| w22 | 9 | -0.017773 | -9.177 |
| w23 | 7 | -0.004094 | -2.187 |
| w24 | 16 | 0.025736 | 7.965 |

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
| w4 | 2 | -0.031611 | -8.028 |
| w5 | 10 | -0.038925 | -19.459 |
| w6 | 32 | 0.015554 | 118.461 |
| w19 | 35 | 0.016868 | 31.987 |
| w20 | 33 | 0.006904 | 0.828 |
| w21 | 9 | 0.003947 | 32.832 |
| w22 | 11 | 0.003331 | -7.914 |
| w23 | 7 | -0.003522 | 0.648 |
| w24 | 10 | 0.001974 | -1.447 |

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
| w4 | 23 | -0.016153 | 35.738 |
| w5 | 30 | 0.000181 | -11.053 |
| w6 | 40 | 0.032813 | 235.774 |
| w19 | 20 | -0.001089 | -6.498 |
| w20 | 4 | -0.021684 | -0.112 |
| w21 | 4 | -0.011359 | -11.662 |
| w22 | 10 | -0.014135 | -9.445 |
| w23 | 9 | -0.023969 | -11.712 |
| w24 | 9 | -0.019525 | -11.78 |

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

