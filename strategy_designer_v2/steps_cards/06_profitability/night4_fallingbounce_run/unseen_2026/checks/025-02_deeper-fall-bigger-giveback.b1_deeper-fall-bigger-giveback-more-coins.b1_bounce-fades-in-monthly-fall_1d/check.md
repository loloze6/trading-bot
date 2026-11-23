---
backtest: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.194 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.26 | above 0 | no |
| Mean daily return, on days in a position | -0.002351 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.791 | above 0 | no |
| Calmar | -0.8582 | above 0.75 | no |
| Trades per day | 0.01017 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.075 % |
| Yearly return | -1.7 % (over 0.87 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_fallingbounce_run/unseen_2026/backtests/025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
