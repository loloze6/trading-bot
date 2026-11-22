# Backtest of 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong_1h

- Plan: `../../../../03_test_plan/night4_volumehour_run/plans/028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 137 | 0.013457 | -13.403 |
| w2 | 137 | -0.018792 | -55.315 |
| w3 | 125 | -0.02718 | -18.9 |
| w4 | 133 | 0.061214 | 149.683 |
| w5 | 138 | 0.021875 | -28.518 |
| w6 | 138 | -0.020027 | 109.995 |
| w7 | 144 | -0.002313 | -3.815 |
| w8 | 129 | 0.023131 | 57.715 |
| w9 | 135 | 0.042676 | -18.104 |
| w10 | 130 | -0.024182 | 16.926 |
| w11 | 117 | 0.008618 | 72.424 |
| w12 | 140 | 0.00793 | 11.859 |
| w13 | 114 | 0.003488 | -19.284 |
| w14 | 137 | -0.050105 | -69.626 |
| w15 | 123 | -0.009935 | 113.521 |
| w16 | 129 | 0.011469 | -28.59 |
| w17 | 144 | -0.002894 | 209.206 |
| w18 | 131 | 0.036844 | -24.168 |
| w19 | 123 | -0.010773 | 67.036 |
| w20 | 167 | -0.015088 | -21.441 |
| w21 | 138 | 0.021922 | 112.445 |
| w22 | 116 | -0.002348 | -3.197 |
| w23 | 150 | -0.021845 | -7.126 |
| w24 | 153 | 0.01551 | -42.694 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 117 | 0.010907 | -7.468 |
| w2 | 125 | 0.001244 | -47.849 |
| w3 | 123 | 0.020603 | -1.149 |
| w4 | 138 | 0.006647 | 79.853 |
| w5 | 163 | -0.036443 | -40.562 |
| w6 | 153 | -0.036222 | 37.079 |
| w7 | 147 | 0.006977 | -9.39 |
| w8 | 127 | -7.6e-05 | 7.678 |
| w9 | 143 | 0.010373 | -24.423 |
| w10 | 135 | -0.000123 | 154.865 |
| w11 | 113 | 0.010518 | 119.113 |
| w12 | 157 | 0.006724 | 28.81 |
| w13 | 57 | 0.010044 | 38.746 |
| w14 | 121 | -0.00228 | -43.986 |
| w15 | 109 | -0.015036 | 23.165 |
| w16 | 116 | -0.011761 | 24.79 |
| w17 | 123 | 0.001645 | 26.405 |
| w18 | 129 | 0.085548 | 40.164 |
| w19 | 124 | -0.025248 | 75.23 |
| w20 | 159 | 0.012149 | 0.444 |
| w21 | 152 | -0.009726 | 37.584 |
| w22 | 121 | 0.047904 | -26.103 |
| w23 | 118 | 0.027429 | 120.97 |
| w24 | 136 | 0.02444 | -44.836 |

