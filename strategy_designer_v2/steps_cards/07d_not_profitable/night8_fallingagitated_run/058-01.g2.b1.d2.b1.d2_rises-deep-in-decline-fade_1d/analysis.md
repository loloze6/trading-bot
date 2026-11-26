---
line: 7.d confirmed, not profitable
backtest: 058-01.g2.b1.d2.b1.d2_rises-deep-in-decline-fade_1d
idea tested: 058-01.g2.b1.d2.b1.d2_rises-deep-in-decline-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4351 USD
---
## Findings
- **F1:** The Calmar failure comes from one squeeze: the book's deepest fall, -7.7 %, is in w14, and it is built on its three worst days (-7.1 %, -3.9 %, -3.5 %), when the coins it held rose +11.0 %, +12.5 % and +5.9 %; all 15 worst book days are days the held coins rose (+1.2 % to +12.5 %), so the falls are short positions caught in rallies that kept going, not in ordinary noise.
- **F2:** The book is short almost only on the signal's own bars (98.5 % of position bars are up days), and the losing positions have a profile of their own: of its 25 worst positions, 52 % followed a rise of more than 0.97 usual swings (19 % of all positions), 96 % had the four days before falling, and their mean size was 0.61 of the book against about 0.3 overall; together they summed -1.78 against a total position gain of +1.28.
- **F3:** The effect is missing on the largest one-day rises, which the forecast's uncapped component (a) and the volatility sizing load most: signal bars by rise in usual swings give an unusual next-day fall of +1.00 % (t 2.24), +1.00 % (t 1.83), +0.82 % (t 1.90) and +1.37 % (t 2.07) in the four lower fifths, up to 0.97 swings, against +0.04 % (t 0.08) in the top fifth (128 cases each); positions in the top fifth carry the largest size (0.56) and lose (-0.05 summed).
- **F4:** The loss sits where a rise of more than 0.97 usual swings ends a four-day fall: those 77 cases give -0.46 % (t -0.70) at a mean size of 0.61 and sum -0.20, while rises up to 0.97 swings after a four-day fall give +1.19 % (t 3.07, 303 cases) and sum +0.94, the largest share of the book's gain.
- **F5:** The deeper the four-day fall before an up day, the larger the give-back: by the prior four-day return in usual swings, the deepest fifth gives +2.56 % (t 4.14, 128 cases, positions summing +1.04), against -0.40 % to +0.43 % in the middle fifths. This depth is not an effect of its own: on in-profile down days after a four-day fall, the coin rises the next day, -1.49 % in the signal's direction (t -4.70, 388 cases), so the condition alone works against the short, and only the up day turns it into a fall.
- **F6:** The brief's own multi-day rally also fades: signal bars in the top fifth of the prior four-day return give +1.35 % (t 2.80, 128 cases), and those in the top fifth of the five-day return +1.25 % (t 2.58). This is not the condition's own effect either: down days after a four-day rise are followed by a rise, -0.92 % (t -2.61, 270 cases).
- **F7:** The total move per case covers the cost of a trade, so the cost is not what blocks the book. Over all signal bars, the unusual next-day fall is +0.85 % (t 3.62, 639 cases) against a cost of 0.22 % a trade. The give-back is a one-day move: the fall over two, three and five days averages +0.11 %, -0.04 % and -0.44 %, so a longer holding would not help. Across windows, the effect is positive in 7 of 10 windows with signals, and negative in w11 (-5.2 %, 13 cases) and w17 (-0.5 %).

## Ideas
- `058-01.g2.b1.d2.b1.d2.d1_capped-rise-fade-next-day` (from F3, F1, F2, F7): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall over the next day, only while that rise stays within about one usual swing.
- `058-01.g2.b1.d2.b1.d2.d2_modest-bounce-in-slide-fades` (from F5, F4, F2, F1): In a falling, agitated market, a one-day rise of up to about one usual swing that follows a fall over the previous four days is given back over the next day, more the deeper that four-day fall against the coin's 30-day swing.
- `058-01.g2.b1.d2.b1.d2.d3_multi-day-rally-fades-next-day` (from F6, F7): In a falling, agitated market, the larger a coin's rise over the past five days against the standard deviation of its daily returns over the past 30 days, the larger the fall over the next day when the last of those days is also an up day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
