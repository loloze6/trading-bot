def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = 72
    rows_cases = []; rows_grid = []
    for coin, wins in data["bars"].items():
        # coin drift and usual move over 72 bars (non-overlapping, all windows)
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
            r7 = c / c.shift(168) - 1
            r30 = c / c.shift(720, fill_value=np.nan) - 1 if len(c) > 720 else c * np.nan
            vol = c.pct_change().rolling(168).std() / c.pct_change().rolling(720, min_periods=200).std()
            f = {h: c.shift(-h) / c - 1 for h in (6, 24, 72, 168)}
            fc = df["forecast"].fillna(0)
            hr = pd.to_datetime(df["timestamp"]).dt.hour
            n = len(df)
            for s in range(0, n - H, H):
                # grid sample (all bars)
                rows_grid.append(dict(coin=coin, sc=sc.iloc[s], depth=depth.iloc[s],
                                      u72=f[72].iloc[s] - drift, r7=r7.iloc[s]))
                cell = fc.iloc[s:s + H]
                hit = np.where(cell.values >= 2)[0]
                if len(hit):
                    i = s + hit[0]
                    rows_cases.append(dict(coin=coin, win=w, fc=fc.iloc[i], sc=sc.iloc[i], depth=depth.iloc[i],
                                           r7=r7.iloc[i], r30=r30.iloc[i], vol=vol.iloc[i], hour=hr.iloc[i],
                                           u6=f[6].iloc[i], u24=f[24].iloc[i] - drift / 3,
                                           u72=f[72].iloc[i] - drift, u168=f[168].iloc[i] - drift * 168 / 72,
                                           tot72=f[72].iloc[i], strength=(f[72].iloc[i] - drift) / usual))
    C = pd.DataFrame(rows_cases); G = pd.DataFrame(rows_grid)
    def agg(g, col="u72"):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out["cases_overall"] = pd.DataFrame({h: agg(C, h) for h in ["u6", "u24", "u72", "u168", "tot72"]})
    out["by_forecast_q"] = C.groupby(pd.qcut(C["fc"].rank(method="first"), 4, labels=False)).apply(agg)
    out["by_sc_bin"] = C.groupby(pd.cut(C["sc"], [-50, -4, -3, -2, -1, 0, 50])).apply(agg)
    out["by_depth_bin"] = C.groupby(pd.cut(C["depth"], [-1, -0.5, -0.4, -0.3, -0.25, -0.2, 0])).apply(agg)
    out["by_r7_q"] = C.groupby(pd.qcut(C["r7"], 4)).apply(agg)
    out["by_r30_q"] = C.dropna(subset=["r30"]).groupby(pd.qcut(C["r30"].dropna(), 4)).apply(agg)
    out["by_vol_q"] = C.dropna(subset=["vol"]).groupby(pd.qcut(C["vol"].dropna(), 4)).apply(agg)
    out["by_coin"] = C.groupby("coin").apply(agg)
    out["by_window"] = C.groupby("win").apply(agg)
    G["deep"] = G["depth"] <= -0.2
    out["grid_sc_x_deep"] = G.dropna().groupby(["deep", pd.cut(G["sc"], [-50, -3, -2, -1, 0, 1, 2, 3, 50])]).apply(agg)
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["win"] = w; d["coin"] = coin; D.append(d)
    D = pd.concat(D)
    B = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().reset_index()
    B["wn"] = B["win"].str[1:].astype(int); B = B.sort_values(["wn", "day"])
    eq = (1 + B["book_return"].fillna(0)).cumprod(); dd = eq / eq.cummax() - 1
    B["dd"] = dd.values
    out["book_by_window"] = B.groupby("wn").agg(book=("book_return", "mean"), hold=("coin_return", "mean"),
                                                 mindd=("dd", "min"))
    out["book_deepest_dd"] = float(dd.min())
    # exposure
    expo = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            a = df["postRebalance_current_allocation"].fillna(0)
            expo.append(dict(inpos=(a > 0.01).mean(), meanalloc=a.mean()))
    out["exposure"] = pd.DataFrame(expo).mean()
    tr = pd.concat([t for wins in data["trades"].values() for t in wins.values()])
    out["trades"] = pd.Series(dict(n=len(tr), pl=tr["profit_loss_percent"].mean(), net=tr["net_profit_loss_percent"].mean(),
                                   dur_h=tr["duration_minutes"].mean() / 60, win=(tr["net_profit_loss_percent"] > 0).mean()))
    return out
