# Phase 1.2 / Dispatch G — Kraken spot-margin fees + perp funding research

Date: 2026-07-20
Precondition check: PASSED — HEAD=93f3d87, `git status --porcelain` showed only
untracked `strategy-research/docs/session_reports/*.md` reports, nothing else.

## Purpose

Dispatch F2 stopped because its spot/perp binary classification was contradicted
by the engine's own code (`portfolio_info.py`'s SHORT logic is margin borrow/sell/
repay, not perpetual futures — see `20260720_venue_cost_wiring.md`). This dispatch
researches the two products that gap left un-costed: Kraken spot-margin (what the
three targets actually simulate) and Kraken perpetual-futures funding (what
FUNDING_MR_DAILY_RETEST's *signal*, not its simulated execution, is drawn from).

## Deliverable

Appended a dated supplement section to `strategy-research/docs/venue_survey_20260719.md`
(chose to extend the existing survey in place rather than create a separate
supplement file, since it's the same venue/research thread and appending avoids
fragmenting closely related material or needing cross-references) — committed as
`102fa8e`. No new file was created, so `DOC_INDEX.md` was left untouched per this
dispatch's own scoping ("update DOC_INDEX.md if a new file is created").

## Findings

**Kraken spot-margin availability for French/EU retail: NOT confirmed either
way.** Two pieces of evidence pull in different directions:
- Kraken's margin-eligibility page excludes only US/UK/Canada/Australia by name
  (France/EU absent from the exclusion list — a weak positive signal, and the page
  never mentions MiCA/MiFID/EEA at all).
- Kraken's own dedicated, current "Overview of changes for EEA clients" page (the
  most authoritative source on what the 2026-07-01 MiCA/MiFID transition actually
  changed) documents derivatives/perpetual-futures access in full detail
  (appropriateness test, TIN, the CySEC entity) but says nothing about margin
  trading at all — a real, unresolved gap, not a confirmation either way.
- Verdict: flagged unresolved in the deliverable, not asserted available. This is
  itself the requested "valid, important finding" per this dispatch's own framing.

**Kraken spot-margin fees:** opening fee 0.01-0.02% (BTC), 0.02-0.04% (other major
crypto), 0.025-0.05% (USD margin) — asset-dependent, per Kraken's official fee
schedule page (fetched in its French-localized form) and corroborated by a
separate support article's worked example. Rollover: same rate, charged every 4
hours, locked in at position open. 10x leverage cap mentioned generically; no
EEA/French-retail-specific cap found (contrast with perp, which has an explicit
3x-10x EEA cap tied to the appropriateness test). 3% liquidation fee on forced
closes.

**Kraken perpetual-futures funding:** interval is a genuine source conflict — the
EEA-specific contract-spec page says 1 hour (used for the deliverable's formula,
as the more specific/current/region-matched source, per this survey's own existing
precedent for handling conflicts), a non-region-specific blog primer says 4 hours
(cited but not reconciled). Rate bound ±0.5%/hour. Representative rate sourced
from CF Benchmarks' Kraken BTC Perpetual Funding Rate Index (a real published
index, not a single snapshot): 1.8738% annualized, ≈0.000214%/hour. No
ETH-specific index found — flagged unsourced for ETH, not extrapolated from BTC.

**Cost-mapping (Step 3, documented not implemented):** spot round_trip = taker×2;
margin round_trip = taker×2 + rollover×ceil(holding/4h); perp round_trip =
taker×2 + funding×ceil(holding/1h) (funding signed, direction-dependent). Both
margin and perp are time-dependent costs; the engine's flat per-side
`commission_rate` (Dispatch C) cannot express that directly — flagged as a
cost-model design question for a future dispatch (effective-rate backed out per
strategy from its own avg holding period, or a structural time-weighted-cost
engine change), not solved here.

## Confirmation

Read-only web research + one doc edit + this report. No code, no `cost_model.yaml`,
no `run_protocol.py`, no state touched. `git status --porcelain` after commit
shows only the same seven pre-existing untracked reports plus this new one —
nothing else changed.
