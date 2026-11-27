import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                              "r": r, "nxt": c.shift(-1)/c-1, "nxt2": c.shift(-2)/c-1,
                              "nxt3": c.shift(-3)/c-1})
            d["trend"] = (c/c.shift(60)-1)*100
            usual = r.abs().rolling(30).mean().shift(1)
            d["vol30"] = r.rolling(30).std()
            d["volrel"] = d["vol30"]/d["vol30"].rolling(60, min_periods=30).median()
            # down run length and loss ending yesterday
            run = np.zeros(len(d)); loss = np.zeros(len(d))
            uprun = np.zeros(len(d)); upgain = np.zeros(len(d))
            for i in range(1, len(d)):
                if r.iloc[i] < 0:
                    run[i] = run[i-1]+1; loss[i] = loss[i-1]+abs(r.iloc[i])
                if r.iloc[i] > 0:
                    uprun[i] = uprun[i-1]+1; upgain[i] = upgain[i-1]+r.iloc[i]
            d["prevrun"] = pd.Series(run).shift(1).values
            d["prevloss"] = pd.Series(loss).shift(1).values/usual.values
            d["prevuprun"] = pd.Series(uprun).shift(1).values
            d["prevupgain"] = pd.Series(upgain).shift(1).values/usual.values
            d["rz"] = r/usual
            d["upbreak"] = (r > 0) & (d["prevrun"] > 0)
            d["dnbreak"] = (r < 0) & (d["prevuprun"] > 0)
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            d["wd"] = d["ts"].dt.weekday
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r"].mean()
    D["mu"] = D["coin"].map(mu)
    D["prof"] = np.where(D["trend"] < -10, "falling", np.where(D["trend"] > 10, "rising", np.where(D["trend"].notna(), "choppy", "na")))
    D["day"] = D["ts"].dt.floor("D")

    def stat(g, col="nxt", sign=1.0, h=1):
        x = sign*(g[col]-h*g["mu"])
        g2 = pd.DataFrame({"x": x, "day": g["day"]}).dropna()
        if len(g2) < 5: return pd.Series({"n": len(g2), "mean%": np.nan, "t": np.nan})
        m = g2["x"].mean(); dev = (g2["x"]-m).groupby(g2["day"]).sum()
        se = np.sqrt((dev**2).sum())/len(g2)
        return pd.Series({"n": len(g2), "days": g2["day"].nunique(), "mean%": 100*m, "t": m/se if se > 0 else np.nan})

    out = {}
    ub = D[D["upbreak"] & (D["prof"] != "na")].copy()
    ub["runlen"] = ub["prevrun"].clip(upper=5)
    out["upbreak next1 short by prof"] = ub.groupby("prof").apply(lambda g: stat(g, sign=-1))
    out["upbreak next1 short by prof x runlen"] = ub.groupby(["prof", "runlen"]).apply(lambda g: stat(g, sign=-1))
    ubf = ub[ub["prof"] == "falling"].copy()
    ubf["lossq"] = pd.qcut(ubf["prevloss"], 3, labels=["lo", "mid", "hi"])
    ubf["upq"] = pd.qcut(ubf["rz"], 3, labels=["smallup", "mid", "bigup"])
    out["falling upbreak by loss x upday size"] = ubf.groupby(["lossq", "upq"]).apply(lambda g: stat(g, sign=-1))
    out["falling upbreak horizons"] = pd.DataFrame({h: stat(ubf, col=f"nxt{'' if h==1 else h}", sign=-1, h=h) for h in [1, 2, 3]})
    # mirror: down break after up runs, next day long, by prof
    db = D[D["dnbreak"] & (D["prof"] != "na")].copy()
    db["runlen"] = db["prevuprun"].clip(upper=5)
    out["dnbreak next1 LONG by prof x runlen"] = db.groupby(["prof", "runlen"]).apply(lambda g: stat(g, sign=1))
    # large moves by prof, next day long
    A = D[D["prof"] != "na"].copy()
    A["rzq"] = pd.qcut(A["rz"], 5, labels=["q1", "q2", "q3", "q4", "q5"])
    out["next1 long by prof x today rz quintile"] = A.groupby(["prof", "rzq"]).apply(lambda g: stat(g))
    A["agit"] = np.where(A["volrel"] > 1, "agit", "calm")
    out["next1 long by prof x agit x rz extremes"] = A[A["rzq"].isin(["q1", "q5"])].groupby(["prof", "agit", "rzq"]).apply(lambda g: stat(g))
    out["weekday next1 long by prof"] = A.groupby(["prof", "wd"]).apply(lambda g: stat(g))["mean%"].unstack()
    # book: position days gain by window
    P = D[D["alloc"].abs() > 0].copy()
    P["g"] = P["alloc"]*P["nxt"]
    out["book pos gain by window"] = P.groupby("win")["g"].agg(["count", "mean", "sum"])
    return out
