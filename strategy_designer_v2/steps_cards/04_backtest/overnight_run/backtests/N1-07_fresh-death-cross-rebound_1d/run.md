# Backtest of N1-07_fresh-death-cross-rebound_1d

- Plan: `../../../../03_test_plan/overnight_run/plans_newcomp/N1-07_fresh-death-cross-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.017287 | -2.577 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 11 | -0.018314 | 1.104 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 8 | -0.056532 | -1.625 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | 0.141042 | 5.051 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 20 | -0.033626 | -2.59 |
| w17 | 0 | None | 0.0 |
| w18 | 12 | 0.009244 | 0.157 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.000278 | -0.003 |
| w21 | 0 | None | 0.0 |
| w22 | 9 | 0.130594 | 3.828 |
| w23 | 0 | None | 0.0 |
| w24 | 19 | 0.041277 | 0.284 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.039707 | 1.18 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 17 | -0.085654 | -1.214 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 10 | -0.05163 | -2.363 |
| w10 | 1 | 0.010068 | 0.585 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 11 | 0.10601 | 7.399 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 12 | 0.056307 | 14.364 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | 0.140138 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 15 | -0.02161 | -1.317 |
| w21 | 0 | None | 0.0 |
| w22 | 20 | 0.01748 | -3.355 |
| w23 | 0 | None | 0.0 |
| w24 | 17 | 0.014444 | -0.671 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.122315 | -18.804 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 12 | -0.017026 | -1.268 |
| w6 | 8 | -0.01964 | -0.325 |
| w7 | 3 | -0.031735 | -2.067 |
| w8 | 0 | None | 0.0 |
| w9 | 11 | 0.10499 | 2.574 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | -0.000382 | -0.29 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 17 | -0.029488 | -2.028 |
| w17 | 1 | 0.047816 | 0.238 |
| w18 | 14 | -0.071954 | -7.395 |
| w19 | 0 | None | 0.0 |
| w20 | 19 | 0.070271 | 4.042 |
| w21 | 0 | None | 0.0 |
| w22 | 16 | 0.051069 | 4.648 |
| w23 | 0 | None | 0.0 |
| w24 | 18 | -0.014183 | -3.079 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 19 | -0.037948 | -10.821 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 19 | 0.153369 | 8.256 |
| w6 | 20 | -0.021879 | 0.506 |
| w7 | 1 | -0.02644 | -1.225 |
| w8 | 0 | None | 0.0 |
| w9 | 20 | 0.025351 | -1.097 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 24 | 0.092438 | 9.266 |
| w13 | 6 | -0.036661 | -0.935 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 17 | 0.01017 | 6.188 |
| w17 | 0 | None | 0.0 |
| w18 | 9 | 0.088913 | 5.462 |
| w19 | 20 | 0.109793 | 31.3 |
| w20 | 0 | None | 0.0 |
| w21 | 9 | 0.121697 | 2.753 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | 0.000491 | 1.091 |

- XRPUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.04517 | -10.402 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | -0.051872 | -0.519 |
| w4 | 3 | 0.080675 | 2.645 |
| w5 | 0 | None | 0.0 |
| w6 | 10 | -0.026217 | 0.111 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.055412 | 2.653 |
| w10 | 0 | None | 0.0 |
| w11 | 5 | 0.096671 | 3.746 |
| w12 | 1 | None | -0.005 |
| w14 | 0 | None | 0.0 |
| w15 | 18 | -0.027234 | -3.844 |
| w16 | 19 | 0.104247 | 16.181 |
| w17 | 0 | None | 0.0 |
| w18 | 12 | 0.107972 | 10.914 |
| w19 | 12 | 0.08486 | 2.349 |
| w20 | 19 | 0.026287 | 6.92 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.06015 | -0.189 |
| w24 | 20 | 0.041065 | 0.376 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 228 prefetch bars (<date> to <date>) -- required_bars=320. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.096679 | 12.806 |
| w2 | 19 | -0.011502 | -9.618 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 12 | 0.014762 | -1.464 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 20 | 0.151599 | 30.907 |
| w14 | 0 | None | 0.0 |
| w15 | 7 | -0.070748 | -2.478 |
| w16 | 10 | 0.051351 | 8.997 |
| w17 | 0 | None | 0.0 |
| w18 | 14 | -0.023587 | -3.747 |
| w19 | 21 | -0.01943 | -4.308 |
| w20 | 17 | -0.015379 | 3.358 |
| w21 | 0 | None | 0.0 |
| w22 | 14 | -6e-06 | -1.902 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

