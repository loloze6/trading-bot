def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; coins = list(bars.keys())
    def streak_info(cl, vol):
        n = len(cl); s = np.zeros(n, int); fade = np.full(n, np.nan)
        for i in range(1, n):
            s[i] = s[i-1] + 1 if cl[i] < cl[i-1] else 0
        for i in range(n):
            k = min(s[i], 180)
            if k >= 2:
                y = vol[i-k+1:i+1]; x = np.arange(k)
                fade[i] = np.polyfit(x, y, 1)[0]
        return s, fade
    for h in [18, 42]:
        recs = []
        for c in coins:
            allf = []
            for w, b in bars[c].items():
                cl = b["close"].values
                allf.append((cl[h:] / cl[:-h] - 1)[::h])
            mu = np.concatenate(allf).mean()
            for w, b in bars[c].items():
                cl = b["close"].values; vol = b["volume"].values; n = len(cl)
                s, fade = streak_info(cl, vol)
                yr = pd.to_datetime(b["timestamp"]).dt.year.values
                for i in range(180, n - h, h):
                    r30 = cl[i] / cl[i-180] - 1
                    r30s = pd.Series(cl[:i+1]).pct_change(180).iloc[-180:]
                    z = (r30 - r30s.mean()) / r30s.std() if r30s.notna().sum() > 45 else np.nan
                    recs.append(dict(coin=c, w=w, year=yr[i], r30=r30, z=z, streak=s[i],
                                     fade=fade[i], u=cl[i+h] / cl[i] - 1 - mu))
        R = pd.DataFrame(recs)
        R["q"] = R.groupby("coin")["r30"].transform(lambda x: pd.qcut(x, 5, labels=False))
        out[f"h{h*4}h_by_r30_quintile"] = R.groupby("q")["u"].agg(["mean", "count"])
        up = R[R.r30 > 0]
        g = {}
        g["all_up"] = up.u
        g["up_downstreak_fade"] = up[(up.streak >= 2) & (up.fade < 0)].u
        g["up_downstreak_risingvol"] = up[(up.streak >= 2) & (up.fade > 0)].u
        g["up_no_downstreak"] = up[up.streak < 2].u
        out[f"h{h*4}h_situations_r30up"] = pd.DataFrame({k: {"mean": v.mean(), "n": len(v), "t": stats.ttest_1samp(v, 0).statistic} for k, v in g.items()}).T
        zz = up.dropna(subset=["z"])
        zz = zz[zz.z > 0]
        out[f"h{h*4}h_corr_z_u_r30up_zpos"] = pd.Series({"spearman": stats.spearmanr(zz.z, zz.u)[0], "n": len(zz)})
        out[f"h{h*4}h_r30up_minus_dn_by_year"] = R.assign(side=np.where(R.r30 > 0, 1, -1)).assign(su=lambda x: x.u * x.side).groupby("year")["su"].agg(["mean", "count"])
        out[f"h{h*4}h_r30up_by_coin"] = up.groupby("coin")["u"].agg(["mean", "count"])
    # book exposure: share of time in position & where
    ex = []
    for c in coins:
        for w, b in bars[c].items():
            a = b["postRebalance_current_allocation"].fillna(0)
            ex.append(pd.DataFrame({"inpos": (a > 0).astype(float), "a": a, "reg": (b["regime"] == "mean_reversion").astype(float)}))
    E = pd.concat(ex)
    out["exposure"] = pd.Series({"share_bars_in_position": E.inpos.mean(), "mean_alloc": E.a.mean(), "share_regime_active": E.reg.mean()})
    return out
