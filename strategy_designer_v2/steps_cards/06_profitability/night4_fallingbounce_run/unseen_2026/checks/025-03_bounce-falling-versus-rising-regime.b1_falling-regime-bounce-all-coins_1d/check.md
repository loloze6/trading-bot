---
backtest: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.07362 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.14 | above 0 | no |
| Mean daily return, on days in a position | -6.947e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.877 | above 0 | no |
| Calmar | -0.1831 | above 0.75 | no |
| Trades per day | 0.2282 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.485 % |
| Yearly return | -6.0 % (over 0.87 years) |
| Days in a position | 82 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_fallingbounce_run/unseen_2026/backtests/025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
