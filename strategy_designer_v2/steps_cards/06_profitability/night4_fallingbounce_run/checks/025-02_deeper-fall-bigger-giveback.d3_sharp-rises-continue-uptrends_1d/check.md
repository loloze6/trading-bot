---
backtest: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6812 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1271 | above 0 | yes |
| Mean daily return | 0.0008685 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4862 | above 0 | yes |
| Calmar | 0.3932 | above 0.75 | no |
| Trades per day | 0.06146 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
