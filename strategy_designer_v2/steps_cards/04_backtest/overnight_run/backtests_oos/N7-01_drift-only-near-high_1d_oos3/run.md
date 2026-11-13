# Backtest of N7-01_drift-only-near-high_1d_oos3

- Plan: `../../../../03_test_plan/overnight_run/plans_oos/N7-01_drift-only-near-high_1d_oos3.md`
- Config: `config.json` (a copy of the plan's config)
- Data: NEAR, SUI, TAO, ONDO as NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; fold D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- NEARUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.144156 | 179.477 |
| w2 | 25 | -0.074796 | -45.843 |
| w3 | 18 | 0.04839 | 34.142 |
| w4 | 6 | -0.054492 | -18.724 |
| w5 | 21 | -0.006144 | -15.131 |
| w6 | 12 | -0.044208 | -28.788 |

- SUIUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | 0.030614 | 36.578 |
| w2 | 16 | -0.072916 | -39.668 |
| w3 | 32 | -0.056682 | 230.768 |
| w4 | 13 | 0.0373 | 9.592 |
| w5 | 19 | 0.08873 | 28.072 |
| w6 | 7 | -0.048516 | -21.54 |

- TAOUSD: 4 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w3 | 19 | -0.103868 | -27.517 |
| w4 | 10 | -0.012842 | -17.88 |
| w5 | 13 | 0.074174 | 27.755 |
| w6 | 10 | -0.05198 | -35.568 |

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

- ONDOUSD: 4 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w3 | 29 | 0.035509 | 85.46 |
| w4 | 10 | -0.046739 | -21.087 |
| w5 | 19 | 0.009253 | -6.097 |
| w6 | 5 | 0.038457 | -3.729 |

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

