def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            rp = df.get("debug_info.components.range_pos.post_pipeline_value")
            r3 = df.get("debug_info.components.ret30.post_pipeline_value")
            rpl = df.get("debug_info.components.range_pos.last_history_value")
            for h in (7, 14, 28):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, year=yr[i],
                        fc=df["forecast"].iat[i], ret=c[i+h]/c[i]-1,
                        rp=np.nan if rp is None else rp.iat[i],
                        r3=np.nan if r3 is None else r3.iat[i],
                        rpl=np.nan if rpl is None else rpl.iat[i],
                        r30=c[i]/c[i-30]-1 if i >= 30 else np.nan,
                        wnum=int(w[1:])))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby(["coin", "h"])["ret"].transform("mean")
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    act = d[d.fc > 0]
    out["by_h_active"] = act.groupby("h")["ex"].apply(tt).unstack()
    out["by_h_flat"] = d[d.fc == 0].groupby("h")["ex"].apply(tt).unstack()
    a7 = act[act.h == 7].copy()
    out["coin_7"] = a7.groupby("coin")["ex"].apply(tt).unstack()
    out["year_7"] = a7.groupby("year")["ex"].apply(tt).unstack()
    a7["fq"] = pd.qcut(a7.fc.rank(method="first"), 5, labels=False)
    out["fc_quint_7"] = a7.groupby("fq").agg(fc=("fc", "mean"), n=("ex", "size"), ex=("ex", "mean"), std=("ex", "std"))
    a7["rpz"] = a7.rp > 0
    a7["r3z"] = a7.r3 > 0
    out["parts_7"] = a7.groupby(["rpz", "r3z"])["ex"].apply(tt).unstack()
    out["corr_7"] = pd.Series({"spear_fc": stats.spearmanr(a7.fc, a7.ex)[0],
                               "spear_rp": stats.spearmanr(a7.rp, a7.ex, nan_policy="omit")[0],
                               "spear_r3": stats.spearmanr(a7.r3, a7.ex, nan_policy="omit")[0],
                               "std_ex": a7.ex.std(), "std_raw_ret": a7.ret.std()})
    a28 = act[act.h == 28].copy()
    a28["fq"] = pd.qcut(a28.fc.rank(method="first"), 5, labels=False)
    out["fc_quint_28"] = a28.groupby("fq").agg(n=("ex", "size"), ex=("ex", "mean"))
    out["coin_28"] = a28.groupby("coin")["ex"].apply(tt).unstack()
    return out
