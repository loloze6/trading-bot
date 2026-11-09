# Exercise 1: reading

`../helper/make_test_plan.py` with `system_prompt_used.md` and the two trimmed references (`../helper/reference/`). Seven ideas from step 2, exercise 3 (opus), one call per idea, on opus and on sonnet. Fourteen calls, none refused. Cost: opus 1.77 USD (0.22 to 0.30 per call), sonnet 0.86 USD (0.11 to 0.13 per call). The references are about 720 lines in every call; that is most of the cost.

No config was run or validated by the engine: everything below is my reading of the configs against the guide and the catalogue.

## Counts

| Idea | Expected | opus | sonnet |
|---|---|---|---|
| 001-01 RSI high, then reversal | testable | plan | plan |
| 001-03 RSI high, then continuation | testable | plan | plan |
| 002-01 up-cross, then drift | testable | plan | plan |
| 002-05 cross-to-cross span | testable | plan | plan |
| 003-01 low-volume up move reverts | doubtful | plan | plan |
| 004-01 altcoins follow bitcoin | untestable | **untestable**, right reason | **untestable**, right reason |
| 005-01 bearish RSI divergence | untestable (no divergence component) | plan, forced | plan, forced |

## The configs, against the two hard rules and the regime rule

| | opus | sonnet |
|---|---|---|
| `standardise` first in every component | 6 of 6 | 6 of 6 |
| Every strategy component graded | 6 of 6 | 6 of 6 |
| Regime only when the idea is a condition | 2 regimes (003-01 low volume, 005-01 near the high), both conditions of the idea | the same 2 |
| No jump from none to some inside the strategy | 5 of 6: **005-01** adds a constant (buy-and-hold, negated, weight 2) inside the regime, so the position jumps to about -6.7 as soon as the regime opens, whatever RSI says | 6 of 6 |
| Config matches the idea's direction and side | 6 of 6 (long-only or short-only clipped to the idea's side) | 4 of 6: **002-01, 002-05** keep the short side, so the test also requires downward stretches to fall, which the idea does not claim (stated in the deviation) |
| Settings from convention | 6 of 6 (RSI 14, SMA 50/200, `standardise` window set by the guide's rule) | 6 of 6 |

**What surprised me.** The volume idea (003-01), which I had marked doubtful, is expressed cleanly by both models: the on/off `VolumeExpansionHedgeComponent` fires exactly on low-volume up bars, so it is used as the regime rule (allowed in the detector), and inside it a graded short sized by the day's move. That is the regime rule used as intended.

## The criteria

- **Every criterion can be measured on the backtest record:** next-bar or next-days returns after the forecast, compared with the coin's average return, buy-and-hold, and between sizes of position.
- **The two examples in the prompt are copied almost everywhere.** 11 of 12 criteria contain "the largest positions" and "gains grow with position size", often both. They fit the RSI ideas; they are less natural for the cross ideas, where the claim is about direction, not size.
- **Several horizons in one criterion** (opus 001-01 "1 to 10 days", sonnet 001-03 "next 1 to 10 days", both 005-01 "5 to 10 days"). That leaves room to pick the horizon that works after seeing the data, which is what a test plan must prevent. 4 of 12 criteria.
- **Several conditions at once** (beat the average, beat buy-and-hold, grow with size, on two or three coins). Fixed before the data, so allowed; but confirm and reject do not always cover every case (opus 001-03: confirm "on each" coin, reject "on all three"), which leaves an unnamed middle.

## The deviations

All 12 are honest and specific: "after X" becomes "while X, fading"; the side not tested; the periods taken from convention. The deviation line does its job: every difference between the config and the idea that I found is stated there.

## Findings for the earlier steps

1. **Two step 2 ideas became the same test.** 002-01 (after an up-cross, the drift persists) and 002-05 (from one cross to the opposite cross, price rises) gave identical configs in both models: a graded spread of the two averages. In this vessel, "after the cross" and "during the stretch" are one test. Step 2 counts them as two ideas.
2. **The divergence idea (005-01) was forced, not marked untestable**, by both models: "a new high with a weaker RSI than at the previous high" became "near the top of the range with a weak RSI level". The deviation says so. Whether that is an acceptable approximation or a different idea is a ruling for the operator; by the prompt's own words ("do not force it") it should have been untestable.

## Models

- **Opus:** right on the side of every idea; one rule fault (the constant inside a regime, 005-01). Twice the cost.
- **Sonnet:** no rule fault; twice changes the idea's side (keeps the short leg of an up-only idea), declared in the deviation. Half the cost.

## Prompt changes the outputs ask for (not made, untested)

1. **One horizon.** "Name one horizon, in bars, and keep to it" in the criterion paragraph.
2. **Confirm and reject cover every case, or name the middle "inconclusive".**
3. **Constants.** "A constant (buy-and-hold) inside a regime makes the position jump: do not use one there."
4. **The examples.** Keep them, or replace them by one sentence that does not suggest a measure ("say which part of the record the idea's truth would show in, and why"); to be tested.

## Recommendation

The step works: plans are feasible, the configs follow the hard rules (one fault in twelve), the untestable case is found, and every gap between test and idea is declared. Rule on 005-01 (forced or untestable), then exercise 2 with changes 1 to 3, the same seven ideas, opus and sonnet.
