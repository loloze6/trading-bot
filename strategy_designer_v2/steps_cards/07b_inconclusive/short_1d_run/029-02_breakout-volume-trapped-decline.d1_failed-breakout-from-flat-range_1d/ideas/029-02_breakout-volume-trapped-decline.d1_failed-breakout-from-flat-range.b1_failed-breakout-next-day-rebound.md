---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range
line: 7.b inconclusive
backtest: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close above the prior 20-day closing high is followed within 3 days by a close back below that high, the coin rises over the next day, and the deeper that close sits under the old high, the larger the rise.
Consequence: A trader would refuse to short a fresh failed breakout on the day it closes back inside the range, and the deeper the close under the old high, the stronger the reason to refuse.
Why:
- F1: The tested short is on the wrong side. After a failed 20-day breakout, the coin rises more than its normal drift. The verdict's main measure is -0.36 % per case over 5 days in the short direction, t -0.85 on 641 cases. My recomputation gives -0.53 % at 5 days (t -1.16, n 509) and -1.74 % at 10 days (t -1.96, n 427).
- F2: The rise is concentrated in the first day after the close back under the old high. The unusual next-day move is +0.55 % (t 3.08, n 573), a strength of 0.117 (t 3.12). From day 2 onward the strength falls to about 0.04–0.05 (t 1.0–1.3). The plan's 5-day horizon dilutes the effect, which is why the result reads unclear.
- F3: The next-day rise is graded by how deep the close sits under the old high.
- F4: The next-day rise is broad, not confined to one part of the data.
- F6: On this data a short on failed breakouts has no move to capture before costs. The total move in the short direction is -0.93 % per case, -4.8 times the 0.19 % cost of a trade. Its unusual part is -1.8 times that cost, so no change of holding or sizing could make the short book pay.
