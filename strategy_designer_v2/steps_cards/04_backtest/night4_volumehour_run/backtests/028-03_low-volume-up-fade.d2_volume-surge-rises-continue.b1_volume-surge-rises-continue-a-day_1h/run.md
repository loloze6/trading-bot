# Backtest of 028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day_1h

- Plan: `../../../../03_test_plan/night4_volumehour_run/plans/028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 131 | -0.000242 | -19.159 |
| w2 | 127 | -0.01211 | -51.708 |
| w3 | 141 | -0.029315 | -15.782 |
| w4 | 136 | 0.031029 | 124.898 |
| w5 | 159 | 0.025342 | -27.473 |
| w6 | 144 | -0.021635 | 83.406 |
| w7 | 144 | 0.004851 | -13.75 |
| w8 | 136 | 0.029403 | 29.52 |
| w9 | 162 | 0.050774 | -13.731 |
| w10 | 161 | -0.01083 | 20.424 |
| w11 | 119 | -0.001417 | 69.984 |
| w12 | 150 | 0.005036 | -1.423 |
| w13 | 126 | 0.015305 | -13.792 |
| w14 | 148 | -0.03035 | -60.662 |
| w15 | 128 | 0.007142 | 95.577 |
| w16 | 137 | 0.008402 | -41.545 |
| w17 | 164 | -0.006586 | 214.743 |
| w18 | 136 | 0.03005 | -19.015 |
| w19 | 134 | -0.006627 | 61.645 |
| w20 | 172 | -0.020276 | -27.964 |
| w21 | 134 | 0.0109 | 116.851 |
| w22 | 118 | -0.010548 | -10.942 |
| w23 | 150 | -0.035054 | -7.967 |
| w24 | 165 | 0.011435 | -48.275 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 119 | -0.018781 | -13.686 |
| w2 | 125 | 0.001751 | -43.09 |
| w3 | 132 | 0.021168 | -11.692 |
| w4 | 158 | 0.016741 | 67.098 |
| w5 | 176 | -0.004846 | -41.398 |
| w6 | 173 | -0.006147 | 10.554 |
| w7 | 146 | 0.004442 | -16.08 |
| w8 | 138 | -0.002297 | 11.055 |
| w9 | 159 | 0.021572 | -27.946 |
| w10 | 134 | 0.011753 | 157.883 |
| w11 | 114 | 0.01301 | 145.866 |
| w12 | 158 | 0.01209 | 30.391 |
| w13 | 70 | 0.012863 | 28.532 |
| w14 | 141 | -0.006221 | -45.483 |
| w15 | 121 | -0.017735 | 24.232 |
| w16 | 105 | -0.004341 | 28.469 |
| w17 | 129 | -0.006537 | 22.732 |
| w18 | 133 | 0.063317 | 31.186 |
| w19 | 134 | -0.016751 | 75.555 |
| w20 | 131 | 0.000156 | -14.584 |
| w21 | 151 | -0.013638 | 49.992 |
| w22 | 131 | 0.038663 | -46.069 |
| w23 | 128 | 0.008064 | 97.642 |
| w24 | 146 | 0.001343 | -57.333 |

