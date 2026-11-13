# Backtest of N2-02_capitulation-rebound_1d

- Plan: `../../../../03_test_plan/overnight_run/plans/N2-02_capitulation-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.195922 | 19.25 |
| w2 | 21 | 0.1418 | 5.758 |
| w3 | 5 | 0.034281 | -1.81 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | 0.13288 | 0.0 |
| w6 | 0 | 0.026704 | 0.0 |
| w7 | 1 | 0.016103 | -0.063 |
| w8 | 3 | -0.084814 | -5.606 |
| w9 | 0 | -0.009928 | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | 0.170329 | 0.0 |
| w13 | 0 | 0.202694 | 0.0 |
| w14 | 19 | 0.050359 | -29.746 |
| w15 | 0 | None | 0.0 |
| w16 | 16 | 0.185402 | 105.68 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | 0.122246 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | 0.305843 | 0.0 |
| w21 | 0 | 0.040804 | 0.0 |
| w22 | 0 | 0.271247 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 18 | 0.101258 | 4.568 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.199135 | 3.795 |
| w2 | 21 | -0.07964 | -69.518 |
| w3 | 2 | 0.23008 | 3.713 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | -0.150787 | 0.0 |
| w6 | 2 | 0.022451 | 4.372 |
| w7 | 3 | 0.038401 | -3.849 |
| w8 | 1 | -0.038316 | -1.182 |
| w9 | 2 | 0.028806 | -0.483 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | 0.073443 | 0.0 |
| w14 | 13 | 0.102308 | -18.434 |
| w15 | 0 | None | 0.0 |
| w16 | 13 | 0.243987 | 84.829 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | 0.067386 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.160446 | 3.227 |
| w21 | 1 | 0.036389 | 2.05 |
| w22 | 17 | 0.147803 | 17.816 |
| w23 | 0 | 0.042738 | 0.0 |
| w24 | 0 | 0.06722 | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.015478 | -15.951 |
| w2 | 15 | 0.033249 | -38.51 |
| w3 | 0 | 0.052043 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 4 | 0.004108 | -1.04 |
| w6 | 5 | 0.013831 | 1.92 |
| w7 | 2 | 0.125111 | 7.675 |
| w8 | 1 | -0.004678 | 1.218 |
| w9 | 2 | 0.049996 | -0.154 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.126661 | 1.402 |
| w13 | 0 | None | 0.0 |
| w14 | 11 | 0.120478 | 0.177 |
| w15 | 0 | None | 0.0 |
| w16 | 8 | 0.275797 | 51.739 |
| w17 | 0 | 0.067404 | 0.0 |
| w18 | 0 | 0.103672 | 0.0 |
| w19 | 2 | 0.077055 | 1.777 |
| w20 | 23 | 0.171463 | 23.776 |
| w21 | 0 | 0.088093 | 0.0 |
| w22 | 0 | 0.108608 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.105701 | 4.869 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | 0.117159 | 41.561 |
| w2 | 16 | 0.164157 | 70.218 |
| w3 | 6 | 0.081711 | 4.617 |
| w4 | 0 | 0.016823 | 0.0 |
| w5 | 17 | 0.128247 | 14.044 |
| w6 | 6 | 0.028768 | 4.448 |
| w7 | 6 | 0.099828 | 11.567 |
| w8 | 3 | -0.012789 | 0.872 |
| w9 | 2 | 0.074333 | -0.971 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | -0.020635 | -13.589 |
| w14 | 11 | 0.082576 | -13.725 |
| w15 | 0 | None | 0.0 |
| w16 | 8 | 0.186674 | 87.225 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | 0.103697 | 0.0 |
| w19 | 18 | 0.177829 | 82.672 |
| w20 | 5 | -0.002415 | 0.894 |
| w21 | 0 | 0.098576 | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | 0.225521 | 0.0 |
| w24 | 0 | 0.065795 | 0.0 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 364 prefetch bars (<date> to <date>) -- required_bars=250. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.344037 | 48.874 |
| w2 | 7 | 0.04946 | -15.015 |
| w3 | 0 | 0.326668 | 0.0 |
| w4 | 0 | -0.002336 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | 0.02313 | 0.0 |
| w8 | 1 | -0.070383 | -1.294 |
| w9 | 9 | 0.158119 | 24.835 |
| w10 | 0 | -0.024973 | 0.0 |
| w11 | 0 | 0.040209 | 0.0 |
| w12 | 2 | 0.12722 | 3.355 |
| w14 | 4 | 0.087447 | 24.493 |
| w15 | 0 | 0.095586 | 0.0 |
| w16 | 15 | 0.191405 | 106.525 |
| w17 | 0 | 0.003415 | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 9 | 0.112151 | 13.676 |
| w20 | 7 | 0.19008 | 40.249 |
| w21 | 0 | 0.005771 | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | 0.09137 | 6.903 |

- w7 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 347 prefetch bars (<date> to <date>) -- required_bars=250. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 228 prefetch bars (<date> to <date>) -- required_bars=250. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.232707 | 16.55 |
| w2 | 22 | 0.040025 | -26.922 |
| w3 | 7 | 0.191674 | 10.242 |
| w4 | 3 | 0.038953 | 0.761 |
| w5 | 13 | 0.228552 | 49.732 |
| w6 | 0 | 0.084777 | 0.0 |
| w7 | 3 | 0.126601 | 12.16 |
| w8 | 1 | -0.075463 | -5.504 |
| w9 | 13 | 0.083423 | 2.284 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | 0.022409 | 0.0 |
| w12 | 0 | 0.040858 | 0.0 |
| w13 | 0 | 0.274765 | 0.0 |
| w14 | 15 | 0.013201 | -30.101 |
| w15 | 0 | 0.094647 | 0.0 |
| w16 | 3 | 0.132457 | 15.661 |
| w17 | 0 | 0.102841 | 0.0 |
| w18 | 0 | 0.111381 | 0.0 |
| w19 | 24 | 0.13086 | 17.855 |
| w20 | 5 | 0.242704 | 26.64 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | 0.127785 | 0.0 |
| w23 | 0 | 0.201742 | 0.0 |
| w24 | 0 | None | 0.0 |

