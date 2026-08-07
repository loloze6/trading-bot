# Venue Survey — French Non-Professional Retail Trader (2026-07-19)

Roadmap item 1.1. Purpose: settle where this operator may legally trade spot
and funding-rate perpetuals today, and parameterize the Phase 1.2 cost model.
All facts below were sourced live on **2026-07-19** via WebSearch/WebFetch —
none from training memory. Where sources conflicted or a claim could not be
directly confirmed, it is flagged inline rather than asserted.

Candidates checked: Binance, Kraken, Bybit, OKX, Coinbase, Bitget (the
mandated minimum set; no additional France-specific PSAN-only venue surfaced
as clearly relevant to a systematic-strategy use case).

## Regulatory backdrop (applies to every row)

The MiCA transitional period ended **1 July 2026**; from that date, any CASP
serving EU/French clients needs full MiCA authorization (via AMF directly or
via an EU passport from another member state's regulator) — legacy PSAN
registration no longer suffices.[^1] Separately, **MiCA does not cover
derivatives**: crypto perpetuals/futures are financial instruments under
MiFID II, so a venue needs a *second*, separate MiFID II authorization (not
just MiCA/CASP) to legally offer leveraged derivatives to EU retail.[^7] ESMA
stated in February 2026 that a leveraged product with no fixed expiry is
treated as a CFD regardless of what it's marketed as ("perpetual futures"
included); the venues below that offer retail perps get around this by
either using a genuine MiFID II exchange-traded-futures wrapper (Kraken) or
by adding a long-dated (5-year) expiry so the product is legally a future,
not a CFD (OKX, Coinbase).[^8]

## Comparison table

| Venue | MiCA CASP authorization (France) | Spot — EU/French retail | Perp/derivatives — EU/French retail | Spot maker / taker (base tier) | Perp maker / taker (base tier) | Fee tier basis | API / historical-data quality |
|---|---|---|---|---|---|---|---|
| **Binance** | **No.** Withdrew its Greek MiCA application 24 Jun 2026; told EU users it would suspend services from 1 Jul 2026 for lack of a license.[^3] Binance France SAS's AMF white-list page returns **404** as of 2026-07-19, consistent with delisting.[^4] | Not legally available to French retail as of survey date. | Not available (no CASP, so moot). | n/a — excluded | n/a | n/a | Not diligenced further — regulatory exclusion makes it moot for Phase 1.2. |
| **Kraken** | **Yes.** Payward Europe Solutions Ltd, MiCA CASP via Central Bank of Ireland, granted 25 Jun 2025, passports to France.[^5][^6] | Yes. | **Yes — the only venue with a confirmed, dedicated MiFID II license for genuine (no-expiry) exchange-traded perpetual futures.** Payward Europe Digital Solutions (CY) Ltd, CySEC licence 342/17. Gated by a mandatory MiFID II appropriateness test; leverage/product limits apply.[^7] | Official page: 0.40% / 0.80% at Level 1, scaling to 0.00% / 0.05% at the top tier.[^9] **Conflicts with a secondary aggregator source citing 0.25%/0.40% base — flagged, not resolved; use the official page for 1.2 and re-verify at implementation time.** | Official docs: 0.0200% / 0.0500% at $0+, scaling to −0.0060% / 0.0125% at $5B+.[^10] | 30-day rolling volume across spot, futures, or assets-on-platform, best-of-three. | Dedicated Futures API with historical OHLC and a historical-funding-rates endpoint (4h funding interval); default rate limit 1 req/s with higher tiers for other endpoints. Official docs at docs.kraken.com / docs.futures.kraken.com.[^11] |
| **Bybit** | **Yes**, but only for spot. Bybit EU GmbH, MiCA CASP via Austria FMA, authorized 28 May 2025, on the AMF white list.[^12] **Trap:** the original bybit.com platform is separately **blacklisted by the AMF since 20 May 2022** — a French user must use the regulated Bybit EU entity, not the global site.[^13] | Yes, via Bybit EU. | **No.** Bybit EU holds only the MiCA CASP license, no MiFID II authorization; derivatives (Bybit's core historical product) are confirmed unavailable on the regulated EU entity as of survey date.[^14] | 0.10% / 0.10% flat (VIP tiers reduce further).[^15] | n/a — not offered to EU retail | Spot volume / BIT-token discount. | Not diligenced further — no perp access makes this a spot-only candidate, and spot fees are less competitive than Kraken's. |
| **OKX** | **Yes.** OKX Europe Ltd / OKCoin Europe Ltd, MiCA CASP via Malta MFSA, granted 27 Jan 2025; the AMF white-list entry for OKCoin Europe Ltd shows French service start 15/02/2025 under free provision of services.[^16][^17] | Yes. | **Yes — X-Perps**, launched across the EEA (explicitly incl. France) in April 2026: a 5-year-expiry perpetual-style future with hourly funding, structured to be classified as a future rather than a CFD under MiFID II.[^18][^19] **Unconfirmed:** which specific MiFID II entity/licence number underwrites X-Perps — not surfaced in this survey; verify before relying on it. | 0.08% / 0.10% at Lv1.[^20] | ~0.02% / 0.05% at base tier, tiered by volume; funding settled hourly.[^21] | 30-day volume + VIP tier. | `/api/v5/market/candles` (up to 1,440 bars/request), dedicated funding-rate and funding-rate-history endpoints (including X-Perps), generous public rate limits (tens of req/s). Docs at okx.com/docs-v5/en/.[^22] |
| **Coinbase** | **Yes.** Coinbase Luxembourg S.A., MiCA CASP via Luxembourg CSSF, consolidating prior national (incl. France) registrations.[^23][^24] | Yes. | **Yes** — futures/"perpetual-style" contracts launched March 2026 via the Cyprus MiFID II entity (Coinbase Financial Services Europe), 5-year expiry, hourly funding, daily settlement, rolled out to 26 European countries including France.[^25] | 0.40% / 0.60% at $0–10K, scaling to 0.00% / 0.04% above $400M.[^26] | 0.04% maker / 0.02% taker at base (promotional — taker below maker), scaling to 0.018%/0.03% at $15M+; some eligible markets reportedly 0%/0% as a promo.[^26] | 30-day volume. | Advanced Trade / Exchange API `get_product_candles`: only 6 fixed granularities (1m–1d), capped at ~300 candles per response — shallower than Kraken/OKX. **Unconfirmed:** whether a funding-rate-history endpoint exists for the perpetual-style futures product — not found in this survey.[^27] |
| **Bitget** | **No, not yet.** CEO publicly confirmed the Austrian FMA application on 17 Jun 2026; as of survey date no authorization had been granted, putting Bitget past the 1 Jul 2026 deadline without a license.[^28] | Not confirmed legally available to French retail as of survey date. | Not available (no CASP, so moot). | n/a — excluded | n/a | n/a | Not diligenced further — regulatory exclusion makes it moot for Phase 1.2. |

## Decision

**Primary venue: Kraken.** It is the only candidate with an unambiguous,
dedicated MiFID II license (CySEC 342/17) underwriting genuine no-expiry
exchange-traded perpetual futures for EU/French retail, on top of a MiCA CASP
license that's been live since June 2025. That directly answers the Phase
1.3 gating question: **the funding-family perp branch is live-tradable**,
not research-only — conditional on the trader passing Kraken's MiFID II
appropriateness test and accepting whatever leverage/product caps apply
under that framework (not fully enumerated in this survey; verify at
account-opening). Kraken also publishes official, machine-readable fee
schedules and a Futures API with a native historical-funding-rate endpoint,
which is exactly what 1.2's cost model needs.

**Shortlist second: OKX.** MiCA CASP since January 2025 (one of the first in
the EU), an established French service presence since February 2025 via
OKCoin Europe, and a retail-accessible funding-rate perpetual product
(X-Perps, live since April 2026) with the deepest public API of the three
perp-capable venues (native funding-rate-history endpoint, high rate
limits). Held back from the primary slot only because the specific MiFID II
legal wrapper for X-Perps wasn't confirmable in this survey — worth
resolving before 1.2 if OKX is to be used as a cross-check or backup venue.

**Not shortlisted:** Coinbase is perp-capable but carries materially higher
spot fees at low volume (0.40%/0.60% vs. Kraken's 0.40%/0.80% base and OKX's
0.08%/0.10%) and a shallower market-data API (300-candle cap, 6 fixed
granularities, unconfirmed funding-history endpoint) — a weaker fit for a
research pipeline that needs deep historical data. Bybit is MiCA-authorized
but has **no** retail derivatives access on its regulated EU entity, so it's
spot-only and not competitive with Kraken there either. Binance and Bitget
are excluded outright: neither holds a MiCA CASP authorization as of
2026-07-19, so neither is legally usable by a French retail trader right
now.

## Explicit ambiguities / open items for 1.2–1.3

1. **RESOLVED (2026-07-20, Dispatch I,
   `engineering/sessions/session_reports/20260720_eea_perp_fee_verification.md`).** Kraken's
   spot base tier genuinely is 0.40%/0.80% maker/taker, per the official
   multi-schedule fee page — that figure was correct all along. The apparent
   0.25%/0.40% conflict was never actually a competing SPOT figure: it is
   "Kraken Perps," a separate, mobile-app-only consumer PERPETUAL product
   (0.25% applied at both entry and exit, plus 8-hourly funding, no other
   fees) with no API surface at all — a different product on a different
   interface, not accessible to an API-driven bot regardless of account
   eligibility. The two figures were being compared across mismatched
   products (spot vs. app-only perp), not two sources disagreeing about the
   same product. Kraken Pro / Futures API (the interface this bot's execution
   path would actually use for perp) is a third, separate schedule: 0.02%
   maker / 0.05% taker base tier, confirmed identical on both the EEA-scoped
   fee page and the generic Kraken Pro futures fee page. No further
   re-verification needed against the live account fee page for this
   specific ambiguity.
2. Kraken's MiFID II leverage caps / product limits for perpetual futures
   were referenced but not enumerated — needed before 1.2 can price realistic
   position sizing.
3. OKX X-Perps' underlying MiFID II licensing entity is unconfirmed.
4. Coinbase's funding-rate-history API availability for its perpetual-style
   futures is unconfirmed.
5. All three perp-capable venues' EU retail derivatives products are recent
   (Kraken's Cyprus MiFID buildout, OKX X-Perps April 2026, Coinbase futures
   March 2026) — regulatory posture here is actively moving; re-check before
   any live-money decision, not just at research time.

## Supplement (2026-07-20): Kraken spot-margin fees + perpetual-futures funding

Roadmap item 1.2 follow-up (Dispatch G). Motivation: three campaign KB findings
(`rsi_momentum_trending_cost_drag`/run_018, `keltner_scoremode_no_edge`/run_028+030,
`FUNDING_MR_DAILY_RETEST`/run_059) were found (2026-07-20 recon, see
`engineering/sessions/session_reports/20260720_venue_cost_wiring.md`) to simulate SHORT positions
via `trading-bot/execution/portfolio_info.py`'s margin borrow/sell/repay mechanics
— not perpetual futures, and not plain (unshortable) spot. This section researches
the two products that recon flagged as un-costed: Kraken spot-margin (the product
those three targets actually simulate) and Kraken perpetual-futures funding (the
product `FUNDING_MR_DAILY_RETEST`'s *signal* is drawn from, distinct from what it
simulates trading). All facts below sourced live on **2026-07-20** via
WebSearch/WebFetch, none from training memory; conflicting or unconfirmed claims
are flagged inline, not asserted.

### Kraken spot-margin trading

**Availability for French/EU retail — NOT explicitly confirmed either way.**
Evidence is mixed:
- *Weak positive signal:* Kraken's margin-eligibility support page states margin
  trading is "available to most verified clients that reside outside of the
  United States, United Kingdom, Canada, and Australia"[^29] — France/EU are not
  named as excluded, but are also not named as included; the page never mentions
  the EEA, MiCA, or MiFID at all.
- *Notable gap:* Kraken's own dedicated "Overview of changes for EEA clients"
  page — the most current, EEA-specific source on what the 2026-07-01 MiCA/MiFID
  transition changed — describes derivatives/perpetual-futures access in detail
  (appropriateness questionnaire, TIN requirement, the CySEC-regulated entity)[^30]
  but says nothing about margin trading at all. Since that page's explicit purpose
  is to document what's now available to EEA clients and under which license, its
  silence on margin (while perpetuals get full treatment) is a real, unresolved
  gap — it is not possible to conclude from this survey whether margin trading is
  covered under Kraken's current EEA authorization, offered under some other basis,
  or not actually available to EEA retail post-MiCA.
- **Verdict: flagged unresolved, not asserted available.** Do not treat spot-margin
  as confirmed-legal for a French retail trader without a direct, current
  confirmation (e.g. checking the live account UI/support chat) before any
  live-money decision.

**Opening fee:** varies by asset — BTC 0.01%–0.02%, other major crypto pairs
0.02%–0.04%, USD-margin (i.e. borrowing USD to go long) 0.025%–0.05%, per
Kraken's official fee schedule page (fetched in its French-localized form)[^9].
This is consistent with, and slightly more granular than, a separate support
article giving a worked example of 0.025% (USD margin, long) and 0.010% (BTC
margin, short)[^31].

**Rollover fee:** the SAME rate as the opening fee, charged every **4 hours**
a position remains open, locked in at the time of order execution (rates
otherwise fluctuate with market conditions)[^9][^31]. Margin fees stack on top
of ordinary volume-based spot trading fees at position open/close[^9].

**Leverage cap:** up to 10x mentioned generically for margin trading[^32], but no
EEA/French-retail-specific cap was found distinct from that generic figure (contrast
with perpetual futures below, where a 3x–10x EEA retail cap tied to the
appropriateness test is explicitly documented). Flagged as unconfirmed for margin
specifically.

**Other:** a 3% liquidation fee applies if a margin position is force-closed[^31].

### Kraken perpetual-futures funding

**Funding interval — conflicting sources, EEA-specific one preferred.** Kraken's
EEA-specific contract-specification page states funding is exchanged **every 1
hour** for EEA (and other non-US) clients, with US CFTC-regulated contracts
settling every 8 hours instead[^33]. A separate, non-region-specific Kraken blog
primer describes settlement "every four hours"[^34]. Per this survey's own
precedent for handling source conflicts (the 0.40%/0.80% vs. 0.25%/0.40% spot-fee
conflict above), the more specific, more current, explicitly-EEA-scoped source
([^33]) is used for a French retail trader — **1 hour** — but this is flagged as
unresolved against [^34], not fully reconciled.

**Funding rate bound:** ±0.50% per hour maximum/minimum, per the same EEA contract
spec page[^33].

**Representative/typical funding rate:** the CF Benchmarks Kraken Bitcoin
Perpetual Funding Rate Index (KFRI) — a third-party benchmark index, not a single
illustrative snapshot — showed **1.8738% annualized** for BTC perpetual funding on
Kraken as of access date[^35]. Converted to the EEA hourly interval for the
cost-mapping formula below: 1.8738% / (365 × 24) ≈ **0.000214% per hour**
(≈0.0214 bps/hour). Kraken's own funding-rate primer separately illustrates a
single point-in-time example (0.0003%/hour, next-estimate −0.0069%/hour, asset
unspecified)[^34] — cited only to show the rate's realistic order of magnitude and
sign volatility, not used as the representative figure (a single snapshot is not
representative of a "typical" rate the way a published index average is). No
ETH-specific published index was found in this pass; flagged as unsourced for ETH
specifically — the BTC KFRI figure should not be silently reused for ETH.

### Cost-mapping note (for cost-model design, not solved here)

Round-trip cost formula per product, using this survey's bps figures:

- **Spot:** `round_trip_cost = taker_fee × 2` (entry + exit, no time-dependent term).
- **Spot-margin:** `round_trip_cost = taker_fee × 2 + rollover_fee × n_rollover_intervals`,
  where `n_rollover_intervals = ceil(holding_period / 4h)` — e.g. a position held
  6 hours pays 2 rollover charges (bars 0-4h, 4-8h), not 1.5.
- **Perpetual futures:** `round_trip_cost = taker_fee × 2 + funding_rate × n_funding_intervals`,
  where `n_funding_intervals = ceil(holding_period / 1h)` for EEA clients per [^33]
  above, and `funding_rate` is signed (can reduce OR increase cost depending on
  position direction vs. funding sign) — unlike margin rollover, which is always a
  cost regardless of direction.

**Finding for cost-model design (not resolved by this dispatch):** both margin and
perpetual-futures round-trip cost are **time-dependent** — they scale with how long
a position is held, not just with trade count. The engine's current
`commission_rate` (threaded per Dispatch C/93f3d87) is a flat, per-side fraction
applied once at entry and once at exit, structurally unable to express a
holding-time-weighted cost. Correctly modeling margin or perp cost would require
either (a) computing an effective flat `commission_rate` per candidate strategy
from its OWN observed average holding period (`taker + rollover_or_funding ×
avg_holding_intervals`, backed out from that strategy's own trade log — a
per-strategy constant, not a venue constant), or (b) a structural engine change to
apply a genuinely time-weighted cost per trade. Neither is implemented by this
research-only doc pass; this is a finding to carry into the next cost-model design
step, not a code change made here.

[^1]: ESMA, MiCA overview & transitional deadline — https://www.esma.europa.eu/esmas-activities/digital-finance-and-innovation/markets-crypto-assets-regulation-mica (accessed 2026-07-19)
[^3]: CoinDesk, "Binance tells EU users it will no longer provide services after failing to secure MiCA license" — https://www.coindesk.com/policy/2026/06/26/binance-tells-eu-users-it-will-no-longer-provide-services-after-failing-to-secure-mica-license (accessed 2026-07-19)
[^4]: AMF white-list page for Binance France SAS (returns HTTP 404) — https://www.amf-france.org/en/warnings/white-lists/daspcasp/binance-france-sas (accessed 2026-07-19)
[^5]: Kraken Blog, "Kraken cements European leadership with MiCA license from Central Bank of Ireland" — https://blog.kraken.com/news/mica-license-central-bank-of-ireland (accessed 2026-07-19)
[^6]: AMF white list — Payward Europe Solutions Limited / Kraken — https://www.amf-france.org/en/warnings/white-lists/daspcasp/payward-europe-solutions-limited-kraken-digital-asset-exchange-kraken (accessed 2026-07-19)
[^7]: Kraken, Perpetual Futures (FR) + Kraken Blog "Announcing Europe's largest regulated futures offering" — https://www.kraken.com/en-fr/features/futures/perpetual ; https://blog.kraken.com/news/euro-reg-futures (accessed 2026-07-19)
[^8]: ESMA, Public statement on derivatives in scope of the CFD product intervention measures (24 Feb 2026) — https://www.esma.europa.eu/sites/default/files/2026-02/ESMA35-243228190-8024_-_Public_statement_on_derivatives_in_scope_of_the_CFD_product_intervention_measures.pdf (accessed 2026-07-19)
[^9]: Kraken, Fee Schedule — https://www.kraken.com/features/fee-schedule (accessed 2026-07-19)
[^10]: Kraken Support, Derivatives fee schedule — https://support.kraken.com/articles/360048917612-fee-schedule (accessed 2026-07-19)
[^11]: Kraken Developers, Futures API — historical funding rates & historical data — https://docs.kraken.com/api/docs/futures-api/trading/historical-funding-rates ; https://docs.futures.kraken.com/ (accessed 2026-07-19)
[^12]: AMF white list — Bybit EU GmbH — https://www.amf-france.org/en/warnings/white-lists/daspcasp/bybit-eu-gmbh (accessed 2026-07-19)
[^13]: AMF news release, "AMF reminds the public that the cryptoasset trading platform BYBIT is blacklisted" — https://www.amf-france.org/en/news-publications/news-releases/amf-news-releases/amf-reminds-public-cryptoasset-trading-platform-bybit-blacklisted (accessed 2026-07-19)
[^14]: LeoDex, "Bybit EU Migration: What EEA Users Must Do Before July 1, 2026" — https://leodex.io/learn/country-restrictions/bybit-eu-mica-migration ; CoinDesk, "MiCA's not enough: Bybit CEO says firms need MiFID, EMI licenses" — https://www.coindesk.com/policy/2026/04/26/mica-s-not-enough-bybit-ceo-says-firms-need-other-licenses-to-turn-a-profit-in-europe (accessed 2026-07-19)
[^15]: Bybit EU Help Center, "Bybit EU Spot Fees Explained" — https://www.bybit.eu/en-EU/help-center/article/Bybit-Spot-Fees-Explained (accessed 2026-07-19)
[^16]: OKX, "OKX: A Regulated Crypto Exchange Under MiCA in Europe" — https://www.okx.com/en-us/learn/okx-regulated-crypto-exchange-mica-europe (accessed 2026-07-19)
[^17]: AMF white list — OKCoin Europe Limited — https://www.amf-france.org/en/warnings/white-lists/daspcasp/okcoin-europe-limited (accessed 2026-07-19)
[^18]: OKX Europe, "Who can access X-Perps in the EEA?" — https://www.okx.com/en-eu/help/okx-x-perps-eea-regional-availability-eligibility (accessed 2026-07-19)
[^19]: BlockEden, "OKX X-Perps: How a 5-Year Expiry Clause Cracked Europe's $85T Derivatives Market" — https://blockeden.xyz/blog/2026/04/17/okx-x-perps-europe-mifid-5-year-expiry-perpetual-futures/ (accessed 2026-07-19)
[^20]: OKX, Trading Fee / Fee Rate — https://www.okx.com/en-us/fees (accessed 2026-07-19)
[^21]: OKX Europe, "X-Perps fees overview" — https://www.okx.com/en-eu/help/okx-x-perps-eea-fees-overview (accessed 2026-07-19)
[^22]: OKX API guide — https://www.okx.com/docs-v5/en/ (accessed 2026-07-19)
[^23]: Coinbase, "Coinbase Secures MiCA Licence" — https://www.coinbase.com/blog/coinbase-secures-mica-licence-a-milestone-in-europes-crypto-evolution (accessed 2026-07-19)
[^24]: AMF white list — Coinbase Luxembourg S.A. — https://www.amf-france.org/en/warnings/white-lists/daspcasp/coinbase-luxembourg-sa (accessed 2026-07-19)
[^25]: Coinbase, "Futures Contracts Now Available on Coinbase in Europe" — https://www.coinbase.com/blog/futures-contracts-europe ; The Block, "Coinbase rolls out crypto futures trading across 26 European countries" — https://www.theblock.co/post/392797/coinbase-opens-crypto-futures-trading-europe (accessed 2026-07-19)
[^26]: Coinbase Help, "Coinbase Advanced fees" — https://help.coinbase.com/en/coinbase/trading-and-funding/advanced-trade/advanced-trade-fees (accessed 2026-07-19)
[^27]: Coinbase Developer Docs, "Get product candles" — https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/products/get-product-candles (accessed 2026-07-19)
[^28]: Cryptonomist, "Bitget MiCAR Authorization Seeks EU Regulatory Approval" — https://en.cryptonomist.ch/2026/07/02/bitget-micar-authorization-eu/ (accessed 2026-07-19)
[^29]: Kraken Support, "Client eligibility for margin trading services" — https://support.kraken.com/articles/4402532394260-client-eligibility-for-margin-trading-services- (accessed 2026-07-20)
[^30]: Kraken Support, "Overview of changes for EEA clients" — https://support.kraken.com/articles/overview-of-changes-for-eea-clients (accessed 2026-07-20)
[^31]: Kraken Support, "What are the fees (opening and rollover) for trading using margin?" — https://support.kraken.com/articles/206161568-what-are-the-fees-opening-and-rollover-for-trading-using-margin- (accessed 2026-07-20)
[^32]: Kraken, "Crypto Margin Trading – Up to 10x Leverage" — https://www.kraken.com/features/margin-trading (accessed 2026-07-20)
[^33]: Kraken Support, "Linear Multi-Collateral Derivatives Contract Specifications for clients in the European Economic Area" — https://support.kraken.com/articles/perpetual-contract-specifications-for-clients-in-the-eea (accessed 2026-07-20)
[^34]: Kraken Blog, "A Quick Primer on Funding Rates" — https://blog.kraken.com/product/quick-primer-on-funding-rates (accessed 2026-07-20)
[^35]: CF Benchmarks, "CF Bitcoin Kraken Perpetual Funding Rate Index (KFRI)" — https://www.cfbenchmarks.com/data/indices/KFRI (accessed 2026-07-20)
