# Backtest of 032-02_choppy-agitated-weekly-fall-reverts_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/032-02_choppy-agitated-weekly-fall-reverts_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.118464 | 3.482 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.055106 | 0.176 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.013046 | -2.647 |
| w10 | 0 | -0.063421 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.078645 | 16.846 |
| w13 | 3 | -0.124945 | -3.457 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.021266 | 4.462 |
| w16 | 5 | -0.350691 | -39.787 |
| w17 | 6 | 0.039558 | 13.176 |
| w18 | 2 | 0.157769 | -2.86 |
| w19 | 5 | 0.001835 | 13.238 |
| w20 | 12 | 0.08097 | -4.299 |
| w21 | 4 | 0.014829 | 0.765 |
| w22 | 1 | -0.290044 | -5.737 |
| w23 | 0 | 0.112478 | 0.0 |
| w24 | 15 | -0.040992 | -13.191 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | 0.016856 | 0.0 |
| w3 | 13 | -0.135119 | -4.658 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | -0.065079 | 5.466 |
| w9 | 4 | -0.020256 | 0.952 |
| w10 | 2 | -0.045078 | 4.966 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.05185 | 3.936 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.024956 | -7.731 |
| w16 | 2 | -0.135025 | -0.714 |
| w17 | 2 | 0.150761 | 3.353 |
| w18 | 4 | -0.078653 | 2.978 |
| w19 | 3 | 0.031268 | 7.194 |
| w20 | 5 | 0.087778 | 6.315 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | 0.14306 | 0.067 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.138761 | -0.552 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 9 | -0.094526 | 0.018 |
| w4 | 10 | 0.131513 | 2.241 |
| w5 | 6 | 0.137479 | 3.052 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | 0.032629 | 9.565 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.050188 | -1.283 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | 0.19801 | -1.774 |
| w16 | 1 | -0.424905 | -16.732 |
| w17 | 8 | 0.013541 | 2.856 |
| w18 | 3 | -0.0872 | 0.35 |
| w19 | 12 | 0.059184 | 7.333 |
| w20 | 4 | -0.050606 | -0.59 |
| w21 | 11 | 0.051788 | 27.866 |
| w22 | 12 | -0.112024 | 3.314 |
| w23 | 4 | -0.028732 | 4.461 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.039802 | 7.456 |
| w2 | 7 | -0.228402 | 1.096 |
| w3 | 4 | -0.082583 | -2.421 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.150474 | 9.316 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | 0.070204 | 12.076 |
| w12 | 4 | 0.233381 | 16.338 |
| w14 | 2 | 0.026237 | -11.924 |
| w15 | 9 | 0.018409 | -6.834 |
| w16 | 3 | -0.358056 | -24.759 |
| w17 | 0 | None | 0.0 |
| w18 | 8 | 0.08968 | 9.456 |
| w19 | 15 | -0.047939 | -0.392 |
| w20 | 2 | 0.133371 | 5.115 |
| w21 | 7 | -0.04369 | 1.755 |
| w22 | 7 | 0.020422 | 15.348 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.018022 | 20.005 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.100754 | 2.095 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | 0.155277 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 8 | 0.018263 | 9.651 |
| w6 | 3 | -0.014894 | -0.39 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | 0.025279 | 1.33 |
| w10 | 0 | None | 0.0 |
| w11 | 5 | -0.076785 | 14.344 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 6 | 0.082627 | 3.09 |
| w16 | 10 | -0.18322 | -7.863 |
| w17 | 7 | 0.10931 | 1.32 |
| w18 | 0 | None | 0.0 |
| w19 | 11 | 0.066562 | -1.826 |
| w20 | 3 | 0.18458 | 4.345 |
| w21 | 8 | -0.052227 | 1.717 |
| w22 | 11 | 0.110599 | 11.858 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | 0.004076 | 0.0 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.275197 | -0.066 |
| w2 | 2 | 0.066074 | -3.515 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 5 | 0.023388 | -2.917 |
| w6 | 3 | 0.017631 | 7.91 |
| w7 | 2 | 0.003579 | -2.349 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 10 | 0.078012 | 16.995 |
| w12 | 6 | 0.012103 | 4.603 |
| w13 | 4 | 0.188093 | 3.698 |
| w14 | 0 | None | 0.0 |
| w15 | 11 | -0.011205 | -0.144 |
| w16 | 0 | None | 0.0 |
| w17 | 17 | 0.044528 | 8.791 |
| w18 | 4 | 0.116965 | 2.147 |
| w19 | 7 | 0.04841 | -5.478 |
| w20 | 3 | -0.072041 | -13.945 |
| w21 | 0 | None | 0.0 |
| w22 | 11 | -0.035909 | 4.995 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | 0.002679 | 0.0 |

