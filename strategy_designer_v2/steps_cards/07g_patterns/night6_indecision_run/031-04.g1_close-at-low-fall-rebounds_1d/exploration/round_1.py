def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); o=b["open"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20, min_periods=20).std()
            z = r / sd
            rng = (h - l) / c.shift(1)
            rngz = rng / sd
            cl = (h - c) / (h - l).replace(0, np.nan)
            r5 = c / c.shift(5) - 1
            r5z = r5 / (sd*np.sqrt(5))
            df = pd.DataFrame({"coin": coin, "w": w, "ts": b["timestamp"], "pos": np.arange(len(b)),
                               "z": z, "cl": cl, "rngz": rngz, "r5z": r5z, "sd": sd,
                               "f1": c.shift(-1)/c-1, "f3": c.shift(-3)/c-1, "f5": c.shift(-5)/c-1,
                               "alloc": b["postRebalance_current_allocation"], "fc": b["forecast"]})
            df["wd"] = pd.to_datetime(b["timestamp"]).dt.dayofweek
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = {hh: D.groupby("coin")[f"f{hh}"].apply(lambda s: s[D.loc[s.index,"pos"] % hh == 0].mean()) for hh in (1,3,5)}
    for hh in (1,3,5):
        D[f"e{hh}"] = D[f"f{hh}"] - D["coin"].map(drift[hh])
    def stat(sub, col):
        sub = sub.dropna(subset=[col])
        n = len(sub)
        if n < 5: return pd.Series({"n": n, "mean%": np.nan, "t_day": np.nan, "days": 0})
        m = sub[col].mean()
        g = (sub[col]-m).groupby(sub["ts"]).sum()
        se = np.sqrt((g**2).sum())/n
        return pd.Series({"n": n, "mean%": 100*m, "t_day": m/se if se>0 else np.nan, "days": sub["ts"].nunique()})
    out = {}
    D["zb"] = pd.cut(D["z"], [-99,-3,-2,-1,-0.3,0.3,1,2,3,99])
    for hh in (1,3,5):
        g = D[D["pos"] % hh == 0]
        out[f"next{hh}d excess by day z"] = g.groupby("zb", observed=True).apply(lambda s: stat(s, f"e{hh}"))
    # up sharp days by close location
    up = D[D["z"] >= 2].copy()
    up["clb"] = pd.cut(up["cl"], [-0.01,0.2,0.5,0.8,1.01])
    out["sharp up: next1 excess by (high-close)/range"] = up.groupby("clb", observed=True).apply(lambda s: stat(s,"e1"))
    dn = D[D["z"] <= -2].copy()
    dn["clb"] = pd.cut(dn["cl"], [-0.01,0.5,0.8,0.95,1.01])
    out["sharp down: next1 excess by cl"] = dn.groupby("clb", observed=True).apply(lambda s: stat(s,"e1"))
    out["sharp down: next3 excess by cl (grid3)"] = dn[dn.pos%3==0].groupby("clb", observed=True).apply(lambda s: stat(s,"e3"))
    # wide-flat days after runs (brief)
    D["absz"] = D["z"].abs()
    flat = D[(D["absz"] < 0.5)].copy()
    flat["dir"] = np.sign(flat["r5z"])
    flat["rb"] = pd.qcut(flat["rngz"], 4)
    flat["rev3"] = -flat["dir"] * flat["e3"]
    flat["rev1"] = -flat["dir"] * flat["e1"]
    fr = flat[flat["r5z"].abs() > 1]
    out["flat day after run: reversal next1 by range quartile"] = fr.groupby("rb", observed=True).apply(lambda s: stat(s,"rev1"))
    out["flat day after run: reversal next3 by range quartile (grid3)"] = fr[fr.pos%3==0].groupby("rb", observed=True).apply(lambda s: stat(s,"rev3"))
    # weekday and vol level
    out["next1 excess by weekday (of signal day)"] = D.groupby("wd").apply(lambda s: stat(s,"e1"))
    D["sdq"] = D.groupby("coin")["sd"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["next1 excess by vol quartile"] = D.groupby("sdq").apply(lambda s: stat(s,"e1"))
    # sharp down days by vol quartile
    out["sharp down next1 by vol quartile"] = dn.assign(sdq=D.loc[dn.index,"sdq"]).groupby("sdq").apply(lambda s: stat(s,"e1"))
    # sharp down by prior 5-day run
    dn["r5b"] = pd.cut(dn["r5z"], [-99,-2,-1,0,99])
    out["sharp down next1 by prior 5d z"] = dn.groupby("r5b", observed=True).apply(lambda s: stat(s,"e1"))
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    out["trades"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
