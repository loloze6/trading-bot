# Backtest of 087-01_agitated-rise-scaled-burst-continues_1d

- Plan: `../../../../03_test_plan/night10_riseagilong_run/plans/087-01_agitated-rise-scaled-burst-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: LTC, ETH, XMR, INJ, GRT, DOGE, XRP, TRX as LTCUSD, ETHUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, XRPUSD, TRXUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | -0.136959 | 0.0 |
| w3 | 2 | -0.188924 | -9.293 |
| w4 | 7 | -0.068014 | -22.204 |
| w5 | 9 | -0.068684 | -11.824 |
| w6 | 9 | 0.250102 | 39.89 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 6 | -0.014279 | 10.577 |
| w11 | 3 | 0.039039 | 13.433 |
| w12 | 0 | None | 0.0 |
| w13 | 3 | 0.03104 | 2.271 |
| w14 | 3 | 0.010085 | 2.077 |
| w15 | 14 | 0.023545 | 26.217 |
| w16 | 15 | -0.130007 | 0.118 |
| w17 | 1 | -0.019293 | -1.882 |
| w18 | 2 | 0.033701 | 0.582 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 1 | -0.099142 | -2.472 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | -0.005556 | -1.096 |
| w24 | 0 | None | 0.0 |
| w25 | 7 | -0.155644 | -1.321 |
| w26 | 0 | None | 0.0 |
| w27 | 19 | 0.026006 | 4.764 |
| w28 | 2 | 0.056801 | -4.555 |
| w29 | 0 | None | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 7 | 0.128085 | 10.324 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | -0.057633 | 2.104 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | 0.002325 | -0.579 |
| w14 | 5 | -0.093766 | -2.683 |
| w15 | 10 | -0.018038 | -15.994 |
| w16 | 8 | 0.049111 | 17.611 |
| w17 | 6 | -0.053501 | 2.986 |
| w18 | 2 | 0.030582 | 1.766 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.025351 | -1.938 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.010562 | -2.875 |
| w25 | 2 | -0.074226 | -4.833 |
| w26 | 4 | -0.035853 | -3.843 |
| w27 | 9 | 0.130614 | 13.181 |
| w28 | 2 | 0.024049 | 1.932 |
| w29 | 4 | -0.057164 | -4.855 |
| w30 | 1 | -0.022664 | -3.105 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.117901 | -1.741 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 3 | -0.167412 | -22.858 |
| w12 | 0 | None | 0.0 |
| w13 | 3 | -0.120618 | -14.943 |
| w14 | 2 | -0.06048 | -3.309 |
| w15 | 5 | -0.147175 | -6.175 |
| w16 | 6 | -0.140252 | -6.476 |
| w17 | 2 | -0.010965 | -2.51 |
| w18 | 2 | -0.037199 | 1.757 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.031579 | -5.955 |
| w25 | 0 | None | 0.0 |
| w26 | 5 | 0.079096 | 18.928 |
| w27 | 5 | -0.224301 | -9.476 |
| w28 | 9 | -0.021156 | -1.831 |
| w29 | 5 | -0.091895 | -24.26 |
| w30 | 9 | -0.125863 | 3.282 |
| w31 | 1 | 0.184959 | 19.005 |
| w32 | 1 | -0.204102 | -9.684 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 5 | -0.098159 | -13.761 |
| w26 | 1 | -0.125573 | -13.447 |
| w27 | 3 | -0.004149 | 2.401 |
| w28 | 3 | 0.061809 | 3.245 |
| w29 | 3 | 0.023345 | -8.761 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 3 | 0.077107 | 4.965 |

- GRTUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 0 | None | 0.0 |
| w24 | 6 | -0.2082 | -24.997 |
| w25 | 7 | 0.016585 | 5.991 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | -0.010169 | 7.84 |
| w28 | 2 | 0.018681 | 1.515 |
| w29 | 1 | -0.097348 | -8.766 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 0 | None | 0.0 |
| w21 | 1 | 0.123867 | 9.588 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | -0.085025 | -10.794 |
| w25 | 7 | 0.1067 | 25.72 |
| w26 | 1 | -0.049294 | -2.69 |
| w27 | 4 | 0.240372 | 52.249 |
| w28 | 3 | -0.012395 | -10.819 |
| w29 | 3 | -0.03675 | -5.92 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- XRPUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w6, w7, w8, w9, w10, w11 (the coin's history is shorter than the plan's warm-up: 790 days asked); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 1 | -0.080404 | 1.175 |
| w13 | 1 | 0.064324 | 4.726 |
| w14 | 1 | 0.095888 | 6.565 |
| w15 | 2 | 0.110183 | 18.663 |
| w16 | 11 | 0.112204 | 55.884 |
| w17 | 1 | -0.070972 | -5.406 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w21 | 0 | 0.010821 | 0.0 |
| w22 | 0 | -0.055489 | 0.0 |
| w23 | 1 | -0.063363 | -3.464 |
| w24 | 4 | 0.002631 | -8.763 |
| w25 | 4 | -0.11255 | -10.256 |
| w26 | 5 | -0.057983 | -5.013 |
| w27 | 5 | 0.275602 | 102.397 |
| w28 | 9 | -0.079432 | -1.46 |
| w29 | 1 | -0.052469 | -3.281 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 1 | 0.251013 | 22.914 |

- TRXUSD: 12 of 32 windows run. 20 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days); w15, w16, w17, w18, w19, w20 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.101903 | -2.293 |
| w23 | 1 | -0.150847 | -10.668 |
| w24 | 2 | -0.014308 | -4.849 |
| w25 | 7 | -0.123834 | -6.874 |
| w26 | 7 | 0.216151 | 26.908 |
| w27 | 7 | 0.102728 | 30.319 |
| w28 | 4 | 0.035925 | -1.175 |
| w29 | 0 | None | 0.0 |
| w30 | 3 | 0.027157 | 6.069 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

