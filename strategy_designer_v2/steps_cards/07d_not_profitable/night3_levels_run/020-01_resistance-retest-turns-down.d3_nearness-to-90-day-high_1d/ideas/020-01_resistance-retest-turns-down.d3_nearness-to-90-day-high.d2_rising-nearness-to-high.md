---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits below its highest close of the past 90 days, the more it rises over the next 5 days, and the more so the more that nearness has grown over the past 10 days.
Consequence: A trader should be most long when the coin is near its 90-day high and still climbing toward it, and least long when it sits near the high after slipping back from it.
Why:
- F1: The check failed on Calmar (0.72 against the 0.75 rule) because of two deep falls: 42 % from w12 to w14, while holding the coins fell 79 % over the same stretch, and 42 % from w1 to w7, while holding fell 75 %; the book's yearly return is 30 % against holding's 13 %.
- F3: Inside the falling legs, nearness to the 90-day high is followed by falls instead of rises. The nearest quintile, held at a position of 1.05, loses 0.32 % per bar, and its 5-day return is -1.27 % (t -2.32, 253 cases); middle nearness is also followed by falls, -1.11 % to -1.79 % (t -2.4 to -3.1). Outside the legs, the nearest quintile is followed by +3.98 % (t 5.51, 449 cases).
- F5: Across all bars, the gain is concentrated where nearness is high and climbing. The nearest quintile earns 0.35 % per bar (5-day return +2.09 %, t 4.08, 702 cases). The quintile whose nearness rose most over the past 10 days carries 11.4 of the book's 16.4 summed bar gain (5-day return +1.40 %, t 3.05, 632). Near-high closes that are also a 10-day closing high earn 0.66 % per bar (+2.88 % over 5 days, t 3.18, 274), against 0.15 % (+1.58 %, t 2.61, 428) for those that are not.
