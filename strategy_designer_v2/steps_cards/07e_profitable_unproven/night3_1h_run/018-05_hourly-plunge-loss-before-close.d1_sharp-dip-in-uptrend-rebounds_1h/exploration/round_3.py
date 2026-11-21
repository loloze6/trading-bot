def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; coins = list(bars.keys())
    def tt(x):
        x = pd.Series(x).dropna(); return pd.Series({"mean": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 1 else np.nan, "n": len(x)})
    gains = []; ev = []; grid = []
    for c in coins:
        rs = []; d72 = []
        for w, b in bars[c].items():
            cl = b["close"].values
            rs.append(cl[1:] / cl[:-1] - 1)
            idx = np.arange(0, len(cl) - 72, 72); d72.append(cl[idx + 72] / cl[idx] - 1)
        mu = np.concatenate(rs).mean(); drift = np.concatenate(d72).mean()
        for w, b in bars[c].items():
            cl = b["close"].values; n = len(cl); s = pd.Series(cl)
            pos = b["postRebalance_current_allocation"].fillna(0).values
            r24 = s.pct_change(24); ma = r24.abs().rolling(720).mean(); r30 = s.pct_change(720)
            dipz = (r24 / ma).values; r30v = r30.values
            hr = pd.to_datetime(b["timestamp"]).dt.hour.values
            r1 = np.r_[cl[1:] / cl[:-1] - 1, np.nan]
            state = np.where(np.isnan(r30v), "na", np.where(r30v > 0, "up", "down"))
            dipstate = np.where(np.isnan(dipz), "na", np.where(dipz <= -1, "dip", "nodip"))
            gains.append(pd.DataFrame({"g": pos * r1, "tim": pos * (r1 - mu), "st": state, "ds": dipstate, "pos": pos}))
            cond = (r30v > 0) & (dipz <= -1)
            prev = np.r_[False, cond[:-1]]
            onset = np.where(cond & ~prev)[0]
            seen = set()
            for i in onset:
                g = i // 72
                if g in seen: continue
                seen.add(g)
                j = i + int((23 - hr[i]) % 24)
                if j + 72 >= n: continue
                ev.append({"coin": c, "dipz": dipz[i], "u_onset": cl[i + 72] / cl[i] - 1 - drift,
                           "u_close": cl[j + 72] / cl[j] - 1 - drift, "to_close": cl[j] / cl[i] - 1, "lag": j - i})
            for i in np.arange(0, n - 72, 72):
                if np.isnan(r30v[i]) or np.isnan(dipz[i]): continue
                grid.append({"coin": c, "r30": r30v[i], "dipz": dipz[i], "u72": cl[i + 72] / cl[i] - 1 - drift})
    Gn = pd.concat(gains).dropna(subset=["g"])
    tot = Gn.g.sum()
    out["gain_by_trend_state"] = Gn.groupby("st").agg(share_gain=("g", lambda x: x.sum() / tot), timing_sum=("tim", "sum"), mean_pos=("pos", "mean"), bars=("g", "size"))
    out["gain_by_trend_dip"] = Gn.groupby(["st", "ds"]).agg(share_gain=("g", lambda x: x.sum() / tot), mean_pos=("pos", "mean"), bars=("g", "size"))
    E = pd.DataFrame(ev)
    out["onset_vs_dailyclose"] = pd.DataFrame({"u_onset": tt(E.u_onset), "u_close": tt(E.u_close), "onset_minus_close": tt(E.u_onset - E.u_close), "to_close": tt(E.to_close), "lag_h": tt(E.lag)})
    out["onset_by_coin"] = E.groupby("coin")[["u_onset", "u_close"]].mean()
    G = pd.DataFrame(grid)
    up = G[G.r30 > 0].copy()
    up["b"] = pd.cut(up.dipz, [-np.inf, -2.5, -1.5, -1, -0.5, 0, np.inf])
    out["up_dip_fine"] = up.groupby("b")["u72"].apply(tt).unstack()
    G["r30q"] = pd.qcut(G.r30.rank(method="first"), 5, labels=False)
    out["all_by_r30_quint"] = G.groupby("r30q")["u72"].apply(tt).unstack()
    d = up[up.dipz <= -1]
    out["updip_coin_t"] = d.groupby("coin")["u72"].apply(tt).unstack()
    return out
