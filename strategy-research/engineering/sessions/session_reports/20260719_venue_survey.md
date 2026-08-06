# Session Report — Venue Survey (2026-07-19)

## Task
Dispatch: Phase 1.1 venue survey, sole-writer implementation role. Research
current MiCA CASP / AMF authorization, spot vs. perp retail availability,
fees, and API quality for Binance, Kraken, Bybit, OKX, Coinbase, Bitget for
a French non-professional retail trader, write the comparison to
`strategy-research/docs/venue_survey_20260719.md`, update `DOC_INDEX.md`,
commit, verify.

## Preconditions
All three passed at start: HEAD was `1d6b92f`, `git status --porcelain`
empty, target file did not exist. Proceeded.

## Research performed (all live, 2026-07-19)
~20 WebSearch calls and 4 WebFetch calls against ESMA, AMF (amf-france.org
white-list and blacklist pages fetched directly for Kraken/Bybit/OKX/
Coinbase/Binance entities), Kraken's official fee-schedule and derivatives
fee-schedule pages, Kraken/OKX/Coinbase developer docs, and press coverage
of the MiCA 1 Jul 2026 deadline and each venue's derivatives rollout.

### Key findings
- **MiCA ≠ perp authorization.** MiCA/CASP covers spot/custody services;
  crypto derivatives are MiFID II financial instruments and need a *second*
  license. ESMA's Feb 2026 statement confirmed perpetuals are CFDs by
  default regardless of naming, unless structured as genuine exchange-traded
  futures (Kraken's approach, via a Cyprus MiFID entity) or given a long
  (5-year) expiry to qualify as a future rather than a CFD (OKX X-Perps,
  Coinbase futures).
- **Binance**: withdrew its Greek MiCA application 24 Jun 2026, told EU
  users it would suspend service from 1 Jul 2026. Confirmed the AMF's
  Binance France SAS white-list page now 404s — direct corroboration beyond
  the press reporting.
- **Bitget**: Austrian FMA application publicly acknowledged 17 Jun 2026 but
  not granted as of survey date — past the 1 Jul deadline unauthorized.
- **Bybit**: MiCA-authorized (Bybit EU GmbH, Austria FMA) for spot only — no
  MiFID II, so derivatives (its core historical product) are unavailable to
  EU retail on the regulated entity. Also surfaced a retail trap: the
  original bybit.com domain has been AMF-blacklisted since 20 May 2022,
  separate from the now-compliant Bybit EU entity.
- **Kraken**: MiCA (Central Bank of Ireland, 25 Jun 2025) + a dedicated
  MiFID II derivatives license (Payward Europe Digital Solutions (CY) Ltd,
  CySEC 342/17) offering genuine no-expiry exchange-traded perpetual
  futures, gated by a MiFID II appropriateness test. Official fee pages and
  a Futures API with a native historical-funding-rate endpoint (4h funding
  interval).
- **OKX**: MiCA (Malta MFSA, 27 Jan 2025), established French presence via
  OKCoin Europe since Feb 2025 (confirmed on AMF white list), X-Perps
  (5-year-expiry perpetual-style product, hourly funding) launched across
  the EEA including France in April 2026. Deep API (funding-rate-history
  endpoint incl. X-Perps, high rate limits). Could not confirm the specific
  MiFID II entity/licence backing X-Perps — flagged as unconfirmed in the
  deliverable.
- **Coinbase**: MiCA (Luxembourg CSSF, consolidating the prior French
  registration), futures/perpetual-style product (5-year expiry, hourly
  funding, daily settlement) launched March 2026 via a Cyprus MiFID entity,
  live in 26 EU countries incl. France. Highest spot fees of the perp-capable
  three at low volume; shallower market-data API (300-candle cap, only 6
  granularities, funding-history endpoint existence unconfirmed).

### Conflicts / unconfirmed items flagged in the deliverable (not resolved)
1. Kraken base-tier spot maker/taker fee: official page says 0.40%/0.80%;
   one secondary aggregator says 0.25%/0.40%. Deliverable instructs 1.2 to
   re-verify against the live account fee page.
2. Kraken's MiFID II leverage/product caps for perpetuals were referenced
   in press coverage but never enumerated with numbers — needed for 1.2's
   position-sizing assumptions.
3. OKX X-Perps' specific MiFID II legal wrapper/entity — not found.
4. Coinbase funding-rate-history API endpoint for its perpetual-style
   futures — existence not confirmed.

None of these blocked the venue decision (Kraken's case doesn't depend on
any of them), but all four should be closed out before 1.2 hardcodes numbers
into the cost model.

## Decision written into the deliverable
**Primary: Kraken** — only venue with an unambiguous MiFID II derivatives
license, official machine-readable fee schedules, and a funding-rate-history
API. **Shortlist backup: OKX** — MiCA since Jan 2025, established French
presence, retail perp product live since April 2026, deepest public API of
the group, held back from primary only on the unconfirmed MiFID wrapper
question. Coinbase and Bybit not shortlisted (weaker fees/API and no-perp
respectively). Binance and Bitget excluded outright (unauthorized).

This directly resolves Phase 1.3's stated immediate consequence: **the
funding-family perp branch is live-tradable** (on Kraken), not
research-only.

## Verification
- `git status --porcelain` before commit showed only the two expected paths
  (`strategy-research/DOC_INDEX.md` modified, `venue_survey_20260719.md`
  untracked) — no unauthorized writes appeared, so no STOP was triggered.
- Committed `618d548`. `git show --stat HEAD` confirms both files landed
  (123 insertions, 2 files). `git log --oneline -1` matches. `git status
  --porcelain` empty post-commit — working tree clean.

## Files touched
- `strategy-research/docs/venue_survey_20260719.md` (new)
- `strategy-research/DOC_INDEX.md` (one-line pointer added)
- `strategy-research/docs/session_reports/20260719_venue_survey.md` (this
  file — written after the read-back verification, per dispatch step
  ordering, and intentionally not part of the commit above)
