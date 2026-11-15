def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 20
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        # pooled mean daily return of the coin
        cr = pd.concat([data["days"][coin][w]["coin_return"] for w in wins]).dropna()
        mu = cr.mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            dist = df.get("debug_info.components.above_ma.last_history_value")
            dist = dist.values if dist is not None else np.full(n, np.nan)
            fc = df["forecast"].values
            lr = np.log(c)
            r1 = np.r_[np.nan, np.diff(lr)]
            vol20 = pd.Series(r1).rolling(20).std().values
            past20 = np.r_[np.full(20, np.nan), c[20:] / c[:-20] - 1] if n > 20 else np.full(n, np.nan)
            past5 = np.r_[np.full(5, np.nan), c[5:] / c[:-5] - 1] if n > 5 else np.full(n, np.nan)
            for i in range(0, n - H, H):
                fwd = c[i + H] / c[i] - 1
                rows.append(dict(coin=coin, w=w, dist=dist[i], fc=fc[i], fwd=fwd, ex=fwd - H * mu,
                                 vol=vol20[i], past20=past20[i], past5=past5[i]))
            # daily grid for weekday / 1-day effects
            ts = pd.to_datetime(df["timestamp"])
            for i in range(1, n - 1):
                daily.append(dict(coin=coin, wd=ts.iloc[i].weekday(), r=c[i + 1] / c[i] - 1 - mu,
                                  prev=c[i] / c[i - 1] - 1))
    R = pd.DataFrame(rows)
    D = pd.DataFrame(daily)
    out = {}
    def tab(g):
        a = g.agg(n=("ex", "size"), mean_ex=("ex", "mean"), sd=("ex", "std"),
                  hit=("ex", lambda x: (x > 0).mean()))
        a["t"] = a["mean_ex"] / (a["sd"] / np.sqrt(a["n"]))
        return a.drop(columns="sd")
    R2 = R.dropna(subset=["dist"])
    R2["dq"] = pd.qcut(R2["dist"], 8, labels=False)
    out["by_dist_octile"] = tab(R2.groupby("dq")).join(R2.groupby("dq")["dist"].median().rename("med_dist"))
    R["fcb"] = pd.cut(R["fc"], [-0.01, 0, 5, 10, 15, 20.1])
    out["by_forecast"] = tab(R.groupby("fcb"))
    R3 = R.dropna(subset=["past20"]).copy()
    R3["pq"] = pd.qcut(R3["past20"], 5, labels=False)
    out["by_past20_quint"] = tab(R3.groupby("pq"))
    R4 = R.dropna(subset=["vol"]).copy()
    R4["vq"] = pd.qcut(R4["vol"], 5, labels=False)
    out["by_vol_quint"] = tab(R4.groupby("vq"))
    R5 = R3.dropna(subset=["dist"]).copy()
    R5["above"] = R5["dist"] > 0
    out["past20q_x_above"] = tab(R5.groupby(["above", "pq"]))
    out["below_by_coin"] = tab(R2[R2["dist"] <= 0].groupby("coin"))
    out["above_by_coin"] = tab(R2[R2["dist"] > 0].groupby("coin"))
    D["ex"] = D["r"]
    out["weekday"] = tab(D.groupby("wd"))
    D["pq"] = pd.qcut(D["prev"], 10, labels=False)
    out["after_1d_move_decile"] = tab(D.groupby("pq"))
    # book days
    bd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            br = df["book_return"].values; cr2 = df["coin_return"].values
            for i in range(len(df)):
                bd.append(dict(coin=coin, br=br[i], cr=cr2[i],
                               nxt=br[i+1] if i+1 < len(df) else np.nan,
                               nxt5=np.nansum(br[i+1:i+6]) if i+5 < len(df) else np.nan))
    B = pd.DataFrame(bd).dropna(subset=["br"])
    inpos = B[B["br"] != 0]
    out["book_inpos_share"] = len(inpos) / len(B)
    inpos = inpos.copy()
    inpos["bq"] = pd.qcut(inpos["br"], 10, labels=False)
    out["book_after_decile"] = inpos.groupby("bq").agg(n=("br", "size"), mean_br=("br", "mean"),
                                                       nxt=("nxt", "mean"), nxt5=("nxt5", "mean"))
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    T["days"] = T["duration_minutes"] / 1440
    T["dq"] = pd.qcut(T["days"].rank(method="first"), 5, labels=False)
    out["trades_by_duration"] = T.groupby("dq").agg(n=("days", "size"), med_days=("days", "median"),
                                                    mean_pl=("profit_loss_percent", "mean"),
                                                    win=("profit_loss_percent", lambda x: (x > 0).mean()))
    return out
