def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(720, min_periods=240).std()
            vr = b["volume"] / b["volume"].rolling(720, min_periods=240).mean()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "r1": r1, "z": r1/sd, "vr": vr,
                               "sd": sd, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                               "ret24p": c/c.shift(24)-1, "alloc": b["postRebalance_current_allocation"],
                               "fc": b["forecast"]})
            for h in [1, 2, 6, 24]:
                df[f"f{h}"] = c.shift(-h)/c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = {h: D[D.pos % h == 0].groupby("coin")[f"f{h}"].mean() for h in [1, 2, 6, 24]}
    def tab(h, key, sub=None):
        S = D[D.pos % h == 0].dropna(subset=["z", "vr", f"f{h}"]).copy()
        if sub is not None: S = sub(S)
        S["u"] = S[f"f{h}"] - S["coin"].map(drift[h])
        g = S.groupby(key)["u"]
        return pd.DataFrame({"n": g.size(), "mean_bp": g.mean()*1e4,
                             "t": g.mean()/(g.std()/np.sqrt(g.size()))}).round(2)
    zb = lambda S: pd.cut(S["z"], [-99, -3, -2, -1, 1, 2, 3, 99])
    vb = lambda S: pd.cut(S["vr"], [0, 1, 2, 4, 1e9])
    for h in [2, 6, 24]:
        S = D[D.pos % h == 0].dropna(subset=["z", "vr", f"f{h}"]).copy()
        S["zb"] = zb(S); S["vb"] = vb(S)
        S["u"] = S[f"f{h}"] - S["coin"].map(drift[h])
        g = S.groupby(["zb", "vb"], observed=True)["u"]
        out[f"zxvol_h{h}"] = pd.DataFrame({"n": g.size(), "mean_bp": g.mean()*1e4,
                                           "t": g.mean()/(g.std()/np.sqrt(g.size()))}).round(2)
    # 24h past return deciles -> next 24h
    S = D[D.pos % 24 == 0].dropna(subset=["ret24p", "f24", "sd"]).copy()
    S["u"] = S["f24"] - S["coin"].map(drift[24])
    S["m"] = S["ret24p"] / (S["sd"]*np.sqrt(24))
    S["mb"] = pd.qcut(S["m"], 5, labels=False)
    g = S.groupby("mb")["u"]
    out["past24_quint_next24"] = pd.DataFrame({"n": g.size(), "mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.size()))}).round(2)
    S["vq"] = S.groupby("coin")["sd"].transform(lambda x: pd.qcut(x, 5, labels=False))
    g = S.groupby("vq")["u"]
    out["vol_quint_next24"] = pd.DataFrame({"n": g.size(), "mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.size()))}).round(2)
    # hour and weekday 1h returns
    S = D.dropna(subset=["f1"]).copy()
    g = S.groupby("hour")["f1"]
    out["hour_ret"] = pd.DataFrame({"n": g.size(), "mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.size()))}).round(2)
    S = D[D.pos % 24 == 0].dropna(subset=["f24"]).copy()
    g = S.groupby("wd")["f24"]
    out["wd_next24"] = pd.DataFrame({"n": g.size(), "mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.size()))}).round(2)
    # book: gain from market vs timing
    A = D.dropna(subset=["alloc", "f1"])
    out["book_bar"] = pd.Series({"mean_alloc": A["alloc"].mean(), "share_bars_in": (A["alloc"].abs() > 0).mean(),
                                 "gain_bp_per_bar": (A["alloc"]*A["f1"]).mean()*1e4,
                                 "market_bp_per_bar": (A["alloc"]*A["coin"].map(drift[1])).mean()*1e4}).round(4)
    # trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()], ignore_index=True)
    out["trades"] = T.groupby(["coin", "side"]).agg(n=("net_profit_loss_percent", "size"),
        mean_net=("net_profit_loss_percent", "mean"), mean_gross=("profit_loss_percent", "mean"),
        dur_h=("duration_minutes", lambda x: x.mean()/60)).round(3)
    return out
