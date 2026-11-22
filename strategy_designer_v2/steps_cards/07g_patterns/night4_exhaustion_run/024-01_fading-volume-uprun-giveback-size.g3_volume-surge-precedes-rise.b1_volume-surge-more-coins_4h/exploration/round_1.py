def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        parts = []
        for w, df in wins.items():
            d = df.copy()
            d = d.reset_index(drop=True)
            c = d["close"]; v = d["volume"]
            d["win"] = w
            d["vr"] = d["debug_info.components.vol_surge.last_history_value"]
            d["r1"] = c.pct_change()
            d["p6"] = c / c.shift(6) - 1
            d["p18"] = c / c.shift(18) - 1
            d["p36"] = c / c.shift(36) - 1
            d["f18"] = c.shift(-18) / c - 1
            d["f6"] = c.shift(-6) / c - 1
            s = np.sign(d["r1"]).fillna(0)
            grp = (s != s.shift()).cumsum()
            d["run"] = s.groupby(grp).cumcount().add(1) * s
            vm = v.shift(1).rolling(180, min_periods=60).mean()
            d["v3"] = v.rolling(3).mean() / vm
            d["v3prev"] = v.shift(3).rolling(3).mean() / vm
            d["vtrend"] = np.log(d["v3"] / d["v3prev"])
            d["rv"] = d["r1"].rolling(42).std()
            d["rvrel"] = d["rv"] / d["r1"].rolling(180).std()
            ts = pd.to_datetime(d["timestamp"])
            d["hour"] = ts.dt.hour; d["wd"] = ts.dt.weekday; d["year"] = ts.dt.year
            d["pos"] = np.arange(len(d))
            d["alloc"] = d["postRebalance_current_allocation"]
            parts.append(d)
        a = pd.concat(parts)
        g = a[a["pos"] % 18 == 0].dropna(subset=["f18"])
        mu, sd = g["f18"].mean(), g["f18"].std()
        a["coin"] = coin
        a["z"] = (a["f18"] - mu) / sd
        a["ex"] = a["f18"] - mu
        a["p18z"] = a["p18"] / sd
        a["p36z"] = a["p36"] / (sd * np.sqrt(2))
        a["r1z"] = a["r1"] / a["r1"].std()
        rows.append(a)
    A = pd.concat(rows)
    G = A[A["pos"] % 18 == 0].dropna(subset=["z"])

    def tab(df, key):
        t = df.groupby(key)["z"].agg(["mean", "std", "count"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["ex_pct"] = df.groupby(key)["ex"].mean() * 100
        return t.drop(columns="std").round(3)

    out = {}
    G = G.copy()
    G["vr_q"] = pd.qcut(G["vr"], 5, labels=False, duplicates="drop")
    G["r1sign"] = np.sign(G["r1z"]).clip(-1, 1)
    G["r1_q"] = pd.qcut(G["r1z"], 5, labels=False)
    out["vr quintile x bar sign"] = tab(G, ["vr_q", "r1sign"])
    out["bar return quintile (z)"] = tab(G, "r1_q")
    G["p18_q"] = pd.qcut(G["p18z"], 7, labels=False)
    out["past 3d return septile"] = tab(G, "p18_q")
    G["p36_q"] = pd.qcut(G["p36z"], 5, labels=False)
    G["vt_s"] = np.where(G["vtrend"] < 0, "fade", "rise")
    out["past 6d quintile x vol trend"] = tab(G.dropna(subset=["vtrend", "p36_q"]), ["p36_q", "vt_s"])
    G["run_b"] = G["run"].clip(-5, 5)
    out["run length signed"] = tab(G, "run_b")
    G["rv_q"] = pd.qcut(G["rvrel"], 4, labels=False)
    out["rel vol quartile"] = tab(G, "rv_q")
    out["past3d septile x relvol half"] = tab(G.assign(rvh=(G["rv_q"] >= 2).astype(int)), ["p18_q", "rvh"])
    out["hour"] = tab(G, "hour")
    out["weekday"] = tab(G, "wd")
    out["year"] = tab(G, "year")
    return out
