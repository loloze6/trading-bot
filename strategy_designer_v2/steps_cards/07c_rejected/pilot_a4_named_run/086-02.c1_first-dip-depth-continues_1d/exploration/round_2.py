def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    drift = {}
    for coin, ws in bars.items():
        r = {h: [] for h in [3, 5, 10]}
        for w, df in ws.items():
            c = df["close"].values
            for h in r:
                for i in range(0, len(c) - h, h):
                    r[h].append(c[i+h]/c[i]-1)
        drift[coin] = {h: np.mean(v) for h, v in r.items()}
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            ret = pd.Series(c).pct_change()
            vol30 = ret.rolling(30, min_periods=15).std()
            tr60 = pd.Series(c).pct_change(60)
            up = (ret > 0).astype(int).values
            run = np.zeros(len(c), int)
            for i in range(1, len(c)):
                run[i] = run[i-1] + 1 if up[i] else 0
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(1, len(c)):
                if ret.iloc[i] < 0 and run[i-1] >= 2:
                    rec = dict(coin=coin, w=w, year=yr[i], run=run[i-1], regime=df["regime"].iloc[i],
                               z=ret.iloc[i]/vol30.iloc[i] if vol30.iloc[i] > 0 else np.nan,
                               runz=(c[i-1]/c[i-1-run[i-1]]-1)/vol30.iloc[i] if vol30.iloc[i] > 0 else np.nan,
                               tr60=tr60.iloc[i], cell10=i//10)
                    for h in [3, 5, 10]:
                        rec[f"u{h}"] = -(c[i+h]/c[i]-1) + drift[coin][h] if i+h < len(c) else np.nan
                    rec["leg3_10"] = -(c[i+10]/c[i+3]-1) if i+10 < len(c) else np.nan
                    rows.append(rec)
    d = pd.DataFrame(rows)
    p = d[d.regime == "mean_reversion"].copy()
    o = d[(d.regime == "chop") & (d.tr60 > 0.10)].copy()  # rising but calm (approx)
    def summ(g):
        out = {"n": len(g)}
        for k in ["u3", "u5", "u10", "leg3_10"]:
            x = g[k].dropna()
            out[f"m_{k}"] = x.mean()
            out[f"t_{k}"] = x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(out)
    res = {}
    res["profile_all"] = summ(p).to_frame().T
    res["rising_calm_approx"] = summ(o).to_frame().T
    # non-overlap 10-day: first case per coin/window/cell10
    pn = p.drop_duplicates(["coin", "w", "cell10"])
    res["profile_nonoverlap10"] = summ(pn).to_frame().T
    res["profile_coin_year"] = p.groupby(["coin", "year"]).apply(summ)
    p["runzq"] = pd.qcut(p["runz"], 3, labels=["smallrun", "midrun", "bigrun"])
    res["profile_by_runz"] = p.groupby("runzq").apply(summ)
    p["zq"] = pd.qcut(p["z"], 3, labels=["deep", "mid", "shallow"])
    res["profile_by_depth"] = p.groupby("zq").apply(summ)
    res["corr"] = pd.Series({"z_u10": p[["z", "u10"]].corr().iloc[0, 1],
                             "runz_u10": p[["runz", "u10"]].corr().iloc[0, 1],
                             "runz_u3": p[["runz", "u3"]].corr().iloc[0, 1],
                             "z_leg": p[["z", "leg3_10"]].corr().iloc[0, 1]})
    return res
