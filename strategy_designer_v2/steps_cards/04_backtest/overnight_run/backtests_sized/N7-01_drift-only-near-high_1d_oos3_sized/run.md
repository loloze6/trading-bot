# Backtest of N7-01_drift-only-near-high_1d_oos3_sized

- Plan: `../../../../03_test_plan/overnight_run/plans_sized/N7-01_drift-only-near-high_1d_oos3_sized.md`
- Config: `config.json` (a copy of the plan's config)
- Data: NEAR, SUI, TAO, ONDO as NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; fold D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- NEARUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.144156 | 64.973 |
| w2 | 24 | -0.074796 | -17.959 |
| w3 | 11 | 0.04839 | 14.738 |
| w4 | 4 | -0.054492 | -6.908 |
| w5 | 21 | -0.006144 | -2.87 |
| w6 | 13 | -0.044208 | -7.929 |

- SUIUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | 0.030614 | 12.441 |
| w2 | 13 | -0.072916 | -13.311 |
| w3 | 37 | -0.056682 | 47.314 |
| w4 | 12 | 0.0373 | 3.709 |
| w5 | 15 | 0.08873 | 19.857 |
| w6 | 7 | -0.048516 | -10.64 |

- TAOUSD: 4 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w3 | 19 | -0.103868 | -8.813 |
| w4 | 8 | -0.012842 | -6.794 |
| w5 | 14 | 0.074174 | 10.662 |
| w6 | 10 | -0.05198 | -14.829 |

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
| w3 | 29 | 0.035509 | 29.982 |
| w4 | 10 | -0.046739 | -7.39 |
| w5 | 16 | 0.009253 | 1.454 |
| w6 | 5 | 0.038457 | -1.643 |

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

