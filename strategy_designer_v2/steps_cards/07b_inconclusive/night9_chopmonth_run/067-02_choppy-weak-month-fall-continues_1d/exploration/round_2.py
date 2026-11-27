def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 7
    drift = {}
    vmed = {}
    for coin, wins in bars.items():
        rs = []; vs = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rs.append(c[i + H] / c[i] - 1)
            v = pd.Series(c).pct_change().rolling(30).std()
            vs += list(v.dropna().values)
        drift[coin] = np.mean(rs) if rs else np.nan
        vmed[coin] = np.median(vs) if vs else np.nan
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            s = pd.Series(c)
            r30 = s.pct_change(30).values
            r7 = s.pct_change(7).values
            vol30 = s.pct_change().rolling(30).std().values
            raw = df.get("debug_info.components.month_fall.last_history_value")
            raw = raw.values if raw is not None else np.full(len(c), np.nan)
            for i in range(0, len(c) - H, H):
                if not (f[i] < 0):
                    continue
                fwd = c[i + H] / c[i] - 1
                rows.append(dict(coin=coin, w=w, day=ts[i].normalize(), af=abs(f[i]),
                                 r30=r30[i], raw=raw[i], r7=r7[i], vol30=vol30[i],
                                 agit=(vol30[i] > vmed[coin]) if not np.isnan(vol30[i]) else np.nan,
                                 fwd=fwd, unus=-(fwd - drift[coin])))
    d = pd.DataFrame(rows)

    def summ(g):
        n = len(g); m = g["unus"].mean()
        dd = g.groupby("day")["unus"].sum()
        tday = dd.mean() / (dd.std(ddof=1) / np.sqrt(len(dd))) * 1 if len(dd) > 2 else np.nan
        return pd.Series(dict(n=n, days=len(dd), unus=m,
                              t=m / (g["unus"].std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan,
                              t_day=tday, w_unus=(g["unus"] * g["af"]).sum() / g["af"].sum()))
    res = {}
    res["overall"] = summ(d)
    res["share_r30_neg"] = pd.Series(dict(share_r30_neg=(d["r30"] < 0).mean(),
                                          share_raw_neg=(d["raw"] < 0).mean(),
                                          r30_median=d["r30"].median(),
                                          corr_raw_r30=d[["raw", "r30"]].corr().iloc[0, 1]))
    d["r30sign"] = np.where(d["r30"] < 0, "r30<0", "r30>=0")
    res["by_r30_sign"] = d.groupby("r30sign").apply(summ)
    neg = d[d["r30"] < 0].copy()
    neg["depth"] = pd.qcut(-neg["r30"], 3, labels=["shallow", "mid", "deep"])
    res["neg_by_depth"] = neg.groupby("depth").apply(summ)
    res["neg_spearman_depth_unus"] = pd.Series(dict(rho=stats.spearmanr(-neg["r30"], neg["unus"])[0],
                                                     p=stats.spearmanr(-neg["r30"], neg["unus"])[1], n=len(neg)))
    d["agit_s"] = d["agit"].map({True: "agitated", False: "calm"})
    res["by_agitation"] = d.groupby("agit_s").apply(summ)
    res["neg_by_agitation"] = neg.assign(agit_s=neg["agit"].map({True: "agitated", False: "calm"})).groupby("agit_s").apply(summ)
    d["r7q"] = pd.qcut(d["r7"], 3, labels=["r7low", "r7mid", "r7high"])
    res["by_r7"] = d.groupby("r7q").apply(summ)
    d["vz"] = d["unus"] / d["vol30"] / np.sqrt(7)
    res["strength_by_agit"] = d.groupby("agit_s")["vz"].agg(["mean", "count"])
    return res
