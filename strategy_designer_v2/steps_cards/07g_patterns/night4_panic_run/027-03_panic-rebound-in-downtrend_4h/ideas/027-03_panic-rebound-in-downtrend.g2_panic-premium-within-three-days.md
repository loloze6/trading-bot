---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-03_panic-rebound-in-downtrend
line: 7.g patterns
backtest: 027-03_panic-rebound-in-downtrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a panic, a 24-hour stretch whose bar ranges are several times their 30-day average while the price falls, the coin rises over the next 3 days. The rise is larger the larger the range expansion of the stretch.
Consequence: The panic premium is a short-horizon trade of one to three days, and holding it for 14 days gives back its edge to the coin's noise.
Why:
- F4: In the strategy's panic events, the premium shows within days and fades by the tested 14-day horizon. These events (range at least 3× its 30-day average with a fall, any prior trend, first per 14-day cell, 124 events) are followed by +2.75 % over 24 hours (t 3.73) and +4.38 % over 3 days (t 3.03). Over 14 days the unusual move has a t of only 1.18 for all 124 events and 2.11 for the 45 with a negative prior 30-day return. The step-5 verdict on 40 cases was t 0.99.
- F3: Range expansion carries the 24-hour reversal on both sides. A deep fall with the 6-bar range in its top tercile against its 30-day average is followed over 24 hours by +0.78 % (t 5.70, 1 811 cases). The same fall in the bottom range tercile is followed by −0.47 % (t −1.89, 350 cases). A large rise in the top range tercile is followed by −0.42 % (t −2.85, 1 647 cases).
- F5: Inside panics, the 14-day move is not graded by depth of fall. The deepest-fall tercile (median −7.3 units) is followed by −2.58 % (t −1.32, 42 events) and the mildest by +3.74 % (t 0.56, 42 events). The tested idea's supporting check passed with a difference of 0, so the "more extreme, more premium" part has no support at 14 days.
- F7: The book held 14 days and traded 0.0042 times a day, so it sat through the drift after the rebound rather than capturing it. Its Sharpe was 0.15, against holding's Sharpe higher by 0.40, and its mean daily return was 0.006 %.
