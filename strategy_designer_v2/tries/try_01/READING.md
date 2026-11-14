# Try 01: the ideas step alone, on three made-up briefs (2026-11-05)

**What ran.** The prompt `steps/ideas/PROMPT.md` and the format `steps/ideas/CLAIM_FORMAT.md`, on three fake briefs, one model call per brief (a strong model, through this session's agent tool; on the PC it would be the SDK). No pipeline, no data, no code in the loop. Then `check_claims.py`, code only.

**Result.**

| Brief | Ideas | Structural problems |
|---|---|---|
| fake_01 BTC overreaction, 1h | 10 | 0 |
| fake_02 ETH volatility regime and trend, 1d | 12 | 0 |
| fake_03 time of week, three pairs, 1h | 10 | 0 |

Every idea has a computable selector, a horizon inside the "then", a baseline, a measure, a numeric pass condition with a window rule, a one-line no-lookahead reason, and one line on how it trades. The mechanisms are distinct (volume, time, trend context, candle shape, range, session clocks, calendar flows, cross-asset). Each run struck its own parameter variants and said why. Ideas that need data the brief did not name were struck. A profit measure was used where the belief was about profit.

**What the runs told us about the prompt.**
1. **The model invented what the operator should give.** Round-trip cost came out as 0.2%, 0.5% and 0.4% across the three briefs. The "5 equal windows", "4 of 5", and minimum event counts (30, 100) were the model's own. These belong in one signed rule of the operator, pasted into every prompt: the cost per venue, the number of windows, how many must agree, the minimum events. This is the "small list of measures, never verdicts" from the challenge: it is coming back, and it should, as one short block.
2. **Contradictory pairs are fine.** Brief 01 produced two ideas with opposite volume beliefs. Both are testable; the prompt should say so in one line.
3. **One brief, one event family.** Brief 01's ten ideas share one trigger (a large bar), nine of them being conditions on the first. That is honest ideation and a natural lineage: a parent claim and conditional children. The record should carry that parent link.
4. **Some claims need a calendar.** NYSE trading days, New York and Chicago clocks with daylight saving, the last Friday of the month. Computable from timestamps, but the measurement step needs a calendar library. Mark it as a known need, not a blocker.
5. **Filters are not books.** Four of brief 03's ideas are volatility-only ("volatility input only"). The format carried that in `how_it_trades`; the config step must read it and not build a trading book from a filter.
6. **The measure types seen**, which the claim judge will have to compute: mean difference of forward returns, ratio of mean absolute returns, rank correlation, hit or touch rate, net return or Sharpe of a position after cost. Five types. That is the whole measure library for now.

**What did not go wrong.** No vague pass conditions. No lookahead in any selector read. No idea outside the brief's scope. No prose outside the format. No horizon above daily.

**Proposed try 02: the claim judge.** Take three claims from fake_01 (the baseline, one conditional, one contradictory pair member), measure them on real Kraken hourly bars on one fold, and compare the number to the pass condition. Code only, no AI. This is the spine's key change and it needs market data, so it runs on the PC, or here if the operator allows the research cache to be read (never the sealed store).
