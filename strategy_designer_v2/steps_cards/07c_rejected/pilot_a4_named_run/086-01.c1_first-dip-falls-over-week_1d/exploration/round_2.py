def explore(data):
    import numpy as np, pandas as pd
    H = [3, 5, 7, 10, 14]
    allbars = []
    drift = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            sd30 = pd.Series(r).rolling(30, min_periods=15).std().values
            run = np.zeros(n, int)
            for t in range(1, n):
                k = 0; j = t - 1
                while j >= 1 and r[j] > 0:
                    k += 1; j -= 1
                run[t] = k
            ts = pd.to_datetime(b["timestamp"])
            for t in range(1, n):
                rec = dict(coin=coin, win=w, pos=t, day=ts.iloc[t].normalize(), year=ts.iloc[t].year,
                           inprof=b["regime"].iloc[t] != "chop", down=r[t] < 0, run=run[t],
                           drop=-r[t] / sd30[t] if sd30[t] > 0 else np.nan)
                for h in H:
                    rec[f"f{h}"] = c[t+h] / c[t] - 1 - drift[(coin, h)] if t + h < n else np.nan
                    rec[f"cell{h}"] = t // h
                allbars.append(rec)
    df = pd.DataFrame(allbars)

    def ct(x, d):
        x = np.asarray(x, float); m = x.mean(); e = x - m
        S = pd.Series(e).groupby(np.asarray(d)).sum().values
        se = np.sqrt((S**2).sum()) / len(x)
        return m, (m / se if se > 0 else np.nan), len(x), len(set(d))

    def cases(sub, h):
        s = sub.dropna(subset=[f"f{h}"])
        return s.sort_values("pos").groupby(["coin", "win", f"cell{h}"]).head(1)

    def slope(s, col, h):
        x = s[[col, f"f{h}"]].dropna()
        if len(x) < 10: return np.nan, np.nan, len(x)
        X = x[col].values; Y = x[f"f{h}"].values
        b, a = np.polyfit(X, Y, 1)
        res = Y - (a + b * X)
        se = np.sqrt((res**2).sum() / (len(X) - 2) / ((X - X.mean())**2).sum())
        return b, b / se, len(X)

    res = {}
    out = []
    for lab, m in [("prof_dip_run2+", df.inprof & df.down & (df.run >= 2)),
                   ("prof_dip_run1+", df.inprof & df.down & (df.run >= 1)),
                   ("prof_down_norun", df.inprof & df.down & (df.run == 0)),
                   ("prof_down_all", df.inprof & df.down),
                   ("out_down_all", ~df.inprof & df.down)]:
        for h in H:
            s = cases(df[m], h)
            mm, t, k, d = ct(s[f"f{h}"], s["day"])
            b, bt, nb = slope(s, "drop", h)
            out.append(dict(set=lab, h=h, mean_up=mm, t=t, n=k, days=d, slope_drop=b, t_slope=bt))
    res["sets"] = pd.DataFrame(out)
    g = []
    for lab, m in [("prof_dip_run1+", df.inprof & df.down & (df.run >= 1)),
                   ("prof_down_all", df.inprof & df.down)]:
        for h in [7, 14]:
            s = cases(df[m], h).dropna(subset=["drop"])
            q = pd.qcut(s["drop"], 3, labels=["lo", "mid", "hi"])
            for k, ss in s.groupby(q):
                mm, t, n, d = ct(ss[f"f{h}"], ss["day"])
                g.append(dict(set=lab, h=h, tercile=str(k), mean_drop=ss["drop"].mean(), mean_up=mm, t=t, n=n))
            for key in ["coin", "year"]:
                for k, ss in s.groupby(key):
                    if len(ss) < 5: continue
                    mm, t, n, d = ct(ss[f"f{h}"], ss["day"])
                    g.append(dict(set=lab, h=h, tercile=f"{key}:{k}", mean_drop=ss["drop"].mean(), mean_up=mm, t=t, n=n))
    res["groups"] = pd.DataFrame(g)
    return res
