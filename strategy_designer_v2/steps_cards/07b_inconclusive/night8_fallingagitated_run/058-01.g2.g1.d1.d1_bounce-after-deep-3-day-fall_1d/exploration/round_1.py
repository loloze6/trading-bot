def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    coin_mean = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            allr.append((c.shift(-1)/c - 1).dropna())
        coin_mean[coin] = pd.concat(allr).mean()
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c/c.shift(1)-1
            sd30 = r1.rolling(30).std()
            prior3 = (c.shift(1)/c.shift(4)-1)/sd30.shift(1)
            f = df["forecast"].astype(float)
            ts = pd.to_datetime(df["timestamp"])
            for i in np.where(f < 0)[0]:
                rec = {"coin": coin, "win": w, "year": ts[i].year, "day": ts[i].normalize(),
                       "fc": f[i], "up": r1[i]/sd30[i] if sd30[i] > 0 else np.nan, "prior3": prior3[i]}
                for h in (1, 2, 3, 5):
                    if i+h < len(c):
                        rec["f%d" % h] = -(c[i+h]/c[i]-1 - h*coin_mean[coin])
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    def tday(s, days):
        g = pd.DataFrame({"v": s, "d": days}).dropna().groupby("d")["v"].sum()
        return pd.Series({"mean_case": s.mean(), "t_day": g.mean()/(g.std(ddof=1)/np.sqrt(len(g))), "n": s.notna().sum(), "days": len(g)})
    out["by_horizon"] = pd.DataFrame({h: tday(d[h], d["day"]) for h in ["f1","f2","f3","f5"]}).T
    out["by_coin"] = pd.DataFrame({k: tday(g["f1"], g["day"]) for k, g in d.groupby("coin")}).T
    out["by_year"] = pd.DataFrame({k: tday(g["f1"], g["day"]) for k, g in d.groupby("year")}).T
    out["by_window"] = pd.DataFrame({k: tday(g["f1"], g["day"]) for k, g in d.groupby("win")}).T
    d["fq"] = pd.qcut(d["fc"].abs().rank(method="first"), 4, labels=["q1_shallow","q2","q3","q4_deep"])
    out["by_fc_quartile"] = pd.DataFrame({k: tday(g["f1"], g["day"]) for k, g in d.groupby("fq")}).T
    d["pq"] = pd.qcut((-d["prior3"]).rank(method="first"), 4, labels=["q1","q2","q3","q4_deep"])
    out["by_prior3_raw_quartile"] = pd.DataFrame({k: tday(g["f1"], g["day"]) for k, g in d.groupby("pq")}).T
    d["uq"] = pd.qcut(d["up"].rank(method="first"), 4, labels=["u1_small","u2","u3","u4_big"])
    out["by_upday_size_quartile"] = pd.DataFrame({k: tday(g["f1"], g["day"]) for k, g in d.groupby("uq")}).T
    out["corr_spearman"] = pd.Series({"fcabs_f1": d["fc"].abs().corr(d["f1"], method="spearman"),
                                      "prior3_f1": (-d["prior3"]).corr(d["f1"], method="spearman"),
                                      "up_f1": d["up"].corr(d["f1"], method="spearman"),
                                      "fcabs_f3": d["fc"].abs().corr(d["f3"], method="spearman")})
    return out
