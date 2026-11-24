import numpy as np, pandas as pd

def ct(v, d):
    v = np.asarray(v, float); m = ~np.isnan(v); v = v[m]; d = np.asarray(d)[m]
    n = len(v)
    if n < 5: return (np.nan, np.nan, n, 0)
    mu = v.mean()
    s = pd.Series(v - mu).groupby(d).sum()
    se = np.sqrt((s**2).sum()) / n
    return (mu, mu/se if se > 0 else np.nan, n, len(s))

def explore(data):
    rows = []; daily = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "close": c, "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "r20": c/c.shift(20)-1, "r60": c/c.shift(60)-1, "r5": c/c.shift(5)-1,
                "r1": r1, "vol20": r1.rolling(20).std(),
                "f10": c.shift(-10)/c-1, "f1": c.shift(-1)/c-1})
            df["pos"] = np.arange(len(df))
            daily.append(df)
            rows.append(df[(df["pos"] % 10 == 0) & df["f10"].notna()])
    D = pd.concat(daily, ignore_index=True)
    G = pd.concat(rows, ignore_index=True)
    st = G.groupby("coin")["f10"].agg(["mean", "std"])
    G = G.join(st, on="coin")
    G["ex"] = G["f10"] - G["mean"]
    G["exz"] = G["ex"] / G["std"]
    G["year"] = G["day"].dt.year
    vmed = D.groupby("coin")["vol20"].median()
    G["vrel"] = G["vol20"] / G["coin"].map(vmed)
    sd60 = D.groupby("coin")["r60"].std(); sd20 = D.groupby("coin")["r20"].std(); sd5 = D.groupby("coin")["r5"].std()
    G["z60"] = G["r60"] / G["coin"].map(sd60)
    G["z20"] = G["r20"] / G["coin"].map(sd20)
    G["z5"] = G["r5"] / G["coin"].map(sd5)
    out = {}

    def tab(key, q=5):
        g = G.dropna(subset=[key, "ex"]).copy()
        g["b"] = pd.qcut(g[key], q, labels=False, duplicates="drop")
        res = []
        for k, s in g.groupby("b"):
            mu, t, n, nd = ct(s["ex"], s["day"])
            res.append({"bin": k, "mid": s[key].median(), "mean_ex10": mu, "t": t, "n": n, "days": nd,
                        "mean_strength": s["exz"].mean()})
        return pd.DataFrame(res)
    out["by forecast quintile"] = tab("fc")
    out["by z20 quintile"] = tab("z20")
    out["by z60 quintile (brief horizon)"] = tab("z60")
    out["by z5 quintile"] = tab("z5")
    out["by vol rel quintile (unsigned ex)"] = tab("vrel")
    # directional ex by vol tercile and year
    G["dirx"] = G["ex"] * np.sign(G["fc"])
    g = G.dropna(subset=["vrel", "dirx"]).copy()
    g["vt"] = pd.qcut(g["vrel"], 3, labels=["low", "mid", "high"])
    out["dir ex by vol tercile"] = pd.DataFrame([dict(zip(["mean", "t", "n", "days"], ct(s["dirx"], s["day"])), vt=k) for k, s in g.groupby("vt")])
    out["dir ex by year"] = pd.DataFrame([dict(zip(["mean", "t", "n", "days"], ct(s["dirx"], s["day"])), year=k) for k, s in G.groupby("year")])
    out["dir ex by side"] = pd.DataFrame([dict(zip(["mean", "t", "n", "days"], ct(s["dirx"], s["day"])), side=k) for k, s in G[G.fc != 0].groupby(np.sign(G.fc[G.fc != 0]))])
    # z20 sign x z60 sign (fresh vs old trend)
    g = G.dropna(subset=["z20", "z60", "ex"]).copy()
    g["s20"] = np.sign(g["z20"]); g["s60"] = np.sign(g["z60"])
    out["ex by sign20 x sign60"] = pd.DataFrame([dict(zip(["mean", "t", "n", "days"], ct(s["ex"], s["day"])), s20=a, s60=b2) for (a, b2), s in g.groupby(["s20", "s60"])])
    # daily: after big daily moves
    D["z1"] = D["r1"] / D["vol20"].shift(1)
    D["zb"] = pd.cut(D["z1"], [-np.inf, -3, -2, -1, 1, 2, 3, np.inf])
    out["next-day ret by today's z1"] = pd.DataFrame([dict(zip(["mean", "t", "n", "days"], ct(s["f1"], s["day"])), zb=str(k)) for k, s in D.dropna(subset=["z1", "f1"]).groupby("zb")])
    D["wd"] = D["day"].dt.weekday
    out["next-day ret by weekday of decision"] = pd.DataFrame([dict(zip(["mean", "t", "n", "days"], ct(s["f1"], s["day"])), wd=k) for k, s in D.dropna(subset=["f1"]).groupby("wd")])
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)], ignore_index=True)
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median", "std"])
    T["efb"] = pd.qcut(T["entry_forecast"].abs(), 4, labels=False, duplicates="drop")
    out["trades by |entry fc| quartile"] = T.groupby("efb")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    # position gain by side
    D["gain"] = D["alloc"] * D["f1"]
    out["gain by alloc side"] = D.dropna(subset=["gain"]).groupby(np.sign(D["alloc"]))["gain"].agg(["count", "mean", "sum"])
    return out
