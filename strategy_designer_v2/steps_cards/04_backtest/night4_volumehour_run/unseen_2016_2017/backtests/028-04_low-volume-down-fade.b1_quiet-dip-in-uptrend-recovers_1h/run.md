# Backtest of 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h

- Plan: `../../../../../03_test_plan/night4_volumehour_run/plans/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; windows unseen_2016_2017
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 164 | 0.019402 | -8.412 |
| w2 | 111 | -0.011463 | 4.878 |
| w3 | 257 | 0.01312 | 35.94 |
| w4 | 235 | 0.01271 | 18.974 |
| w5 | 260 | -0.004313 | -5.455 |
| w6 | 321 | -0.02687 | 20.981 |

- ETHUSD: 5 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 145 | 0.008078 | 10.722 |
| w3 | 85 | -0.001916 | -6.544 |
| w4 | 217 | -0.000429 | 79.879 |
| w5 | 219 | -0.007104 | 13.043 |
| w6 | 214 | -0.015513 | 10.105 |

- w1 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 585 warm-up bars -- required_bars=1441. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

