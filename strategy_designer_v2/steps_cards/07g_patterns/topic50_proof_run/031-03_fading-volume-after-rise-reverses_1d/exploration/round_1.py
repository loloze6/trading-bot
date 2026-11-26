import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    # coin overall mean h-day return on grid
    def grid_rows(h, lookbacks):
        rows = []
        for coin, ws in bars.items():
            for w, df in ws.items():
                c = df["close"].astype(float).values
                v = df["volume"].astype(float).values
                n = len(c)
                r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
                for t in range(0, n-h, h):
                    row = {"coin": coin, "w": w, "t": t, "fwd": c[t+h]/c[t]-1,
                           "wd": pd.Timestamp(df["timestamp"].iloc[t]).weekday()}
                    for k in lookbacks:
                        if t-k >= 0:
                            row[f"past{k}"] = c[t]/c[t-k]-1
                            sd = np.nanstd(r1[max(1,t-k+1):t+1])
                            row[f"z{k}"] = (np.log(c[t]/c[t-k]))/(sd*np.sqrt(k)) if sd>0 else np.nan
                            row[f"vr{k}"] = np.mean(v[max(0,t-13):t+1])/np.mean(v[t-k+1:t+1]) - 1
                    rows.append(row)
        g = pd.DataFrame(rows)
        g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
        return g
    res = []
    for h in [3, 5, 10, 20, 30]:
        lbs = [5, 10, 20, 30, 60]
        g = grid_rows(h, lbs)
        for k in lbs:
            col = f"z{k}"
            if col not in g: continue
            s = g[[col, "ex"]].dropna()
            if len(s) < 30: continue
            lr = stats.linregress(s[col], s["ex"])
            # also signed by top/bottom quartile
            q = s[col].quantile([0.2, 0.8]).values
            hi = s[s[col] >= q[1]]["ex"].mean(); lo = s[s[col] <= q[0]]["ex"].mean()
            res.append({"h": h, "lookback": k, "n": len(s), "slope": lr.slope, "t": lr.slope/lr.stderr,
                        "ex_top20": hi, "ex_bot20": lo})
            colv = f"vr{k}"
            s2 = g[[colv, "ex"]].dropna()
            if k >= 20 and len(s2) > 30:
                lr2 = stats.linregress(s2[colv], s2["ex"])
                res.append({"h": h, "lookback": f"volratio14/{k}", "n": len(s2), "slope": lr2.slope, "t": lr2.slope/lr2.stderr,
                            "ex_top20": np.nan, "ex_bot20": np.nan})
    out["past move z vs fwd excess"] = pd.DataFrame(res).round(4)
    # weekday and next-day after big moves on daily
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].astype(float).values
            r = c[1:]/c[:-1]-1
            sd = pd.Series(r).rolling(30, min_periods=15).std().shift(1).values
            ts = pd.to_datetime(df["timestamp"]).iloc[1:].dt.weekday.values
            for i in range(len(r)):
                rows.append({"coin": coin, "w": w, "r": r[i], "z": r[i]/sd[i] if sd[i] > 0 else np.nan,
                             "nxt": r[i+1] if i+1 < len(r) else np.nan, "wd": ts[i]})
    d = pd.DataFrame(rows)
    d["rex"] = d["r"] - d.groupby("coin")["r"].transform("mean")
    wd = d.groupby("wd")["rex"].agg(["mean", "std", "count"])
    wd["t"] = wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    out["weekday excess daily"] = wd.round(5)
    s = d.dropna(subset=["z", "nxt"])
    s["zb"] = pd.cut(s["z"], [-99, -2, -1, 0, 1, 2, 99])
    nb = s.groupby("zb")["nxt"].agg(["mean", "std", "count"])
    nb["t"] = nb["mean"]/(nb["std"]/np.sqrt(nb["count"]))
    out["next day by today's z"] = nb.round(5)
    # book by window
    days = data["days"]
    br = []
    for coin, ws in days.items():
        for w, df in ws.items():
            br.append({"coin": coin, "w": w, "book": df["book_return"].mean()*1e4, "coin_r": df["coin_return"].mean()*1e4})
    out["book bps/day by coin"] = pd.DataFrame(br).groupby("coin")[["book", "coin_r"]].mean().round(2)
    tr = []
    for coin, ws in data["trades"].items():
        for w, df in ws.items():
            if len(df): tr.append(df.assign(coin=coin))
    if tr:
        T = pd.concat(tr)
        out["trades"] = T.groupby(["coin", "side"])["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    return out
