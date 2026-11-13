# Backtest of N4-04_dip-rebound-spans-days_1d_oos3

- Plan: `../../../../03_test_plan/overnight_run/plans_oos/N4-04_dip-rebound-spans-days_1d_oos3.md`
- Config: `config.json` (a copy of the plan's config)
- Data: NEAR, SUI, TAO, ONDO as NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; fold D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- NEARUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.128255 | 83.93 |
| w2 | 4 | 0.06401 | 8.142 |
| w3 | 16 | -0.051258 | -13.279 |
| w4 | 0 | None | 0.0 |
| w5 | 9 | -0.0376 | -10.082 |
| w6 | 4 | -0.102778 | -20.435 |

- SUIUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | 0.078472 | 35.645 |
| w2 | 3 | -0.139149 | -28.696 |
| w3 | 22 | 0.057008 | 62.286 |
| w4 | 9 | 0.005056 | -1.149 |
| w5 | 13 | -0.051444 | -12.292 |
| w6 | 0 | 0.041011 | 0.0 |

- TAOUSD: 4 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w3 | 19 | -0.060935 | -16.214 |
| w4 | 1 | -0.054525 | -0.785 |
| w5 | 9 | -0.03458 | -6.336 |
| w6 | 7 | -0.02411 | -16.029 |

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
| w3 | 16 | 0.119596 | 56.845 |
| w4 | 1 | -0.150969 | -7.979 |
| w5 | 15 | -0.107763 | -24.034 |
| w6 | 2 | -0.006357 | -5.611 |

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

