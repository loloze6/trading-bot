# Build A8, A10, A11: a run judged by what it adds; one holding bar; the return at a 20 % fall (2026-11-27)

Branch `build-a8-a10`, from `ccr-6624e33e-aakrpv`. The operator's go: "Go for next" (2026-11-27), next steps A8, A10, A11.

## Purpose (written before the build)
1. **A10:** the bar a portfolio must beat (holding its coins) is one number, whatever the order of its strategies.
2. **A11:** every version shows its yearly return at the risk the operator accepts (a worst fall of 20 %).
3. **A8:** a run or a batch is read by what it adds to the portfolio, with one command.

## Expected outcomes (written before the build)
| # | Outcome | How it is seen |
|---|---|---|
| 1 | Holding's Sharpe on v3 and v4 is the same in every order of the strategies | a test; v3 and v4 measured in three orders |
| 2 | v3 and v4 stay ready (the designer: v4 is above both 1.075 and 0.945) | measured again |
| 3 | The portfolio's own numbers do not move (Sharpe 1.914, yearly +21 %, worst fall 9.7 %) | measured again |
| 4 | v4's scale is about 2 and its yearly return at a 20 % fall roughly +40 % | measured |
| 5 | Nights 7 to 9 together: without them 87 candidates and 6 strategies, Sharpe 1.88 against 1.91, yearly +17 % against +21 % (the designer's check), or the difference explained | `addition.py` |
| 6 | Calling `addition.py` twice gives the same file | compared byte by byte |
| 7 | Both test suites pass | run |
