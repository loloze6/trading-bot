---
name: hypothesis-design
description: Writes the hypothesis card for one research brief in four steps (0 Mode, 1 Idea, 2 Statement with the criterion, 3 Proof): the idea as quantities, a statement with its horizon, one criterion picked from the statement, and the tests of the claim.
---

# Hypothesis Design

Write the hypothesis card for one research brief, in four steps: 0 Mode, 1 Idea, 2 Statement, 3 Proof.

Input: `research_brief.yaml`, with its scope block. When they are among your inputs: `config/criterion_menu.yaml` and the files named in step 0.

Output: `hypothesis_card.yaml`. The fields are listed under "The card" below.

## 0. Mode

Read the brief first. It puts the run in one or more of the modes below. With none of them, write one card.

- **Pass-through.** A brief or candidate that arrives with `config`, `manifest`, `criteria` and `source` is already authored. Copy the four into the card unchanged and set `pass_through: true`. Its criteria stay as they arrive. A candidate missing any of the four is not a pass-through: author it with steps 1 to 3.
- **Decide-next candidate.** `DECIDE_NEXT_CANDIDATES.md` is among your inputs. That file governs the candidate. Steps 1 to 3 still apply, and criteria that arrive with the candidate stay unchanged.
- **Composition brief.** Code writes the card. Its criterion is `profit_bars`, the campaign's profit bars. You write no criterion for it.
- **Pre-filled claim.** `PREFILLED_CLAIM.md` is among your inputs. Copy the brief's `candidate.claim` into the card's `claim` as it is. There is no exception.
- **Several cards.** `BRIEF_HYPOTHESES.md` is among your inputs. One brief may yield several cards. That file says how to write and score them.
- **Brief exhausted.** Also `BRIEF_HYPOTHESES.md`. Declare a brief exhausted only when no honest card remains. Never declare it after an approximation run. A run that tested an approximation (a tried_ideas row with `approximation: n`) has not tested the idea.
- **Claim tests.** `CLAIM_TESTS.md` is among your inputs. It says how to write `claim` (step 3). When `CLAIM_TESTS_TRADE.md` is among your inputs, it adds the trade-level tests. When `CLAIM_TESTS_EXECUTION.md` is among your inputs, it adds the claim kind `execution_behaviour`.

## 1. Idea

Write the idea in the operator's words first, then in formulas.

- `thesis` opens with the brief's `research_goal`, word for word.
- `idea_quantities` lists every quantity the idea says matters. Give each one as the operator's words, then its formula. Each formula must be computable from the feeds in the brief's scope block.
- Keep every quantity. A competing reading of a quantity becomes a test (step 3) or a variant. It never deletes the quantity.
- `not_expressible` lists the parts of the idea a forecast cannot express: exits, holds, position state.
- `edge_source` says why the edge should exist. `library_lookup` names the library entry the idea builds on.

## 2. Statement

### 2a. The statement

Write `statement` after the idea. It has six keys: `predicts`, `predicts_kind`, `horizon_bars`, `condition`, `if_pass` and `if_fail`. `predicts_kind` is `return_direction` when `predicts` names the direction of a future return, and `market_state` when it names a state. The card list gives their meaning.

### 2b. The criterion
Pick the criterion after the statement is written, from the statement alone, by id from the menu's live entries. Write nothing in `criteria` that is not a menu id.
1. Match the measure to what the statement predicts. A statement that predicts the direction of a return takes the measure that correlates the forecast with the forward return over all bars. A statement that predicts a market state takes the measure that correlates the label with the outcome the statement names. If the menu holds no measure for what the statement predicts, pick nothing and write `criteria_fit` naming the measure that is missing; the run parks on it.
2. Measure at the statement's horizon. Set the criterion's horizon to the card's horizon_bars, rounded to the nearest horizon the menu offers. A measure at another horizon tests a different statement.
3. One criterion per statement. The residual-information criterion is added by code where a block is proven; name nothing beside your one pick.
4. Never a profit measure. Sharpe, return, drawdown and cost ratios are the campaign's bars, checked on every backtest; a menu entry of that kind exists for briefs and is not yours.
5. Never a measure because it was picked before. Earlier cards, the brief template, the order of the menu and the number of times an entry was used are not reasons. Write the reason in one sentence in `criteria_rationale`: what the statement predicts, at which horizon, hence which measure.
6. Pre-registered criteria are not yours. A brief or a pass-through candidate that arrives with criteria keeps them unchanged.
7. Sign consistency across eras is a criterion only when the protocol's windows lie in two or more eras of the data policy. On one era it adds nothing to the forecast measure.

## 3. Proof

The proof of the statement is its test. It is written in the card's `claim`, and `CLAIM_TESTS.md` says how.

- Test the statement at horizons around `horizon_bars`, not at `horizon_bars` alone.
- The opposite reading of the statement is its own test.
- A pre-filled claim is not touched (step 0).

## Regime idea

A regime idea goes through the same steps.

- Step 1: the regime measure is the idea quantity. Its threshold is a parameter.
- Step 2: `predicts` is a market state, named by its outcome. `condition` is the label.
- The host and the twin are code's. Write neither.
- A bar size with no registered block parks the run with that reason.

## The card

- `hypothesis_id`: the id of the idea.
- `thesis`: opens with the brief's `research_goal`, word for word (step 1).
- `idea_quantities`: one entry per quantity: the operator's words, then the formula (step 1).
- `not_expressible`: one entry per part of the idea a forecast cannot express (step 1).
- `edge_source`: `category` (information_asymmetry, structural_forced_flow, liquidity_provision, cross_venue_dislocation or persistent_behavioral_bias), `specific_mechanism`, `why_not_arbitraged`, `evidence_type` (`price_volume_only` when the idea uses price bars alone) and `measurable_proxy`.
- `library_lookup`: `indicator_id` (the id in `config/indicator_library.yaml` the idea builds on, null if none), `regime_affinity_for_target` and `crowding_risk` (null if `indicator_id` is null). Code groups tried ideas by `indicator_id`.
- `target_market`: the coin or coins of the brief.
- `timeframe`: the bar size of the brief.
- `statement`: `predicts` is what the forecast predicts. `predicts_kind` is its kind, `return_direction` or `market_state`. `horizon_bars` is how many bars of `timeframe` ahead it looks, an integer of 1 or more. `condition` is when the statement applies. `if_pass` and `if_fail` say what each result would mean for the idea.
- `criteria`: written only when `config/criterion_menu.yaml` is among your inputs. A list of `{id: <menu id>}`, with only the fields the menu entry lists under `card_overridable`. Step 2b.
- `criteria_rationale`: one sentence (step 2b, rule 5).
- `criteria_fit`: written only when the menu holds no measure for the statement: `none: ` then the measure that is missing (step 2b, rule 1).
- `claim`: written only when `CLAIM_TESTS.md` is among your inputs (step 3).
- `pass_through`, `config`, `manifest`, `source`: pass-through mode only (step 0).
