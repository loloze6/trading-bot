"""Reads CoinGecko's public category lists (no key) into one JSON file: the top coins by market cap (symbol -> id) and,
for each category read, the ids it lists. Gentle: a pause between calls, a longer wait and a retry on a rate limit.
Usage: python3 fetch_categories.py OUT.json"""
import json, sys, time, urllib.request, urllib.error

API = "https://api.coingecko.com/api/v3/coins/markets"
PAUSE, TOP_PAGES, CAT_PAGES = 7, 10, 8
OUR7 = ["payment-solutions", "smart-contract-platform", "layer-1", "privacy-coins", "decentralized-finance-defi",
        "infrastructure", "oracle", "storage", "depin", "artificial-intelligence", "meme-token"]
OTHER = ["gaming", "metaverse", "non-fungible-tokens-nft", "exchange-based-tokens", "layer-2", "stablecoins",
         "wrapped-tokens", "liquid-staking-tokens", "liquid-staking", "tokenized-gold", "tokenized-commodities",
         "tokenized-stock", "real-world-assets-rwa", "interoperability", "bitcoin-layer-2"]


def get(params):
    url = API + "?" + "&".join(f"{k}={v}" for k, v in params.items())
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "research-client"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            wait = 70 * (attempt + 1) if e.code == 429 else 15
            print(f"HTTP {e.code} on {params}, wait {wait}s", flush=True)
            time.sleep(wait)
        except Exception as e:
            print(f"error {e}, wait 15s", flush=True); time.sleep(15)
    raise SystemExit(f"gave up on {params}")


def pages(base, max_pages):
    rows = []
    for p in range(1, max_pages + 1):
        time.sleep(PAUSE)
        got = get({**base, "per_page": 250, "page": p})
        rows += [{"id": r["id"], "symbol": r["symbol"].upper(), "rank": r.get("market_cap_rank")} for r in got]
        if len(got) < 250:
            break
    return rows


out = {"top": pages({"vs_currency": "usd", "order": "market_cap_desc"}, TOP_PAGES), "categories": {}}
print("top", len(out["top"]), flush=True)
for c in OUR7 + OTHER:
    out["categories"][c] = pages({"vs_currency": "usd", "order": "market_cap_desc", "category": c}, CAT_PAGES)
    print(c, len(out["categories"][c]), flush=True)
    json.dump(out, open(sys.argv[1], "w"))
