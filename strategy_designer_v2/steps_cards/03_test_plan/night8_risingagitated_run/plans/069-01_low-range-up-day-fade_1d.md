---
idea: 069-01_low-range-up-day-fade
brief: 069_low-in-range-rise-fades
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 78914cf300b5
---
Fidelity:
- Situation: a coin closes up on the day -> kept: a regime rule, the 1-day return above 0; the book is flat on every other bar.
- Comparison: the lower the close sits in its 20-day high-low range, the larger the fall -> kept: the 20-day high-low range position, more negative toward the bottom, sets the short size.
- Outcome: it falls over the next day -> kept: short for 1 bar; long-only side removed per the brief's "short only".
- Verdict transfer: yes: the test shorts exactly the up days, sized by how low the close sits in the 20-day range, over the next day.
Forecast: Only on bars whose 1-day return is above 0, the forecast is the close's position in its 20-day high-low range, from -20 at the range's low to +20 at its high. It is standardised over its last 60 values (20 minimum) and clipped at 0 from above. The forecast is therefore negative (short) when the close sits in the lower half of the range, and larger in size the nearer the close is to the 20-day low. It is 0 at or above mid-range. It is 0 on every down or flat day.
Config: 069-01_low-range-up-day-fade_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Criterion:
- Horizon: 1 bar
- Main measure: Each case is a bar with forecast below 0. For each case, take the next-day return minus the coin's mean daily return over all windows. Multiply it by -forecast / 10, giving the short's excess gain weighted by size. Report the mean and its t, with cases pooled per day.
- Supporting check: Compare the mean next-day excess return of the cases with forecast at or below -10 against that of up days with forecast 0 (deep minus non-short). The difference must be below 0.
- Confirm: The main measure's mean is above 0 with t ≥ 2, and the supporting difference is below 0.
- Reject: The main measure's mean is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2, or a confirming t with a supporting difference at or above 0. A verdict needs at least 200 days with a case.
