import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            b["fwd"] = c.shift(-H) / c - 1
            b["r1"] = c.pct_change()
            b["r28"] = c / c.shift(28) - 1
            b["r14"] = c / c.shift(14) - 1
            b["rng"] = (b["high"] - b["low"]) / c
            b["rr7_40"] = b["rng"].rolling(7).mean() / b["rng"].rolling(40).mean()
            b["vr7_40"] = b["volume"].rolling(7).mean() / b["volume"].rolling(40).mean()
            b["vr14_40"] = b["volume"].rolling(14).mean() / b["volume"].rolling(40).mean()
            b["coin"] = coin; b["w"] = w
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b.iloc[::H])
    d = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    drift = d.groupby("coin")["fwd"].mean(); usual = d.groupby("coin")["fwd"].std()
    d["un"] = d["fwd"] - d["coin"].map(drift)
    d["z"] = d["un"] / d["coin"].map(usual)
    d["r28z"] = d["r28"] / d.groupby("coin")["r28"].transform("std")
    d["trend"] = d["regime"] == "trending"
    out = {}
    def slope(df, x):
        df = df.dropna(subset=[x, "z"])
        r = stats.linregress(df[x], df["z"])
        # day-clustered t for sum of x*z
        p = (df[x] - df[x].mean()) * df["z"]
        pd_ = p.groupby(df["day"]).sum()
        tday = pd_.mean() / (pd_.std() / np.sqrt(len(pd_)))
        return pd.Series({"slope": r.slope, "t_ols": r.slope / r.stderr, "t_day": tday, "n": len(df), "days": len(pd_)})
    res = {}
    for reg in [True, False]:
        sub = d[d["trend"] == reg]
        res[f"lowvol={reg} all r28"] = slope(sub, "r28z")
        res[f"lowvol={reg} r28>0"] = slope(sub[sub["r28"] > 0], "r28z")
        res[f"lowvol={reg} r28<0"] = slope(sub[sub["r28"] < 0], "r28z")
        res[f"lowvol={reg} all r14"] = slope(sub.assign(r28z=sub["r14"] / sub.groupby("coin")["r14"].transform("std")), "r28z")
    out["slope z on r28 by regime"] = pd.DataFrame(res).T.round(3)
    # per window, low-vol regime, r28 slope
    pw = {}
    for w, sub in d[d["trend"]].groupby("w"):
        if len(sub.dropna(subset=["r28z"])) > 10:
            pw[w] = slope(sub, "r28z")
    out["lowvol r28 slope per window"] = pd.DataFrame(pw).T.round(3)
    pc = {}
    for cn, sub in d[d["trend"]].groupby("coin"):
        pc[cn] = slope(sub, "r28z")
    out["lowvol r28 slope per coin"] = pd.DataFrame(pc).T.round(3)
    # range compression and volume ratio, short windows
    res2 = {}
    for x in ["rr7_40", "vr7_40", "vr14_40", "r1"]:
        d[x + "s"] = d[x] / d.groupby("coin")[x].transform("std")
        res2[x + " all"] = slope(d, x + "s")
        res2[x + " lowvol"] = slope(d[d["trend"]], x + "s")
    out["other slopes"] = pd.DataFrame(res2).T.round(3)
    d["qrr"] = d.groupby("coin")["rr7_40"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    s = d.groupby("qrr")["z"].agg(["mean", "count", "std"]); s["t"] = s["mean"] / (s["std"] / np.sqrt(s["count"]))
    out["z by range-compression quintile"] = s.round(3)
    # interaction: r28 sign x range compression
    d["up28"] = d["r28"] > 0
    d["lowrng"] = d["qrr"] <= 1
    s = d.groupby(["up28", "lowrng"])["z"].agg(["mean", "count", "std"]); s["t"] = s["mean"] / (s["std"] / np.sqrt(s["count"]))
    out["z by r28 sign x low range"] = s.round(3)
    return out
