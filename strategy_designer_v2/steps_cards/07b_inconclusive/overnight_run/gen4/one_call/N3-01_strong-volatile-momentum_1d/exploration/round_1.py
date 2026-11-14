def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            fwd = np.full(n, np.nan)
            if n > 5:
                fwd[:-5] = c[5:] / c[:-5] - 1
            r20 = df["debug_info.components.ret20.last_history_value"] if "debug_info.components.ret20.last_history_value" in df else pd.Series(np.nan, index=df.index)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n, 5):
                if np.isnan(fwd[i]):
                    continue
                rows.append(dict(coin=coin, win=int(w[1:]), year=ts.iloc[i].year, ts=ts.iloc[i],
                                 fc=df["forecast"].iloc[i], fwd=fwd[i], r20=r20.iloc[i]))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    # market move: mean fwd of all coins at same timestamp
    d["mkt"] = d.groupby("ts")["fwd"].transform("mean")
    d["nact"] = d.groupby("ts")["fc"].transform(lambda x: (x >= 10).sum())
    s = d[d.fc >= 10].copy()
    s["resid"] = s["fwd"] - s["mkt"]
    def summ(g, col="ex"):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), sd=x.std(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, hit=(x > 0).mean()))
    out = {}
    out["all_fc10"] = summ(s).to_frame().T
    out["by_coin"] = s.groupby("coin").apply(summ)
    out["by_year"] = s.groupby("year").apply(summ)
    s["wg"] = pd.cut(s.win, [0, 6, 12, 18, 24], labels=["w1-6", "w7-12", "w13-18", "w19-24"])
    out["by_wingroup"] = s.groupby("wg").apply(summ)
    s["fb"] = pd.cut(s.fc, [9.99, 12, 15, 19.99, 20.01], labels=["10-12", "12-15", "15-20", "20cap"])
    out["by_fcbucket"] = s.groupby("fb").apply(summ)
    act = d[(d.fc > 0) & (d.fc < 10)]
    out["active_below10"] = summ(act).to_frame().T
    out["inactive"] = summ(d[d.fc <= 0]).to_frame().T
    out["fc10_vs_mkt_resid"] = summ(s, "resid").to_frame().T
    s["breadth"] = pd.cut(s.nact, [0, 1, 2, 4, 6], labels=["alone", "2", "3-4", "5-6"])
    out["by_breadth"] = s.groupby("breadth").apply(summ)
    out["by_breadth_resid"] = s.groupby("breadth").apply(lambda g: summ(g, "resid"))
    s["r20b"] = pd.qcut(s.r20, 3, labels=["low", "mid", "high"]) if s.r20.notna().sum() > 30 else np.nan
    out["by_r20_tercile"] = s.groupby("r20b").apply(summ)
    out["median_ex_fc10"] = s.ex.median()
    out["top5pct_contrib"] = s.ex.sort_values(ascending=False).head(int(len(s) * 0.05)).sum() / s.ex.sum()
    return out
