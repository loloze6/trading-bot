def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [5, 10, 20]
    rows = []
    # drift per coin per horizon on grid
    drift = {}
    usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            f = df["forecast"].values
            raw = df.get("debug_info.components.support_cluster.last_history_value")
            sma = pd.Series(cl).rolling(50, min_periods=20).mean().values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r20 = pd.Series(cl).pct_change(20).values
            for h in H:
                for i in range(0, len(cl) - h, h):
                    if f[i] <= -2:
                        mv = -(cl[i + h] / cl[i] - 1 - drift[(c, h)])
                        rows.append(dict(coin=c, win=w, h=h, year=yr[i], f=f[i],
                                         raw=(raw.values[i] if raw is not None else np.nan),
                                         dsma=cl[i] / sma[i] - 1 if not np.isnan(sma[i]) else np.nan,
                                         r20=r20[i], mv=mv, tot=-(cl[i + h] / cl[i] - 1),
                                         st=mv / usual[(c, h)]))
    d = pd.DataFrame(rows)
    def summ(g):
        return pd.Series(dict(n=len(g), mean=g.mv.mean(), t=g.mv.mean() / (g.mv.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                              tot=g.tot.mean(), strength=g.st.mean()))
    out = {}
    out["by_h"] = d.groupby("h").apply(summ)
    d10 = d[d.h == 10].copy()
    out["f_dist"] = d10.f.describe()
    out["f_rounded_counts"] = d10.f.round(0).value_counts().sort_index().head(25)
    out["by_coin"] = d10.groupby("coin").apply(summ)
    out["by_year"] = d10.groupby("year").apply(summ)
    d10["fq"] = pd.qcut(d10.f.rank(method="first"), 4, labels=False)
    out["by_fq"] = d10.groupby("fq").apply(summ)
    d10["dq"] = pd.qcut(d10.dsma, 4, labels=False)
    out["by_dsma_q"] = d10.groupby("dq").apply(summ)
    out["dsma_q_edges"] = d10.groupby("dq").dsma.agg(["min", "max"])
    d10["rq"] = pd.qcut(d10.r20, 4, labels=False)
    out["by_r20_q"] = d10.groupby("rq").apply(summ)
    out["rq_edges"] = d10.groupby("rq").r20.agg(["min", "max"])
    d10["rawq"] = pd.qcut(d10.raw.rank(method="first"), 4, labels=False)
    out["by_raw_q"] = d10.groupby("rawq").apply(summ)
    out["by_h_coin_t"] = d.groupby(["h", "coin"]).apply(summ)["t"].unstack()
    return out
