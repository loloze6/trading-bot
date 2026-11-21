def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = 72
    rows = []
    for coin, wins in data["bars"].items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rets += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(rets); usual = np.std(rets)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r24 = c / c.shift(24) - 1
            mad = r24.abs().rolling(720, min_periods=200).mean()
            sc = r24 / mad
            depth = c / c.rolling(720, min_periods=200).max() - 1
            vol = c.pct_change().rolling(168).std() / c.pct_change().rolling(720, min_periods=200).std()
            r30 = c / c.shift(720) - 1
            f = {h: c.shift(-h) / c - 1 for h in (24, 72, 168)}
            fc = df["forecast"].fillna(0)
            for s in range(0, len(df) - H, H):
                hit = np.where(fc.iloc[s:s + H].values >= 2)[0]
                if len(hit):
                    i = s + hit[0]
                    rows.append(dict(coin=coin, sc=sc.iloc[i], depth=depth.iloc[i], vol=vol.iloc[i], r30=r30.iloc[i],
                                     u24=f[24].iloc[i] - drift / 3, u72=f[72].iloc[i] - drift,
                                     u168=f[168].iloc[i] - drift * 168 / 72, s72=(f[72].iloc[i] - drift) / usual))
    C = pd.DataFrame(rows)
    def agg(g):
        o = {}
        for col in ["u24", "u72", "u168", "s72"]:
            x = g[col].dropna()
            o[col] = x.mean(); 
            if col in ("u72",):
                o["t72"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        o["n"] = len(g)
        return pd.Series(o)
    C["strong"] = C["sc"] <= -2
    C["hivol"] = C["vol"] > C["vol"].median()
    out["sc_horizons"] = C.groupby(pd.cut(C["sc"], [-50, -3, -2, -1, 0])).apply(agg)
    out["strong_x_vol"] = C.dropna(subset=["vol"]).groupby(["strong", "hivol"]).apply(agg)
    out["vol_q_horizons"] = C.dropna(subset=["vol"]).groupby(pd.qcut(C["vol"].dropna(), 4)).apply(agg)
    out["sc_vs_vol_corr"] = float(C[["sc", "vol"]].corr().iloc[0, 1])
    # trades
    tr = pd.concat([t for wins in data["trades"].values() for t in wins.values()])
    tr["dur_h"] = tr["duration_minutes"] / 60
    out["trades_by_dur"] = tr.groupby(pd.cut(tr["dur_h"], [0, 24, 72, 100, 168, 336, 10000])).agg(
        n=("net_profit_loss_percent", "size"), pl=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    out["trades_by_entry_fc"] = tr.groupby(pd.qcut(tr["entry_forecast"].rank(method="first"), 4, labels=False)).agg(
        n=("net_profit_loss_percent", "size"), fcmed=("entry_forecast", "median"),
        net=("net_profit_loss_percent", "mean"), dur=("dur_h", "mean"))
    # book falls: daily book exposure vs coin returns
    D = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df[["timestamp", "postRebalance_current_allocation", "close"]].copy()
            d["day"] = pd.to_datetime(d["timestamp"]).dt.floor("D")
            g = d.groupby("day").agg(alloc=("postRebalance_current_allocation", "mean"), close=("close", "last")).reset_index()
            g["cr"] = g["close"].pct_change(); g["win"] = w; g["coin"] = coin
            D.append(g)
    D = pd.concat(D)
    DD = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d[["day", "book_return"]].copy(); x["win"] = w; x["coin"] = coin; DD.append(x)
    DD = pd.concat(DD)
    DD["day"] = pd.to_datetime(DD["day"]).dt.floor("D")
    D["day"] = pd.to_datetime(D["day"]).dt.tz_localize(None) if D["day"].dt.tz is not None else D["day"]
    DD["day"] = DD["day"].dt.tz_localize(None) if DD["day"].dt.tz is not None else DD["day"]
    M = D.merge(DD, on=["coin", "win", "day"], how="inner")
    B = M.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("cr", "mean"), alloc=("alloc", "mean")).reset_index()
    B["wn"] = B["win"].str[1:].astype(int); B = B.sort_values(["wn", "day"]).reset_index(drop=True)
    eq = (1 + B["br"].fillna(0)).cumprod(); B["dd"] = eq / eq.cummax() - 1
    B["indd"] = B["dd"] < -0.3
    out["book_in_deep_fall"] = B.groupby("indd").agg(days=("br", "size"), br=("br", "mean"), cr=("cr", "mean"), alloc=("alloc", "mean"))
    B["coin30"] = B.groupby("wn")["cr"].transform(lambda s: (1 + s.fillna(0)).rolling(30).apply(np.prod, raw=True) - 1)
    out["book_by_coin30_q"] = B.dropna(subset=["coin30"]).groupby(pd.qcut(B["coin30"].dropna(), 5)).agg(
        days=("br", "size"), br=("br", "mean"), cr=("cr", "mean"), alloc=("alloc", "mean"))
    return out
