# Backtest of 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d

- Plan: `../../../../03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.011112 | -14.647 |
| w2 | 10 | 0.037537 | -9.127 |
| w3 | 16 | 0.003857 | -46.054 |
| w4 | 21 | 0.131911 | 59.573 |
| w5 | 17 | -0.019471 | -14.662 |
| w6 | 26 | -0.067873 | 72.737 |
| w7 | 12 | 0.210467 | 4.357 |
| w8 | 16 | 0.047308 | 27.539 |
| w9 | 7 | 0.065697 | -2.364 |
| w10 | 19 | 0.024317 | 14.081 |
| w11 | 19 | -0.042529 | 8.74 |
| w12 | 20 | 0.010421 | 11.845 |
| w13 | 6 | -0.008899 | -2.339 |
| w14 | 14 | 0.03557 | -17.913 |
| w15 | 19 | 0.091924 | 57.792 |
| w16 | 18 | 0.001483 | 32.107 |
| w17 | 30 | 0.08044 | 94.846 |
| w18 | 15 | 0.050539 | -5.158 |
| w19 | 20 | 0.130861 | 46.685 |
| w20 | 18 | -0.066614 | -29.405 |
| w21 | 25 | 0.110908 | 30.027 |
| w22 | 21 | -0.066484 | -9.845 |
| w23 | 36 | 0.173283 | 5.918 |
| w24 | 13 | 0.030693 | -11.761 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.0574 | -0.12 |
| w2 | 6 | -0.04879 | 5.623 |
| w3 | 13 | 0.066589 | -34.161 |
| w4 | 32 | -0.09836 | 3.876 |
| w5 | 13 | -0.133349 | -17.853 |
| w6 | 22 | -0.012545 | 0.922 |
| w7 | 9 | 0.007659 | -13.833 |
| w8 | 21 | -0.110861 | 4.998 |
| w9 | 15 | -0.015427 | -28.741 |
| w10 | 25 | 0.076375 | 82.559 |
| w11 | 23 | 0.202469 | 98.621 |
| w12 | 18 | -0.01588 | 8.536 |
| w13 | 12 | 0.167677 | 7.303 |
| w14 | 11 | 0.025672 | -5.337 |
| w15 | 14 | -0.01251 | 28.893 |
| w16 | 18 | -0.06238 | 60.877 |
| w17 | 15 | -0.072625 | 8.587 |
| w18 | 8 | 0.023681 | 11.995 |
| w19 | 10 | 0.003144 | 8.709 |
| w20 | 14 | 0.003087 | -14.49 |
| w21 | 21 | -0.078083 | 14.564 |
| w22 | 4 | -0.111568 | -11.1 |
| w23 | 28 | -0.016935 | 9.47 |
| w24 | 4 | -0.07337 | -21.423 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.031985 | -18.486 |
| w2 | 8 | 0.03754 | 3.355 |
| w3 | 16 | 0.099693 | 23.638 |
| w4 | 20 | -0.162082 | -8.356 |
| w5 | 14 | -0.052913 | -4.603 |
| w6 | 30 | -0.087259 | -18.975 |
| w7 | 7 | 0.045686 | -8.952 |
| w8 | 22 | 0.10972 | 52.185 |
| w9 | 6 | 0.036085 | -5.874 |
| w10 | 18 | -0.030239 | 28.292 |
| w11 | 19 | 0.03652 | 17.966 |
| w12 | 21 | 0.09011 | -7.56 |
| w13 | 11 | -0.012389 | -3.001 |
| w14 | 7 | -0.165989 | -27.864 |
| w15 | 18 | 0.113533 | 17.504 |
| w16 | 22 | -0.041024 | 20.86 |
| w17 | 15 | -0.016225 | 30.864 |
| w18 | 12 | 0.007045 | -12.584 |
| w19 | 19 | -0.097264 | 3.486 |
| w20 | 10 | -0.083999 | -22.458 |
| w21 | 24 | -0.121147 | 19.199 |
| w22 | 16 | -0.087805 | -16.962 |
| w23 | 17 | 0.053643 | 37.916 |
| w24 | 16 | -0.204397 | -34.437 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.080708 | -16.295 |
| w2 | 7 | -0.037598 | -1.972 |
| w3 | 23 | 0.011037 | -8.752 |
| w4 | 19 | -0.031399 | 8.528 |
| w5 | 12 | 0.071683 | 10.48 |
| w6 | 27 | 0.076738 | 7.785 |
| w7 | 7 | -0.034922 | -15.365 |
| w8 | 27 | -0.07321 | 20.571 |
| w9 | 9 | -0.088375 | -19.012 |
| w10 | 27 | -0.1664 | 33.896 |
| w11 | 18 | -0.110441 | 34.68 |
| w12 | 17 | 0.030864 | -8.307 |
| w13 | 8 | -0.038018 | -4.441 |
| w14 | 10 | -0.115039 | -22.019 |
| w15 | 13 | -0.033642 | 13.076 |
| w16 | 16 | 0.063751 | 22.21 |
| w17 | 27 | -0.204962 | 0.443 |
| w18 | 19 | -0.071567 | -23.385 |
| w19 | 7 | -0.063355 | -55.402 |
| w20 | 24 | -0.036054 | 8.01 |
| w21 | 23 | -0.017437 | 1.913 |
| w22 | 24 | -0.054004 | 22.451 |
| w23 | 16 | -0.01067 | -3.904 |
| w24 | 38 | -0.058468 | 15.749 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.051044 | -18.287 |
| w2 | 0 | -0.061408 | 0.0 |
| w3 | 13 | -0.008887 | 8.479 |
| w4 | 18 | -0.176459 | 18.987 |
| w5 | 9 | -0.125027 | -10.941 |
| w6 | 16 | 0.194327 | 8.136 |
| w7 | 3 | -0.027311 | -8.308 |
| w8 | 12 | -0.21166 | -12.971 |
| w9 | 11 | -0.075183 | -16.325 |
| w10 | 16 | -0.137982 | 27.365 |
| w11 | 16 | 0.041893 | 41.405 |
| w12 | 17 | 0.079369 | -15.416 |
| w13 | 5 | 0.168904 | 18.655 |
| w14 | 13 | 0.099008 | -2.042 |
| w15 | 10 | 0.265607 | 0.259 |
| w16 | 19 | 0.020556 | 0.214 |
| w17 | 15 | 0.002106 | 234.534 |
| w18 | 6 | 0.013307 | 24.325 |
| w19 | 14 | -0.073909 | 0.359 |
| w20 | 12 | 0.156875 | -16.018 |
| w21 | 16 | 0.238382 | 160.278 |
| w22 | 13 | -0.056123 | -11.107 |
| w23 | 17 | 0.055043 | 20.168 |
| w24 | 7 | -0.15331 | -21.51 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.051892 | 21.086 |
| w2 | 7 | 0.100979 | -2.657 |
| w3 | 10 | 0.086988 | -30.488 |
| w4 | 22 | -0.044957 | -8.388 |
| w5 | 10 | 0.092027 | -9.976 |
| w6 | 19 | 0.138235 | 5.759 |
| w7 | 7 | 0.071707 | -1.846 |
| w8 | 18 | -0.013872 | 21.608 |
| w9 | 9 | -0.00783 | -17.237 |
| w10 | 20 | -0.138001 | 0.392 |
| w11 | 19 | -0.014934 | 44.334 |
| w12 | 14 | 0.171437 | 25.567 |
| w13 | 14 | 0.005357 | 1.64 |
| w14 | 5 | -0.024904 | -10.328 |
| w15 | 15 | -0.084967 | 28.066 |
| w16 | 20 | 0.221796 | 62.18 |
| w17 | 15 | -0.005312 | 1.956 |
| w18 | 15 | -0.090266 | -17.533 |
| w19 | 11 | 0.039277 | 8.796 |
| w20 | 16 | 0.072405 | 32.283 |
| w21 | 17 | 0.106248 | 63.261 |
| w22 | 10 | 0.03104 | -22.825 |
| w23 | 21 | 0.139196 | 23.286 |
| w24 | 22 | 0.075484 | 148.402 |

- ADAUSD: 20 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.049724 | -32.631 |
| w2 | 13 | -0.047929 | -12.544 |
| w3 | 7 | -0.052173 | -22.17 |
| w4 | 24 | 0.078619 | 27.071 |
| w5 | 7 | -0.173934 | -15.122 |
| w6 | 18 | -0.128767 | 66.045 |
| w9 | 9 | -0.026311 | -13.304 |
| w10 | 16 | -0.067827 | 36.297 |
| w11 | 28 | -0.021142 | 26.05 |
| w12 | 6 | -0.081076 | -15.258 |
| w15 | 19 | -0.018265 | -2.494 |
| w16 | 19 | 0.055106 | 63.5 |
| w17 | 19 | 0.072834 | 15.429 |
| w18 | 15 | 0.000431 | 32.698 |
| w19 | 11 | 0.081227 | -4.287 |
| w20 | 16 | 0.021687 | -13.16 |
| w21 | 25 | 0.08304 | 78.945 |
| w22 | 12 | -0.133297 | -10.931 |
| w23 | 19 | 0.125075 | 10.612 |
| w24 | 5 | 0.015604 | -9.265 |

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
AssertionError: warmup_prefetch: strategy not ready after 95 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 17 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.15554 | 8.696 |
| w2 | 10 | -0.073344 | -21.19 |
| w3 | 7 | -0.044427 | 87.757 |
| w4 | 19 | -0.055206 | 6.106 |
| w5 | 11 | -0.068089 | 1.163 |
| w6 | 14 | 0.10702 | 17.753 |
| w10 | 20 | 0.24956 | 36.882 |
| w11 | 14 | 0.040368 | 233.944 |
| w12 | 7 | -0.040396 | -1.663 |
| w17 | 11 | 0.152123 | 108.257 |
| w18 | 7 | 0.031465 | 22.556 |
| w19 | 15 | 0.161739 | 87.531 |
| w20 | 11 | 0.037471 | -14.743 |
| w21 | 20 | -0.022329 | 91.079 |
| w22 | 8 | 0.025817 | -2.869 |
| w23 | 22 | 0.077495 | 32.384 |
| w24 | 6 | 0.04416 | 0.845 |

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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 13 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- LINKUSD: 17 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.005357 | -15.607 |
| w2 | 19 | 0.089417 | 3.522 |
| w3 | 17 | -0.045017 | -29.202 |
| w4 | 29 | 0.012409 | -11.435 |
| w5 | 13 | 0.079702 | 11.758 |
| w6 | 22 | -0.039048 | 42.506 |
| w10 | 29 | -0.063027 | 92.94 |
| w11 | 22 | 0.035627 | 47.104 |
| w12 | 18 | -0.00779 | 0.285 |
| w17 | 19 | -0.031091 | 0.801 |
| w18 | 12 | -0.036085 | -0.448 |
| w19 | 15 | 0.026798 | 1.318 |
| w20 | 8 | -0.023525 | -4.131 |
| w21 | 19 | -0.138216 | 50.511 |
| w22 | 10 | -0.040993 | -13.814 |
| w23 | 15 | -0.027424 | 42.04 |
| w24 | 1 | -0.067149 | -3.594 |

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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 98 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- TRXUSD: 16 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.029351 | -2.974 |
| w2 | 18 | -0.071393 | 4.705 |
| w3 | 15 | -0.088435 | -34.091 |
| w4 | 31 | -0.154851 | 5.447 |
| w5 | 24 | 0.008371 | -6.528 |
| w6 | 28 | -0.016851 | 34.855 |
| w11 | 22 | 0.026277 | 77.645 |
| w12 | 19 | 0.040753 | 2.068 |
| w17 | 9 | 0.094348 | -3.0 |
| w18 | 6 | -0.059106 | 13.088 |
| w19 | 15 | 0.076118 | 4.488 |
| w20 | 18 | 0.119325 | 23.685 |
| w21 | 24 | 0.298744 | 133.682 |
| w22 | 24 | -0.117167 | -18.701 |
| w23 | 31 | -0.026869 | 26.331 |
| w24 | 8 | -0.107375 | -15.236 |

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
AssertionError: warmup_prefetch: strategy not ready after 57 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- UNIUSD: 14 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.079887 | -18.414 |
| w2 | 10 | 0.093184 | -0.822 |
| w3 | 19 | -0.048987 | -37.679 |
| w4 | 21 | 0.088089 | -22.468 |
| w5 | 17 | 0.060271 | -11.535 |
| w6 | 24 | -0.006769 | 22.747 |
| w12 | 15 | -0.048406 | -24.78 |
| w18 | 14 | -0.040114 | -26.59 |
| w19 | 11 | 0.05646 | 18.204 |
| w20 | 7 | 0.04117 | 0.467 |
| w21 | 22 | -0.057002 | 40.615 |
| w22 | 2 | -0.111044 | -6.671 |
| w23 | 28 | 0.008586 | 12.643 |
| w24 | 8 | 0.085273 | -4.642 |

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
AssertionError: warmup_prefetch: strategy not ready after 78 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- AAVEUSD: 14 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.018417 | 7.987 |
| w2 | 10 | -0.038988 | -1.505 |
| w3 | 15 | 0.13612 | -20.239 |
| w4 | 22 | -0.088659 | 11.223 |
| w5 | 9 | 0.031315 | 0.311 |
| w6 | 27 | 0.04751 | 0.101 |
| w12 | 15 | -0.116154 | -25.499 |
| w18 | 18 | -0.190489 | -20.816 |
| w19 | 13 | 0.06375 | -11.05 |
| w20 | 23 | 0.020387 | 25.796 |
| w21 | 22 | -0.012244 | 66.779 |
| w22 | 8 | 0.013716 | -5.61 |
| w23 | 21 | -0.008076 | 26.676 |
| w24 | 5 | -0.106411 | -4.327 |

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
AssertionError: warmup_prefetch: strategy not ready after 17 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- AVAXUSD: 11 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 17 | 0.133718 | 11.618 |
| w3 | 10 | -0.042881 | -22.041 |
| w4 | 23 | -0.060936 | 32.61 |
| w5 | 6 | -0.004008 | 0.09 |
| w6 | 21 | 0.127882 | 143.968 |
| w19 | 12 | 0.061492 | 25.731 |
| w20 | 14 | 0.066135 | -15.807 |
| w21 | 24 | 0.068445 | 21.197 |
| w22 | 8 | 0.005426 | -11.093 |
| w23 | 25 | 0.036843 | 7.183 |
| w24 | 7 | 0.107246 | 11.414 |

- w1 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 11 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
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

- SOLUSD: 12 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.043447 | 7.437 |
| w2 | 14 | -0.009044 | -15.694 |
| w3 | 9 | -0.100178 | -63.235 |
| w4 | 15 | -0.123203 | -4.207 |
| w5 | 7 | 0.0703 | 14.869 |
| w6 | 25 | 0.164891 | 202.959 |
| w19 | 13 | 0.057867 | 35.352 |
| w20 | 17 | 0.056569 | -11.224 |
| w21 | 20 | 0.079723 | 24.283 |
| w22 | 10 | 0.109298 | 10.933 |
| w23 | 29 | 0.031098 | 23.566 |
| w24 | 12 | 0.074027 | 7.166 |

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
AssertionError: warmup_prefetch: strategy not ready after 76 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- INJUSD: 12 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.134652 | -22.098 |
| w2 | 11 | 0.012324 | -0.246 |
| w3 | 15 | -0.031916 | 17.509 |
| w4 | 24 | -0.014092 | 126.784 |
| w5 | 16 | 0.133435 | -10.159 |
| w6 | 26 | -0.091881 | 57.612 |
| w19 | 13 | -0.08196 | -23.381 |
| w20 | 16 | 0.002419 | -36.939 |
| w21 | 19 | 0.118129 | -2.119 |
| w22 | 7 | -0.102987 | -8.854 |
| w23 | 27 | -0.041619 | -13.446 |
| w24 | 6 | 0.017385 | -4.836 |

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
AssertionError: warmup_prefetch: strategy not ready after 22 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- NEARUSD: 9 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w4 | 12 | -0.17001 | -10.439 |
| w5 | 8 | -0.044522 | -18.288 |
| w6 | 14 | 0.142901 | 236.184 |
| w19 | 10 | -0.082306 | 64.807 |
| w20 | 12 | -0.075732 | -14.076 |
| w21 | 13 | 0.028672 | 2.264 |
| w22 | 8 | -0.057884 | -16.2 |
| w23 | 21 | 0.10703 | -10.156 |
| w24 | 16 | -0.046444 | -32.195 |

- w1 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for NEARUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w2 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w3 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 77 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w7 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for NEARUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w8 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for NEARUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w9 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for NEARUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w10 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for NEARUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w11 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for NEARUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w12 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for NEARUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w13 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for NEARUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w14 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for NEARUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w15 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for NEARUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w16 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for NEARUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w17 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for NEARUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w18 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for NEARUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- SUIUSD: 7 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 19 | -0.111794 | 25.29 |
| w19 | 21 | -0.027442 | -3.981 |
| w20 | 10 | -0.081417 | -17.15 |
| w21 | 20 | 0.009909 | 33.687 |
| w22 | 10 | 0.109976 | -4.508 |
| w23 | 16 | 0.105766 | -0.935 |
| w24 | 8 | -0.080738 | -24.937 |

- w1 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w2 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w3 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w4 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w5 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w7 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w8 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w9 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w10 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w11 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w12 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w13 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w14 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w15 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w16 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w17 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w18 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for SUIUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- TAOUSD: 3 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 12 | 0.045738 | -5.659 |
| w23 | 17 | -0.050261 | -8.616 |
| w24 | 12 | 0.077478 | -13.927 |

- w1 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w2 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w3 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w4 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w5 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w6 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w7 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w8 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w9 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w10 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w11 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w12 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w13 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w14 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w15 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w16 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w17 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w18 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w19 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w20 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w21 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 62 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ONDOUSD: 4 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 14 | -0.00182 | 39.152 |
| w22 | 10 | -0.041585 | -7.71 |
| w23 | 19 | 0.023963 | 1.394 |
| w24 | 7 | 0.131812 | -5.146 |

- w1 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w2 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w3 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w4 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w5 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w6 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w7 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w8 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w9 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w10 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w11 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w12 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w13 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w14 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w15 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w16 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w17 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w18 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ONDOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w19 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w20 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 20 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

