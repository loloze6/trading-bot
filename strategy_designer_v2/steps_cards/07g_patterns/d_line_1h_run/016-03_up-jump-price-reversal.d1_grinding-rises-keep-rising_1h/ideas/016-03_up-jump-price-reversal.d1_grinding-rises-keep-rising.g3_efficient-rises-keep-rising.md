---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger that net rise is as a share of the summed absolute hourly moves over those 3 days, the more the coin rises over the next 3 days.
Consequence: A trader would add to 3-day rises that took a straight path, sized by the path's efficiency, and would refuse to chase rises built through choppy back-and-forth.
Why:
- F4: How a 3-day rise was built matters, through its path efficiency (net log move divided by the sum of absolute hourly log moves). Higher efficiency was followed by a larger next-3-day excess return (slope 0.059, t 3.43, 2865 cases). The tested top-3-gains share of the rise showed nothing (t -1.24). With the 3-day return held fixed, the signed efficiency keeps a t of 2.51 (5539 cases), while the return itself drops to t -1.56. The per-coin slope is positive in 5 of 6 coins, but each alone has t below 1.5.
- F3: Over 3 days, rises and falls behave in opposite ways. After a 3-day fall, the next 3-day excess return has a slope of -0.104 on the size of the fall (t -3.56, 2669 cases), so deeper falls rebound more. After a 3-day rise the slope is +0.067 (t 2.81, 2865 cases).
