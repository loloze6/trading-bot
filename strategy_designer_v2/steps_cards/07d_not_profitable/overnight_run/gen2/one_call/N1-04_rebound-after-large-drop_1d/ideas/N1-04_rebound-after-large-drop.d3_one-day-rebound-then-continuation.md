---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-04_rebound-after-large-drop
line: 7.d not profitable
backtest: N1-04_rebound-after-large-drop_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, the rebound after a large standardised drop is spent by the first next close. When the next day instead closes lower by an ordinary amount, the decline continues over the following days.
Consequence: Hold the rebound long for one day only, and exit rather than stay in when the day after the drop closes lower without being a large drop itself.
Why:
- F5: Trades are all long, 3983 in total, with a median holding of 1 day; fees cost only about 0.10% per trade. The 1-day trades gain +1.30% before fees (win 63%, n=2642). Trades kept open for 2 days lose -4.45% (win 15%, n=493), those kept 3–4 days lose -6.54% (win 13%, n=284), and the mean over all trades before fees is -0.42% (t -3.32).
- F6: The rebound is concentrated in the first day. After a first large drop (forecast ≥16), the next day earns +0.48% (t 2.80, n=1127, hit 59%), while the second day alone adds only +0.31% (t 1.94, n=1122, hit 53%).
- F1: The book fails only on Calmar (0.748 against 0.75) because its drawdowns are deep: the worst drawdown per coin runs from -46% (LTC) to -85% (XRP), the worst 1% of book days lose 10.2% or more, and on bars with forecast ≥16 the book holds about 2.0x while the next-day return has a standard deviation of 5.9% and a 5% quantile of -8.2% (n=1280).
