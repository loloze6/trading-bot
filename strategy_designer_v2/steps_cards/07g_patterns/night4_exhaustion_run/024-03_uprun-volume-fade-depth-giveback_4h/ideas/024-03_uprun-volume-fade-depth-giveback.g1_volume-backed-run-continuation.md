---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-03_uprun-volume-fade-depth-giveback
line: 7.g patterns
backtest: 024-03_uprun-volume-fade-depth-giveback_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day return against its usual 3-day move, and the higher its volume over those 3 days against its usual volume, the more the coin keeps moving the same way over the next 3 days.
Consequence: After a strong 3-day rise on heavy volume, a trader should lean long or refuse a fade, since such rises tend to extend rather than give back.
Why:
- F2: Large 3-day rises continue rather than give back: on the non-overlapping 18-bar grid, bars whose 18-bar return is 1 to 2 of the coin's usual 18-bar moves are followed by an unusual 18-bar move of +0.141 usual moves (t 3.19, 573 cases), and the top decile of the 18-bar return by +0.160 (t 3.13, 530 cases). Five of six coins are positive, BTC +0.223 (t 2.42) and ZEC +0.245 (t 2.43), and XMR is flat at +0.001.
- F3: Among those large 3-day rises (more than 1 usual move), the third with the highest 18-bar volume against its 180-bar median is followed by +0.217 usual moves (t 2.64, 255 cases), against +0.119 (t 1.74) for the lowest-volume third, so rising volume rather than fading volume goes with the larger move up.
- F6: Up-streaks of 3 or more bars show no give-back that depends on fading volume: with volume faded the unusual move is +0.041 (t 0.69, 261 cases), and with volume risen it is +0.090 (t 1.22, 286 cases). Both are in the up direction, which is the opposite of the tested idea.
- F1: The book lost because it was short a rising market, not because of timing: it was short on 99.2 % of bars with a mean allocation of -1.17, its mean daily return was -0.19 % against +0.12 % for holding the coins, and the idea's unusual move of +0.13 % per case is only 0.7 times the 0.19 % cost of a trade.
