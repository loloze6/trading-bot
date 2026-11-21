# Backtest of 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold_1d

- Plan: `../../../../03_test_plan/night3_ichimoku_run/plans/021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.005108 | -1.565 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.026227 | -6.689 |
| w4 | 3 | 0.17477 | 50.745 |
| w5 | 2 | -0.012151 | -1.377 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | 0.258022 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | 0.019459 | 0.0 |
| w11 | 1 | None | -0.011 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 2 | 0.045823 | -9.236 |
| w15 | 2 | -0.076969 | -5.94 |
| w16 | 2 | -0.006427 | 2.422 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.033973 | 2.216 |
| w19 | 2 | -0.03109 | 20.422 |
| w20 | 2 | 0.003071 | -4.494 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | -0.118521 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.086498 | -11.966 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.063655 | -4.689 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | -0.019937 | 0.0 |
| w4 | 4 | 0.121318 | 22.246 |
| w5 | 2 | -0.042673 | -2.538 |
| w6 | 2 | 0.02885 | 12.417 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | 0.093337 | 15.687 |
| w9 | 2 | -0.056755 | -11.615 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.034337 | 5.38 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | -0.032755 | 0.0 |
| w18 | 2 | 0.033693 | -4.703 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | 0.091817 | 0.0 |
| w21 | 1 | 0.167145 | 48.618 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.120412 | 10.052 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.00027 | -2.599 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | 0.080611 | -15.702 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | -0.030416 | -14.068 |
| w6 | 2 | -0.034949 | 1.324 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.064737 | 15.411 |
| w9 | 0 | None | 0.0 |
| w10 | 6 | -0.076037 | 7.774 |
| w11 | 2 | 0.002585 | 10.563 |
| w12 | 2 | -0.086306 | 0.006 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.079924 | 13.088 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.03179 | 17.267 |
| w22 | 2 | 0.119545 | -3.749 |
| w23 | 1 | -0.10123 | -6.353 |
| w24 | 2 | 0.021821 | -6.914 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.125668 | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | -0.022063 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.022843 | 15.99 |
| w12 | 3 | -0.159486 | -25.607 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.029801 | 21.669 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.026099 | 22.429 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.032684 | 1.106 |
| w21 | 4 | 0.003141 | 10.333 |
| w22 | 0 | 0.01365 | 0.0 |
| w23 | 0 | -0.082705 | 0.0 |
| w24 | 2 | 0.011942 | 4.444 |

- XRPUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.042056 | -2.007 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | -0.10274 | 0.0 |
| w4 | 0 | -0.266905 | 0.0 |
| w5 | 2 | -0.153277 | -14.881 |
| w6 | 3 | -0.10892 | 1.373 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.083755 | -16.763 |
| w9 | 2 | -0.080404 | -5.917 |
| w10 | 2 | 0.05765 | 9.315 |
| w11 | 4 | 0.024565 | 66.2 |
| w12 | 0 | None | 0.0 |
| w14 | 1 | -0.039515 | -24.866 |
| w15 | 2 | 0.240155 | 11.854 |
| w16 | 0 | -0.005417 | 0.0 |
| w17 | 3 | 0.009283 | 23.203 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.032813 | 4.07 |
| w21 | 1 | 0.070215 | 364.606 |
| w22 | 1 | -0.333753 | -2.292 |
| w23 | 2 | 0.013076 | -1.765 |
| w24 | 0 | -0.073148 | 0.0 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=327. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 3 | 0.084485 | -1.863 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | 0.116416 | 6.804 |
| w7 | 2 | 0.221574 | -10.104 |
| w8 | 0 | -0.017336 | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | 0.254022 | 107.559 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.113689 | -8.897 |
| w14 | 0 | -0.011498 | 0.0 |
| w15 | 2 | -0.057429 | 33.478 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.079221 | -9.61 |
| w18 | 2 | -0.03322 | 0.383 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.213667 | 48.644 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | -0.047379 | -3.3 |
| w23 | 4 | 0.042841 | 2.775 |
| w24 | 3 | -0.016927 | 49.682 |

