# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d

- Plan: `../../../../03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.073766 | -6.442 |
| w2 | 6 | 0.053154 | -1.579 |
| w3 | 8 | -0.133932 | -5.286 |
| w4 | 15 | -0.055608 | 19.386 |
| w5 | 10 | 0.035194 | 3.456 |
| w6 | 21 | 0.022112 | 75.788 |
| w7 | 10 | -0.030646 | -4.839 |
| w8 | 16 | -0.012647 | 12.852 |
| w9 | 10 | -0.054829 | -5.324 |
| w10 | 31 | -0.009186 | 22.759 |
| w11 | 30 | -0.081303 | 24.721 |
| w12 | 17 | 0.025853 | 1.274 |
| w13 | 10 | -0.094714 | -4.641 |
| w14 | 7 | -0.108914 | -7.127 |
| w15 | 33 | -0.102111 | 15.003 |
| w16 | 20 | 0.006043 | 7.114 |
| w17 | 16 | 0.118724 | 184.881 |
| w18 | 11 | 0.062419 | 5.225 |
| w19 | 20 | 0.056248 | 34.78 |
| w20 | 24 | -0.1442 | -18.511 |
| w21 | 31 | -0.01521 | 55.529 |
| w22 | 21 | -0.088432 | -9.461 |
| w23 | 29 | 0.020868 | 7.369 |
| w24 | 11 | -0.016252 | -8.769 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.02202 | -6.05 |
| w2 | 11 | 0.074358 | 2.45 |
| w3 | 10 | -0.073902 | -6.119 |
| w4 | 13 | -0.073723 | 7.077 |
| w5 | 21 | -0.089857 | -12.354 |
| w6 | 28 | 0.000883 | 34.146 |
| w7 | 4 | 0.068153 | -2.591 |
| w8 | 22 | -0.226409 | -7.112 |
| w9 | 14 | -0.118498 | -4.272 |
| w10 | 19 | 0.056906 | 69.34 |
| w11 | 33 | 0.024731 | 100.405 |
| w12 | 24 | -0.045864 | -8.483 |
| w13 | 15 | 0.077844 | 19.529 |
| w14 | 5 | -0.17604 | -5.275 |
| w15 | 15 | 0.045598 | 5.795 |
| w16 | 18 | 0.001073 | 15.262 |
| w17 | 29 | 0.047045 | 40.34 |
| w18 | 17 | 0.006112 | 15.661 |
| w19 | 25 | 0.002099 | 12.377 |
| w20 | 13 | -0.009332 | -3.811 |
| w21 | 24 | -0.024363 | 10.924 |
| w22 | 1 | -0.047881 | -0.421 |
| w23 | 19 | -0.019963 | 49.684 |
| w24 | 10 | -0.040869 | -7.707 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.086747 | -8.246 |
| w2 | 10 | 0.023381 | 0.386 |
| w3 | 17 | -0.031836 | 1.696 |
| w4 | 26 | -0.122041 | -7.163 |
| w5 | 22 | -0.159653 | -27.013 |
| w6 | 19 | -0.178736 | -8.75 |
| w7 | 5 | -0.046094 | -4.219 |
| w8 | 19 | -0.11885 | 8.739 |
| w9 | 8 | -0.065882 | -2.528 |
| w10 | 17 | 0.011414 | 11.57 |
| w11 | 41 | -0.133758 | 11.23 |
| w12 | 16 | -0.03155 | -6.076 |
| w13 | 16 | -0.051733 | -3.127 |
| w14 | 4 | -0.137322 | -3.761 |
| w15 | 22 | 0.038652 | 3.084 |
| w16 | 15 | 0.034877 | 9.892 |
| w17 | 34 | 0.03387 | 34.249 |
| w18 | 13 | 0.016973 | 0.276 |
| w19 | 32 | -0.011979 | 9.135 |
| w20 | 5 | -0.141022 | -1.917 |
| w21 | 34 | -0.043457 | 15.42 |
| w22 | 19 | -0.128117 | -14.915 |
| w23 | 27 | -0.066224 | 2.546 |
| w24 | 12 | -0.271332 | -24.693 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.024394 | -5.521 |
| w2 | 12 | -0.042206 | -3.606 |
| w3 | 15 | -0.101229 | -7.201 |
| w4 | 19 | -0.032274 | -0.774 |
| w5 | 8 | 0.019255 | 0.754 |
| w6 | 39 | -0.171817 | -9.579 |
| w7 | 7 | -0.059448 | -4.009 |
| w8 | 26 | -0.059117 | 4.603 |
| w9 | 6 | -0.021651 | -2.236 |
| w10 | 24 | 0.010302 | 33.476 |
| w11 | 40 | -0.036128 | 49.567 |
| w12 | 12 | -0.113876 | -8.219 |
| w14 | 15 | -0.024462 | -7.051 |
| w15 | 21 | -0.080223 | -6.29 |
| w16 | 21 | 0.00803 | 9.776 |
| w17 | 38 | -0.100078 | 3.921 |
| w18 | 22 | -0.037662 | -8.939 |
| w19 | 12 | -0.284924 | -40.408 |
| w20 | 30 | -0.092309 | -3.769 |
| w21 | 30 | -0.040324 | -3.263 |
| w22 | 37 | -0.100573 | 7.878 |
| w23 | 15 | 0.123589 | 30.276 |
| w24 | 50 | -0.222488 | -2.29 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 364 prefetch bars (<date> to <date>) -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.128521 | -6.4 |
| w2 | 7 | 0.03686 | -0.551 |
| w3 | 12 | 0.046456 | 6.52 |
| w4 | 16 | -0.118458 | -3.649 |
| w5 | 21 | -0.127034 | -18.149 |
| w6 | 22 | -0.100948 | -2.237 |
| w8 | 20 | -0.214705 | -12.784 |
| w9 | 10 | 0.047506 | -2.034 |
| w10 | 13 | 0.06564 | 23.313 |
| w11 | 36 | -0.005723 | 49.636 |
| w12 | 19 | -0.097976 | -10.02 |
| w14 | 8 | -0.035931 | -4.183 |
| w15 | 12 | -0.032723 | -5.287 |
| w16 | 15 | 0.008143 | 5.542 |
| w17 | 25 | 0.170044 | 108.954 |
| w18 | 14 | -0.069059 | -2.822 |
| w19 | 21 | -0.077486 | -9.462 |
| w20 | 15 | -0.060068 | -2.233 |
| w21 | 26 | 0.261198 | 235.093 |
| w22 | 11 | -0.075656 | -6.787 |
| w23 | 35 | 0.050192 | 25.029 |
| w24 | 6 | -0.094757 | -7.952 |

- w7 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 347 prefetch bars (<date> to <date>) -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 228 prefetch bars (<date> to <date>) -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.016242 | 0.341 |
| w2 | 12 | -0.02312 | -4.487 |
| w3 | 5 | -0.060085 | -3.302 |
| w4 | 18 | -0.117717 | -8.02 |
| w5 | 9 | 0.005389 | -0.547 |
| w6 | 27 | -0.181032 | -13.999 |
| w7 | 11 | -0.038733 | -5.979 |
| w8 | 17 | 0.016222 | 5.07 |
| w9 | 1 | -0.043761 | -0.891 |
| w10 | 27 | -0.046467 | 8.861 |
| w11 | 39 | -0.114936 | 45.035 |
| w12 | 19 | -0.08438 | -9.426 |
| w14 | 3 | -0.110036 | -8.778 |
| w15 | 21 | 0.053856 | -1.949 |
| w16 | 13 | 0.139247 | 32.094 |
| w17 | 21 | -0.096596 | -9.332 |
| w18 | 15 | 0.021347 | 0.795 |
| w19 | 5 | 0.024707 | -0.629 |
| w20 | 20 | 0.029169 | 19.082 |
| w21 | 37 | -0.040358 | 20.278 |
| w22 | 7 | -0.150365 | -7.804 |
| w23 | 19 | -0.022262 | -0.91 |
| w24 | 33 | 0.167687 | 205.179 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 429 prefetch bars (<date> to <date>) -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

