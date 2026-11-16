# Backtest of 002-01_sma-golden-cross-upward-drift.b2_fresh-golden-cross-fades_1d

- Plan: `../../../03_test_plan/plans/002-01_sma-golden-cross-upward-drift.b2_fresh-golden-cross-fades_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 3 | 0.15856 | 3.235 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | 0.020137 | -5.906 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.088456 | 1.894 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.006089 | -1.324 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.091227 | -6.517 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.144332 | -15.852 |
| w16 | 2 | 0.166175 | 15.214 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | -0.159777 | -15.944 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.132487 | 4.314 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | 0.077838 | 0.145 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.078943 | -7.342 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.067334 | 2.338 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.001908 | -3.423 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.081784 | 1.739 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.22868 | -13.835 |
| w16 | 2 | 0.179633 | 14.091 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.020553 | -3.216 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.1085 | 4.565 |
| w22 | 1 | -0.12865 | -1.477 |
| w23 | 2 | -0.117977 | -15.129 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.050503 | 0.592 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | 0.05134 | 3.555 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.047874 | -8.624 |
| w9 | 0 | None | 0.0 |
| w10 | 1 | 0.104625 | 3.423 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.159166 | 11.368 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.177709 | 12.086 |
| w17 | 4 | 0.061763 | -6.286 |
| w18 | 0 | None | 0.0 |
| w19 | 3 | -0.140733 | -13.469 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | -0.082617 | -9.268 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.061097 | 1.785 |
| w24 | 1 | -0.04699 | -0.582 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.115802 | 3.456 |
| w2 | 2 | 0.030355 | 2.229 |
| w3 | 0 | None | 0.0 |
| w4 | 3 | -0.053397 | -5.912 |
| w5 | 3 | 0.112754 | 7.323 |
| w6 | 3 | 0.066478 | 0.422 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.01014 | -1.546 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.042097 | 4.969 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.139073 | -11.572 |
| w16 | 2 | 0.243649 | 18.82 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.101191 | 2.434 |
| w21 | 3 | 0.024693 | -0.845 |
| w22 | 1 | -0.009478 | -0.08 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.055737 | -7.877 |

- XRPUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.056223 | 4.243 |
| w4 | 2 | 0.072625 | 1.45 |
| w5 | 1 | 0.011348 | 0.076 |
| w6 | 2 | 0.121299 | 3.671 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.069133 | 1.739 |
| w11 | 2 | 0.180139 | 3.163 |
| w12 | 2 | 0.040638 | 3.386 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.029593 | 2.222 |
| w16 | 2 | 0.19946 | 14.633 |
| w17 | 1 | 0.093113 | 3.327 |
| w18 | 0 | None | 0.0 |
| w19 | 3 | 0.038539 | 4.203 |
| w20 | 1 | 0.048081 | 1.308 |
| w21 | 2 | 0.065214 | -1.565 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.14681 | 6.078 |
| w24 | 0 | None | 0.0 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 228 prefetch bars (<date> to <date>) -- required_bars=281. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.093449 | 4.952 |
| w2 | 1 | 0.018042 | 0.761 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.082804 | 4.63 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.020199 | -1.781 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.041626 | -7.474 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.109621 | -5.683 |
| w16 | 2 | 0.124312 | 4.63 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 3 | 0.067514 | 4.794 |
| w20 | 3 | -0.078504 | -6.755 |
| w21 | 1 | 0.013368 | -0.085 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.061662 | 2.213 |
| w24 | 0 | None | 0.0 |

