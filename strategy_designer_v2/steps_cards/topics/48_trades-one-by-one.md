# Topic 48: the trades one by one (parked)

Status: parked (2026-11-23, the operator: "park the continuation of this analysis, with observations")  
Where: research: what makes a trade win or lose, and what a book can act on (steps 3, 5, 6; the engine's diagnostics)  
Opened: 2026-11-23, the operator: "how to increase the winning rate? what is the profile of losing trades? limit them?
increase the winners? the trades file, the forecast profile: you have a goldmine of data". Measurements 1d-8 to 1d-10 of
topic 47.

## Question
What separates a winning trade from a losing one, and can a book act on it (by number of trades, or by their size)?

## What was done
- The trade table: every trade of the 81 real books of night 5 (1.55 million: 204 thousand on daily bars, 1.35 million
  on hourly), from the engine's trade diagnostics (`trade_diagnostics.json.gz`, committed with every record), with what
  was known at its entry (the forecast, the coin's volatility, trend and distance from its high, the market's trend and
  volatility, how many coins entered the same day, weekday, side). `topics/47_review/trade_table.py` rebuilds it (57 MB,
  kept out of git), `clean_excursions.py` adds the excursions without the entry bar.
- Rules judged out of fold (chosen on three folds, judged on the fourth): `trade_rules.py`, `breakeven.py`,
  `deep_trades.py`, `event_study.py`; per book at its horizon: `edge_at_horizon.py`.

## Observations
1. **At entry, losers look like winners.** Win rates move 2 to 5 points across any feature; a filter chosen on three
   folds makes the fourth worse (daily mean trade 0.97 % to 0.76 %). Exception: the side; in 2018-2025 shorts lose
   (hourly books long only: win rate 46 % to 58 %, out of fold better on 67 % of book-folds).
2. **The forecast's size:** on daily books it does not change the bet's quality (slope -0.02 % per point, t -0.56, each
   book its own base; errors clustered by day), only its size: 48 % of the money is made at the cap of 20. On hourly
   books the stronger the forecast, the worse (win rate 46.8 % at 0-2.5, 40.9 % at 15-20; t -18).
3. **The win rate is not the target.** A take profit at +1 % gives 88 % winners and a mean trade of 0.00 % (from
   +0.97 %): the best tenth of trades makes 1.8 times a daily book's total (5.2 times hourly). Stops cut winners too
   (38 % of daily winners first go 3 % against).
4. **One small exit rule helps:** once +1 % is reached, the stop moves to the entry price: daily mean trade 0.97 % to
   1.21 %, better on 62 % of book-folds (simulated on daily bars, fills at the entry price assumed).
5. **Losing streaks are real but not a signal at entry:** losses cluster per coin far beyond chance (runs test: 53 % of
   daily series, 69 % hourly, against 5 %), yet the trade after a loss is not worse; skipping it is worse on 72 % of daily
   book-folds. The clusters are market periods (2018, 2022 for long books).
6. **When an idea's gain comes (all trades pooled):** daily, beyond the coin's drift, +0.09 % at 1 day, +0.12 % at 2-3
   days, gone at 5, negative after; hourly, below the drift from the first hour. **But book by book at the plan's
   horizon** the picture is different: daily median +0.50 % per trade beyond the drift (above a 0.2 % round trip in 29 of
   45 books), hourly median +0.30 % (23 of 36): the pooled figures are dominated by a few books with hundreds of
   thousands of trades. To be discussed (below).
7. **Churn:** 19 % of daily trades reopen the same coin and side within 3 bars; they earn +0.34 % against +1.56 %.
8. **Coins:** daily, a coin that lost on three folds does not lose more on the fourth (54 %); hourly it does (71 %).
9. **Fees:** 2 % of the daily gross gains; on hourly books the gross is already negative.
10. **The engine's diagnostics include the entry bar** (`trading-bot/backtest/run_protocol.py`, `_compute_mae_mfe`
    over `bars[entry_idx : exit_idx + 1]`): the entry bar's high and low come before the entry at its close. Median
    daily MFE reported 6.2 %, after the entry 3.9 %.

## To discuss when resumed (the operator, 2026-11-23)
1. **"Most ideas pay their cost, hourly included."** What was measured: the price move in the trade's direction from
   the entry close to the plan's horizon, less the coin's mean move over that span, per trade, before costs, at a fixed
   horizon whatever the book's real exit. 23 of 36 hourly books are above a 0.2 % round trip on that measure, yet
   hourly books lose. The gap is between the idea held for its horizon and the book's real trades (exits on the
   signal's flip, re-entries, 1.35 million trades): the discussion starts there.
2. **Is a daily strategy an hourly one with its settings times 24?** The designer's view (to be tested, not measured):
   - **The same, in the simplest case:** a signal built only from closes, every lookback times 24 (a 20-day mean
     becomes a 480-hour mean), measures nearly the same thing, and the holding time is the same in hours.
   - **What differs:**
     - The hourly book decides every hour, the daily one once a day at the 00:00 UTC close. A signal near its
       threshold crosses it back and forth during the day: more trades, more costs, the same idea.
     - Hourly closes add noise to the same measure.
     - What is defined by the day does not translate: a day's high-low range, where the day closed in it, the day's
       volume, the weekday.
     - The entry hour differs (any hour against 00:00 UTC), which may matter for effects tied to a time of day.
   - **So:** in principle, a ×24 hourly book is the daily book decided more often: the same gain per unit of time,
     more turnover. If it does worse, the cause is turnover and noise, not the idea.
   - **The test:** two or three daily real books with close-based signals, their ×24 hourly versions, compared on the
     gain beyond the drift, trades a year, costs and Calmar.

## Status and next
Parked. To resume: rebuild the trade table (`trade_table.py`, then `clean_excursions.py`), start with the two points to
discuss. Steps it gave to the next-steps list: the engine's diagnostics without the entry bar; step 5's measure of the
gain beyond the drift at the idea's horizon; and, kept for later, the stop moved to the entry after +1 %, long only on
hourly books, merging re-entries, the ×24 test.

## Links
`topics/47_why-real-books-do-not-pay.md` (measurements 1d-8 to 1d-10), `topics/47_review/`.
