# Kraken Perp Fee Schedule Verification — EEA/French Retail API Account

Date: 2026-07-20 (all sources accessed this date)
Scope: web research only, read-only. No repo tree precondition per dispatch (runs parallel
to Dispatch H; does not read or depend on HEAD state). No files touched other than this report.

## Question

For a French non-professional retail client trading Kraken perpetual futures through the
**Futures API / Kraken Pro** interface (entity: Payward Europe Digital Solutions (CY) Ltd,
CySEC 342/17) — which fee schedule applies: the Kraken Pro Futures tier table (0.02% maker /
0.05% taker at <$5M) or the consumer "Perpetual Contracts" pricing (0.25% open / 0.25% close)?

## Verdict: **Kraken Pro / Futures API schedule applies (0.02% maker / 0.05% taker at base tier)** — not the 25bps consumer schedule

This is not ambiguous once platform-access is checked: the two schedules apply to two
**different, mutually exclusive products/interfaces**, and the 0.25% schedule is explicitly
inaccessible via API.

## (a) Kraken's EEA-specific derivatives fee page

`https://support.kraken.com/articles/fees-for-derivatives-trading-eea` (accessed 2026-07-20):

- States it is scoped **"for clients residing in the European Economic Area (EEA)"** and that
  **"Investment services in relation to derivatives are provided by Payward Europe Digital
  Solutions (CY) Limited"** — the exact CySEC 342/17 entity named in the dispatch question.
- Gives a tiered maker/taker table starting at 30-day volume $0+: **maker 0.0200%, taker
  0.0500%** (the top tier at $1B+ volume shows maker -0.0050% / taker 0.0100%).
- States these fees apply **"On the legacy futures.kraken.com platform"** and **"the Kraken
  Pro platform"** — i.e., this EEA-scoped page is describing the Kraken Pro / Futures
  schedule, not a separate consumer-app number.

## (b) Kraken Pro futures fee schedule (general, non-EEA-labeled)

`https://support.kraken.com/articles/360048917612-fee-schedule` (accessed 2026-07-20) — full
table confirms the same base tier (**$0+: 0.0200% maker / 0.0500% taker**), scaling down to
0.0135%/0.0125% taker at $1B–$5B+ volume. This page **does not mention EEA/MiFID at all** —
it's the generic Kraken Pro futures schedule, which the EEA-specific page in (a) mirrors at
the base tier. No alternative 0.25% number appears anywhere on this page.

## (c) Is the EEA/MiFID retail 0.25% product even accessible via the Futures API?

`https://support.kraken.com/articles/kraken-perps` (accessed 2026-07-20) — this is the page
describing the 0.25% product, and it is explicit that it is a **different product on a
different interface**:

> "Perpetual futures on the Kraken App are only available for certain geographies (excl. US,
> UK, Canada, and Australia)."

> The product is **"App only"** and is described as separate from **"our Futures trading
> offering on Kraken Pro"** — i.e. it cannot be accessed via Kraken Pro or the Futures API.

> Fee: **"0.25% fee applied to"** the leveraged position size at both entry and exit, plus
> 8-hourly funding; **"Besides funding rates, no other fees apply."**

**This settles the access question decisively**: "Kraken Perps" (0.25% open/close) is a
mobile-app-only consumer product with no API surface. Anything trading via the Futures
API — which is what `trading-bot`'s execution path would need — is necessarily using the
Kraken Pro / futures.kraken.com product, i.e. the 0.02%/0.05% schedule in (a)/(b), regardless
of the trader's EEA/retail/non-professional classification. The 25bps consumer schedule is
not a live candidate for an API-driven bot at all — it isn't a matter of which schedule is
"more correct" for a retail client, it's that the two products are on different rails and
only one has an API.

## Step 2 — Is the 0.02% maker rate realistically available to EEA retail?

`https://support.kraken.com/articles/360000526126-what-are-maker-and-taker-fees-` (accessed
2026-07-20): maker-fee qualification is achieved via the **post-only/limit-order mechanism**
— "use the post limit order option to ensure that your limit order will be placed in the
correct side of the order book, and get the maker fee, or else it will get cancelled" — a
standard order-type flag with no EEA-specific gate found in any source reviewed (the EEA fee
page in (a) lists the same maker column with no regional carve-out or disclaimer). One
sentence: **the 0.02% base-tier maker rate is available to any account (EEA retail included)
that places post-only limit orders on the Kraken Pro futures book, since no source found
restricts maker-order placement or the maker fee column by client region — the caveat is
practical, not regulatory: whether the strategy's signal frequency/urgency tolerates resting
limit orders instead of crossing the book, which is a fill-rate question, not an access
question.**

## Sources

- [Fees for Derivatives trading for EEA clients | Kraken](https://support.kraken.com/articles/fees-for-derivatives-trading-eea)
- [Fees for Derivatives trading | Kraken](https://support.kraken.com/articles/360048917612-fee-schedule)
- [Linear Multi-Collateral Derivatives Contract Specifications for clients in the EEA | Kraken](https://support.kraken.com/articles/perpetual-contract-specifications-for-clients-in-the-eea)
- [Kraken Perps trading](https://support.kraken.com/articles/kraken-perps)
- [What are Maker and Taker fees? | Kraken](https://support.kraken.com/articles/360000526126-what-are-maker-and-taker-fees-)
- [CySEC entity record — Payward Europe Digital Solutions (CY) Limited, 342/17](https://www.cysec.gov.cy/en-GB/entities/investment-firms/cypriot/45914/)

## Unsourced / not settled

- The exact fee percentage on the EEA-specific contract-specifications page
  (`perpetual-contract-specifications-for-clients-in-the-eea`) was not stated in the fetched
  content — it referred out to the two fee pages above rather than restating numbers itself.
  Not load-bearing for the verdict since (a) and (b) both give the same base-tier numbers
  directly.
- No source explicitly confirms France-specific applicability beyond "EEA" — Payward Europe
  Digital Solutions (CY) Ltd's CySEC MiFID passporting into France was described generically
  (search result, not a fetched primary quote); if the dispatch needs a France-specific
  passporting citation (vs. EEA-wide), that would need a separate lookup (e.g. AMF/ACPR
  register) not performed here.
