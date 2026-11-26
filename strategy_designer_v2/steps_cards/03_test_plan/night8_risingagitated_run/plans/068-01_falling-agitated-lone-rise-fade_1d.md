---
idea: 068-01_falling-agitated-lone-rise-fade
brief: 068_falling-agitated-first-bounce-fades
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 78914cf300b5
---
Fidelity:
- Situation: in a falling, agitated market, a day that closes up -> adapted: the up close is a regime (one-day return above 0); code adds the profile.
- Comparison: the more of the five days before it closed down -> kept: graded by the count of prior closes, as 5 minus the count of up closes in days t-5..t-1 (flat closes are rare).
- Outcome: the coin falls over the next day, more after more falls -> kept: short over 1 bar, sized by the count.
- Verdict transfer: yes: the test bets short exactly on up days in the profile, sized by the number of falls in the five days before.
Forecast: The regime is active only on bars whose one-day return (PriceEvolutionComponent, period 1) is above 0, inside the code-added falling-agitated profile; every other bar is flat. Inside the regime, the forecast has two parts: - u is the number of up closes among the five days before bar t (PriorBreakoutCloseCountComponent, window 5, period 1, bar t excluded). Since flat closes are rare, the number of falls is 5 - u. - u is standardised (60/20, about 4u at a typical past mean of 2.5) with weight 1. It is mixed with the constant standardised and negated (-10) at weight 2. The forecast is (S(u) - 20) / 3. Because standardise caps S(u) at 20, the forecast is never above 0, so the book is short only. It is about 0 after five prior rises and grows short, linearly, with each further prior fall, to about -6.7 after five falls.
Config: 068-01_falling-agitated-lone-rise-fade_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The unusual move per case, taken in the short direction. A case is a short bet: the forecast falling by at least 2 points. Its value is minus (next-day return minus the coin's mean daily return over all windows). Its t is computed with the cases of one day taken together.
- Supporting check: On regime bars (up days in the profile), take the mean next-day return of bars with prior_ups 0 or 1 (4 to 5 prior falls) minus that of bars with prior_ups 4 or 5 (0 to 1 prior falls). The check passes if this difference is below 0.
- Confirm: The mean unusual move is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The mean unusual move is below 0 with t ≤ -2 (the up day is followed by a rise beyond the drift).
- Inconclusive: Anything else is inconclusive: a t between -2 and 2, or a confirming t with a failed check. At least 30 cases on at least 30 distinct days are required, else inconclusive.
