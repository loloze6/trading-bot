# E-044 — Trade a portfolio of strategies, not one strategy at a time

**State:** parked — deliberately, not started
**Owner:** Jérémy
**Updated:** 2026-09-01

## Why

Jérémy's vision, 2026-09-01: *"we have an epic to enhance the bot in trading a
portfolio of coins, each following a unique strategy but following their
strategy result. That's indeed a way to decrease variance of portfolio,
decrease risk associated to drawdown, increase potential leverage, so having
more benefits for the same level of risk."*

Concretely: if Strategy A trades BTC and Strategy B trades ETH, and the two
are not perfectly correlated, running both at half-size each produces a
smoother equity curve than running either alone at full size — same expected
return, fewer bad days. Because the ride is smoother, leverage can safely go
up on both, for more profit at the same drawdown risk a single strategy would
carry alone.

**This is not the same question as [E-026](../E-026/EPIC.md).** E-026 asks
whether one strategy's *signal* can be computed by comparing many coins to
each other (a cross-sectional signal, like "buy whichever coin is rising
fastest relative to the others"). This epic asks whether *already-decided*
strategies — each producing its own independent signal, however it is
computed — can be **combined into one shared risk budget**. E-026 is about
signal generation; this is about capital allocation across strategies that
already exist. The two would eventually compose (a cross-sectional strategy
could be one more thing this epic allocates capital to), but neither is a
prerequisite for the other, and they should not be conflated when deciding
what to build next.

## Why it is parked, not queued

Jérémy, 2026-09-01: *"this enhancement would increase profitability but would
not make a strategy unprofitable, profitable."* This is a lever on top of an
edge — it cannot create one. The project's current objective is finding a
single profitable strategy at all; the portfolio benefit only exists once
there are strategies worth combining. Building this now would be building
infrastructure for something that does not yet exist to combine.

**Trigger to unpark:** at least one strategy has cleared the full bar
(validation, cost stress, parameter plateau, era stability, sample floor,
holdout) and is either promoted or in holdout — the point at which a second
one running alongside it would already start to matter.

## Scope (once unparked — not decided now)

### Likely in
- A capital/risk allocator sitting above multiple independently-running
  strategies, each still producing its own single-symbol (or cross-sectional,
  if E-026 lands separately) signal exactly as today.
- Correlation-aware sizing: the diversification benefit only exists if the
  strategies are not simply the same bet twice.
- A leverage policy that can safely use the smoother combined curve, without
  quietly raising per-strategy risk past what each was validated at alone.

### Likely out (for this epic; may already exist elsewhere)
- Generating a cross-sectional signal itself — that is E-026, if it proceeds.
- Finding the first profitable strategy — that is the whole rest of the
  project's current work.

None of this is a commitment; it is a placeholder for what S1 would need to
characterize once the trigger above is met.

## Log

- 2026-09-01 — `parked`. Raised by Jérémy while reviewing the #70/E-026
  discussion, explicitly to correct a conflation: multi-symbol *breadth in one
  signal* (E-026, informed today by Dorian's H003 kill) and *multi-strategy
  portfolio combination* (this epic) are different questions. Recorded as its
  own epic so the vision is not lost, and explicitly sequenced after a
  profitable strategy exists rather than competing with finding one.
