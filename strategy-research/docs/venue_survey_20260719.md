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

1. Kraken's base-tier spot maker/taker fee has two conflicting figures across
   sources (0.40%/0.80% per the official page vs. 0.25%/0.40% per a
   secondary aggregator) — re-verify against the live account fee page before
   hardcoding into the cost model.
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
