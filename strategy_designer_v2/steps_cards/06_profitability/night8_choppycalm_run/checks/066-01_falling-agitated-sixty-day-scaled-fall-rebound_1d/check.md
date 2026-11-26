---
backtest: 066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8083 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2555 | above 0 | yes |
| Mean daily return, on days in a position | 0.00251 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7 | above 0 | yes |
| Calmar | 0.915 | above 0.75 | yes |
| Trades per day | 0.04019 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.421 % |
| Yearly return | +6.4 % (over 7.94 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
