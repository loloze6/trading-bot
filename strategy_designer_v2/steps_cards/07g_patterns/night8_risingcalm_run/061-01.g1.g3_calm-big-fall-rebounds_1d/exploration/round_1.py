import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            b["r"] = r; b["z"] = r / sd.shift(1)
            b["calm"] = (b["regime"] != "chop").astype(int)
            b["tr60"] = c / c.shift(60) - 1
            b["sdrank"] = sd
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            for h in (1, 3, 10):
                b[f"f{h}"] = c.shift(-h) / c - 1
                b[f"g{h}"] = (np.arange(len(b)) % h == 0)
            b["coin"] = coin; b["win"] = w
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b[["coin","win","day","yr","wd","r","z","calm","tr60","sdrank","f1","f3","f10","g1","g3","g10"]])
    d = pd.concat(rows, ignore_index=True)
    out = {}
    for h in (1, 3, 10):
        g = d[d[f"g{h}"]].dropna(subset=[f"f{h}", "z"]).copy()
        g["ex"] = g[f"f{h}"] - g.groupby("coin")[f"f{h}"].transform("mean")
        g["zb"] = pd.cut(g["z"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
        t = g.groupby(["calm", "zb"], observed=True)["ex"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        out[f"h{h} excess by calm x z"] = t.round(4)
        reg = []
        for cm in (0, 1):
            s = g[g.calm == cm]
            dd = s.groupby("day")[["ex", "z"]].sum()
            lr = stats.linregress(dd["z"], dd["ex"])
            reg.append([cm, lr.slope, lr.slope / lr.stderr, len(dd)])
        out[f"h{h} slope ex on z (day-summed)"] = pd.DataFrame(reg, columns=["calm", "slope", "t", "days"])
    g = d[d["g1"]].dropna(subset=["f1"]).copy()
    g["ex"] = g["f1"] - g.groupby("coin")["f1"].transform("mean")
    t = g.groupby(["calm", "wd"])["ex"].agg(["mean", "count", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["h1 by calm x weekday"] = t.round(4)
    g = d[d["g10"]].dropna(subset=["f10", "tr60"]).copy()
    g["ex"] = g["f10"] - g.groupby("coin")["f10"].transform("mean")
    g["trb"] = pd.cut(g["tr60"], [-9, -0.1, 0.1, 99])
    t = g.groupby(["calm", "trb"], observed=True)["ex"].agg(["mean", "count", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["h10 by calm x trend60"] = t.round(4)
    g = d[d["g3"]].dropna(subset=["f3", "z", "tr60"]).copy()
    g["ex"] = g["f3"] - g.groupby("coin")["f3"].transform("mean")
    g["trb"] = pd.cut(g["tr60"], [-9, -0.1, 0.1, 99]); g["zs"] = np.sign(g["z"]) * (g["z"].abs() > 1)
    t = g.groupby(["trb", "calm", "zs"], observed=True)["ex"].agg(["mean", "count", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["h3 by trend x calm x bigday sign"] = t.round(4)
    # book
    dy = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dy.append(x)
    dy = pd.concat(dy).dropna(subset=["book_return"])
    bk = dy.groupby(["win", "day"])[["book_return", "coin_return"]].mean()
    bw = bk.groupby(level=0).agg(["mean", "count"])
    out["book by window"] = bw.round(5)
    q = bk["book_return"]
    out["book top/bottom 5% days: coin return"] = pd.DataFrame({
        "top": [q[q >= q.quantile(.95)].mean(), bk["coin_return"][q >= q.quantile(.95)].mean()],
        "bottom": [q[q <= q.quantile(.05)].mean(), bk["coin_return"][q <= q.quantile(.05)].mean()]}, index=["book", "coin"])
    return out
