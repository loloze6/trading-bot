---
line: 7.c rejected
backtest: 002-05_sma-up-regime-positive-drift_1d_minus1pct
idea tested: 002-05_sma-up-regime-positive-drift
step 5: rejected
step 6: none
mode: one call
explorations: 2
cost: 0.1864 USD
---
## Findings
- **F1:** The rejection comes from the gap between one bar's close and the next bar's open, not from trading during the bar. On in-stretch bars the next open sits a mean −0.9985% below the prior close, with a standard deviation of only 0.025%. 99.66% of the 290 in-stretch bars fall within ±0.1% of exactly −1%. On out-of-stretch bars the gap is −0.0007%, and 99.77% of the 434 bars fall within ±0.1% of zero.
- **F2:** Without that gap, in-stretch bars do not differ from out-of-stretch bars. The next bar's open-to-close return is +0.113% in-stretch against −0.030% out-of-stretch (Welch t 0.69). The share of up bars is 47.6% against 47.5%.
- **F3:** The constant −1% gap shows up in every window that has in-stretch bars: w1 −1.004%, w4 −0.996%, w5 −1.000% and w6 −0.997%. It also shows up at every stretch age, between −0.993% and −1.003% for ages 0–10, 10–30, 30–60 and 60–120 bars. It does not grow with forecast size either: the mean close-to-close return is −1.19%, −0.85%, −0.54% and −0.97% across forecast quartiles. A market effect would vary across these; a fixed offset does not.
- **F4:** The close-to-close result (−0.856 pp difference, t −4.14; 20.5 pp fewer up bars) is fully explained by the −1% gap. The rest of the next bar adds −0.86 + 1.00 ≈ +0.14 pp, which is no measurable reversal.
- **F5:** The next bar's high-low range is narrower in-stretch, 3.42% of the open against 4.42% out-of-stretch. No test statistic was computed for this, and every window lost money for the coin (from −18% to −73%), so this cannot be separated from the regime mix.

## Ideas
- No ideas: The rejection rests on a fixed −1% close-to-open shift placed on exactly the in-stretch bars. That shift is a property of this data, not of the market: BTC trades around the clock, so a real market has no such gap. Once the shift is removed, the in-stretch bars show neither persistence nor reversal (t 0.69), so no finding supports a market idea in either direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
