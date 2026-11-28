"""Builds common/universe_measure_2026-11-28.csv from the raw Kraken and CoinGecko answers
(fetch_kraken.py, fetch_categories.py). Reads dates, volumes, prices and category lists only; nothing here reads
a bar to make a trading decision.
Usage: python3 -I build_table.py KRAKEN.json COINGECKO.json OUT.csv"""
import csv, datetime as dt, json, statistics, sys
from pathlib import Path

COMMON = Path(__file__).resolve().parents[2] / "common"
sys.path.insert(0, str(COMMON))
import coins   # the repository's own rules: windows, 90-day rule, warm-up start, groups

END = dt.date(2026, 11, 27)            # the last complete UTC day of the measure (run on 2026-11-28)
D12, D3 = 365, 90                      # the 12 months and the 3 months, in days
WARMUPS = {"90rule": 0, "w395": 395, "w790": 790}
LIQUID, YEARS, CHECK_NEED = 100_000, 3, 7
BASE_NAMES = {"XBT": "BTC", "XDG": "DOGE"}           # Kraken's own names for BTC and DOGE
FIAT = {"AUD", "EUR", "GBP", "CAD", "CHF", "JPY", "USD"}
OUR7 = {"payments": ["payment-solutions"], "platforms": ["smart-contract-platform", "layer-1"],
        "privacy": ["privacy-coins"], "finance": ["decentralized-finance-defi"],
        "infrastructure": ["infrastructure", "oracle", "storage", "depin"], "ai": ["artificial-intelligence"],
        "meme": ["meme-token"]}
STABLE, WRAPPED, TOKENIZED = ["stablecoins"], ["wrapped-tokens", "liquid-staking-tokens", "liquid-staking"], \
    ["tokenized-gold", "tokenized-commodities", "tokenized-stock", "real-world-assets-rwa"]
OTHERS = ["gaming", "metaverse", "non-fungible-tokens-nft", "exchange-based-tokens", "layer-2", "interoperability",
          "bitcoin-layer-2"]


def day(ts):
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).date()


def stats(by_day, first, n_days):
    """median and mean of the traded value (close x volume), and median trades, over the last n_days calendar days
    (from the coin's first day if it is younger); a day with no row counts as 0."""
    start = max(first, END - dt.timedelta(days=n_days - 1))
    days = [start + dt.timedelta(days=i) for i in range((END - start).days + 1)]
    if not days:
        return None
    v = [by_day.get(d, (0, 0))[0] for d in days]
    t = [by_day.get(d, (0, 0))[1] for d in days]
    return {"n": len(days), "median": statistics.median(v), "mean": sum(v) / len(v), "trades": statistics.median(t)}


def window_counts(first, windows):
    """per warm-up: windows usable on the first day alone (holes ignored): all, check half, before the check half.
    A window is used when it starts after the coin's first 90 days and the coin's first day is on or before the
    first day the wrapper loads (coins.warmup_start)."""
    out = {}
    for name, w in WARMUPS.items():
        ok = []
        for x in windows:
            s = x["test"]["start"]
            good = dt.date.fromisoformat(s) >= first + dt.timedelta(days=coins.LISTING_DAYS)
            if good and w:
                good = first <= coins.warmup_start(s, w * 86400)
            ok.append(good)
        chk = [g for g, x in zip(ok, windows) if x["test"]["start"] >= coins.CHECK_FROM]
        out[name] = (sum(ok), sum(chk), sum(ok) - sum(chk))
    return out


def main(kraken_file, cg_file, out_file):
    K, CG = json.loads(Path(kraken_file).read_text()), json.loads(Path(cg_file).read_text())
    windows = json.loads(coins.WINDOWS.read_text(encoding="utf-8"))
    check_n = len(coins.check_half(windows))
    have = {p.name[len("kraken_"):-len("USD_1d.csv")] for p in coins.DATA.glob("kraken_*USD_1d.csv")}
    final, portfolio = set(coins.FINAL), set(coins.portfolio_group())
    cat_of = {c: k for k, v in coins.CATEGORIES.items() for c in v}

    # CoinGecko: symbol -> best-ranked id among the top coins; id -> the categories read that list it
    best = {}
    for r in sorted(CG["top"], key=lambda r: (r["rank"] is None, r["rank"] or 0)):
        best.setdefault(r["symbol"], r["id"])
    member = {}
    for cat, rows in CG["categories"].items():
        for r in rows:
            member.setdefault(r["id"], set()).add(cat)
    perps = {}
    for s, f in K["futures"].items():
        if f["quote"] == "USD" and f["tag"] == "perpetual":
            perps.setdefault(BASE_NAMES.get(f["base"], f["base"]), (s, f))

    rows = []
    for alt, meta in sorted(K["asset_pairs"].items()):
        rec = K["pairs"].get(alt, {})
        coin = BASE_NAMES.get(meta["wsname"][:-4], meta["wsname"][:-4])
        row = {"coin": coin, "pair": alt, "status": meta["status"]}
        if "first_day_ts" not in rec:
            row.update({"class": "no data", "notes": "; ".join(rec.get("errors", ["no OHLC rows"]))})
            rows.append(row); continue
        first = day(rec["first_day_ts"])
        by_day = {day(t): (c * v, n) for t, c, v, n in rec["daily"] if day(t) <= END}
        s12, s3 = stats(by_day, first, D12), stats(by_day, first, D3)
        tk = K["ticker"].get(meta["key"]) or K["ticker"].get(alt)
        spread = None
        if tk and tk["ask"] and tk["bid"]:
            spread = round((tk["ask"] - tk["bid"]) / ((tk["ask"] + tk["bid"]) / 2) * 100, 4)
        price = next((c for t, c, v, n in reversed(rec["daily"]) if day(t) <= END), None)
        wc = window_counts(first, windows)
        ids = best.get(coin)
        cats = member.get(ids, set()) if ids else set()
        # class: listed apart, never dropped
        if coin in FIAT:
            cls = "fiat"
        elif not ids:
            cls = "unclassified"
        elif cats & set(STABLE):
            cls = "stablecoin"
        elif cats & set(WRAPPED):
            cls = "wrapped_or_staked"
        elif cats & set(TOKENIZED) and "tokenized-gold" in cats:
            cls = "tokenized_commodity"
        else:
            cls = "coin"
        matches = [k for k, v in OUR7.items() if cats & set(v)]
        if coin in cat_of:
            category, source = cat_of[coin], "coins.md"
        elif not ids:
            category, source = "unknown", "not in CoinGecko's top 2,500"
        elif len(matches) == 1:
            category, source = matches[0], "coingecko"
        elif len(matches) > 1:
            category, source = "ambiguous", "coingecko"
        else:
            category, source = "unknown", "coingecko lists none of the 7"
        group = "final" if coin in final else "portfolio" if coin in portfolio else "file, left out of the universe" \
            if coin in have else ""
        perp = perps.get(coin)
        pc = {}
        if perp:
            s, f = perp
            vals = [c * v for t, c, v in (f["candles"] or []) if day(t) <= END and day(t) > END - dt.timedelta(days=D3)]
            pc = {"perp_symbol": s, "perp_tradeable": f["tradeable"] and not f["suspended"],
                  "perp_opened": (f["opening_date"] or "")[:10], "perp_volume_usd_24h": f["volume_quote_24h"],
                  "perp_median_daily_usd_3m": round(statistics.median(vals)) if vals else None,
                  "perp_kraken_category": f["category"]}
        row.update({
            "class": cls, "price_last": price, "first_day": first.isoformat(),
            "years_history": round((END - first).days / 365.25, 2),
            "value_median_12m": round(s12["median"]), "value_mean_12m": round(s12["mean"]), "days_12m": s12["n"],
            "value_median_3m": round(s3["median"]), "value_mean_3m": round(s3["mean"]), "days_3m": s3["n"],
            "trades_median_12m": s12["trades"], "trades_median_3m": s3["trades"], "spread_pct": spread,
            "has_perp": bool(perp), **pc})
        for name, (a, c, p) in wc.items():
            row.update({f"win_{name}_all32": a, f"win_{name}_check14": c, f"win_{name}_before2022": p})
        row.update({"have_file": coin in have, "group": group, "category": category, "category_source": source,
                    "cg_our7_matches": "|".join(matches), "cg_other_categories":
                    "|".join(sorted(c for c in cats if c in OTHERS)), "cg_all_read": "|".join(sorted(cats))})
        row["pass_liquid_100k_12m"] = s12["median"] >= LIQUID
        row["pass_3y"] = first <= END + dt.timedelta(days=1) - dt.timedelta(days=round(365.25 * YEARS))
        row["pass_w790_7of14"] = wc["w790"][1] >= CHECK_NEED
        row["pass_w395_7of14"] = wc["w395"][1] >= CHECK_NEED
        rows.append(row)

    cols = ["coin", "pair", "status", "class", "category", "category_source", "have_file", "group", "first_day",
            "years_history", "price_last", "value_median_12m", "value_mean_12m", "days_12m", "value_median_3m",
            "value_mean_3m", "days_3m", "trades_median_12m", "trades_median_3m", "spread_pct", "has_perp",
            "perp_symbol", "perp_tradeable", "perp_opened", "perp_volume_usd_24h", "perp_median_daily_usd_3m",
            "perp_kraken_category"] + [f"win_{n}_{k}" for n in WARMUPS for k in ("all32", "check14", "before2022")] + \
           ["pass_liquid_100k_12m", "pass_3y", "pass_w790_7of14", "pass_w395_7of14", "cg_our7_matches",
            "cg_other_categories", "cg_all_read", "notes"]
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "rows;", sum(r.get("class") == "no data" for r in rows), "without data;", check_n, "check windows")


main(*sys.argv[1:4])
