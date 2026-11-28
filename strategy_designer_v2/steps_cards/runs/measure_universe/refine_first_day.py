"""Fixes the first day of the pairs older than the 720 daily candles Kraken's OHLC keeps (the daily call
returns the last 720 days whatever `since` says): the first trade after the pair's first week (public Trades,
count=1) gives the exact first trading day. Reads and rewrites the file made by fetch_kraken.py.
Usage: python3 -I refine_first_day.py KRAKEN.json"""
import json, sys, time, urllib.request, datetime as dt
p = sys.argv[1]
d = json.load(open(p))
n = 0
for alt, r in sorted(d["pairs"].items()):
    if "daily" not in r or not r["daily"]:
        continue
    clipped = r["first_week_ts"] <= r["daily"][0][0] - 7 * 86400 or r["daily"][0][0] <= time.time() - 715 * 86400
    if not clipped or "first_trade_ts" in r:
        continue
    for attempt in range(6):
        time.sleep(1.2)
        try:
            req = urllib.request.Request(f"https://api.kraken.com/0/public/Trades?pair={alt}&since={r['first_week_ts'] - 1}&count=1",
                                         headers={"User-Agent": "research-client"})
            x = json.load(urllib.request.urlopen(req, timeout=40))
            if x.get("error"):
                print(alt, x["error"], flush=True); time.sleep(30); continue
            t = next(v for k, v in x["result"].items() if k != "last")[0][2]
            r["first_trade_ts"] = int(t)
            r["first_day_ts"] = int(t) // 86400 * 86400
            n += 1
            break
        except Exception as e:
            print(alt, e, flush=True); time.sleep(10)
    if n % 50 == 0:
        json.dump(d, open(p, "w"))
json.dump(d, open(p, "w"))
print("refined", n, flush=True)
