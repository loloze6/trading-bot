def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    reg_counts = {}
    zrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30).std()
            z = (c / c.shift(14) - 1) / (sd * np.sqrt(14))
            fwd = c.shift(-7) / c - 1
            reg = b["regime"].astype(str)
            inprof = reg.isin(["mean_reversion", "unknown"])
            for k, v in reg.value_counts().items():
                reg_counts[(coin, k)] = reg_counts.get((coin, k), 0) + v
            act = b["postRebalance_current_allocation"].fillna(0).abs() > 1e-9
            rows.append({"coin": coin, "window": w, "bars": len(b),
                         "z_valid": int(z.notna().sum()),
                         "in_profile": int(inprof.sum()),
                         "z<=-2 all": int((z <= -2).sum()),
                         "z<=-2 in profile": int(((z <= -2) & inprof).sum()),
                         "z>=2 in profile": int(((z >= 2) & inprof).sum()),
                         "mr bars": int((reg == "mean_reversion").sum()),
                         "fc<0 bars": int((b["forecast"].fillna(0) < 0).sum()),
                         "pos bars": int(act.sum())})
            df = pd.DataFrame({"z": z, "fwd": fwd, "inprof": inprof})
            # non-overlapping grid of 7
            g = df.iloc[::7].dropna()
            g["coin"] = coin
            zrows.append(g)
    t = pd.DataFrame(rows)
    out["per coin"] = t.drop(columns="window").groupby("coin").sum()
    out["per window"] = t.drop(columns="coin").groupby("window").sum()
    out["regime counts"] = pd.Series(reg_counts).unstack(fill_value=0)
    Z = pd.concat(zrows)
    drift = Z["fwd"].mean()
    out["z quantiles all grid"] = Z["z"].quantile([0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
    out["z quantiles in profile grid"] = Z.loc[Z.inprof, "z"].quantile([0.01, 0.05, 0.1, 0.5, 0.9, 0.95, 0.99])
    bins = pd.cut(Z["z"], [-10, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 10])
    def agg(s):
        x = -(s - drift)
        return pd.Series({"n": len(x), "short_unusual_mean": x.mean(),
                          "sd": x.std(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 1 else np.nan})
    out["grid by z bin, all profiles"] = Z.groupby(bins)["fwd"].apply(agg).unstack()
    Zp = Z[Z.inprof]
    out["grid by z bin, in profile"] = Zp.groupby(pd.cut(Zp["z"], [-10, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 10]))["fwd"].apply(agg).unstack()
    out["share in profile grid"] = float(Z.inprof.mean())
    out["7d sd all grid"] = float(Z["fwd"].std())
    return out
