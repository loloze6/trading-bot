---
brief: 010_rsi-midline-regime-direction
source-idea: 010-04_rsi-below-streak-continuation
line: 7.d not profitable
backtest: 010-04_rsi-below-streak-continuation_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The longer a coin's 14-day RSI has stayed below 50 without a break, measured in days up to the current close, the lower the coin's return over the next 14 days. This holds only while the coin's close stands close to its 100-day average, so that its 30-day fall is still shallow, not after a deep fall.
Consequence: A trader would short a lengthening RSI-below-50 stretch only in a fresh, shallow decline, and would stand aside once the coin is far below its 100-day average, where these shorts were squeezed.
Why:
- F2: The losses come from the longest runs below 50, which is also where the position is largest. On short bars with a run above 35 days, the mean gain per bar is -0.00334, the coin's next-day return is +0.00345, and the mean position is -1.09. On runs of 20–35 days the gain per bar is +0.00228.
- F3: The short loses when the coin has already fallen deep, measured at the bar's close:
- F4: On the 14-day grid, the deepest states rebound and the moderate ones continue:
- F5: The book's 20 worst 14-day stretches lose 10.5% on average. They start when the coin's 30-day return is -24.9%, against +3.6% on all grid bars, while the book holds a mean position of -0.83. These are short squeezes after deep falls, and they drive the failed Calmar.
