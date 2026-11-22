def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    W = []; H = []
    for coin in bars:
        for w, df in bars[coin].items():
            d = df[["timestamp", "close"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("ts").reset_index(drop=True)
            c = pd.Series(d["close"].values); ts = d["ts"]
            ok1 = (ts - ts.shift(1)) == pd.Timedelta(hours=1)
            r1 = pd.Series(np.where(ok1, c / c.shift(1) - 1, np.nan))
            vol = r1.rolling(720, min_periods=200).std().shift(1)
            def back(k):
                ok = (ts - ts.shift(k)) == pd.Timedelta(hours=k)
                return pd.Series(np.where(ok, c / c.shift(k) - 1, np.nan))
            def fwd(k):
                ok = (ts.shift(-k) - ts) == pd.Timedelta(hours=k)
                return pd.Series(np.where(ok, c.shift(-k) / c - 1, np.nan))
            r24 = back(24); r48 = back(48); f24 = fwd(24); f48 = fwd(48)
            sat = (1 + r48) / (1 + r24) - 1  # at Sunday 23:00 bar: Saturday's move
            sel = (ts.dt.hour == 23) & (ts.dt.weekday == 6)
            W.append(pd.DataFrame({"coin": coin, "w": w, "yr": ts.dt.year, "wk": ts.dt.isocalendar().week.values,
                                   "zsat": sat / (vol * np.sqrt(24)), "zsun": r24 / (vol * np.sqrt(24)),
                                   "ymon": f24 / (vol * np.sqrt(24)), "y48": f48 / (vol * np.sqrt(48)),
                                   "mon_pct": f24, "f48": f48, "vol": vol})[sel])
            # hour 22 bar: its own move vs the prior 22h move
            r22 = back(22).shift(1)  # move from 00:00 close... up to bar 21 close
            own = r1  # move of bar starting at ts (close[t]/close[t-1])? keep consistent with round 2
            sel2 = ts.dt.hour == 22
            H.append(pd.DataFrame({"coin": coin, "yr": ts.dt.year, "z": own / vol,
                                   "zprior": back(22).shift(1) / (vol * np.sqrt(22)), "vol": vol})[sel2])
    A = pd.concat(W).dropna(subset=["zsat", "zsun", "ymon", "y48"])
    out = {}
    def mreg(df, xs, y):
        X = np.column_stack([np.ones(len(df))] + [df[x].values for x in xs]); Y = df[y].values
        b, *_ = np.linalg.lstsq(X, Y, rcond=None); e = Y - X @ b
        s2 = e @ e / (len(Y) - X.shape[1]); se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        return {**{f"b_{x}": b[i + 1] for i, x in enumerate(xs)}, **{f"t_{x}": b[i + 1] / se[i + 1] for i, x in enumerate(xs)}, "n": len(Y)}
    Wk = A.groupby(["w", "yr", "wk"])[["zsat", "zsun", "ymon", "y48"]].mean().dropna()
    out["joint_monday"] = pd.DataFrame([dict(sample="pooled", **mreg(A, ["zsat", "zsun"], "ymon")),
                                        dict(sample="week_avg", **mreg(Wk, ["zsat", "zsun"], "ymon")),
                                        dict(sample="pooled_48h", **mreg(A, ["zsat", "zsun"], "y48")),
                                        dict(sample="week_avg_48h", **mreg(Wk, ["zsat", "zsun"], "y48"))])
    out["joint_monday_by_year_weekavg"] = pd.DataFrame([dict(yr=y, **mreg(g, ["zsat", "zsun"], "ymon")) for y, g in Wk.groupby("yr") if len(g) > 20])
    out["joint_monday_by_coin"] = pd.DataFrame([dict(coin=k, **mreg(g, ["zsat", "zsun"], "ymon")) for k, g in A.groupby("coin")])
    A["vq"] = A.groupby("coin")["vol"].transform(lambda v: pd.qcut(v.rank(method="first"), 3, labels=False))
    out["joint_monday_by_vol"] = pd.DataFrame([dict(vq=q, **mreg(g, ["zsat", "zsun"], "ymon")) for q, g in A.groupby("vq")])
    A["sign_sun"] = np.sign(A.zsun)
    out["sunday_by_sign_48h"] = pd.DataFrame([dict(sign=s, **mreg(g, ["zsun"], "y48"), mean_f48=g.f48.mean()) for s, g in A.groupby("sign_sun")])
    Hh = pd.concat(H).dropna()
    Hh["pq"] = pd.qcut(Hh.zprior, 5, labels=False); Hh["vq"] = Hh.groupby("coin")["vol"].transform(lambda v: pd.qcut(v.rank(method="first"), 3, labels=False))
    out["hour22_by_prior_quintile"] = Hh.groupby("pq").agg(zprior=("zprior", "mean"), z=("z", "mean"), n=("z", "size"))
    out["hour22_by_vol"] = Hh.groupby("vq").agg(z=("z", "mean"), n=("z", "size"))
    return out
