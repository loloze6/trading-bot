---
line: 7.g patterns
backtest: 034-01.b1_nearness-to-high-10-days_1d
idea tested: 034-01.b1_nearness-to-high-10-days
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4666 USD
---
## Findings
- **F1:** The book's gain comes almost entirely from long positions in the rising profile: their summed gain before costs is +8.45 (mean +0.226 % per bar, 3741 bars). Shorts in the rising profile summed only +0.11 (1958 bars). Short trades lost 8.66 % on average after fees over 438 trades, against +16.3 % for 858 long trades. The far-below-high side does not fall by more than the coin's drift.
- **F2:** Inside the rising profile, the nearness-to-high slope on the 10-day excess return lives in calm markets. With cases of one day clustered, the slope is +0.0228 (t 2.25, 242 cases, 59 days) when the coin's 30-day swing is at or below its median. It is +0.0117 (t 1.08, 212 cases, 60 days) when the swing is above it.
- **F3:** Split by the coin's own 20-day volatility tercile inside the rising profile, the slope is clear in the low and mid terciles and absent in the high one: low t 3.27 (121 cases), mid t 3.33 (157 cases), high +0.0054, t 0.35 (176 cases).
- **F4:** Outside the rising profile the same calm/agitated split appears. In calm markets the slope is +0.0215 over 10 days (t 1.98, 311 cases, 76 days) and +0.0131 over 5 days (t 1.90, 614 cases, 146 days). In agitated markets it is -0.0095 (t -0.69) and -0.0028 (t -0.46).
- **F5:** In the rising profile the effect is graded across distance bins. Mean 10-day excess return is -4.2 % below -6 swings (10 cases), -2.2 % from -6 to -4 (40), -1.5 % from -4 to -2.5 (87), +0.2 % from -2.5 to -1.5 (91), +5.9 % from -1.5 to -0.5 (121), and +8.9 % above the high (63).
- **F6:** The effect fades with horizon. In the rising profile the slope's t is 2.12 at 5 days (906 cases), 2.73 at 10 days (454) and 1.31 at 20 days (218). Outside the rising profile it turns negative at 20 days (t -2.16, 268 cases).
- **F7:** Other angles did not stand out once cases on the same day are counted together:

## Ideas
- `034-01.b1.g1_calm-rising-nearness-drift` (from F2, F3, F5, F1): In a rising, calm market, the closer a coin's daily close sits below its 20-day high, measured in units of its own daily swing over the last 20 days, the more it rises over the next 10 days, and more still the further the close stands above that high.
- `034-01.b1.g2_calm-market-nearness-short-drift` (from F4, F2, F3, F6): In a calm market, the closer a coin's daily close sits to its 20-day high, measured in units of its own daily swing over the last 20 days, the more it rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
