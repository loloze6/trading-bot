---
backtest: 058-02.b1.g1.b2.b1_agitated-falling-selloffs-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9929 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4233 | above 0 | yes |
| Mean daily return, on days in a position | 0.002249 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.833 | above 0 | yes |
| Calmar | 0.6761 | above 0.75 | no |
| Trades per day | 0.07027 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.529 % |
| Yearly return | +10.0 % (over 7.94 years) |
| Days in a position | 12 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.g1.b2.b1_agitated-falling-selloffs-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
