---
backtest: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.541 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.241 | above 0 | no |
| Mean daily return, on days in a position | 0.003337 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.178 | above 0 | yes |
| Calmar | 4.788 | above 0.75 | yes |
| Trades per day | 0.2447 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.161 % |
| Yearly return | +162.6 % (over 1.99 years) |
| Days in a position | 86 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night4_fallingbounce_run/unseen_2016_2017/backtests/025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
