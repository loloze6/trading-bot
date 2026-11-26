def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    out = {}
    rows = []
    H = [1, 2, 3, 5]
    for coin, ws in bars.items():
        # coin mean daily return over all windows
        allr = pd.concat([w["close"].pct_change() for w in ws.values()]).dropna()
        mu = allr.mean()
        for wn, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; h = b["high"].values; l = b["low"].values; o = b["open"].values
            rng = h - l
            cl = np.where(rng > 0, (c - l) / np.where(rng > 0, rng, 1), np.nan)
            r1 = pd.Series(c).pct_change().values
            vol20 = pd.Series(r1).rolling(20).std().values
            ret5 = pd.Series(c).pct_change(5).values
            inprof = (b["regime"] == "unknown").values
            n = len(b)
            for i in range(n):
                d = dict(coin=coin, w=wn, i=i, cl=cl[i], inprof=inprof[i],
                         rngrel=(rng[i] / c[i]) / vol20[i] if vol20[i] and vol20[i] > 0 else np.nan,
                         day_ret=r1[i], ret5=ret5[i],
                         body=(c[i] - o[i]) / c[i],
                         pos=b["postRebalance_current_allocation"].iloc[i])
                for hh in H:
                    if i + hh < n:
                        d[f"f{hh}"] = c[i + hh] / c[i] - 1 - hh * mu
                    else:
                        d[f"f{hh}"] = np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    df["grp"] = pd.cut(df["cl"], [-0.01, 1/3, 2/3, 1.01], labels=["low", "mid", "top"])

    def tab(sub, hh):
        s = sub[sub["i"] % hh == 0]
        g = s.groupby("grp", observed=True)[f"f{hh}"]
        return g.agg(["mean", "count"])
    # profile vs out of profile, by horizon
    res = []
    for prof in [True, False]:
        for hh in H:
            s = df[(df["inprof"] == prof) & (df["i"] % hh == 0)].dropna(subset=[f"f{hh}", "cl"])
            top = s[s.grp == "top"][f"f{hh}"]; mid = s[s.grp == "mid"][f"f{hh}"]; low = s[s.grp == "low"][f"f{hh}"]
            t = stats.ttest_ind(top, mid, equal_var=False).statistic
            res.append(dict(prof=prof, h=hh, top=top.mean(), mid=mid.mean(), low=low.mean(),
                            n_top=len(top), n_mid=len(mid), t_top_mid=t,
                            t_top=top.mean() / top.std() * np.sqrt(len(top))))
    out["by_horizon_profile"] = pd.DataFrame(res)

    # inside profile, top group split by day's own return sign, range size, 5d return
    p = df[df.inprof & df.grp.eq("top")].dropna(subset=["f1"])
    pm = df[df.inprof & df.grp.eq("mid")].dropna(subset=["f1"])
    res = []
    for name, col in [("day_ret", "day_ret"), ("rngrel", "rngrel"), ("ret5", "ret5")]:
        q = df[df.inprof][col].quantile([1/3, 2/3]).values
        for lab, m1, m2 in [("lo", -np.inf, q[0]), ("md", q[0], q[1]), ("hi", q[1], np.inf)]:
            for gname, g in [("top", p), ("mid", pm)]:
                x = g[(g[col] > m1) & (g[col] <= m2)]
                for hh in [1, 3]:
                    xx = x[x["i"] % hh == 0][f"f{hh}"].dropna()
                    res.append(dict(split=name, q=lab, grp=gname, h=hh, mean=xx.mean(), n=len(xx),
                                    t=xx.mean() / xx.std() * np.sqrt(len(xx)) if len(xx) > 2 else np.nan))
    out["splits_in_profile"] = pd.DataFrame(res)

    # book by window
    bw = []
    for coin, ws in days.items():
        for wn, d in ws.items():
            bw.append(dict(w=wn, coin=coin, br=d["book_return"].mean(), cr=d["coin_return"].mean(), n=d["book_return"].count()))
    bw = pd.DataFrame(bw)
    out["book_by_window"] = bw.groupby("w").agg(book=("br", "mean"), coin=("cr", "mean"), n=("n", "sum"))

    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in trades.items() for t in ws.values()], ignore_index=True)
    out["trades"] = pd.DataFrame(dict(n=[len(tr)], gross=[tr["profit_loss_percent"].mean()],
                                     net=[tr["net_profit_loss_percent"].mean()],
                                     dur_days=[tr["duration_minutes"].mean() / 1440],
                                     dur_med=[tr["duration_minutes"].median() / 1440]))
    # rebalance frequency on position bars
    pos = df[df.pos.abs() > 0]
    out["pos_bars"] = len(pos)
    out["share_inprof"] = df.inprof.mean()
    return out
