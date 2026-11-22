def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [6, 18, 42, 84, 126]
    drift = {}
    rows = []
    for coin, wins in bars.items():
        # normal drift per horizon
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            hi = df["high"].values; lo = df["low"].values
            rng = pd.Series((hi - lo) / c)
            m6 = rng.rolling(6).mean(); m180 = rng.rolling(180).mean()
            ratio = (m6 / m180).values
            cs = pd.Series(c)
            prior = (cs.shift(6) / cs.shift(186) - 1).values
            r6 = (cs / cs.shift(6) - 1)
            scale = r6.abs().rolling(180).mean()
            depth = (r6 / scale).values
            r6 = r6.values
            fc = df["forecast"].values
            n = len(c)
            for t in range(n):
                if np.isnan(ratio[t]) or r6[t] >= 0 or ratio[t] < 2:
                    continue
                d = dict(coin=coin, win=w, cell=t // 84, t=t, ratio=ratio[t],
                         prior=prior[t], depth=depth[t], r6=r6[t], fc=fc[t],
                         year=pd.Timestamp(df["timestamp"].iloc[t]).year)
                for h in H:
                    d[f"f{h}"] = c[t + h] / c[t] - 1 - drift[(coin, h)][0] if t + h < n else np.nan
                rows.append(d)
    ev = pd.DataFrame(rows)
    out = {}
    def summ(sub, label):
        r = {}
        s = sub.groupby(["coin", "win", "cell"]).first().reset_index()
        for h in H:
            x = s[f"f{h}"].dropna()
            r[f"mean{h}"] = x.mean(); r[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        r["n"] = len(s)
        return pd.Series(r, name=label)
    tested = ev[(ev.fc > 0)]
    tab = [summ(tested, "tested fc>0"),
           summ(ev[(ev.ratio >= 3) & (ev.prior < 0)], "3x,prior<0"),
           summ(ev[(ev.ratio >= 3) & (ev.prior >= 0)], "3x,prior>=0"),
           summ(ev[(ev.ratio >= 3)], "3x,all"),
           summ(ev[(ev.ratio >= 2) & (ev.prior < 0)], "2x,prior<0"),
           summ(ev[(ev.ratio >= 2)], "2x,all"),
           summ(ev[(ev.ratio >= 3) & (ev.depth < -2)], "3x,depth<-2"),
           summ(ev[(ev.ratio >= 2) & (ev.depth < -2)], "2x,depth<-2")]
    out["variants"] = pd.DataFrame(tab)
    s = tested.groupby(["coin", "win", "cell"]).first().reset_index()
    out["tested_by_coin"] = s.groupby("coin")["f84"].agg(["count", "mean", "median"])
    out["tested_by_year"] = s.groupby("year")["f84"].agg(["count", "mean", "median"])
    s["dq"] = pd.qcut(s["depth"], 3, labels=["deep", "mid", "shallow"])
    out["tested_by_depth"] = s.groupby("dq")[["f18", "f42", "f84", "fc"]].mean()
    s["pq"] = pd.qcut(s["prior"], 2, labels=["very neg", "mild neg"])
    out["tested_by_prior"] = s.groupby("pq")[["f42", "f84"]].agg(["count", "mean"])
    out["tested_f84_dist"] = s["f84"].describe()
    out["tested_hit"] = float((s["f84"] > 0).mean())
    return out
