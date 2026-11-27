def explore(data):
    import numpy as np, pandas as pd
    H = [1, 3, 5, 7, 10, 14]
    rows = []
    allbars = []
    drift = {}
    for coin, wins in data["bars"].items():
        # coin drift over all windows, per horizon, non-overlapping
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            sd30 = pd.Series(r).rolling(30, min_periods=15).std().values
            run = np.zeros(n, int)
            for t in range(1, n):
                k = 0
                j = t - 1
                while j >= 1 and r[j] > 0:
                    k += 1; j -= 1
                run[t] = k
            ts = pd.to_datetime(b["timestamp"])
            for t in range(1, n):
                rec = dict(coin=coin, win=w, pos=t, day=ts.iloc[t].normalize(), year=ts.iloc[t].year,
                           inprof=b["regime"].iloc[t] != "chop", down=r[t] < 0, run=run[t],
                           drop=-r[t] / sd30[t] if sd30[t] > 0 else np.nan,
                           rungain=(c[t-1] / c[t-1-run[t]] - 1) / sd30[t] if (run[t] > 0 and sd30[t] > 0) else np.nan)
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

    def table(mask, label):
        out = []
        for h in H:
            s = cases(df[mask], h)
            if len(s) < 5: continue
            m, t, k, d = ct(s[f"f{h}"], s["day"])
            out.append(dict(set=label, h=h, mean_up=m, t=t, n=k, days=d))
        return out
    sig = df.down & (df.run >= 2)
    res = {}
    res["by_horizon"] = pd.DataFrame(
        table(df.inprof & sig, "prof_dip") + table(df.inprof, "prof_all") +
        table(df.inprof & ~df.down, "prof_upday") + table(~df.inprof & sig, "outprof_dip"))
    s7 = cases(df[df.inprof & sig], 7)
    g = []
    for key in ["coin", "year"]:
        for k, s in s7.groupby(key):
            m, t, n, d = ct(s["f7"], s["day"]); g.append(dict(by=key, k=str(k), mean_up=m, t=t, n=n))
    s7 = s7.copy()
    s7["runb"] = s7["run"].clip(upper=5)
    for k, s in s7.groupby("runb"):
        m, t, n, d = ct(s["f7"], s["day"]); g.append(dict(by="run", k=str(k), mean_up=m, t=t, n=n))
    for col in ["drop", "rungain"]:
        q = pd.qcut(s7[col], 3, labels=["lo", "mid", "hi"])
        for k, s in s7.groupby(q):
            m, t, n, d = ct(s["f7"], s["day"]); g.append(dict(by=col, k=str(k), mean_up=m, t=t, n=n))
    res["groups_h7_dip"] = pd.DataFrame(g)
    # graded: correlation of f3/f7 with run and drop, in profile, all down days
    dd = df[df.inprof & df.down]
    cor = []
    for h in [3, 7]:
        s = cases(dd, h)
        for col in ["run", "drop", "rungain"]:
            x = s[[col, f"f{h}"]].dropna()
            cor.append(dict(h=h, var=col, corr=x.corr().iloc[0, 1], n=len(x)))
    res["corr_downdays_prof"] = pd.DataFrame(cor)
    res["share_inprof"] = float(df.inprof.mean())
    return res
