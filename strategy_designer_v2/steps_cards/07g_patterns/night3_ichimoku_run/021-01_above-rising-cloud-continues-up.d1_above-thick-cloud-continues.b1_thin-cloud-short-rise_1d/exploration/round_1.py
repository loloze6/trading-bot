def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            ten = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            kij = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            sa = ((ten + kij) / 2).shift(26)
            sb = ((hi.rolling(52).max() + lo.rolling(52).min()) / 2).shift(26)
            top = np.maximum(sa, sb); bot = np.minimum(sa, sb)
            mid = (sa + sb) / 2
            dist = (c - top) / c * 100
            width = (sa - sb).abs() / c * 100
            slope = mid.pct_change(26) * 100
            r1 = c.pct_change()
            ret20 = c / c.shift(20) - 1
            ret5p = c / c.shift(5) - 1
            vol20 = r1.rolling(20).std()
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fwd=fwd.iloc[i], fc=b["forecast"].iloc[i],
                    dist=dist.iloc[i], width=width.iloc[i], slope=slope.iloc[i],
                    ret20=ret20.iloc[i], ret5p=ret5p.iloc[i], vol20=vol20.iloc[i],
                    wd=ts.iloc[i].weekday(), year=ts.iloc[i].year,
                    bir=b["debug_info.bars_in_regime"].iloc[i] if "debug_info.bars_in_regime" in b else np.nan,
                    below=float(c.iloc[i] < bot.iloc[i]) if not np.isnan(bot.iloc[i]) else np.nan))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    out = {}
    def tab(col, q=5, sub=None):
        x = d if sub is None else sub
        x = x.dropna(subset=[col, "ex"])
        g = pd.qcut(x[col].rank(method="first"), q, labels=False)
        r = x.groupby(g)["ex"].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["lo"] = x.groupby(g)[col].min(); r["hi"] = x.groupby(g)[col].max()
        return r.round(4)
    act = d[d["fc"] > 0]; ina = d[d["fc"] <= 0]
    out["active_vs_inactive"] = pd.DataFrame({"active": [act.ex.mean(), len(act)], "inactive": [ina.ex.mean(), len(ina)]}, index=["mean_ex", "n"])
    out["fc_quint_active"] = tab("fc", 5, act)
    out["dist_above_top_all"] = tab("dist", 8)
    out["slope_all"] = tab("slope", 6)
    out["ret20_all"] = tab("ret20", 6)
    out["ret5p_all"] = tab("ret5p", 6)
    out["vol20_all"] = tab("vol20", 5)
    out["bars_in_regime_active"] = tab("bir", 4, act)
    out["width_inactive_below"] = tab("width", 5, d[d["below"] == 1])
    out["width_all"] = tab("width", 5)
    out["weekday"] = d.groupby("wd")["ex"].agg(["mean", "count"]).round(4)
    out["year_active"] = act.groupby("year")["ex"].agg(["mean", "count"]).round(4)
    out["coin_active"] = act.groupby("coin")["ex"].agg(["mean", "count"]).round(4)
    # book
    dd = []
    for coin, ws in data["days"].items():
        for w, x in ws.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    D = pd.concat(dd)
    out["book_by_window_mean"] = D.groupby("w")[["book_return", "coin_return"]].mean().round(5)
    return out
