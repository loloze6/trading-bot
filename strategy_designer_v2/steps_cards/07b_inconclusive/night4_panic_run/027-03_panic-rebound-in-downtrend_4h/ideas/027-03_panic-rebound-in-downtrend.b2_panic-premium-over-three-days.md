---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-03_panic-rebound-in-downtrend
line: 7.b inconclusive
backtest: 027-03_panic-rebound-in-downtrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: A 24-hour stretch in which the coin falls hard while its range is several times its 30-day average is followed by higher than usual returns over the next 3 days, and the further the range exceeds its 30-day average, the higher the return.
Consequence: A trader providing liquidity into a panic should expect the premium to be paid mostly in the first few days, and more so in the most violent panics.
Why:
- F4: The premium is clearest over the next 3 days (18 bars), and it grows with how far the range exceeds its average. Falls with a range of at least 3x give +4.07 % over 18 bars, t 3.98 on 109 cases. Falls with a range of at least 2x give only +1.72 %, t 3.17 on 335 cases.
- F5: Grading by depth of fall did not work in the test, because the forecast saturates. Deep and mid terciles both sit at the forecast cap of 20, so the forecast-weighted check reads exactly 0. The 84-bar returns do not rise with depth: −2.6 % for deep, +7.4 % for mid, −1.2 % for shallow.
