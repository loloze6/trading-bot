---
line: 7.d confirmed, not profitable
backtest: 081-01.d3_deep-up-day-fade-outside-uptrends_1d
idea tested: 081-01.d3_deep-up-day-fade-outside-uptrends
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4495 USD
---
## Findings
- **F1:** The fade is carried entirely by the deeper up days, and the shallow fifth loses. By forecast quintile, the next-day unusual short return runs from +1.13 % (t 3.80, 532 cases) in the deepest fifth, to +0.74 % (t 3.42), +0.51 % (t 2.39), +0.36 % (t 2.06), and finally to −0.22 % (t −1.13) in the shallowest fifth. Only the deepest fifth's total move (+0.88 %, t 2.95) is about four times the 0.22 % trade cost; the shallowest fifth's total move is −0.48 % (t −2.42).
- **F2:** In the book, gross gain per active bar is 81 bp in the deepest quintile, 34 bp, 7 bp, 0.3 bp, and −2.7 bp in the shallowest. Net of an approximate 0.11 % per unit traded, the bottom two quintiles lose (−1.7 bp and −3.6 bp) while still turning the book over (0.19 and 0.09 of the book per bar), so the shallow cases add fees and swings but no gain.
- **F3:** The fade is much stronger when the coin is agitated, and agitation alone does not earn it.
- **F4:** The effect is the theory's own relief-selling on up days. Down days outside rising trends at the deeper half of depth show +0.07 % (t 0.42, 1252) unusual short return, against +0.65 % to +1.50 % for deep up days. The effect holds across 60-day trends, at +0.56 % (t 2.26) below −30 %, +0.74 % (t 3.97) from −30 % to −10 %, and +0.60 % (t 2.60) when choppy.
- **F5:** The horizon is right at one day.
- **F6:** The book's falls come from a few large squeezes.

## Ideas
- `081-01.d3.d1_deep-up-day-fade-agitated` (from F3, F4, F1): In an agitated market, a day that closes up while sitting deeper below the coin's 20-day high, measured in the coin's own usual daily swing over the last 20 days, is followed by a larger fall over the next day, except when the coin has been rising over the last 60 days.
- `081-01.d3.d2_unusually-deep-up-day-fade` (from F1, F2, F5): In any market, a day that closes up while sitting deeper below the coin's 20-day high than its usual depth over the last 60 days, measured in the coin's own usual daily swing over the last 20 days, is followed by a fall over the next day that grows with how far that depth exceeds its usual depth, except when the coin has been rising over the last 60 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
