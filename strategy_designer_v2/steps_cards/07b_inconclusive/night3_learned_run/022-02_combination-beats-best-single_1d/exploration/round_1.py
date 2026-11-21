def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    C = "debug_info.components.combined.post_pipeline_value"
    B = "debug_info.components.best.post_pipeline_value"
    rows = []
    for coin, ws in bars.items():
        grid = []
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            n = len(df)
            r28 = pd.Series(cl).pct_change(28).values
            r1 = pd.Series(cl).pct_change(1).values
            vol = pd.Series(cl).pct_change().rolling(30).std().values
            for i in range(0, n - 5, 5):
                grid.append(dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                 ret=cl[i+5]/cl[i]-1, c=df[C].iloc[i] if C in df else np.nan,
                                 b=df[B].iloc[i] if B in df else np.nan,
                                 r28=r28[i], r1=r1[i], vol=vol[i]))
        g = pd.DataFrame(grid)
        g["y"] = g["ret"] - g["ret"].mean()
        rows.append(g)
    d = pd.concat(rows).dropna(subset=["c", "b"])
    d["m"] = d["y"] * (d["c"] - d["b"]) / 10
    def summ(x):
        return pd.Series(dict(n=len(x), mean_m=x["m"].mean(),
                              t_m=x["m"].mean()/(x["m"].std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                              corr_c=x["y"].corr(x["c"]), corr_b=x["y"].corr(x["b"]),
                              corr_cb=x["c"].corr(x["b"])))
    out = {}
    out["all"] = summ(d).to_frame().T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["side"] = np.sign(d["c"])
    out["by_side_c"] = d.groupby("side").apply(lambda x: pd.Series(dict(n=len(x), mean_y=x["y"].mean(),
                         t=x["y"].mean()/(x["y"].std()/np.sqrt(len(x))))))
    d["cq"] = pd.qcut(d["c"], 5, labels=False)
    out["by_c_quint"] = d.groupby("cq").agg(n=("y","size"), c=("c","mean"), mean_y=("y","mean"))
    d["bq"] = pd.qcut(d["b"], 5, labels=False)
    out["by_b_quint"] = d.groupby("bq").agg(n=("y","size"), b=("b","mean"), mean_y=("y","mean"))
    sig = d.dropna(subset=["r28","r1","vol"])
    out["single_corr"] = pd.Series({k: sig["y"].corr(sig[k]) for k in ["r28","r1","vol","c","b"]}).to_frame("corr")
    out["single_corr_n"] = len(sig)
    out["single_by_year"] = sig.groupby("year").apply(lambda x: pd.Series({k: x["y"].corr(x[k]) for k in ["r28","r1","vol","c","b"]}))
    return out
