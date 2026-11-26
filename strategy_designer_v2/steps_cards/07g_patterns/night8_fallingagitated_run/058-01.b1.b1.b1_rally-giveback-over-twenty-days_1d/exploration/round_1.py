def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = [5, 10, 20]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            r1 = pd.Series(c).pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r3 = pd.Series(c).pct_change(3)
            sc = r3 / sd30
            r60 = pd.Series(c).pct_change(min(60, 60))
            inprof = (b["regime"] == "unknown").values
            n = len(b)
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, ts=b["timestamp"].iloc[i],
                                     fwd=c[i + h] / c[i] - 1, sc=sc.iloc[i], prof=inprof[i],
                                     fc=b["forecast"].iloc[i], sd=sd30.iloc[i],
                                     wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday()))
    df = pd.DataFrame(rows)
    drift = df.groupby(["coin", "h"])["fwd"].mean().rename("drift")
    df = df.join(drift, on=["coin", "h"])
    df["ex"] = df["fwd"] - df["drift"]
    df["exz"] = df["ex"] / (df["sd"] * np.sqrt(df["h"]))
    out = {}
    def tab(g):
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(),
                              t=g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                              mean_fwd=g["fwd"].mean()))
    d = df.dropna(subset=["sc"]).copy()
    d["scq"] = pd.cut(d["sc"], [-99, -2, -1, 0, 1, 2, 99])
    out["prof_by_scaled3d_bin"] = d[d.prof].groupby(["h", "scq"]).apply(tab)
    out["outprof_by_scaled3d_bin"] = d[~d.prof].groupby(["h", "scq"]).apply(tab)
    out["prof_vs_out_all"] = d.groupby(["h", "prof"]).apply(tab)
    out["prof_by_window_h20"] = d[(d.prof) & (d.h == 20)].groupby("w").apply(tab)
    # book daily
    dd = []
    for coin, ws in days.items():
        for w, x in ws.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w
            dd.append(x)
    D = pd.concat(dd)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    bk = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index()
    out["book_by_window"] = bk.groupby("w").agg(n=("br", "size"), book_mean=("br", "mean"), coin_mean=("cr", "mean"), book_sum=("br", "sum"))
    # trades
    tr = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; tr.append(t)
    T = pd.concat(tr) if tr else pd.DataFrame()
    if len(T):
        T["dur_d"] = T["duration_minutes"] / 1440
        T["fq"] = pd.qcut(T["entry_forecast"].abs(), 3, duplicates="drop")
        out["trades_by_forecast_tercile"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median"), dur=("dur_d", "mean"))
        out["trades_by_side"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"))
        out["trades_by_window"] = T.groupby("w").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"))
    return out
