def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]
    top = {"w11", "w17", "w21"}
    def grid(h):
        recs = []
        for c in bars:
            allr = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                allr.append(cl[idx + h] / cl[idx] - 1)
            m = np.concatenate(allr).mean()
            for w, b in bars[c].items():
                cl = b["close"].values; f = b["forecast"].values
                cols = b.columns
                nh = b["debug_info.components.near_high.last_history_value"].values if "debug_info.components.near_high.last_history_value" in cols else np.full(len(cl), np.nan)
                rs = b["debug_info.components.rise.last_history_value"].values if "debug_info.components.rise.last_history_value" in cols else np.full(len(cl), np.nan)
                idx = np.arange(0, len(cl) - h, h)
                for i in idx:
                    recs.append((c, w, f[i], nh[i], rs[i], cl[i + h] / cl[i] - 1 - m))
        return pd.DataFrame(recs, columns=["coin", "window", "f", "nh", "rise", "y"]).dropna(subset=["f", "y"])
    def st(x, y):
        ok = ~np.isnan(x) & ~np.isnan(y)
        if ok.sum() < 5: return np.nan
        lr = stats.linregress(x[ok], y[ok]); return lr.slope / lr.stderr
    rows = []; rows_c = []; rows_q = []; rows_comp = []
    for h in [5, 10, 20]:
        G = grid(h)
        r = {"h": h, "all": st(G.f.values, G.y.values)}
        H = G[~G.window.isin(top)]
        r["ex_top3_windows"] = st(H.f.values, H.y.values); r["n_ex"] = len(H)
        for c, g in G.groupby("coin"):
            rows_c.append({"h": h, "coin": c, "t": st(g.f.values, g.y.values), "n": len(g), "n_on": int((g.f > 0).sum())})
        on = G[G.f > 0].copy()
        on["q"] = pd.qcut(on.f.rank(method="first"), 3, labels=["low", "mid", "high"])
        q = on.groupby("q", observed=True)["y"].agg(["mean", "count"])
        q["off_mean"] = G[G.f <= 0].y.mean()
        q["h"] = h
        rows_q.append(q.reset_index())
        rows_comp.append({"h": h, "t_near_high_raw": st(on.nh.values, on.y.values), "t_rise_raw": st(on.rise.values, on.y.values), "n_on": len(on)})
        # by year split halves
        rows.append(r)
    out["robust"] = pd.DataFrame(rows)
    out["by_coin"] = pd.DataFrame(rows_c)
    out["terciles_on"] = pd.concat(rows_q, ignore_index=True)
    out["components_within_on"] = pd.DataFrame(rows_comp)
    # book by window ex top3
    days = data["days"]
    D = pd.concat([d.assign(coin=c, window=w) for c in days for w, d in days[c].items()], ignore_index=True).dropna(subset=["book_return"])
    daily = D.groupby(["window", "day"])["book_return"].mean().reset_index()
    ex = daily[~daily.window.isin(top)]["book_return"]
    out["book_ex_top3"] = pd.Series({"mean": ex.mean(), "sharpe": ex.mean() / ex.std() * np.sqrt(365), "n": len(ex)})
    return out
