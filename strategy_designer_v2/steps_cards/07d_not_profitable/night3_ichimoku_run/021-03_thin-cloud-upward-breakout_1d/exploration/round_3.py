def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    T = []
    P = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            b = data["bars"][c][w].reset_index(drop=True)
            if t is None or len(t) == 0: continue
            ts = pd.to_datetime(b["timestamp"]); cl = b["close"]
            a = b["postRebalance_current_allocation"].fillna(0).values
            g = (cl.shift(-1) / cl - 1).values
            for _, r in t.iterrows():
                i = ts.searchsorted(pd.to_datetime(r["entry_time"]))
                j = min(ts.searchsorted(pd.to_datetime(r["exit_time"])), len(b) - 1)
                if i >= len(b): continue
                def pr(k): return cl.iloc[i] / cl.iloc[i - k] - 1 if i - k >= 0 else np.nan
                seg = cl.iloc[max(0, i - 40):i + 1]
                dd40 = seg.iloc[-1] / seg.max() - 1 if len(seg) > 5 else np.nan
                pathmin = cl.iloc[i:j + 1].min() / cl.iloc[i] - 1
                T.append({"net": r["net_profit_loss_percent"], "r40": pr(40), "r60": pr(60), "dd40": dd40, "pathmin": pathmin,
                          "f52": cl.iloc[i + 52] / cl.iloc[i] - 1 if i + 52 < len(b) else np.nan,
                          "f26": cl.iloc[i + 26] / cl.iloc[i] - 1 if i + 26 < len(b) else np.nan,
                          "dur": r["duration_minutes"] / 1440, "endwin": j >= len(b) - 2})
                for k in range(i, min(j, len(b) - 1)):
                    P.append({"age": k - i, "pg": a[k] * g[k]})
    T = pd.DataFrame(T)
    res = {}
    for f in ["r40", "r60", "dd40"]:
        s = T.dropna(subset=[f])
        q = pd.qcut(s[f].rank(method="first"), 3, labels=["lo", "mid", "hi"])
        m = s.groupby(q)["net"].mean()
        res[f] = {"lo": m["lo"], "mid": m["mid"], "hi": m["hi"], "n": len(s), "rho": stats.spearmanr(s[f], s.net)[0],
                  "f26_lo": s.f26[q == "lo"].mean(), "f26_hi": s.f26[q == "hi"].mean()}
    out["net_by_prior"] = pd.DataFrame(res).T.round(4)
    out["share_closed_by_window_end"] = pd.Series({"endwin": T.endwin.mean(), "dur<5_share": (T.dur < 5).mean(),
        "net_dur<5": T.net[T.dur < 5].mean(), "pathmin_mean": T.pathmin.mean(), "pathmin_q10": T.pathmin.quantile(0.1)})
    out["f26_vs_f52"] = T[["f26", "f52"]].agg(["mean", "median", "count"]).round(4)
    P = pd.DataFrame(P)
    P["ab"] = pd.cut(P.age, [-1, 5, 12, 25, 40, 200])
    out["pos_gain_by_age"] = P.groupby("ab")["pg"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))]).round(5)
    return out
