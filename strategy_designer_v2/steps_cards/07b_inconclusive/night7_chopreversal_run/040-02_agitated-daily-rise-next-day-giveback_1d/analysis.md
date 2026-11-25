---
line: 7.b inconclusive
backtest: 040-02_agitated-daily-rise-next-day-giveback_1d
idea tested: 040-02_agitated-daily-rise-next-day-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3364 USD
---
## Findings
- **F1:** On agitated up days the next-day give-back is not graded by the rise: the fade gain is +0.62 % (t 3.68, 944 cases) after rises up to one usual move, then +0.16 % (t 0.48), +0.00 % (t 0.00) and +0.20 % (t 0.29) for larger rises. The slope of the next-day excess return on the rise is +25.9 bp per usual move (t 1.99, 1505 cases), the wrong sign. This matches step 5's failed slope (−9.3e-05) and its main t of 1.33.
- **F2:** The up-side fade also changes sign across windows. It is −1.06 % (t −2.37, 320 cases) in w11 against +2.55 % (t 4.64) in w18. By coin it is positive everywhere but clear only in XMR (t 2.33) and ZEC (t 2.22), so the small average edge is mixed rather than a steady effect.
- **F3:** The mirror side carries the brief's graded reversal. On agitated down days the slope of the next-day excess return on the fall is −93.2 bp per usual move (t −5.64, 1439 cases), negative in all six coins (t from −1.77 to −3.01). On calm down days the same slope is only −21.9 bp (t −2.10), so the reversal is stronger in agitated markets, as the brief claims.
- **F4:** Inside agitated markets the graded rebound after falls lives in a falling trend. There the slope is −134.0 bp per usual move (t −7.12, 377 cases), against −6.2 bp (t −0.14, 358 cases) in a rising trend.
- **F5:** The rebound is largest after the largest agitated falls, which makes it large against costs. The largest-fall tercile rebounds +1.37 % (t 2.26 over 199 days). Falls beyond three usual moves rebound +4.16 % (t 4.13, 56 cases). Both are far above the 0.19 % cost of a trade, while the tested idea's unusual move is only +0.38 % per case.
- **F6:** The down-side effect is not uniform across windows. It is strong in w15 (−134 bp, t −3.12) and w16 (−143 bp, t −4.26), but flat or reversed in w10, w12 and w13 (t −0.16, +0.05, +0.71), so it needs the held-out folds to confirm it.

## Ideas
- `040-02.b1_falling-agitated-fall-rebound` (from F3, F4, F5, F6): In a falling, agitated market, the larger a coin's one-day fall, measured as its percent change from the previous close, the larger its rise over the next day.
- `040-02.b2_agitated-daily-fall-rebound` (from F3, F5): In an agitated market, the larger a coin's one-day fall, measured as its percent change from the previous close, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
