import numpy as np
import pandas as pd
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    n = len(x)
    if n < 3 or x.std(ddof=1) == 0:
        return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
    return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(n))})

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        g3 = []
        frames = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r1 = c.pct_change()
            d = pd.DataFrame({
                "wd": ts.dt.weekday.values,
                "year": ts.dt.year.values,
                "r1": r1.values,
                "rprev": r1.shift(1).values,
                "f1": (c.shift(-1) / c - 1).values,
                "f3": (c.shift(-3) / c - 1).values,
                "vol20": r1.rolling(20).std().values,
                "vol60": r1.rolling(60).std().values,
                "mabs": r1.abs().rolling(20).mean().shift(1).values,
                "alloc": b["postRebalance_current_allocation"].values,
            })
            d["coin"] = coin
            frames.append(d)
            g3.append((c.iloc[::3].shift(-1) / c.iloc[::3] - 1).dropna())
        g3 = pd.concat(g3)
        drift, usual = g3.mean(), g3.std(ddof=1)
        D = pd.concat(frames)
        D["drift3"] = drift
        D["u3"] = (D["f3"] - drift) / usual
        D["volratio"] = D["vol20"] / D["vol60"]
        D["vrank"] = D["vol20"].rank(pct=True)
        D["z"] = D["r1"] / D["mabs"]
        rows.append(D)
    A = pd.concat(rows).dropna(subset=["r1", "u3"])
    A["fade3"] = -np.sign(A["r1"]) * A["u3"]
    out = {}

    # coin daily return by weekday, t (each weekday's bars 7 days apart)
    out["coin 1d return by weekday of the return"] = A.groupby("wd")["r1"].apply(_t).unstack()

    S = A[A["wd"] == 6].copy()
    # graded vol: regression of fade3 on vol rank, Sunday and other days
    for nm, sub in [("Sun", S), ("Mon-Sat", A[A["wd"] != 6])]:
        sub = sub.dropna(subset=["vrank"])
        sl = stats.linregress(sub["vrank"], sub["fade3"])
        out[f"{nm}: fade3 on vol rank slope"] = pd.Series({"n": len(sub), "slope": sl.slope, "t": sl.slope / sl.stderr})
    # vol rising vs falling (vol20/vol60) on Sunday
    S["vrq"] = pd.qcut(S["volratio"], 3, labels=["volfalling", "mid", "volrising"])
    out["Sun fade3 by vol20/vol60 tercile"] = S.groupby("vrq")["fade3"].apply(_t).unstack()
    # per-coin Sunday fade, high vs low vol half
    S["hv"] = S.groupby("coin")["vol20"].transform(lambda x: x > x.median())
    pc = S.groupby(["coin", "hv"])["fade3"].mean().unstack()
    pc["diff"] = pc[True] - pc[False]
    out["per coin Sunday fade3: high minus low vol half"] = pc.round(3)
    out["share of coins hv>lv"] = float((pc["diff"] > 0).mean())
    # Sunday move after same-sign Saturday vs opposite
    S["same"] = np.sign(S["rprev"]) == np.sign(S["r1"])
    out["Sun fade3 by Sat move same sign"] = S.groupby("same")["fade3"].apply(_t).unstack()
    # Saturday: 1d fade but 3d continuation, by vol
    Sa = A[A["wd"] == 5].copy()
    Sa["vq"] = pd.qcut(Sa["vrank"], 3, labels=["lowvol", "midvol", "highvol"])
    out["Sat fade3 by vol tercile"] = Sa.groupby("vq")["fade3"].apply(_t).unstack()
    # weekday (Mon-Fri) low-vol continuation, graded by z within low vol
    W = A[(A["wd"] < 5)].copy()
    W["vq"] = pd.qcut(W["vrank"], 3, labels=["lowvol", "midvol", "highvol"])
    W["zq"] = pd.qcut(W["z"].abs(), 3, labels=["small", "mid", "large"])
    out["Mon-Fri fade3 by vol x |z|"] = W.groupby(["vq", "zq"])["fade3"].mean().unstack().round(4)
    # Sunday fade by year in high vs low vol half
    out["Sun fade3 by year x hv"] = S.groupby(["year", "hv"])["fade3"].mean().unstack().round(3)

    # trades: side by year and drift explanation
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tt = t[["side", "net_profit_loss_percent", "profit_loss_percent", "duration_minutes", "entry_time"]].copy()
            tt["year"] = pd.to_datetime(tt["entry_time"], utc=True).dt.year
            tr.append(tt)
    tr = pd.concat(tr)
    tr["days"] = tr["duration_minutes"] / 1440
    out["trades side stats"] = tr.groupby("side").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"),
                                                      net=("net_profit_loss_percent", "mean"), days=("days", "mean"))
    out["trades net by year x side"] = tr.groupby(["year", "side"])["net_profit_loss_percent"].mean().unstack().round(3)
    # Sunday fade split by sign, unusual vs total 3d
    S["tot3"] = -np.sign(S["r1"]) * S["f3"]
    S["sign"] = np.where(S["r1"] > 0, "rise", "fall")
    out["Sun total 3d fade return by sign"] = S.groupby("sign")["tot3"].apply(_t).unstack()

    # book's worst/best days: weekday distribution
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d[["day", "book_return"]].copy()
            dd["w"] = w
            bd.append(dd)
    bd = pd.concat(bd).dropna()
    book = bd.groupby(["w", "day"])["book_return"].mean().reset_index()
    book["wd"] = pd.to_datetime(book["day"]).dt.weekday
    q = book["book_return"].quantile([0.02, 0.98])
    out["book worst 2% days by weekday"] = book[book["book_return"] <= q.iloc[0]]["wd"].value_counts().sort_index()
    out["book best 2% days by weekday"] = book[book["book_return"] >= q.iloc[1]]["wd"].value_counts().sort_index()
    out["book daily by weekday t"] = book.groupby("wd")["book_return"].apply(_t).unstack()
    return out
