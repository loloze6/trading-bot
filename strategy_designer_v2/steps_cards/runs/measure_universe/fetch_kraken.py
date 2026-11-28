"""Reads Kraken's public API (no key) for every USD spot pair and writes the raw answers to one JSON file:
the pair list, each pair's first week (weekly OHLC) and first day (daily OHLC from that week), its last 720 daily
candles, the Ticker, and the Kraken Futures instruments, tickers and daily candles. Gentle: a pause between calls,
a wait and a retry on a rate limit; resumable (a pair already in the file is not read again).
Usage: python3 -I fetch_kraken.py OUT.json"""
import json, sys, time, urllib.request, urllib.error, datetime as dt
from pathlib import Path

SPOT = "https://api.kraken.com/0/public/"
FUT = "https://futures.kraken.com/"
PAUSE = 1.2          # seconds between calls
NOW = int(time.time())
TODAY = int(dt.datetime.fromtimestamp(NOW, dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).timestamp())


def get(url, tries=8):
    for attempt in range(tries):
        time.sleep(PAUSE)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "research-client"})
            with urllib.request.urlopen(req, timeout=40) as r:
                d = json.load(r)
            err = d.get("error") if isinstance(d, dict) else None
            if err and any("Rate limit" in e or "Too many" in e for e in err):
                print("rate limit, wait 40s", flush=True); time.sleep(40); continue
            return d
        except urllib.error.HTTPError as e:
            wait = 60 if e.code == 429 else 10
            print(f"HTTP {e.code} {url[:90]}, wait {wait}s", flush=True); time.sleep(wait)
        except Exception as e:
            print(f"error {e}, wait 10s", flush=True); time.sleep(10)
    return {"error": ["gave up"], "result": {}}


def ohlc(pair, interval, since=None):
    d = get(f"{SPOT}OHLC?pair={pair}&interval={interval}" + (f"&since={since}" if since is not None else ""))
    if d.get("error"):
        return None, d["error"]
    rows = next((v for k, v in d["result"].items() if k != "last"), [])
    return rows, []


def main(out):
    out_path = Path(out)
    data = json.loads(out_path.read_text()) if out_path.exists() else {"pairs": {}, "ticker": {}, "futures": {}}
    data["fetched_at_utc"] = dt.datetime.fromtimestamp(NOW, dt.timezone.utc).isoformat(timespec="seconds")
    ap = get(SPOT + "AssetPairs")["result"]
    usd = {v["altname"]: {"key": k, "wsname": v["wsname"], "base": v["base"], "status": v.get("status"),
                          "ordermin": v.get("ordermin"), "costmin": v.get("costmin")}
           for k, v in ap.items() if v["wsname"].endswith("/USD")}
    data["asset_pairs"] = usd
    print("USD pairs:", len(usd), flush=True)

    for i, (alt, meta) in enumerate(sorted(usd.items()), 1):
        if alt in data["pairs"]:
            continue
        rec = {"errors": []}
        wk, err = ohlc(alt, 10080)
        if err or not wk:
            rec["errors"] += ["weekly: " + "; ".join(err or ["no rows"])]
            data["pairs"][alt] = rec
            continue
        rec["first_week_ts"] = wk[0][0]
        daily_from, err = ohlc(alt, 1440, wk[0][0] - 1)      # the 720 days from the first week: its first row is the first trading day
        if err or not daily_from:
            rec["errors"] += ["daily from first week: " + "; ".join(err or ["no rows"])]
            data["pairs"][alt] = rec
            continue
        rec["first_day_ts"] = daily_from[0][0]
        if daily_from[-1][0] >= TODAY - 86400:               # the 720 days reach yesterday: one call covers all
            recent = daily_from
        else:
            recent, err = ohlc(alt, 1440)
            if err:
                rec["errors"] += ["daily last 720: " + "; ".join(err)]; recent = []
        # keep time, close, volume, trade count of each candle (the day still forming is left out later)
        rec["daily"] = [[r[0], float(r[4]), float(r[6]), int(r[7])] for r in recent]
        data["pairs"][alt] = rec
        if i % 25 == 0:
            out_path.write_text(json.dumps(data)); print(i, "pairs", flush=True)
    out_path.write_text(json.dumps(data))

    # the Ticker, 40 pairs a call
    alts = sorted(usd)
    for j in range(0, len(alts), 40):
        d = get(SPOT + "Ticker?pair=" + ",".join(alts[j:j + 40]))
        for k, v in d.get("result", {}).items():
            data["ticker"][k] = {"ask": float(v["a"][0]), "bid": float(v["b"][0]), "last": float(v["c"][0])}
    data["ticker_keys"] = {meta["key"]: alt for alt, meta in usd.items()}
    out_path.write_text(json.dumps(data))

    # Kraken Futures: instruments, tickers, and each perpetual's daily candles of the last 120 days
    ins = get(FUT + "derivatives/api/v3/instruments")["instruments"]
    tick = {t["symbol"]: t for t in get(FUT + "derivatives/api/v3/tickers")["tickers"]}
    data["futures"] = {i["symbol"]: {"base": i.get("base"), "quote": i.get("quote"), "tradeable": i.get("tradeable"),
                                     "type": i.get("type"), "opening_date": i.get("openingDate"),
                                     "category": i.get("category"), "suspended": i.get("suspended"),
                                     "tag": tick.get(i["symbol"], {}).get("tag"),
                                     "vol24h": tick.get(i["symbol"], {}).get("vol24h"),
                                     "volume_quote_24h": tick.get(i["symbol"], {}).get("volumeQuote"),
                                     "open_interest": tick.get(i["symbol"], {}).get("openInterest"),
                                     "candles": None} for i in ins}
    for s, f in data["futures"].items():
        if f["quote"] != "USD" or f["tag"] != "perpetual":
            continue
        d = get(f"{FUT}api/charts/v1/trade/{s}/1d?from={TODAY - 120 * 86400}&to={TODAY - 1}")
        f["candles"] = [[int(c["time"]) // 1000, float(c["close"]), float(c["volume"])] for c in d.get("candles", [])]
    out_path.write_text(json.dumps(data))
    print("done", flush=True)


main(sys.argv[1])
