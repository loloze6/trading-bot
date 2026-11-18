---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-02_weekend-drop-rebounds-monday
line: 7.b inconclusive
backtest: 011-02_weekend-drop-rebounds-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 2 days (Monday and Tuesday), and the larger the weekend drop, the larger the rebound.
Consequence: Weekend drops are partly undone once weekday liquidity returns.
Why:
- F1: The test's main measure is on the predicted side but short of the bar: the forecast-weighted excess 2-day return after Sunday drops has t 1.35 over 1197 cases (my recount: t 1.30, n 1196), and the top-minus-bottom-third check passes (+0.0025). The six coins all have positive per-coin means but per-coin t only 0.04 to 1.44, so the sign is consistent and the size is too small for these six coins.
- F2: The plain rebound exists but is weakly graded. Sunday drops are followed by a mean excess 2-day return of +0.0065 (t 2.84, n 967), against +0.00044 after weekday drops (Welch t, Sunday minus weekday, 2.46). Yet the deepest quartile of drops rebounds less (+0.0047, t 0.90) than the second and third quartiles (+0.0113 and +0.0101, t 2.64 and 2.20). The depth-weighted product therefore reaches only t 1.53, and the grading the plan rewards is what dilutes it.
- F6: More data is available. Thirteen more coins (ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO) have folds A and D, plus parts of B and C. This could multiply the 1197 cases, which is what a positive t of 1.35 needs.
