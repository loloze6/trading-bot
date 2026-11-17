# Backtest of 010-05_rsi-above-share-reversal_1d

- Plan: `../../../../03_test_plan/night_rsi_run/plans/010-05_rsi-above-share-reversal_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | 0.06849 | 8.132 |
| w2 | 20 | -0.001517 | -30.876 |
| w3 | 20 | 0.113463 | 2.475 |
| w4 | 31 | 0.206125 | 9.808 |
| w5 | 39 | 0.042195 | 0.95 |
| w6 | 22 | -0.041937 | -35.412 |
| w7 | 31 | 0.097277 | 16.681 |
| w8 | 21 | -0.071427 | -32.812 |
| w9 | 28 | 0.075101 | -15.494 |
| w10 | 24 | 0.099965 | 7.642 |
| w11 | 9 | 0.171123 | -26.22 |
| w12 | 30 | 0.040295 | 9.663 |
| w13 | 32 | 0.135446 | 24.292 |
| w14 | 21 | 0.042129 | -56.499 |
| w15 | 9 | -0.085692 | -37.556 |
| w16 | 29 | 0.071728 | 25.806 |
| w17 | 33 | -0.058682 | -59.531 |
| w18 | 22 | 0.005035 | -2.641 |
| w19 | 28 | -0.049111 | -36.288 |
| w20 | 42 | 0.162801 | 54.756 |
| w21 | 27 | -0.068368 | -49.52 |
| w22 | 27 | -0.034248 | -11.856 |
| w23 | 21 | -0.01508 | -9.867 |
| w24 | 41 | 0.027836 | -16.603 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.031463 | -3.881 |
| w2 | 22 | -0.081519 | -44.804 |
| w3 | 27 | 0.130076 | 15.124 |
| w4 | 38 | 0.198035 | 18.62 |
| w5 | 38 | -0.03117 | -14.07 |
| w6 | 23 | -0.042337 | -18.216 |
| w7 | 21 | 0.019678 | -14.334 |
| w8 | 35 | 0.111261 | 6.803 |
| w9 | 28 | 0.111971 | 7.588 |
| w10 | 20 | 0.137203 | -35.444 |
| w11 | 14 | -0.035066 | -47.763 |
| w12 | 28 | 0.040033 | 9.932 |
| w13 | 25 | -0.086372 | -22.559 |
| w14 | 12 | 0.193137 | -12.189 |
| w15 | 15 | -0.097747 | -29.45 |
| w16 | 34 | 0.041009 | 2.648 |
| w17 | 29 | -0.030679 | -34.657 |
| w18 | 27 | -0.022973 | -17.453 |
| w19 | 26 | 0.039221 | -13.933 |
| w20 | 35 | 0.111859 | 12.493 |
| w21 | 23 | 0.030387 | -0.846 |
| w22 | 14 | -0.047098 | -36.262 |
| w23 | 25 | 0.146224 | -23.886 |
| w24 | 20 | -0.01477 | -15.363 |

- BNBUSD: 0 of 24 windows run.
- w1 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w2 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w3 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w4 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w5 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w6 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w7 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w8 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w9 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w10 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w11 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w12 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w13 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w14 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w15 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w16 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w17 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w18 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w19 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w20 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w21 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w22 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w23 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w24 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for BNBUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

