**Draft for the operator's review (topic 34). No step reads it yet.**

Why a book does or does not pay: the diagnosis of a backtest's book. It is an observation, not a check: it refuses
nothing, and step 6 stays the profitability check (topic 08). It is read the same way for every timeframe, and for
paying and non-paying books alike. Every term below follows `measures.md` (simple returns; the coin's average over
all windows; never across two windows) and `forecast.md` 7 (a bet and its holding period).

**Business definition.** An idea predicts a move: when its condition is seen, the coin moves by some amount over the
idea's horizon. The book pays when the move it captures, from the moment it can act, is larger than what the trades
cost, and is not just the coin's own rise. The diagnosis says, from the backtest's own record, which of these went
wrong: the move was too small, it came before the bot could act, the book stayed in after the move, or the book earned
the market's rise rather than the idea's move.

**Terms**
- **Unit traded:** a change of 1 in the position, as a share of the book (`postRebalance_current_allocation` minus
  `previous_allocation`, in absolute value). Opening a position of 1 and closing it is 2 units: a **round trip**.
- **Book without costs:** the position held after bar t's trade x the coin's return from t's close to t+1's close,
  summed over the bars (`measures.md`, the position's gain before costs).
- **Cost per unit traded:** (book without costs − the backtest's own book) / units traded. This is what the backtest
  actually paid (fees, spread, slippage), read from its record. No cost is assumed or read from a config.
- **Drift:** the coin's mean return per bar over all its windows together (`measures.md`, the coin's average).
- **A bet:** a rise in the forecast's size, in its direction (a turn from 0 counts as a rise). It asks for the
  position for the idea's horizon H (`forecast.md` 7, option 2). **A bet's age:** bars since that rise.

**The four readings**, each for the whole book (all coins and windows) and per coin:
1. **Size: does the move pay for its trip?** The book without costs per unit traded, against the cost per unit
   traded. Earned per unit below the cost per unit: the move captured is smaller than its trades cost.
2. **Timing: did the move come before the bot could act?** At each bet, the coin's move in the bet's direction, minus
   the drift, on the bar that fires it (bar 0, the bot acts at its close) and over the H bars after (bars 1 to H).
   It is read on non-overlapping bets (`measures.md`): the first bet of each grid cell of H bars. A large bar 0 and a
   small bars 1 to H: the idea sees the move when it is already spent.
3. **Closing: did the book stay in after its bets?** The bars in a position where no bet is younger than H (no rise
   of the forecast in the last H bars), as a share of the bars in a position, and the book without costs, minus the
   drift, earned on them per bar, against the bars covered by a bet. A large share earning little: the book takes the
   coin's risk after the idea's horizon.
4. **Trend: is the gain the market's rise?** The book's gain from the market's own rise (`measures.md`), as a share
   of the book's mean daily gain; the rest is timing.

**Why this can't leak:** it reads a finished backtest after the fact and changes no decision; bar 0's move is
measured, not traded on.

**Open, for the operator's review**
- **Reading 3 counts a forecast that stays on, with no new rise, as after its bets.** That follows option 2, where
  each rise is the event that asks for a hold. The alternative: each bar the condition holds is a new prediction. If
  so, a book that stays in while the forecast stays on is never "late".
- **Reading 2 uses the first bet of each H-bar cell.** A bet inside another's horizon is not counted twice.
- **Whether a reading should also give a threshold** (e.g. "earned per unit below the cost: too small"), or only the
  numbers for step 7 to read. Proposed: only the numbers. No threshold was asked for.
