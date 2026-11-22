def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    def feats(df):
        c = df["close"].astype(float); h=df["high"].astype(float); l=df["low"].astype(float)
        rng = (h-l)/c
        r6 = c/c.shift(6)-1
        mabs6 = r6.abs().rolling(180, min_periods=60).mean()
        f = pd.DataFrame({
            "r6z": r6/mabs6,
            "rr": rng.rolling(6).mean()/rng.rolling(180, min_periods=60).mean(),
            "prior30": c.shift(6)/c.shift(186)-1,
            "r84p": c/c.shift(84)-1,
            "vol": np.log(c).diff().rolling(180, min_periods=60).std(),
        })
        return c, f
    H = {"h6":6, "h42":42, "h84":84}
    grid = {k: [] for k in H}
    events = []
    hourly = []
    for coin, wins in bars.items():
        g84 = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            idx = np.arange(0, len(c)-84, 84)
            g84 += list(c.values[idx+84]/c.values[idx]-1)
        drift84 = np.nanmean(g84)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c, f = feats(df)
            n = len(c)
            for k, h in H.items():
                idx = np.arange(0, n-h, h)
                fwd = c.values[idx+h]/c.values[idx]-1
                d = f.iloc[idx].copy(); d["fwd"]=fwd; d["coin"]=coin; d["w"]=w
                grid[k].append(d)
            # events: panic any trend, first per 84 cell
            cond = (f["rr"]>=3)&(f["r6z"]<0)
            for s in range(0, n-84, 84):
                sub = np.where(cond.values[s:s+84])[0]
                if len(sub):
                    t = s+sub[0]
                    if t+84 < n:
                        events.append({"coin":coin,"w":w,"fwd":c[t+84]/c[t]-1-drift84,
                          "r6z":f["r6z"][t],"rr":f["rr"][t],"prior30":f["prior30"][t],
                          "fwd6":c[t+6]/c[t]-1 if t+6<n else np.nan,
                          "fwd18":c[t+18]/c[t]-1 if t+18<n else np.nan})
            ts = pd.to_datetime(df["timestamp"])
            r1 = c.shift(-1)/c-1
            hourly.append(pd.DataFrame({"hour":ts.dt.hour,"wd":ts.dt.weekday,"r":r1,"coin":coin}))
    def tab(d, col, q=5, fcol="fwd"):
        d = d.dropna(subset=[col, fcol]).copy()
        d["dm"] = d[fcol]-d.groupby("coin")[fcol].transform("mean")
        d["b"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        g = d.groupby("b")["dm"].agg(["mean","std","count"])
        g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
        g["xmed"] = d.groupby("b")[col].median()
        return g[["xmed","mean","t","count"]].round(4)
    for k in H:
        G = pd.concat(grid[k])
        for col in ["r6z","rr","r84p","vol"]:
            out[f"{k} by {col}"] = tab(G, col)
    E = pd.DataFrame(events)
    out["panic all n"] = len(E)
    E["neg"] = E["prior30"]<0
    g = E.groupby("neg")["fwd"].agg(["mean","std","count"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["panic by prior30 neg (fwd84-drift)"]=g.round(4)
    out["panic by r6z tercile"] = tab(E.assign(fwd2=E["fwd"]), "r6z", 3, "fwd2")
    out["panic fwd6/fwd18 mean,t"] = pd.DataFrame({c_:[E[c_].mean(), E[c_].mean()/(E[c_].std()/np.sqrt(E[c_].count())), E[c_].count()] for c_ in ["fwd6","fwd18"]}, index=["mean","t","n"]).round(4)
    Hh = pd.concat(hourly).dropna()
    Hh["dm"]=Hh["r"]-Hh.groupby("coin")["r"].transform("mean")
    for col in ["hour","wd"]:
        g = Hh.groupby(col)["dm"].agg(["mean","std","count"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        out[f"1bar by {col}"] = g.round(5)
    return out
