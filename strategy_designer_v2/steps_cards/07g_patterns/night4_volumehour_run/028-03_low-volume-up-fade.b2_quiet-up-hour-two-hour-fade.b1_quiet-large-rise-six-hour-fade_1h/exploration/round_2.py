import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            ma = r1.abs().rolling(720, min_periods=720).mean().shift(1)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "c": c, "ma": ma, "r1": r1,
                              "hour": ts.dt.hour, "year": ts.dt.year, "pos": np.arange(len(b))})
            for L in [12, 24, 48, 72]:
                d[f"r{L}z"] = (c / c.shift(L) - 1) / (ma * np.sqrt(L))
            for H in [12, 24, 48]:
                d[f"f{H}"] = c.shift(-H) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # lookback x horizon grid of reversal slopes, per coin
    res = []
    for L in [12, 24, 48, 72]:
        for H in [12, 24, 48]:
            G = D[D.pos % H == 0].dropna(subset=[f"r{L}z", f"f{H}"]).copy()
            G["u"] = G[f"f{H}"] - G.groupby("coin")[f"f{H}"].transform("mean")
            for coin, g in G.groupby("coin"):
                r = stats.linregress(g[f"r{L}z"].clip(-6, 6), g.u)
                res.append({"L": L, "H": H, "coin": coin, "n": len(g),
                            "slope_%perz": 100 * r.slope, "t": r.slope / r.stderr})
    out["reversal grid"] = pd.DataFrame(res)
    # 24->24 by year and by bins, size
    G = D[D.pos % 24 == 0].dropna(subset=["r24z", "f24"]).copy()
    G["u"] = G.f24 - G.groupby("coin")["f24"].transform("mean")
    G["s"] = -np.sign(G.r24z) * G.u
    yy = []
    for (coin, y), g in G.groupby(["coin", "year"]):
        r = stats.linregress(g.r24z.clip(-6, 6), g.u)
        yy.append({"coin": coin, "year": y, "n": len(g), "slope_%perz": 100 * r.slope, "t": r.slope / r.stderr})
    out["24->24 slope by year"] = pd.DataFrame(yy)
    G["zb"] = pd.cut(G.r24z, [-np.inf, -2, -1, 0, 1, 2, np.inf])
    sd = G.groupby("coin")["f24"].transform("std")
    G["str"] = G.s / sd
    out["24->24 by bin: u (%), fade-signed, strength"] = G.groupby(["coin", "zb"], observed=True).apply(
        lambda x: pd.Series({"n": len(x), "u_%": 100 * x.u.mean(), "fade_%": 100 * x.s.mean(),
                             "t_fade": x.s.mean() / (x.s.std() / np.sqrt(len(x))), "strength": x["str"].mean()}))
    # side asymmetry: after rises vs after falls
    # hour 21-22 effect by coin and year
    D2 = D.dropna(subset=["r1"]).copy()
    D2["u1"] = D2.r1 - D2.groupby("coin")["r1"].transform("mean")
    D2["h2122"] = D2.hour.isin([21, 22])
    hh = D2[D2.h2122].groupby(["coin", "year"])["u1"].agg(["count", "mean", "std"])
    hh["mean_%"] = 100 * hh["mean"]; hh["t"] = hh["mean"] / (hh["std"] / np.sqrt(hh["count"]))
    out["hours 21-22 u1 by coin x year"] = hh[["count", "mean_%", "t"]]
    # 2-hour block 21-23 return per day, total
    blk = D2[D2.h2122].groupby(["coin"])["u1"].agg(["count", "mean"])
    blk["per_day_%"] = 2 * 100 * blk["mean"]
    out["hours 21-22 per coin"] = blk
    # book worst/best days: coin returns that day and prior day
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["prev_coin"] = d.coin_return.shift(1); bk.append(d.assign(coin=coin))
    B = pd.concat(bk).dropna(subset=["book_return", "coin_return"])
    B["q"] = pd.qcut(B.book_return, 10, labels=False)
    out["book decile: coin ret same/prev day"] = B.groupby("q")[["book_return", "coin_return", "prev_coin"]].mean() * 100
    return out
