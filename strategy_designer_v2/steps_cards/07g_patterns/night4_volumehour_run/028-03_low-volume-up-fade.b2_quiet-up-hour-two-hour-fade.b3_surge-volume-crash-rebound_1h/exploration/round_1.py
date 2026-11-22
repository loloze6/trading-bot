def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std()
            vr = v / v.rolling(720, min_periods=240).mean()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "r": r, "z": r / sd, "vr": vr, "sd": sd,
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "fc": b["forecast"].astype(float)})
            for h in (1, 2, 6, 24):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["r24"] = c / c.shift(24) - 1
            df["g"] = df["alloc"] * df["f1"]
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)

    def grid(h):
        d = A[(A["pos"] % h) == 0].dropna(subset=[f"f{h}", "z", "vr"]).copy()
        drift = d.groupby("coin")[f"f{h}"].transform("mean")
        d["u"] = d[f"f{h}"] - drift
        return d

    def summ(g, col="u"):
        x = g[col]
        return pd.Series({"n": len(x), "mean_bp": x.mean() * 1e4,
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    # 1. signed move x volume bucket, 2h and 6h
    for h in (2, 6):
        d = grid(h)
        d["zb"] = pd.cut(d["z"], [-np.inf, -3, -1.5, 1.5, 3, np.inf], labels=["<-3", "-3..-1.5", "mid", "1.5..3", ">3"])
        d["vb"] = pd.cut(d["vr"], [0, 1, 2.5, np.inf], labels=["vr<1", "1-2.5", ">2.5"])
        out[f"z_x_vol_{h}h"] = d.groupby(["zb", "vb"], observed=True).apply(summ).round(2)

    # 2. 24h past return -> next 24h (per coin)
    d = grid(24).dropna(subset=["r24"])
    d["q"] = d.groupby("coin")["r24"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["past24_quint_next24"] = d.groupby(["coin", "q"]).apply(summ).round(2)

    # 3. hour of day, 1h returns
    d = grid(1)
    hh = d.groupby(["hour"]).apply(summ).round(2)
    out["hour_1h"] = hh
    # weekday 24h
    d = grid(24)
    out["weekday_24h"] = d.groupby(["wd"]).apply(summ).round(2)

    # 4. vol level -> next 6h unusual move and abs
    d = grid(6)
    d["vq"] = d.groupby("coin")["sd"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["vol_tercile_6h"] = d.groupby(["coin", "vq"]).apply(summ).round(2)

    # 5. book: gain when positioned, by forecast bucket and by year
    P = A.dropna(subset=["g"])
    act = P[P["alloc"].abs() > 1e-9].copy()
    out["active_share"] = float(len(act) / len(P))
    act["fb"] = pd.cut(act["fc"], [-1, 0.01, 2, 5, 10, 21], labels=["0", "0-2", "2-5", "5-10", "10+"])
    out["gain_by_fc_bp"] = act.groupby("fb", observed=True).apply(lambda g: pd.Series({"n": len(g), "gain_bp": g["g"].mean() * 1e4, "alloc": g["alloc"].mean(), "f1_bp": g["f1"].mean()*1e4})).round(3)
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w
            x["year"] = pd.to_datetime(x["day"]).dt.year
            dd.append(x)
    D = pd.concat(dd).dropna(subset=["book_return"])
    out["book_by_year"] = D.groupby("year").agg(n=("book_return", "size"), book_bp=("book_return", lambda x: x.mean()*1e4), coin_bp=("coin_return", lambda x: x.mean()*1e4)).round(2)
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    T["eb"] = pd.qcut(T["entry_forecast"], 4, duplicates="drop")
    out["trades_by_entry_fc"] = T.groupby("eb", observed=True).agg(n=("profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"), dur_min=("duration_minutes", "mean")).round(3)
    return out
