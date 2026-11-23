---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's volume on a day relative to its own prior 20-day average, and the larger that day's fall, the more the coin rises over the next day. This holds while its daily volatility over the past 20 days is high against its volatility over the past 4 months, and the more so the higher that ratio.
Consequence: A trader buys heavy-volume down days only when the coin's recent volatility runs above its longer norm, sized up with that ratio. They stay out in calm markets, where these days carried the losses of the deepest fall.
Why:
- F1: The book fails only on Calmar (0.627 against 0.75), and its deepest fall is -25.7 % over 121 days from w8 into w9. Holding the coins fell -39.0 % over the same stretch, so the book's falls come from long days in a falling market. In w8–w9, the held bars in a calm state lost -0.106 in summed gain over 114 bars. The mid state gained +0.195 over 135 bars and the wild state +0.240 over 73 bars.
- F2: The effect lives only when the coin's recent volatility is high against its own longer volatility (20-day standard deviation of daily returns over the 120-day one, cut in thirds).
- F3: The condition is not an effect of its own. Wild bars without the signal lose -0.38 % the next day, against +0.62 % when both hold. The heavy-volume fall is what carries the move, and high volatility is where absorption by a patient buyer matters.
- F4: Inside the wild state the effect stays graded. The upper half of the forecast gives +0.82 % and the lower half +0.42 % (708 cases each). In the calm state the two halves are flat: -0.19 % against -0.22 %.
- F5: On held bars, the book's gain per bar rises with the volatility state.
- F6: An approximate rebuild of the book, with the same positions and costs, compares three versions.
