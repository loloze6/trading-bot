# Backtest of 032-03.b1_thin-volume-decline-more-coins_1d

- Plan: `../../../../03_test_plan/night7c_steadydecline_run/plans/032-03.b1_thin-volume-decline-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.094886 | 23.451 |
| w2 | 10 | 0.154022 | 37.345 |
| w3 | 13 | 0.025587 | -3.825 |
| w4 | 10 | -0.041846 | -38.42 |
| w5 | 19 | 0.077124 | 12.931 |
| w6 | 6 | 0.028903 | -8.293 |
| w7 | 7 | 0.047814 | 4.564 |
| w8 | 7 | -0.003559 | -6.475 |
| w9 | 13 | 0.038211 | 17.244 |
| w10 | 10 | 0.016886 | -6.845 |
| w11 | 7 | -0.007248 | -6.632 |
| w12 | 7 | -0.044028 | -7.316 |
| w13 | 8 | 0.060597 | 10.222 |
| w14 | 17 | 0.036791 | 49.453 |
| w15 | 6 | -0.040909 | -1.417 |
| w16 | 7 | 0.25934 | 27.803 |
| w17 | 3 | 0.235795 | 5.268 |
| w18 | 12 | 0.001887 | 0.486 |
| w19 | 13 | 0.067094 | -5.119 |
| w20 | 16 | -0.034193 | -7.271 |
| w21 | 2 | -0.051455 | -5.448 |
| w22 | 29 | -0.015958 | 0.736 |
| w23 | 14 | -0.112353 | -24.73 |
| w24 | 2 | 0.020087 | 0.127 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.1473 | 20.43 |
| w2 | 7 | 0.147061 | 39.978 |
| w3 | 15 | 0.014944 | -4.117 |
| w4 | 12 | -0.061454 | -14.223 |
| w5 | 28 | -0.069829 | 13.366 |
| w6 | 10 | 0.034971 | -4.206 |
| w7 | 27 | 0.120127 | 49.544 |
| w8 | 9 | -0.085645 | -7.819 |
| w9 | 19 | -0.138238 | -16.223 |
| w10 | 7 | -0.060386 | -31.76 |
| w11 | 9 | 0.057168 | -6.417 |
| w12 | 13 | -0.246929 | -15.729 |
| w13 | 4 | 0.116219 | 5.115 |
| w14 | 6 | 0.105933 | 19.524 |
| w15 | 17 | 0.102922 | 5.45 |
| w16 | 4 | -0.025637 | -8.321 |
| w17 | 4 | -0.026445 | -0.625 |
| w18 | 6 | 0.018741 | -9.317 |
| w19 | 14 | 0.04892 | -8.997 |
| w20 | 20 | -0.09516 | -23.374 |
| w21 | 13 | -0.030767 | -17.668 |
| w22 | 16 | 0.053396 | 9.281 |
| w23 | 3 | -0.170643 | -4.102 |
| w24 | 23 | 0.074583 | 13.259 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | 0.069685 | 25.389 |
| w2 | 15 | 0.062413 | 12.088 |
| w3 | 29 | -0.161691 | -30.124 |
| w4 | 14 | 0.11753 | 13.984 |
| w5 | 15 | 0.102686 | 19.547 |
| w6 | 12 | -0.132562 | -18.98 |
| w7 | 11 | 0.098889 | 58.579 |
| w8 | 3 | -0.323676 | -5.416 |
| w9 | 14 | -0.109313 | 7.668 |
| w10 | 21 | -0.102836 | -9.92 |
| w11 | 5 | -0.16184 | -12.512 |
| w12 | 2 | -0.021546 | -0.079 |
| w13 | 16 | 0.080866 | 1.149 |
| w14 | 10 | 0.104415 | 28.083 |
| w15 | 10 | 0.026333 | 2.234 |
| w16 | 3 | -0.063454 | -9.619 |
| w17 | 4 | -0.01037 | -6.984 |
| w18 | 10 | -0.048345 | -11.662 |
| w19 | 8 | -0.034955 | -1.294 |
| w20 | 29 | -0.090241 | 8.076 |
| w21 | 10 | -0.057129 | -12.342 |
| w22 | 13 | -0.108241 | -7.435 |
| w23 | 14 | 0.003492 | -4.516 |
| w24 | 13 | -0.0237 | -1.466 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.135446 | -28.159 |
| w2 | 10 | 0.043184 | -0.531 |
| w3 | 18 | 0.080172 | 4.223 |
| w4 | 14 | 0.028342 | -0.138 |
| w5 | 27 | 0.036994 | 11.749 |
| w6 | 5 | -0.039874 | -3.147 |
| w7 | 14 | 0.120659 | 34.607 |
| w8 | 9 | -0.024238 | -5.557 |
| w9 | 16 | -0.067903 | 2.639 |
| w10 | 10 | -0.094857 | -13.116 |
| w11 | 6 | 0.109816 | 0.298 |
| w12 | 2 | -0.009895 | 0.772 |
| w13 | 7 | -0.148974 | -17.661 |
| w14 | 13 | 0.053217 | 43.335 |
| w15 | 9 | -0.020214 | 8.309 |
| w16 | 0 | -0.078144 | 0.0 |
| w17 | 2 | -0.125684 | -6.23 |
| w18 | 6 | -0.010106 | -3.435 |
| w19 | 3 | -0.076096 | 0.359 |
| w20 | 17 | -0.004279 | -7.578 |
| w21 | 15 | 0.011524 | -10.139 |
| w22 | 16 | -0.048477 | -16.086 |
| w23 | 10 | 0.036461 | 9.157 |
| w24 | 0 | None | 0.0 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.039184 | 21.34 |
| w2 | 8 | 0.100587 | 27.19 |
| w3 | 3 | 0.003739 | 4.624 |
| w4 | 20 | 0.016003 | -12.565 |
| w5 | 9 | -0.177667 | -65.79 |
| w6 | 12 | -0.080242 | -14.365 |
| w7 | 11 | 0.036726 | 21.559 |
| w8 | 13 | -0.080297 | -7.82 |
| w9 | 12 | -0.045299 | -3.895 |
| w10 | 8 | -0.021881 | -16.253 |
| w11 | 5 | 0.010159 | -5.707 |
| w12 | 8 | 0.094009 | 2.262 |
| w13 | 7 | -0.031875 | -14.675 |
| w14 | 8 | -0.120787 | 1.599 |
| w15 | 14 | 0.001394 | -10.263 |
| w16 | 5 | -0.060901 | -11.698 |
| w17 | 12 | -0.035701 | -14.173 |
| w18 | 8 | 0.019424 | -2.036 |
| w19 | 11 | -0.07716 | -6.408 |
| w20 | 20 | 0.043358 | 3.253 |
| w21 | 13 | 0.102195 | -7.884 |
| w22 | 12 | -0.053259 | -4.413 |
| w23 | 12 | 0.013038 | -15.398 |
| w24 | 24 | 0.053211 | 19.364 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.103903 | -25.507 |
| w2 | 14 | -0.067054 | -3.147 |
| w3 | 10 | 0.009824 | 10.481 |
| w4 | 7 | -0.154479 | -12.888 |
| w5 | 16 | 0.164598 | 53.386 |
| w6 | 10 | -0.066256 | -20.858 |
| w7 | 9 | -0.091809 | -7.599 |
| w8 | 19 | -0.09164 | -16.795 |
| w9 | 11 | -0.073387 | -0.917 |
| w10 | 8 | -0.056339 | -18.894 |
| w11 | 4 | -0.075661 | -7.685 |
| w12 | 4 | -0.072292 | -7.551 |
| w13 | 16 | 0.04257 | 0.938 |
| w14 | 16 | -0.096006 | -4.369 |
| w15 | 9 | 0.123689 | 24.656 |
| w16 | 3 | 0.240372 | 8.933 |
| w17 | 3 | -0.031174 | -4.561 |
| w18 | 13 | -0.052168 | -10.066 |
| w19 | 4 | -0.03051 | -0.645 |
| w20 | 7 | 0.107958 | 6.823 |
| w21 | 8 | -0.003561 | -14.871 |
| w22 | 13 | -0.074331 | -10.614 |
| w23 | 19 | -0.022413 | -12.508 |
| w24 | 3 | -0.015494 | -1.372 |

- ADAUSD: 20 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.06082 | 13.028 |
| w2 | 16 | -0.040188 | 3.385 |
| w3 | 17 | 0.031252 | 17.468 |
| w4 | 9 | -0.076298 | -15.006 |
| w5 | 14 | 0.09474 | 47.099 |
| w6 | 9 | 0.112438 | -17.177 |
| w9 | 12 | -0.114665 | -10.825 |
| w10 | 2 | 0.016896 | -0.45 |
| w11 | 3 | 0.008634 | -5.315 |
| w12 | 15 | -0.044782 | 12.08 |
| w15 | 7 | 0.015776 | 7.858 |
| w16 | 4 | -0.04426 | -7.031 |
| w17 | 16 | 0.008957 | -20.102 |
| w18 | 7 | 0.062192 | -8.757 |
| w19 | 9 | -0.020489 | 1.47 |
| w20 | 27 | -0.028335 | 15.267 |
| w21 | 14 | -0.008989 | -30.377 |
| w22 | 9 | -0.191944 | -16.953 |
| w23 | 13 | 0.068191 | 6.737 |
| w24 | 18 | 0.104608 | 34.105 |

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
AssertionError: warmup_prefetch: strategy not ready after 95 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 16 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.042007 | -5.197 |
| w2 | 20 | 0.027881 | 1.957 |
| w3 | 12 | 0.005434 | -6.724 |
| w4 | 5 | -0.090155 | -6.31 |
| w5 | 15 | 0.017427 | 10.504 |
| w6 | 15 | 0.071544 | -4.188 |
| w11 | 9 | 0.035895 | -1.875 |
| w12 | 14 | 0.030826 | 9.361 |
| w17 | 14 | 0.125606 | -0.046 |
| w18 | 9 | 0.013481 | -10.711 |
| w19 | 11 | -0.045284 | -5.112 |
| w20 | 17 | -0.025065 | -0.75 |
| w21 | 7 | 0.03253 | -3.402 |
| w22 | 13 | 0.012931 | 14.322 |
| w23 | 0 | None | 0.0 |
| w24 | 10 | 0.067534 | 40.317 |

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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w10 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 134 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 13 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- LINKUSD: 17 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.016165 | 15.993 |
| w2 | 13 | 0.138258 | 21.263 |
| w3 | 15 | -0.06984 | -11.52 |
| w4 | 12 | -0.09971 | -17.503 |
| w5 | 18 | 0.070045 | 23.284 |
| w6 | 5 | -0.122395 | -11.724 |
| w10 | 2 | -0.039393 | -3.041 |
| w11 | 11 | -0.011372 | -31.278 |
| w12 | 6 | 0.031022 | 4.45 |
| w17 | 6 | 0.030123 | 6.186 |
| w18 | 9 | -0.062422 | -18.184 |
| w19 | 16 | 0.107761 | 29.55 |
| w20 | 15 | 0.037836 | 10.552 |
| w21 | 12 | -0.034654 | -17.322 |
| w22 | 10 | -0.0917 | -6.325 |
| w23 | 0 | -0.024984 | 0.0 |
| w24 | 14 | -0.042973 | 4.606 |

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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 98 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- TRXUSD: 16 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.011077 | 3.601 |
| w2 | 9 | -0.012299 | 2.91 |
| w3 | 11 | -0.039278 | 0.241 |
| w4 | 5 | 0.201149 | -1.955 |
| w5 | 2 | -0.055244 | -0.227 |
| w6 | 0 | None | 0.0 |
| w11 | 2 | -0.036565 | -10.143 |
| w12 | 11 | 0.070215 | 11.28 |
| w17 | 16 | -0.086296 | -24.794 |
| w18 | 11 | -0.064904 | -17.778 |
| w19 | 13 | -0.001401 | -2.905 |
| w20 | 14 | 0.016636 | -14.591 |
| w21 | 6 | -0.003417 | -22.814 |
| w22 | 14 | -0.045206 | -6.846 |
| w23 | 8 | -0.051993 | -6.355 |
| w24 | 33 | 0.034253 | 9.993 |

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
AssertionError: warmup_prefetch: strategy not ready after 57 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- UNIUSD: 14 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.035202 | 23.84 |
| w2 | 8 | 0.098533 | 12.763 |
| w3 | 10 | -0.017213 | 3.44 |
| w4 | 10 | -0.062748 | -11.304 |
| w5 | 9 | 0.100241 | 27.797 |
| w6 | 14 | 0.045415 | -7.774 |
| w12 | 13 | -0.003369 | 4.9 |
| w18 | 20 | -0.161927 | -28.583 |
| w19 | 16 | 0.034447 | -13.006 |
| w20 | 20 | -0.030935 | -15.465 |
| w21 | 5 | -0.023074 | -13.461 |
| w22 | 11 | 0.084828 | 43.244 |
| w23 | 7 | -0.105506 | -20.146 |
| w24 | 15 | 0.028509 | 19.249 |

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
AssertionError: warmup_prefetch: strategy not ready after 78 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- AAVEUSD: 13 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.056711 | -6.309 |
| w2 | 8 | 0.119784 | 10.573 |
| w3 | 7 | -0.008954 | 10.214 |
| w4 | 16 | 0.026345 | -24.153 |
| w5 | 18 | 0.100294 | 23.109 |
| w6 | 8 | -0.004539 | -27.116 |
| w12 | 16 | -0.020857 | -2.407 |
| w19 | 11 | 0.016054 | 3.307 |
| w20 | 12 | -0.085798 | -20.211 |
| w21 | 8 | -0.042647 | -21.274 |
| w22 | 24 | 0.00925 | 12.048 |
| w23 | 9 | -0.096403 | -14.792 |
| w24 | 20 | 0.031237 | 26.587 |

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
AssertionError: warmup_prefetch: strategy not ready after 17 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w18 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 137 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- AVAXUSD: 10 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w3 | 16 | -0.104267 | 1.174 |
| w4 | 5 | -0.187056 | -13.008 |
| w5 | 22 | 0.174521 | 64.173 |
| w6 | 10 | 0.161031 | 2.473 |
| w19 | 8 | -0.046995 | -3.917 |
| w20 | 23 | -0.025264 | 8.069 |
| w21 | 6 | -0.01585 | -9.306 |
| w22 | 17 | 0.04402 | 15.593 |
| w23 | 9 | -0.062224 | -9.053 |
| w24 | 7 | 0.017868 | 7.408 |

- w1 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 11 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w2 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 131 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
| w1 | 6 | 0.249964 | 27.199 |
| w2 | 11 | 0.19813 | 39.957 |
| w3 | 14 | -0.078108 | -4.807 |
| w4 | 7 | 0.141913 | 3.634 |
| w5 | 14 | 0.135577 | 19.756 |
| w6 | 5 | 0.139963 | -1.379 |
| w19 | 9 | 0.037738 | -0.264 |
| w20 | 12 | -0.008064 | -11.736 |
| w21 | 7 | -0.00178 | -1.524 |
| w22 | 24 | -0.026551 | -6.927 |
| w23 | 8 | -0.016675 | -11.089 |
| w24 | 7 | 0.078386 | 2.914 |

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
AssertionError: warmup_prefetch: strategy not ready after 76 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- INJUSD: 11 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 24 | 0.185162 | 34.759 |
| w3 | 11 | 0.069171 | 12.789 |
| w4 | 2 | 0.003812 | -15.696 |
| w5 | 18 | -0.035232 | -0.826 |
| w6 | 9 | 0.115541 | -25.761 |
| w19 | 12 | 0.031693 | 7.511 |
| w20 | 16 | -0.084198 | -14.324 |
| w21 | 15 | -0.108559 | -14.265 |
| w22 | 23 | 0.066353 | 24.843 |
| w23 | 1 | -0.051399 | -0.039 |
| w24 | 22 | 0.052971 | 24.736 |

- w1 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 144 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 22 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
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
AssertionError: warmup_prefetch: strategy not ready after 0 warm-up bars -- required_bars=148. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

