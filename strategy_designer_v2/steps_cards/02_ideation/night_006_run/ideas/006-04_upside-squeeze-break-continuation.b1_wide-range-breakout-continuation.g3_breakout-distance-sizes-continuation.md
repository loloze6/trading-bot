---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's close sits above the highest high of its prior 20 days, as a share of that high, the further its price rises over the next 10 days.
Consequence: A trader would size upside breakouts by how far price clears the prior high, not by how compressed the range was before it.
Why:
- F3: Grid bars that close above the prior 20-day high are followed by a mean excess 10-day return of +6.44 % (n 86, std 0.249, t ≈ 2.4), against −0.30 % on the other 1317 grid bars, yet the tested width forecast does not grade this (slope t 0.39 on 404 cases), so the gain comes from the break, not from the prior range.
- F4: Compression does not precede larger moves: the 10-over-30-day range ratio leaves the absolute 10-day move flat (10.2 % bottom third vs 10.7 % top, t 0.52), and so does the realised-volatility ratio (t 0.23), while plain 30-day volatility predicts it (9.3 % vs 12.6 %, t 4.14); this is ordinary volatility clustering, against the brief.
- F6: The book is invested on only 9.4 % of days, and its top 1 % of days sum to +9.88 against a total of +1.79, so a few breakout days carry the whole result; trades held 1.5–3.5 days gain +5.7 % on average (n 212), while one-day trades lose −2.3 % (n 520).
