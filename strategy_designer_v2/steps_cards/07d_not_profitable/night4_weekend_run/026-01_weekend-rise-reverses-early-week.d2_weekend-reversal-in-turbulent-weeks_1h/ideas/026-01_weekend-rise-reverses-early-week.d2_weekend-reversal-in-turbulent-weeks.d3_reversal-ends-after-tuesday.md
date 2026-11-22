---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks
line: 7.d not profitable
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's price rises from Saturday 00:00 UTC to Monday 00:00 UTC, it falls over the following two days, only while the coin's 30-day hourly volatility is high against its own last 6 months, and from Wednesday over the next five days it returns to rising with its normal drift, the more so the larger the weekend gain was.
Consequence: A trader would close the fade by Tuesday's end and carry no short past it, since shorts held into the rest of the week give back most of what the two days earned.
Why:
- F3: 18.8 % of cases still hold a short after the 48 bars, and the book is short on about 12 % of all Wednesday-to-Sunday bars. Those bars lose −0.526 in summed gain, which is about two thirds of the Monday–Tuesday gain. The 86 trades held over 200 hours average −4.24 % each before fees.
- F2: The Monday–Tuesday hold itself pays: its gain before costs sums to +0.822 (Monday +0.081, Tuesday +0.741). Per case it is +0.122 % of the book over the 48 bars, with t 0.84 over 563 cases. Each case's entry and exit fees are about 0.072 % of the book. So the hold nets roughly +0.05 % per case before what happens after it.
- F6: The effect exists and is large per case: an unusual fall of +0.84 % over 48 bars (strength 0.118, t 2.80, 557 cases), against a 0.19 % cost per trade. But it is earned against the coin's normal drift (−0.27 % in the short's direction), and the book is short only, with a mean position of −0.39 of the book at entry.
