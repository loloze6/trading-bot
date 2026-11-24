# Backtest of 032-02.b1_choppy-downside-break-one-day-rebound_1d

- Plan: `../../../../03_test_plan/night7_rangefail_run/plans/032-02.b1_choppy-downside-break-one-day-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.048752 | 0.15 |
| w2 | 2 | 0.04303 | 0.181 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | -0.068838 | -1.894 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | 0.10763 | 0.192 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.009543 | 0.044 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | 0.030682 | 0.16 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.030317 | 0.088 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | 0.079872 | 0.988 |
| w21 | 0 | -0.002471 | 0.0 |
| w22 | 1 | -0.204021 | -1.818 |
| w23 | 0 | 0.001538 | 0.0 |
| w24 | 2 | 0.111053 | 0.678 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | -0.183904 | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | -0.052874 | -1.159 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | 0.097107 | 0.0 |
| w8 | 0 | -0.03611 | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.076739 | -0.435 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.020574 | -2.118 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | 0.069361 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | 0.122795 | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.05535 | 0.0 |
| w2 | 0 | 0.008964 | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 1 | -0.217179 | -1.354 |
| w5 | 2 | -0.148548 | -0.896 |
| w6 | 0 | 0.148163 | 0.0 |
| w7 | 0 | 0.148299 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.062497 | -0.595 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 1 | 0.039301 | 0.258 |
| w18 | 1 | 0.169854 | 2.156 |
| w19 | 1 | 0.035557 | 0.49 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | 0.023023 | 0.0 |
| w23 | 1 | 0.036808 | 0.285 |
| w24 | 0 | 0.01209 | 0.0 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | -0.18394 | -2.444 |
| w3 | 0 | -0.002797 | 0.0 |
| w4 | 1 | 0.04467 | 0.472 |
| w5 | 3 | 0.206196 | 4.131 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.163937 | 0.005 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | 0.030187 | 0.185 |
| w15 | 0 | 0.049498 | 0.0 |
| w16 | 2 | -0.026241 | -0.148 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | 0.136203 | 5.051 |
| w20 | 0 | 0.01435 | 0.0 |
| w21 | 2 | -0.051962 | -0.003 |
| w22 | 0 | 0.165377 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 1 | 0.053661 | 0.16 |
| w3 | 0 | 0.346715 | 0.0 |
| w4 | 0 | 0.019295 | 0.0 |
| w5 | 1 | -0.005544 | -0.022 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | 0.191893 | 0.0 |
| w8 | 2 | -0.098827 | -0.661 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | 0.059944 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.017986 | 0.112 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | 0.090517 | 0.322 |
| w16 | 1 | 0.042137 | 0.541 |
| w17 | 1 | 0.323625 | 3.417 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | -0.307497 | 0.0 |
| w20 | 1 | 0.090563 | 0.429 |
| w21 | 0 | 0.017992 | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | 0.033845 | 0.168 |
| w24 | 0 | None | 0.0 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.036754 | -0.008 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | 0.052642 | 0.0 |
| w4 | 1 | -0.069104 | -0.683 |
| w5 | 2 | 0.010666 | -0.053 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | 0.055302 | 0.233 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | -0.049074 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | 0.032118 | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | 0.147843 | 1.017 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | 0.274456 | 3.572 |
| w19 | 1 | 0.220953 | 0.392 |
| w20 | 1 | -0.099977 | -0.377 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

