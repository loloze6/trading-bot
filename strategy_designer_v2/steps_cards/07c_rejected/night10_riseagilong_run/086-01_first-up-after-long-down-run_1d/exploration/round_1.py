def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 2, 3, 5, 10]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            r1 = np.full(n, np.nan); r1[1:] = c[1:] / c[:-1] - 1
            inprof = (df["regime"].astype(str) != "chop").values
            # down-run count ending at t-1, up close at t
            run = np.zeros(n, int); cum = np.zeros(n)
            downrun = 0; dcum = 0.0
            prevrun = np.zeros(n, int); prevcum = np.zeros(n)
            for i in range(1, n):
                prevrun[i] = downrun; prevcum[i] = dcum
                if r1[i] < 0:
                    downrun += 1; dcum += np.log(1 + r1[i])
                else:
                    downrun = 0; dcum = 0.0
            sd30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            up = r1 > 0
            # current down run length at t (if t is down day)
            curdown = np.zeros(n, int)
            for i in range(1, n):
                curdown[i] = curdown[i-1] + 1 if r1[i] < 0 else 0
            curup = np.zeros(n, int)
            for i in range(1, n):
                curup[i] = curup[i-1] + 1 if r1[i] > 0 else 0
            r1d = pd.Series(r1)
            ret5past = np.full(n, np.nan); ret5past[5:] = c[5:] / c[:-5] - 1
            for i in range(n):
                d = dict(coin=coin, w=w, pos=i, inprof=inprof[i],
                         first_up=bool(up[i] and prevrun[i] >= 1), prun=prevrun[i],
                         depth=(-prevcum[i] / sd30[i]) if sd30[i] > 0 else np.nan,
                         upmove=(r1[i] / sd30[i]) if sd30[i] > 0 else np.nan,
                         curdown=curdown[i], curup=curup[i],
                         past5=(ret5past[i] / sd30[i]) if sd30[i] > 0 else np.nan,
                         year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                         day=str(pd.Timestamp(df["timestamp"].iloc[i]).date()))
                for h in H:
                    d[f"f{h}"] = c[i+h] / c[i] - 1 if i + h < n else np.nan
                rows.append(d)
    A = pd.DataFrame(rows)
    # drift per coin per h: grid positions 0,h,2h of each window, all bars
    drift = {}; usual = {}
    for h in H:
        g = A[(A.pos % h == 0)]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
        usual[h] = g.groupby("coin")[f"f{h}"].std()
        A[f"u{h}"] = A[f"f{h}"] - A.coin.map(drift[h])
    def cases(mask, h):
        s = A[mask & A[f"u{h}"].notna()].copy()
        s["cell"] = s.pos // h
        s = s.drop_duplicates(["coin", "w", "cell"])
        return s
    def summ(s, h):
        if len(s) < 3: return pd.Series(dict(n=len(s)))
        dd = s.groupby("day")[f"u{h}"].sum()
        nd = len(dd); m = s[f"u{h}"].mean()
        # day clustered t
        se = np.sqrt((dd - dd.mean()*0 - (s[f"u{h}"].mean()*s.groupby("day").size())).pow(2).sum()) / len(s)
        se *= np.sqrt(nd / max(nd - 1, 1))
        return pd.Series(dict(n=len(s), days=nd, mean_unusual=m, t=m / se if se > 0 else np.nan,
                              mean_total=s[f"f{h}"].mean()))
    out = {}
    P = A.inprof
    # 1. tested event, by horizon
    ev = P & A.first_up & (A.prun >= 2)
    out["event_run2plus_by_horizon"] = pd.DataFrame({h: summ(cases(ev, h), h) for h in H}).T
    ev1 = P & A.first_up & (A.prun >= 1)
    out["event_run1plus_by_horizon"] = pd.DataFrame({h: summ(cases(ev1, h), h) for h in H}).T
    # 2. by run length, h=5 and h=2
    res = {}
    for k, msk in {"1": A.prun == 1, "2": A.prun == 2, "3": A.prun == 3, "4+": A.prun >= 4}.items():
        for h in [2, 5, 10]:
            res[(k, h)] = summ(cases(P & A.first_up & msk, h), h)
    out["by_runlen_h"] = pd.DataFrame(res).T
    # 3. by depth tercile (events run>=1)
    s = A[ev1].copy()
    q = s.depth.quantile([1/3, 2/3]).values
    res = {}
    for k, msk in {"shallow": A.depth <= q[0], "mid": (A.depth > q[0]) & (A.depth <= q[1]), "deep": A.depth > q[1]}.items():
        for h in [2, 5, 10]:
            res[(k, h)] = summ(cases(ev1 & msk, h), h)
    out["by_depth_h"] = pd.DataFrame(res).T
    # 4. by coin and year at h=5
    s5 = cases(ev, 5)
    out["event_by_coin_h5"] = s5.groupby("coin")["u5"].agg(["count", "mean"])
    out["event_by_year_h5"] = s5.groupby("year")["u5"].agg(["count", "mean"])
    # 5. alternatives in profile: still inside the down run (buy the dip day), up runs, past 5d
    res = {}
    for k, msk in {"all_prof": P, "down_day_run1": P & (A.curdown == 1), "down_day_run2": P & (A.curdown == 2),
                   "down_day_run3plus": P & (A.curdown >= 3), "up_run2": P & (A.curup == 2), "up_run3plus": P & (A.curup >= 3)}.items():
        for h in [2, 5]:
            res[(k, h)] = summ(cases(msk, h), h)
    out["alternatives"] = pd.DataFrame(res).T
    # 6. past 5-day move in vol units, tercile, h=5
    q = A.loc[P, "past5"].quantile([0.2, 0.4, 0.6, 0.8]).values
    res = {}
    bins = [-np.inf] + list(q) + [np.inf]
    for j in range(5):
        msk = P & (A.past5 > bins[j]) & (A.past5 <= bins[j+1])
        for h in [2, 5]:
            res[(f"q{j+1}", h)] = summ(cases(msk, h), h)
    out["past5_quintile"] = pd.DataFrame(res).T
    # 7. size of the up day itself
    q = A.loc[ev1, "upmove"].quantile([1/3, 2/3]).values
    res = {}
    for k, msk in {"small_up": A.upmove <= q[0], "mid_up": (A.upmove > q[0]) & (A.upmove <= q[1]), "big_up": A.upmove > q[1]}.items():
        for h in [2, 5]:
            res[(k, h)] = summ(cases(ev1 & msk, h), h)
    out["by_upday_size"] = pd.DataFrame(res).T
    out["share_in_profile"] = float(P.mean())
    return out
