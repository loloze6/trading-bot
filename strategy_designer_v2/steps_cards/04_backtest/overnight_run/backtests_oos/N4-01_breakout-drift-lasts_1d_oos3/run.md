# Backtest of N4-01_breakout-drift-lasts_1d_oos3

- Plan: `../../../../03_test_plan/overnight_run/plans_oos/N4-01_breakout-drift-lasts_1d_oos3.md`
- Config: `config.json` (a copy of the plan's config)
- Data: NEAR, SUI, TAO, ONDO as NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; fold D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- NEARUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.182699 | 276.892 |
| w2 | 23 | -0.129627 | -69.251 |
| w3 | 26 | 0.028821 | 21.87 |
| w4 | 10 | 0.003021 | -27.81 |
| w5 | 31 | 0.035296 | -5.391 |
| w6 | 18 | -0.060741 | -47.588 |

- SUIUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | 0.003187 | 33.96 |
| w2 | 17 | -0.111243 | -62.851 |
| w3 | 32 | -0.000277 | 518.579 |
| w4 | 19 | 0.054444 | 12.143 |
| w5 | 26 | 0.081999 | 26.687 |
| w6 | 9 | 0.00666 | -30.658 |

- TAOUSD: 3 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w4 | 21 | -0.126424 | -68.474 |
| w5 | 23 | 0.037805 | -0.734 |
| w6 | 20 | 0.023132 | -36.469 |

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
| w3 | 30 | -0.053778 | 70.132 |
| w4 | 11 | -0.01899 | -26.784 |
| w5 | 29 | 0.033839 | 1.207 |
| w6 | 8 | 0.025635 | -12.31 |

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

