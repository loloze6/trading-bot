---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size
line: 7.d not profitable
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just risen in an unbroken streak of four-hour periods, it keeps rising over the next three days, and the larger the streak's gain relative to the coin's typical four-hour move over the past 30 days, the larger the further rise, only while the coin's 30-day return is positive, and the more so the larger that 30-day return.
Consequence: Join strong 4-hour up-runs for three days when the coin is already up over the past month, and refuse them when it is down over the month, which is where the book's deep falls came from.
Why:
- F1: The Calmar failed because the book falls with the coin rather than apart from it: its deepest fall is -75.3 % over 276 days (w12–w14), while the coins fell -81.2 %, with a mean position of 0.75. The next falls show the same pattern: -70.2 % over 223 days (w1–w3) against the coins' -66.9 % at a position of 0.96, and -40.0 % (w19–w20) against -30.3 % at 1.19.
- F3: Up-streak cases gain more when the coin's 30-day return is high. The excess 18-bar return is -0.18 % in the lowest 30-day-return quintile (mean -28 %, t -0.45, 426 cases) and +0.64 % in the highest (mean +57 %, t 1.14, 426 cases). Cases with a positive 30-day return beat those with a negative one by 0.43 % (Welch t 1.20, 1142/988 cases). The rank correlation over all cases is only -0.003, so the gain sits mainly in the top quintile.
- F4: The book's coin-days also do better after a higher 30-day return. Its mean daily return is 0.30 % in the top 30-day-return quartile against 0.06 % in the bottom one, where daily risk is highest (sd 5.2 % against 5.1 % and 4.2–4.5 % in the middle quartiles). The book earns 0.22 % a day when the 30-day return is positive and 0.06 % when it is negative.
- F5: As a diagnostic, keeping only the coin-days with a positive 30-day return cuts the deepest fall from -89 % to -57 % and lifts Calmar from 0.28 to 0.64 and Sharpe from 0.68 to 0.91, while the mean daily return goes from 0.14 % to 0.11 %. (The -89 % is measured on the subset of days with a known 30-day return, which is why it differs from the -75 % in F1.)
