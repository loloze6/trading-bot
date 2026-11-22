---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The farther a coin's close sits from the middle of its 30-day closing range, the larger its move away from that middle, in the same direction, over the next 5 days. The flatter the 30 days were (the smaller the net move against the range), the larger that move.
Consequence: A close pushing toward the edge of a flat month is the start of a breakout to follow, not a stretch to fade, and fading it should be refused.
Why:
- F2: In the data, a close away from the middle of its 30-day range keeps going the same way rather than coming back. Measured as the side of the middle times the unusual move, the continuation is +0.61 % over 5 days (t 2.93, 2555 non-overlapping cases) and +1.09 % over 10 days (t 2.54, 1259 cases). It fades by 20 days (+1.12 %, t 1.15, 539 cases).
- F3: The continuation holds on both sides of the middle. Over 5 days it is +0.57 % below the middle (t 2.08, 1316 cases) and +0.65 % above it (t 2.07, 1239 cases), so it can be traded long and short.
- F4: Flatness makes the continuation stronger, not the reversion. In the flattest third of the 30-day net-move-to-range ratio, the 5-day continuation is +0.72 % (t 2.34, 852 cases, strength 0.070). In the most trending third it is +0.58 % (t 1.38, 852 cases, strength 0.048). The supporting check came out -0.20 against the tested idea.
- F5: The continuation is graded at the far end of the range. In the farthest fifth of distance from the middle it is +1.34 % over 5 days (t 2.32, 511 cases). By the signed distance, the top sixth (mean +0.96) is followed by +1.49 % and the bottom sixths (-0.94 and -0.64) by -0.41 % and -0.73 %.
- F6: Continuation is large enough to pay. In the two farthest fifths of distance it earns +0.79 % total per case over 5 days, about 4.2 times the 0.19 % cost of a trade (strength 0.070). The tested reversion has a total move of -0.39 %, -2.0 times the cost.
- F1: The book loses its money on its shorts. Days held short average -0.130 % (8106 days, summed -10.53), while days held long average +0.029 % (9246 days, summed +2.67). On the 5-day grid, the cases where the book was short with the close above the range's middle lose -0.62 % each (1025 cases).
