---
line: 7.g patterns
backtest: 058-01.b1_rally-giveback-all-coins_1d
idea tested: 058-01.b1_rally-giveback-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4007 USD
---
## Findings
- **F1:** Inside the falling, agitated profile (folds B, C), the 5-day unusual move does not grow with the 3-day scaled rise. By rise quintile, from smallest to largest, the raw unusual move is +4.6 %, -1.3 %, +2.2 %, -2.7 % and -0.7 %, with day-clustered t of 1.14, -0.53, 1.04, -1.30 and -0.39, on 21 to 35 days each. The largest rises show no graded give-back, which agrees with step 5's failed supporting check (top minus bottom give-back share -0.37).
- **F2:** The book loses on its trades whatever their size. All 444 trades are short. Their mean net return is -2.88 %, -2.81 %, -3.46 % and -1.09 % by entry-forecast quartile. Book days average near 0 in every window, and w16 is the worst (summed -8.4 %).
- **F3:** Outside the profile, a coin's 10-day move against its 30-day swing tends to continue over the next 5 days, but only at the edges. By 10-day quintile the unusual 5-day move is -1.6 %, -2.2 % (t -2.58), +0.6 %, +1.1 % and +2.2 % (t 1.87), on about 272 cases per quintile. Split by size, the continuation reaches t 2.13 only in the largest-rise tercile and t 2.06 only in the middle-fall tercile. No other value passes 2.6.
- **F4:** Split by profile and side, that continuation is borderline everywhere and reverses in rising agitated markets:
- **F5:** Outside the profile, next-day unusual returns differ by weekday: Wednesday -0.61 % (t -3.32), Thursday +0.50 % (t 3.38), Friday +0.44 % (t 3.18). These t values are not clustered by day, so the coins of one day count as separate cases and the t values are overstated. The late-week gain is also already held (045-01, "rising market late week gain").

## Ideas
- No ideas: Across the 10 angles examined (scaled rises over 3, 5 and 10 days, range, close location, weekday, trend and agitation profiles, years, coins, trades), no pattern stood out beyond what that many looks produce by chance. The best ones are a borderline momentum outside the profile (t about 2, F3, F4) and a weekday effect that is overstated and already held (F5). The brief's graded give-back is absent inside its profile (F1).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
