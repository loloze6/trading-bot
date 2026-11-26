---
backtest: 058-02.g1_choppy-agitated-deep-fall-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.0952 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.462 | above 0 | no |
| Mean daily return, on days in a position | 0.0002684 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.277 | above 0 | no |
| Calmar | 0.03422 | above 0.75 | no |
| Trades per day | 0.02834 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.427 % |
| Yearly return | +0.5 % (over 7.94 years) |
| Days in a position | 8 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-02.g1_choppy-agitated-deep-fall-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
