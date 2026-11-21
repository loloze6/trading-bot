import numpy as np, pandas as pd

def explore(data):
    H = 18
    rows = []; hb = []
    for coin, wins in data["bars"].items():
        per = []
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c, hi, lo = b["close"], b["high"], b["low"]
            rng = (hi - lo).rolling(180, min_periods=90).mean()
            b["fwd"] = c.shift(-H) / c - 1
            b["fwd6"] = c.shift(-6) / c - 1
            b["fwd36"] = c.shift(-36) / c - 1
            b["r1"] = c.shift(-1) / c - 1
            b["brk_up"] = (c - hi.shift(1).rolling(12).max()) / rng
            b["brk_dn"] = (lo.shift(1).rolling(12).min() - c) / rng
            b["r42"] = c / c.shift(42) - 1
            b["narrow"] = (hi - lo).shift(1).rolling(12).mean() / rng
            b["cell"] = np.arange(len(b)) // H
            b["coin"] = coin; b["win"] = w
            ts = pd.to_datetime(b["timestamp"])
            b["hour"] = ts.dt.hour; b["wd"] = ts.dt.weekday; b["year"] = ts.dt.year
            per.append(b)
        allb = pd.concat(per)
        g = pd.concat([x.iloc[::H] for x in per])
        drift = g["fwd"].mean(); sd = g["fwd"].std()
        hb.append(allb[["hour", "wd", "r1", "coin", "year"]])
        for side in ["up", "dn"]:
            col = "brk_" + side
            s = allb[allb[col] > 0].dropna(subset=["fwd", "r42", "narrow"])
            s = s.groupby(["win", "cell"]).head(1).copy()
            sign = 1 if side == "up" else -1
            s["un"] = sign * (s["fwd"] - drift)
            s["un6"] = sign * (s["fwd6"] - drift / 3)
            s["un36"] = sign * (s["fwd36"] - 2 * drift)
            s["tot"] = sign * s["fwd"]
            s["side"] = side; s["bsize"] = s[col]
            rows.append(s)
    cs = pd.concat(rows)

    def summ(df, keys, col="un"):
        a = df.groupby(keys)[col].agg(["mean", "std", "count"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.drop(columns="std").round(5)

    out = {}
    dn = cs[cs.side == "dn"].copy()
    dn["nq"] = pd.qcut(dn["narrow"], 5, labels=False)
    out["dn breaks by range-width quintile (high=wide)"] = summ(dn, ["nq"])
    dn["rise"] = -dn["un"]  # unusual rise after a down break
    wide = dn[dn["nq"] == 4]
    out["dn wide: rise by coin"] = summ(wide, ["coin"], "rise")
    out["dn wide: rise by year"] = summ(wide, ["year"], "rise")
    out["dn wide: horizons"] = (-wide[["un6", "un", "un36"]]).agg(["mean", "count"])
    out["dn wide: rise by break size tercile"] = summ(wide.assign(bt=pd.qcut(wide["bsize"], 3, labels=False)), ["bt"], "rise")
    up = cs[cs.side == "up"].copy()
    upn = up[up.r42 <= 0].copy()
    upn["fq"] = pd.qcut(upn["r42"], 4, labels=False)
    out["up in falling week by 7d ret quartile (0=deepest)"] = summ(upn, ["fq"])
    out["up falling week by coin"] = summ(upn, ["coin"])
    out["up falling week by year"] = summ(upn, ["year"])
    upp = up[up.r42 > 0].copy()
    upp["bq"] = pd.qcut(upp["bsize"], 8, labels=False)
    out["up rising week by break octile"] = summ(upp, ["bq"])
    top = upp[upp.bq >= 6]
    out["up rising top quarter by coin"] = summ(top, ["coin"])
    out["up rising top quarter by year"] = summ(top, ["year"])
    h = pd.concat(hb).dropna()
    a = h[h.hour == 16].groupby("year")["r1"].agg(["mean", "count"])
    out["16h bar by year"] = a.round(6)
    a = h[h.hour == 16].groupby("coin")["r1"].agg(["mean", "count"])
    out["16h bar by coin"] = a.round(6)
    return out
