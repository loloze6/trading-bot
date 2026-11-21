import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 18
    rows = []      # breakout cases, up and down
    grid = []      # non-overlapping bar-level samples
    hb = []        # 1-bar returns by hour/weekday
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
            b["barmove"] = (c / c.shift(1) - 1) / ((hi - lo) / c).rolling(180, min_periods=90).mean()
            b["cell"] = np.arange(len(b)) // H
            b["coin"] = coin; b["win"] = w
            ts = pd.to_datetime(b["timestamp"])
            b["hour"] = ts.dt.hour; b["wd"] = ts.dt.weekday
            per.append(b)
        allb = pd.concat(per)
        g = allb[np.arange(len(allb)) >= 0]
        g = pd.concat([x.iloc[::H] for x in per])
        drift = g["fwd"].mean(); sd = g["fwd"].std()
        g = g.assign(un=(g["fwd"] - drift) / sd, unraw=g["fwd"] - drift)
        grid.append(g)
        hb.append(allb[["hour", "wd", "r1", "coin"]])
        for side in ["up", "dn"]:
            col = "brk_" + side
            s = allb[allb[col] > 0].dropna(subset=["fwd", "r42", "narrow"])
            s = s.groupby(["win", "cell"]).head(1).copy()
            sign = 1 if side == "up" else -1
            s["un"] = sign * (s["fwd"] - drift)
            s["un6"] = sign * (s["fwd6"] - drift / 3)
            s["un36"] = sign * (s["fwd36"] - 2 * drift)
            s["strength"] = s["un"] / sd
            s["side"] = side; s["bsize"] = s[col]
            rows.append(s)
    cs = pd.concat(rows); gr = pd.concat(grid)

    def summ(df, keys, col="un"):
        a = df.groupby(keys)[col].agg(["mean", "std", "count"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.drop(columns="std").round(5)

    cs["reg"] = np.where(cs["r42"] > 0, "r7pos", "r7neg")
    cs["bq"] = cs.groupby(["side", "reg"])["bsize"].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates="drop"))
    cs["nq"] = cs.groupby("side")["narrow"].transform(lambda x: pd.qcut(x, 3, labels=False))
    cs["mq"] = cs.groupby("side")["r42"].transform(lambda x: pd.qcut(x, 5, labels=False))
    gr["mq"] = pd.qcut(gr["r42"], 5, labels=False)
    gr["nq"] = pd.qcut(gr["narrow"], 3, labels=False)
    gr["abs"] = gr["un"].abs()
    gr["bm"] = pd.qcut(gr["barmove"], 5, labels=False)
    out = {
        "breaks by side x 7d regime": summ(cs, ["side", "reg"]),
        "breaks size quartile": summ(cs, ["side", "reg", "bq"]),
        "breaks by narrowness tercile": summ(cs, ["side", "nq"]),
        "breaks by 7d return quintile": summ(cs, ["side", "mq"]),
        "up r7pos horizons 6/18/36": cs[(cs.side=="up")&(cs.reg=="r7pos")][["un6","un","un36"]].agg(["mean","count"]),
        "breaks by coin": summ(cs, ["side", "coin"]),
        "grid: fwd18 std-units by 7d ret quintile": summ(gr, ["mq"]),
        "grid: abs move by narrowness": summ(gr, ["nq"], "abs"),
        "grid: fwd by last bar move quintile": summ(gr, ["bm"]),
    }
    h = pd.concat(hb).dropna()
    for k in ["hour", "wd"]:
        a = h.groupby(k)["r1"].agg(["mean", "std", "count"]); a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        out["1bar by " + k] = a.drop(columns="std").round(6)
    d = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            d.append(x.assign(coin=coin, year=pd.to_datetime(x["day"]).dt.year))
    d = pd.concat(d).dropna(subset=["book_return"])
    dd = d.groupby(["year"])[["book_return", "coin_return"]].mean()
    dd["n"] = d.groupby("year").size()
    out["book by year"] = dd.round(5)
    return out
