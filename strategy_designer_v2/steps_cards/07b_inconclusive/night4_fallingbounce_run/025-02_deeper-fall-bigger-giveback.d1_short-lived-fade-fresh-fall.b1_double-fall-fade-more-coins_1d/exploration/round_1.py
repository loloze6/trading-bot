def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        for H in [1, 2, 3, 5, 10]:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                rs += list(c[idx + H] / c[idx] - 1)
            drift[(coin, H)] = np.mean(rs) if rs else np.nan
            usual[(coin, H)] = np.std(rs) if rs else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ret = pd.Series(c).pct_change()
            vol = ret.rolling(20).std()
            z = (ret / vol).values
            r30 = pd.Series(c).pct_change(30).values
            r90 = pd.Series(c).pct_change(90).values
            r1 = ret.values
            prev = np.r_[0, f[:-1]]
            cand = (f - prev <= -2)
            n = len(c)
            for t in np.where(cand)[0]:
                rec = dict(coin=coin, w=w, t=t, cell2=t // 2, f=f[t], z=z[t], r1=r1[t],
                           r30=r30[t], r90=r90[t], year=pd.Timestamp(df["timestamp"].iloc[t]).year)
                for H in [1, 2, 3, 5, 10]:
                    if t + H < n:
                        tot = -(c[t + H] / c[t] - 1)
                        rec[f"ex{H}"] = tot + drift[(coin, H)]
                        rec[f"tot{H}"] = tot
                    else:
                        rec[f"ex{H}"] = np.nan; rec[f"tot{H}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    d = d.drop_duplicates(["coin", "w", "cell2"])
    d = d[d["ex2"].notna()]

    def summ(g, col="ex2"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    out["all"] = summ(d).to_frame().T
    hz = []
    for H in [1, 2, 3, 5, 10]:
        s = summ(d, f"ex{H}"); s["H"] = H; s["tot%"] = 100 * d[f"tot{H}"].mean(); hz.append(s)
    out["by_horizon(cases on 2d grid)"] = pd.DataFrame(hz)
    d["fq"] = pd.qcut(d["f"].abs().rank(method="first"), 5, labels=False)
    out["by_|forecast|_quintile"] = d.groupby("fq").apply(summ).join(d.groupby("fq")["f"].mean())
    d["zq"] = pd.qcut(d["z"].rank(method="first"), 5, labels=False)
    out["by_z_quintile"] = d.groupby("zq").apply(summ).join(d.groupby("zq")["z"].mean())
    out["by_year"] = d.groupby("year").apply(summ)
    out["by_coin"] = d.groupby("coin").apply(summ)
    d["r30q"] = pd.qcut(d["r30"].rank(method="first"), 4, labels=False)
    out["by_r30_quartile"] = d.groupby("r30q").apply(summ).join(d.groupby("r30q")["r30"].mean())
    d["r90q"] = pd.qcut(d["r90"].rank(method="first"), 4, labels=False)
    out["by_r90_quartile"] = d.groupby("r90q").apply(summ).join(d.groupby("r90q")["r90"].mean())
    out["share_f_at_-20"] = float((d["f"] <= -19.9).mean())
    out["corr_z_ex2"] = float(d[["z", "ex2"]].corr().iloc[0, 1])
    return out
