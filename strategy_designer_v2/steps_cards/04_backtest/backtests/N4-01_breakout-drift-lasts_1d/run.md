# Backtest of N4-01_breakout-drift-lasts_1d

- Plan: `../../../03_test_plan/plans/N4-01_breakout-drift-lasts_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: NEAR, SUI, TAO, ONDO as NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; fold D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- NEARUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | 0.078809 | 33.505 |
| w2 | 32 | -0.07737 | -13.527 |
| w3 | 23 | 0.054517 | 16.574 |
| w4 | 6 | -0.121989 | -11.386 |
| w5 | 24 | 0.045934 | 5.933 |
| w6 | 12 | 0.012348 | -1.103 |

- SUIUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 40 | -0.018272 | 2.998 |
| w2 | 16 | -0.136586 | -16.323 |
| w3 | 36 | -0.075911 | 33.457 |
| w4 | 12 | 0.055321 | 3.103 |
| w5 | 23 | 0.029483 | 5.882 |
| w6 | 8 | -0.065737 | -11.986 |

- TAOUSD: 3 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w4 | 9 | 0.017919 | -1.76 |
| w5 | 23 | 0.047808 | 4.636 |
| w6 | 10 | -0.126572 | -17.114 |

- w1 not run: no historical data on the venue.

```
    raise RuntimeError(
    ...<4 lines>...
    )
RuntimeError: No historical data for TAOUSD over <date>..<date> (exchange=kraken). The fetch returned nothing, so there is nothing to backtest. Refusing to emit a zero-metric run that would be indistinguishable from a strategy that simply never traded.
```

- w2 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 0 prefetch bars (<date> to <date>) -- required_bars=61. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w3 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 62 prefetch bars (<date> to <date>) -- required_bars=61. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ONDOUSD: 4 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w3 | 28 | 0.089954 | 40.473 |
| w4 | 6 | -0.004322 | -1.845 |
| w5 | 15 | 0.082223 | 12.587 |
| w6 | 7 | 0.032301 | -2.099 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 0 prefetch bars (<date> to <date>) -- required_bars=61. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w2 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 20 prefetch bars (<date> to <date>) -- required_bars=61. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

