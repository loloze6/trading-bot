def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin in bars:
        dr = {}
        for h in [12, 72]:
            rs = []
            for w, b in bars[coin].items():
                c = b["close"].values; idx = np.arange(0, len(c)-h, h)
                rs.append(c[idx+h]/c[idx]-1)
            dr[h] = np.concatenate(rs).mean()
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values; v = b["volume"].values
            sel = np.where((ts.dt.weekday.values == 6) & (ts.dt.hour.values == 23))[0]
            for i in sel:
                if i < 720 or i + 72 >= len(c): continue
                wk = c[i]/c[i-48]-1; mo = c[i]/c[i-720]-1
                pv = v[i-167:i-47].mean()
                vr = v[i-47:i+1].mean()/pv if pv > 0 else np.nan
                s = np.sign(wk)
                if s == 0: continue
                r = {"coin": coin, "year": ts[i].year, "side": s, "same": int(np.sign(mo) == s),
                     "heavy": int(vr > 1), "absmove": abs(wk), "vr": vr}
                for h in [12, 72]:
                    r[f"u{h}"] = (c[i+h]/c[i]-1)*s - dr[h]*s
                rows.append(r)
    C = pd.DataFrame(rows)
    def summ(g):
        d = {"n": len(g)}
        for h in [12, 72]:
            x = g[f"u{h}"].dropna(); d[f"u{h}"] = x.mean(); d[f"t{h}"] = x.mean()/(x.std()/np.sqrt(len(x)))
        return pd.Series(d)
    out = {}
    out["by_side_trend_heavy"] = C.groupby(["side","same","heavy"]).apply(summ)
    S = C[(C.side == -1) & (C.same == 1) & (C.heavy == 1)].copy()
    S["g"] = S["absmove"]*S["vr"]
    S["gq"] = pd.qcut(S["g"], 3, labels=False)
    out["short_idea_by_grade_tercile"] = S.groupby("gq").apply(summ)
    out["short_idea_by_year"] = S.groupby("year").apply(summ)
    out["short_idea_by_coin"] = S.groupby("coin").apply(summ)
    L = C[(C.side == 1) & (C.same == 1) & (C.heavy == 1)].copy()
    out["long_idea_by_year"] = L.groupby("year").apply(summ)
    D = C[(C.side == -1)].copy(); D["g"] = D["absmove"]*D["vr"]
    D["gq"] = pd.qcut(D["g"], 3, labels=False)
    out["all_down_weekends_by_grade"] = D.groupby("gq").apply(summ)
    return out
