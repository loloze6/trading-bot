def explore(data):
    import numpy as np, pandas as pd
    out = {}
    wins = [f"w{i}" for i in range(1, 25)]
    coins = list(data["bars"].keys())
    def tt(x):
        x = pd.Series(x).dropna()
        return x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 and x.std() > 0 else np.nan
    def rq(x, k):
        return pd.qcut(x.rank(method="first"), k, labels=False)
    # book chain
    try:
        rows = []
        for w in wins:
            frames = []
            for c in coins:
                d = data["days"][c].get(w)
                if d is None: continue
                frames.append(d.set_index("day")["book_return"].rename(c))
            if not frames: continue
            m = pd.concat(frames, axis=1).mean(axis=1).dropna()
            for i, v in enumerate(m.values):
                rows.append((w, i, v))
        bk = pd.DataFrame(rows, columns=["w", "i", "r"])
        val = (1 + bk.r).cumprod()
        dd = val / val.cummax() - 1
        bk["dd"] = dd.values
        trough = int(dd.idxmin()); peak = int(val[:trough + 1].idxmax())
        out["deepest_fall"] = pd.Series({"dd": dd.min(), "peak_win": bk.w[peak], "trough_win": bk.w[trough],
                                         "days": trough - peak})
        # second and third falls (separate episodes)
        ep = []
        dd2 = dd.copy()
        under = dd2 < 0
        grp = (under != under.shift()).cumsum()
        for k, gq in dd2[under].groupby(grp[under]):
            ep.append((gq.min(), bk.w[gq.idxmin()], len(gq)))
        ep = sorted(ep)[:5]
        out["worst_fall_episodes"] = pd.DataFrame(ep, columns=["dd", "trough_win", "days_under"])
        wb = bk.groupby("w").apply(lambda g: pd.Series({"ret": (1 + g.r).prod() - 1,
               "mindd": ((1 + g.r).cumprod() / (1 + g.r).cumprod().cummax() - 1).min(), "days": len(g)}))
        out["by_window"] = wb.reindex(wins)
        fw = bk.w[peak:trough + 1].unique().tolist()
    except Exception as e:
        out["book_err"] = str(e); fw = []
    cs = []; ns = []; grid = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b.close.values.astype(float); vo = b.volume.values.astype(float)
            n = len(b)
            ts = pd.to_datetime(b.timestamp)
            lr = np.diff(np.log(cl))
            fc = b.forecast.fillna(0).values
            sig = (fc != 0) & (b.regime.values == "trending")
            wd = ts.dt.weekday.values; hr = ts.dt.hour.values
            for t in range(n):
                sun = (wd[t] == 6 and hr[t] == 23)
                if not (sig[t] or sun): continue
                if t + 48 >= n or t < 720: continue
                wk = cl[t] / cl[t - 48] - 1
                s = np.sign(fc[t]) if sig[t] else np.sign(wk)
                if s == 0: continue
                vol = np.std(lr[t - 720:t]) * np.sqrt(48)
                p30 = cl[t - 48] / cl[t - 720] - 1
                vr = vo[t - 47:t + 1].mean() / max(vo[t - 167:t - 47].mean(), 1e-12)
                r48 = cl[t + 48] / cl[t] - 1
                path = cl[t:t + 49] / cl[t] - 1
                rec = dict(coin=c, w=w, year=ts[t].year, s=s, f=abs(fc[t]), vr=vr,
                           d48=s * r48, d12=s * (cl[t + 12] / cl[t] - 1),
                           rest=s * (cl[t + 48] / cl[t + 12] - 1), mae=np.min(s * path),
                           wkz=abs(wk) / vol, trend=s * np.sign(p30), p30z=s * p30 / (vol * np.sqrt(15)),
                           vol=vol, alloc=b.postRebalance_current_allocation.values[t])
                rec["pnl"] = rec["alloc"] * r48
                (cs if sig[t] else ns).append(rec)
            # grid of 48 for condition-alone (30d trend direction)
            for t in range(720, n - 48, 48):
                p30 = cl[t - 48] / cl[t - 720] - 1
                s = np.sign(p30)
                if s == 0: continue
                grid.append(dict(coin=c, d48=s * (cl[t + 48] / cl[t] - 1)))
    cs = pd.DataFrame(cs); ns = pd.DataFrame(ns); grid = pd.DataFrame(grid)
    def g(df, key):
        return df.groupby(key).agg(n=("d48", "size"), d48=("d48", "mean"), t=("d48", tt),
                                   pnl=("pnl", "mean"), pnlsum=("pnl", "sum"), mae=("mae", "mean"))
    for name, fn in [
        ("by_side", lambda: g(cs, "s")),
        ("by_coin", lambda: g(cs, "coin")),
        ("by_year", lambda: g(cs, "year")),
        ("by_fq", lambda: g(cs.assign(q=rq(cs.f, 4)), "q")),
        ("by_vr_q", lambda: g(cs.assign(q=rq(cs.vr, 4)), "q")),
        ("by_wkz_q", lambda: g(cs.assign(q=rq(cs.wkz, 4)), "q")),
        ("by_volq", lambda: g(cs.assign(q=cs.groupby("coin").vol.transform(lambda x: rq(x, 3))), "q")),
        ("by_trend_align", lambda: g(cs, "trend")),
        ("by_p30z_q", lambda: g(cs.assign(q=rq(cs.p30z, 4)), "q")),
        ("fall_by_side", lambda: g(cs[cs.w.isin(fw)], "s")),
        ("fall_by_trend", lambda: g(cs[cs.w.isin(fw)], "trend")),
        ("fall_by_coin", lambda: g(cs[cs.w.isin(fw)], "coin")),
        ("side_x_trend", lambda: g(cs, ["s", "trend"])),
    ]:
        try: out[name] = fn()
        except Exception as e: out[name + "_err"] = str(e)
    try:
        cs["early"] = pd.cut(cs.d12, [-1, -0.03, -0.01, 0.01, 0.03, 1])
        out["rest_after_first12h"] = cs.groupby("early").agg(n=("rest", "size"), rest=("rest", "mean"), t=("rest", tt))
        out["tail"] = pd.Series({"sum_all": cs.pnl.sum(), "worst10": cs.pnl.nsmallest(10).sum(),
                                 "best10": cs.pnl.nlargest(10).sum(), "mean_abs_alloc": cs.alloc.abs().mean(),
                                 "n": len(cs)})
        # condition alone: non-signal Sundays (light-volume weekends), followed in weekend direction
        out["nonsig_sunday_by_trend"] = ns.groupby("trend").agg(n=("d48", "size"), d48=("d48", "mean"), t=("d48", tt))
        out["nonsig_sunday_all"] = pd.Series({"n": len(ns), "d48": ns.d48.mean(), "t": tt(ns.d48)})
        out["grid_30d_trend_follow"] = pd.Series({"n": len(grid), "d48": grid.d48.mean(), "t": tt(grid.d48)})
    except Exception as e:
        out["rest_err"] = str(e)
    return out
