# Backtest of 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues_1d

- Plan: `../../../../03_test_plan/night3_learned_run/plans/022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.015788 | -20.285 |
| w2 | 25 | -0.005203 | 53.559 |
| w3 | 31 | -0.149461 | -0.96 |
| w4 | 35 | -0.076341 | -24.805 |
| w5 | 37 | -0.124542 | -44.991 |
| w6 | 30 | 0.046263 | 2.686 |
| w7 | 21 | -0.077183 | -13.511 |
| w8 | 17 | 0.113369 | 56.099 |
| w9 | 27 | -0.154893 | -3.268 |
| w10 | 20 | -0.10879 | 10.097 |
| w11 | 21 | 0.019135 | 30.405 |
| w12 | 29 | -0.078971 | -27.801 |
| w13 | 17 | -0.069139 | -14.208 |
| w14 | 25 | -0.030144 | 82.859 |
| w15 | 23 | 0.128434 | 81.241 |
| w16 | 28 | -0.137758 | -50.876 |
| w17 | 20 | 0.03428 | 27.167 |
| w18 | 25 | 0.007666 | -13.015 |
| w19 | 18 | 0.04835 | 40.671 |
| w20 | 17 | -0.117157 | 15.925 |
| w21 | 20 | 0.03622 | 51.865 |
| w22 | 23 | -0.071878 | -7.149 |
| w23 | 29 | -0.097722 | -5.764 |
| w24 | 26 | -0.007068 | 35.354 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.028572 | -11.733 |
| w2 | 23 | 0.009589 | 27.046 |
| w3 | 17 | -0.104858 | -21.052 |
| w4 | 36 | -0.101585 | -30.736 |
| w5 | 23 | -0.109816 | -35.118 |
| w6 | 34 | 0.027804 | 13.848 |
| w7 | 34 | -0.039204 | 5.072 |
| w8 | 19 | 0.105609 | 29.34 |
| w9 | 25 | -0.003256 | -7.371 |
| w10 | 26 | 0.05808 | 72.694 |
| w11 | 19 | 0.037162 | 87.804 |
| w12 | 25 | -0.15368 | -27.049 |
| w13 | 25 | 0.001968 | 0.744 |
| w14 | 21 | -0.096491 | 17.637 |
| w15 | 24 | 0.145936 | 54.653 |
| w16 | 21 | -0.120007 | -36.103 |
| w17 | 27 | -0.024755 | -14.286 |
| w18 | 28 | -0.039128 | -34.016 |
| w19 | 27 | -0.01063 | 22.79 |
| w20 | 27 | 0.032831 | -51.259 |
| w21 | 20 | 0.034665 | -10.21 |
| w22 | 22 | -0.014418 | 16.014 |
| w23 | 32 | -0.26635 | 9.32 |
| w24 | 25 | -0.004627 | 3.982 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | -0.064434 | -6.959 |
| w2 | 15 | 0.011476 | 28.607 |
| w3 | 32 | -0.135815 | -54.289 |
| w4 | 20 | -0.068494 | 5.586 |
| w5 | 15 | -0.075618 | -35.619 |
| w6 | 21 | -0.06885 | -10.36 |
| w7 | 22 | -0.056019 | 39.683 |
| w8 | 20 | 0.036763 | 28.517 |
| w9 | 25 | -0.120121 | 9.653 |
| w10 | 14 | 0.043327 | 35.139 |
| w11 | 20 | -0.009154 | 26.151 |
| w12 | 16 | -0.122682 | -26.918 |
| w13 | 15 | -0.10661 | -20.954 |
| w14 | 26 | -0.063702 | 28.067 |
| w15 | 20 | 0.060826 | 12.49 |
| w16 | 21 | -0.111602 | -40.88 |
| w17 | 24 | 0.015725 | -25.231 |
| w18 | 27 | -0.033533 | -26.735 |
| w19 | 16 | -0.033839 | -42.863 |
| w20 | 35 | -0.077285 | 6.331 |
| w21 | 23 | 0.029528 | 49.806 |
| w22 | 26 | -0.041359 | -5.552 |
| w23 | 16 | -0.125053 | 1.155 |
| w24 | 24 | -0.056742 | 0.623 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | -0.02572 | -16.092 |
| w2 | 25 | -0.074048 | -9.927 |
| w3 | 31 | -0.132777 | -20.02 |
| w4 | 27 | -0.073119 | -37.763 |
| w5 | 34 | -0.110693 | -38.637 |
| w6 | 37 | -0.070651 | -22.68 |
| w7 | 20 | -0.128755 | 12.574 |
| w8 | 14 | 0.057377 | 27.594 |
| w9 | 18 | -0.089239 | 29.218 |
| w10 | 25 | 0.021757 | 45.216 |
| w11 | 28 | -0.15054 | 70.856 |
| w12 | 28 | -0.128139 | -15.452 |
| w13 | 17 | -0.077386 | -15.808 |
| w14 | 21 | 0.007211 | -5.72 |
| w15 | 28 | 0.062759 | 23.894 |
| w16 | 22 | -0.137418 | -53.473 |
| w17 | 21 | -0.367464 | 10.292 |
| w18 | 22 | -0.083456 | -39.806 |
| w19 | 22 | -0.191604 | 0.641 |
| w20 | 28 | -0.083374 | -43.251 |
| w21 | 24 | 0.014169 | -60.845 |
| w22 | 21 | 0.056728 | -32.428 |
| w23 | 23 | 0.054322 | 21.257 |
| w24 | 29 | -0.097687 | 12.731 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.000179 | 7.282 |
| w2 | 18 | 0.020205 | 41.411 |
| w3 | 23 | -0.053466 | 26.712 |
| w4 | 17 | -0.204859 | 13.464 |
| w5 | 19 | 0.039316 | 73.28 |
| w6 | 29 | -0.083936 | -29.268 |
| w7 | 25 | -0.035537 | 23.633 |
| w8 | 20 | -0.064023 | 2.151 |
| w9 | 29 | -0.014095 | -14.063 |
| w10 | 24 | 0.046167 | -31.66 |
| w11 | 22 | -0.083086 | 38.491 |
| w12 | 23 | -0.091739 | -32.186 |
| w13 | 13 | -0.186807 | -24.423 |
| w14 | 22 | -0.080792 | -40.031 |
| w15 | 29 | 0.013862 | -27.958 |
| w16 | 29 | -0.165455 | -50.501 |
| w17 | 33 | 0.040262 | 16.606 |
| w18 | 22 | -0.095066 | -25.733 |
| w19 | 23 | -0.191904 | -34.291 |
| w20 | 26 | -0.081192 | -43.614 |
| w21 | 22 | 0.19286 | -33.597 |
| w22 | 23 | 0.022174 | 10.088 |
| w23 | 22 | -0.044216 | 23.049 |
| w24 | 32 | -0.03311 | 19.424 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | -0.085635 | -37.483 |
| w2 | 17 | -0.079579 | -4.242 |
| w3 | 24 | -0.075328 | 3.496 |
| w4 | 27 | -0.151116 | -44.054 |
| w5 | 22 | -0.128756 | 9.506 |
| w6 | 33 | -0.103638 | -27.276 |
| w7 | 19 | -0.137629 | -14.305 |
| w8 | 23 | 0.065301 | 12.039 |
| w9 | 21 | -0.129561 | 13.418 |
| w10 | 25 | -0.038211 | 26.809 |
| w11 | 28 | -0.015069 | 95.287 |
| w12 | 28 | -0.092607 | -26.26 |
| w13 | 20 | -0.02571 | -14.741 |
| w14 | 24 | -0.123802 | 31.663 |
| w15 | 22 | 0.083953 | 38.038 |
| w16 | 21 | -0.091267 | -53.267 |
| w17 | 19 | -0.120679 | -38.95 |
| w18 | 23 | -0.0574 | -27.903 |
| w19 | 36 | -0.123508 | -26.749 |
| w20 | 26 | -0.028787 | -38.835 |
| w21 | 35 | -0.000746 | 24.952 |
| w22 | 22 | -0.100409 | -11.584 |
| w23 | 30 | -0.016176 | -14.764 |
| w24 | 14 | 0.138158 | 537.072 |

- ADAUSD: 21 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.105186 | 1.474 |
| w2 | 21 | -0.06665 | 11.512 |
| w3 | 36 | -0.050138 | 43.037 |
| w4 | 25 | -0.246507 | -42.605 |
| w5 | 30 | -0.052746 | -46.043 |
| w6 | 31 | 0.139368 | 27.772 |
| w8 | 20 | 0.01809 | 58.764 |
| w9 | 21 | -0.062273 | 1.546 |
| w10 | 18 | 0.058348 | 69.056 |
| w11 | 14 | 0.144558 | 168.478 |
| w12 | 24 | -0.063603 | -7.535 |
| w15 | 18 | 0.016141 | 8.891 |
| w16 | 21 | -0.127772 | -62.823 |
| w17 | 29 | 0.043866 | -22.108 |
| w18 | 15 | 0.015637 | -49.626 |
| w19 | 23 | -0.135668 | -36.138 |
| w20 | 29 | -0.09782 | -6.123 |
| w21 | 30 | 0.133446 | -23.119 |
| w22 | 19 | -0.044747 | -9.857 |
| w23 | 31 | -0.137453 | -50.017 |
| w24 | 24 | 0.04839 | 31.386 |

- w7 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for ADAUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 17 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.091112 | -16.537 |
| w2 | 19 | -0.059452 | -18.65 |
| w3 | 30 | -0.005847 | -65.238 |
| w4 | 24 | -0.237684 | -25.491 |
| w5 | 33 | -0.100345 | -16.081 |
| w6 | 25 | 0.046849 | 3.512 |
| w10 | 25 | -0.240683 | -17.74 |
| w11 | 24 | -0.06015 | 131.528 |
| w12 | 23 | -0.132127 | 9.953 |
| w17 | 20 | 0.081835 | 21.78 |
| w18 | 10 | -0.056223 | -15.033 |
| w19 | 22 | 0.034532 | -34.588 |
| w20 | 27 | -0.014175 | 1.298 |
| w21 | 21 | 0.120243 | 131.171 |
| w22 | 16 | -0.023679 | 8.712 |
| w23 | 26 | -0.188428 | -37.685 |
| w24 | 20 | 0.063683 | 19.954 |

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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 13 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- LINKUSD: 18 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.137474 | -3.619 |
| w2 | 27 | -0.0377 | 21.157 |
| w3 | 18 | -0.062264 | -2.651 |
| w4 | 16 | -0.121828 | -34.038 |
| w5 | 33 | -0.105756 | -22.62 |
| w6 | 24 | 0.037465 | -14.216 |
| w10 | 26 | 0.034212 | 125.803 |
| w11 | 16 | -0.088897 | 67.814 |
| w12 | 21 | -0.093521 | -43.276 |
| w16 | 20 | -0.095946 | -30.403 |
| w17 | 15 | -0.140299 | -33.32 |
| w18 | 31 | -0.091022 | -33.844 |
| w19 | 18 | -0.006048 | -9.486 |
| w20 | 22 | -0.027155 | 1.164 |
| w21 | 21 | 0.078954 | 70.852 |
| w22 | 20 | -0.000557 | 9.856 |
| w23 | 23 | -0.070903 | -0.574 |
| w24 | 27 | -0.001276 | 2.566 |

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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
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

- TRXUSD: 16 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | 0.04055 | -2.713 |
| w2 | 26 | -0.098703 | -11.561 |
| w3 | 27 | -0.230195 | 5.282 |
| w4 | 23 | -0.072029 | -18.887 |
| w5 | 26 | -0.047771 | -4.831 |
| w6 | 23 | -0.082177 | 0.816 |
| w11 | 31 | -0.04388 | 161.356 |
| w12 | 15 | -0.009352 | -9.455 |
| w17 | 19 | -0.155145 | -35.472 |
| w18 | 19 | -0.050564 | -19.482 |
| w19 | 20 | -0.049773 | -0.039 |
| w20 | 33 | -0.013342 | 33.499 |
| w21 | 26 | 0.044013 | 165.457 |
| w22 | 17 | -0.134856 | -9.732 |
| w23 | 32 | -0.158197 | 53.363 |
| w24 | 25 | -0.00854 | 11.257 |

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
AssertionError: warmup_prefetch: strategy not ready after 57 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- UNIUSD: 14 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | -0.044804 | 19.397 |
| w2 | 30 | -0.010507 | -0.424 |
| w3 | 27 | -0.167512 | -6.771 |
| w4 | 29 | -0.062186 | -24.063 |
| w5 | 33 | -0.076926 | -19.741 |
| w6 | 27 | 0.029569 | 6.188 |
| w12 | 23 | -0.101567 | 1.128 |
| w18 | 28 | -0.039677 | -17.282 |
| w19 | 18 | -0.063807 | 13.082 |
| w20 | 21 | -0.047015 | -18.791 |
| w21 | 20 | -0.043707 | 31.931 |
| w22 | 17 | -0.024615 | 8.4 |
| w23 | 20 | -0.111714 | -0.988 |
| w24 | 26 | -0.124402 | -15.43 |

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
AssertionError: warmup_prefetch: strategy not ready after 78 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- AAVEUSD: 14 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.026736 | -20.781 |
| w2 | 24 | -0.086958 | -9.407 |
| w3 | 21 | -0.042392 | 7.66 |
| w4 | 26 | -0.086967 | -41.497 |
| w5 | 26 | -0.106944 | -20.603 |
| w6 | 32 | -0.012459 | -24.413 |
| w12 | 26 | -0.152531 | -12.21 |
| w18 | 33 | -0.113651 | -49.865 |
| w19 | 19 | -0.137814 | -38.127 |
| w20 | 25 | 0.004464 | -32.751 |
| w21 | 21 | 0.019343 | 85.354 |
| w22 | 15 | -0.004323 | 5.981 |
| w23 | 23 | -0.127347 | -10.508 |
| w24 | 19 | -0.040209 | 24.78 |

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
AssertionError: warmup_prefetch: strategy not ready after 17 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- AVAXUSD: 11 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 22 | 0.036452 | 31.231 |
| w3 | 24 | -0.077017 | 9.634 |
| w4 | 22 | -0.142012 | -49.385 |
| w5 | 31 | -0.120323 | 29.874 |
| w6 | 31 | 0.212746 | 161.66 |
| w19 | 13 | -0.090516 | -30.273 |
| w20 | 31 | -0.079288 | 9.005 |
| w21 | 29 | -0.032378 | 30.881 |
| w22 | 19 | 0.006033 | 3.143 |
| w23 | 31 | -0.133923 | -31.278 |
| w24 | 22 | 0.053631 | 17.752 |

- w1 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 11 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
| w1 | 21 | 0.024193 | -1.661 |
| w2 | 21 | -0.026781 | 15.267 |
| w3 | 28 | -0.011157 | 47.265 |
| w4 | 22 | -0.192122 | -36.731 |
| w5 | 23 | -0.128559 | -44.81 |
| w6 | 24 | 0.098219 | 18.137 |
| w19 | 18 | -0.036758 | 8.115 |
| w20 | 14 | -0.171637 | -0.327 |
| w21 | 30 | -0.036184 | -7.068 |
| w22 | 21 | -0.046318 | 24.098 |
| w23 | 23 | -0.085996 | 1.93 |
| w24 | 24 | 0.055733 | 14.585 |

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
AssertionError: warmup_prefetch: strategy not ready after 76 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- INJUSD: 12 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | 0.001016 | -5.415 |
| w2 | 19 | -0.004968 | 15.995 |
| w3 | 18 | -0.041 | -2.419 |
| w4 | 28 | -0.071137 | -41.99 |
| w5 | 14 | -0.183929 | -27.643 |
| w6 | 26 | 0.150392 | 24.11 |
| w19 | 10 | -0.012007 | -14.046 |
| w20 | 38 | -0.077124 | -12.765 |
| w21 | 19 | -0.078732 | -9.032 |
| w22 | 25 | 0.06889 | 31.111 |
| w23 | 20 | -0.22143 | -23.697 |
| w24 | 23 | 0.043762 | 21.963 |

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
AssertionError: warmup_prefetch: strategy not ready after 22 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=81. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

