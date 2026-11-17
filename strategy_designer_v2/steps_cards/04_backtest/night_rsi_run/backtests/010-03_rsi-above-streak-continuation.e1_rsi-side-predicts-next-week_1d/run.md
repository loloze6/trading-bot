# Backtest of 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d

- Plan: `../../../../03_test_plan/night_rsi_run/plans/010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 75 | -0.044088 | -12.481 |
| w2 | 66 | 0.021682 | 24.224 |
| w3 | 70 | -0.114984 | -22.523 |
| w4 | 50 | 0.016313 | 58.707 |
| w5 | 65 | -0.037534 | -10.512 |
| w6 | 48 | 0.023501 | 39.268 |
| w7 | 65 | 0.016184 | 3.72 |
| w8 | 42 | 0.034433 | 30.997 |
| w9 | 68 | -0.074407 | -12.754 |
| w10 | 65 | -0.027969 | 11.127 |
| w11 | 57 | -0.026723 | 12.271 |
| w12 | 71 | 0.003694 | -4.002 |
| w13 | 69 | -0.050572 | -9.428 |
| w14 | 57 | 0.023447 | 53.003 |
| w15 | 67 | 0.072979 | 42.319 |
| w16 | 63 | 0.002944 | 20.135 |
| w17 | 51 | 0.084541 | 122.694 |
| w18 | 66 | 0.054992 | 16.312 |
| w19 | 51 | 0.09651 | 48.227 |
| w20 | 73 | -0.071747 | -18.47 |
| w21 | 59 | -0.005823 | 43.271 |
| w22 | 70 | -0.108806 | -32.13 |
| w23 | 70 | -0.004311 | 0.2 |
| w24 | 78 | -0.048353 | -10.604 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 66 | 0.030301 | 5.06 |
| w2 | 62 | 0.08892 | 49.594 |
| w3 | 61 | -0.106685 | -19.06 |
| w4 | 65 | -0.054396 | 11.962 |
| w5 | 76 | -0.121283 | -25.509 |
| w6 | 62 | 0.003557 | 11.432 |
| w7 | 72 | -0.024413 | 18.179 |
| w8 | 50 | -0.05744 | -9.255 |
| w9 | 74 | -0.056193 | -6.273 |
| w10 | 66 | -0.033842 | 48.151 |
| w11 | 61 | -0.049684 | 52.592 |
| w12 | 84 | -0.107563 | -24.809 |
| w13 | 57 | 0.139549 | 50.367 |
| w14 | 49 | 0.065371 | 50.892 |
| w15 | 63 | 0.103147 | 34.031 |
| w16 | 57 | 0.007225 | 31.508 |
| w17 | 65 | -0.048683 | 8.719 |
| w18 | 60 | 0.04902 | 34.179 |
| w19 | 49 | 0.090938 | 42.879 |
| w20 | 69 | -0.012317 | -3.604 |
| w21 | 73 | -0.045031 | -8.601 |
| w22 | 62 | -0.159826 | -9.235 |
| w23 | 51 | -0.023349 | 48.555 |
| w24 | 67 | -0.122313 | -16.043 |

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

