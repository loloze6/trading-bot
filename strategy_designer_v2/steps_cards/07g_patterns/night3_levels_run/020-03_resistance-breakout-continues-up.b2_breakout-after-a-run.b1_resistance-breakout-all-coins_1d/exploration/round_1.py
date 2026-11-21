def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [5, 10, 20]
    # coin drift & usual move per horizon
    drift = {}; usual = {}
    for c, ws in bars.items():
        for h in H + [1]:
            r = []
            for w, b in ws.items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                r.extend(cl[idx + h] / cl[idx] - 1)
            r = np.array(r)
            drift[(c, h)] = r.mean() if len(r) else np.nan
            usual[(c, h)] = r.std() if len(r) > 1 else np.nan
    # grid rows for all bars, horizon 5
    rows = []
    cases = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(cl)
            lr = np.log(cl)
            ret1 = pd.Series(cl).pct_change()
            vol20 = ret1.rolling(20).std().values
            r20 = pd.Series(cl).pct_change(20).values
            r5 = pd.Series(cl).pct_change(5).values
            hi90 = pd.Series(cl).rolling(90, min_periods=30).max().shift(1).values
            ts = pd.to_datetime(b["timestamp"])
            wd = ts.dt.weekday.values
            yr = ts.dt.year.values
            for i in range(0, n - 5, 5):
                rows.append(dict(coin=c, win=w, yr=yr[i], wd=wd[i],
                                 u5=(cl[i+5]/cl[i]-1-drift[(c,5)])/usual[(c,5)],
                                 r20=r20[i], r5=r5[i], vol=vol20[i],
                                 nh=(cl[i]/hi90[i]-1) if not np.isnan(hi90[i]) else np.nan))
            f = b["forecast"].fillna(0).values
            df_ = np.diff(np.r_[0, f])
            sig = (df_ >= 2) & (f > 0)
            m = b.get("debug_info.components.break_touches.last_history_value")
            m = m.values if m is not None else np.full(n, np.nan)
            seen = set()
            for i in np.where(sig)[0]:
                cell = i // 5
                if cell in seen or i + 5 >= n: continue
                seen.add(cell)
                d = dict(coin=c, win=w, yr=yr[i], wd=wd[i], f=f[i], brk=m[i],
                         r20=r20[i], vol=vol20[i], r5=r5[i])
                for h in H:
                    if i + h < n:
                        d[f"u{h}"] = (cl[i+h]/cl[i]-1-drift[(c,h)])
                        d[f"s{h}"] = d[f"u{h}"]/usual[(c,h)]
                # move on signal bar itself
                d["u0"] = cl[i]/cl[i-1]-1 - drift[(c,1)] if i > 0 else np.nan
                cases.append(d)
    G = pd.DataFrame(rows); C = pd.DataFrame(cases)
    def summ(df, col, by):
        g = df.dropna(subset=[col, by]).groupby(by)[col]
        return pd.DataFrame({"n": g.size(), "mean": g.mean(), "t": g.mean()/(g.std()/np.sqrt(g.size()))})
    # per-coin ranks for quintiles
    for col in ["r20", "r5", "vol", "nh"]:
        G[col+"_q"] = G.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out = {}
    out["all_r20q"] = summ(G, "u5", "r20_q")
    out["all_r5q"] = summ(G, "u5", "r5_q")
    out["all_volq"] = summ(G, "u5", "vol_q")
    out["all_nearhigh_q"] = summ(G, "u5", "nh_q")
    out["all_weekday"] = summ(G, "u5", "wd")
    out["all_year"] = summ(G, "u5", "yr")
    # cases
    hz = {}
    for h in H + [0]:
        s = C[f"u{h}"].dropna()
        hz[h] = dict(n=len(s), mean=s.mean(), t=s.mean()/(s.std()/np.sqrt(len(s))),
                     strength=C[f"s{h}"].mean() if h else np.nan)
    out["cases_by_horizon"] = pd.DataFrame(hz).T
    for col in ["r20", "vol", "brk", "f", "r5"]:
        C[col+"_q"] = pd.qcut(C[col].rank(method="first"), 4, labels=False)
        out[f"cases_{col}_q_u5"] = summ(C, "u5", col+"_q")
    out["cases_vol_q_u20"] = summ(C, "u20", "vol_q")
    out["cases_year_u5"] = summ(C, "u5", "yr")
    out["cases_coin_u5"] = summ(C, "u5", "coin")
    return out
