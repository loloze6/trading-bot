def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    coins = list(bars.keys())
    H = [24, 72, 168, 336]
    grid = []; cases = []
    for c in coins:
        drift = {}
        for h in H:
            r = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                r.append(cl[idx + h] / cl[idx] - 1)
            drift[h] = np.concatenate(r).mean()
        for w, b in bars[c].items():
            cl = b["close"].values; n = len(cl)
            s = pd.Series(cl)
            r24 = s.pct_change(24); ma = r24.abs().rolling(720).mean(); r30 = s.pct_change(720)
            sd30 = s.pct_change(720).rolling(2000, min_periods=500).std()
            vol = s.pct_change().rolling(720).std()
            vol_q = vol.rank(pct=True)
            idx = np.arange(0, n - 72, 72)
            for i in idx:
                if np.isnan(ma.iloc[i]) or np.isnan(r30.iloc[i]): continue
                rec = {"coin": c, "w": w, "dipz": r24.iloc[i] / ma.iloc[i], "r30": r30.iloc[i],
                       "r30z": r30.iloc[i] / sd30.iloc[i] if sd30.iloc[i] > 0 else np.nan,
                       "year": pd.Timestamp(b["timestamp"].iloc[i]).year}
                for h in H:
                    rec[f"u{h}"] = cl[i + h] / cl[i] - 1 - drift[h] if i + h < n else np.nan
                grid.append(rec)
            f = b["forecast"].fillna(0).values
            raw = b["debug_info.components.dip_in_rise.last_history_value"].values
            onset = np.where((f > 0) & (np.r_[0, f[:-1]] == 0))[0]
            seen = set()
            for i in onset:
                g = i // 72
                if g in seen: continue
                seen.add(g)
                rec = {"coin": c, "raw": raw[i], "year": pd.Timestamp(b["timestamp"].iloc[i]).year,
                       "dipz": r24.iloc[i] / ma.iloc[i] if ma.iloc[i] > 0 else np.nan, "r30": r30.iloc[i]}
                for h in H:
                    rec[f"u{h}"] = cl[i + h] / cl[i] - 1 - drift[h] if i + h < n else np.nan
                cases.append(rec)
    G = pd.DataFrame(grid); C = pd.DataFrame(cases)
    def tt(x):
        x = x.dropna(); return pd.Series({"mean": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 1 else np.nan, "n": len(x)})
    up = G[G.r30 > 0]; dn = G[G.r30 <= 0]
    up_d = up[up.dipz <= -1]
    out["up_dip_le-1_by_h"] = pd.DataFrame({h: tt(up_d[f"u{h}"]) for h in H})
    dn_d = dn[dn.dipz <= -1]
    out["down_dip_le-1_by_h"] = pd.DataFrame({h: tt(dn_d[f"u{h}"]) for h in H})
    big = G[G.dipz.abs() >= 2]
    out["abs_move_ge2_by_side_h72"] = pd.DataFrame({"up_trend_fall": tt(up[up.dipz <= -2].u72), "up_trend_rise": tt(up[up.dipz >= 2].u72),
                                                    "down_trend_fall": tt(dn[dn.dipz <= -2].u72), "down_trend_rise": tt(dn[dn.dipz >= 2].u72)})
    # graded: in uptrend, spearman of -dipz with u72; and of r30z among dips
    x = up.dropna(subset=["u72"])
    out["spearman_up_negdip_u72"] = pd.Series(stats.spearmanr(-x.dipz, x.u72)[:2], index=["rho", "p"])
    y = up_d.dropna(subset=["u72", "r30z"])
    out["spearman_updips_r30z_u72"] = pd.Series(stats.spearmanr(y.r30z, y.u72)[:2], index=["rho", "p"])
    y["r30q"] = pd.qcut(y.r30z.rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["updips_by_r30z_tercile"] = y.groupby("r30q")["u72"].agg(["mean", "count"])
    out["updips_by_coin"] = up_d.groupby("coin")["u72"].agg(["mean", "count"])
    out["updips_by_year"] = up_d.groupby("year")["u72"].agg(["mean", "count"])
    # cases: graded by raw continuous
    z = C.dropna(subset=["u72", "raw"])
    out["cases_spearman_raw"] = pd.DataFrame({h: pd.Series(stats.spearmanr(C.dropna(subset=[f"u{h}", "raw"]).raw, C.dropna(subset=[f"u{h}", "raw"])[f"u{h}"])[:2], index=["rho", "p"]) for h in H})
    out["cases_by_year_u72"] = C.groupby("year")["u72"].agg(["mean", "count"])
    out["cases_dipz_quint"] = C.assign(q=pd.qcut(C.dipz.rank(method="first"), 4, labels=False)).groupby("q").agg(dipz=("dipz", "mean"), u72=("u72", "mean"), u168=("u168", "mean"), n=("u72", "size"))
    # trades: by duration and concentration
    T = pd.concat([trades[c][w].assign(coin=c, w=w) for c in coins for w in trades[c] if len(trades[c][w])])
    T["durd"] = pd.cut(T.duration_minutes / 1440, [0, 3.01, 7, 14, 30, np.inf])
    out["trades_by_dur_days"] = T.groupby("durd")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    p = T.net_profit_loss_percent.sort_values(ascending=False)
    out["trade_conc"] = pd.Series({"sum_all": p.sum(), "sum_wo_top1pct": p.iloc[int(len(p) * .01):].sum(),
                                   "sum_wo_top5pct": p.iloc[int(len(p) * .05):].sum(), "top1pct_count": int(len(p) * .01),
                                   "top1pct_xrp_share": (T.loc[p.index[:int(len(p) * .01)]].coin == "XRPUSD").mean() if p.index.is_unique else np.nan})
    # book daily: share of gain from top days
    rows = []
    for c in coins:
        for w, d in days[c].items():
            rows.append(d.assign(w=w))
    Dd = pd.concat(rows).groupby(["w", "day"])["book_return"].mean().dropna().sort_values(ascending=False)
    out["book_days_conc"] = pd.Series({"mean": Dd.mean(), "mean_wo_top1pct_days": Dd.iloc[int(len(Dd) * .01):].mean(),
                                       "mean_wo_top5pct_days": Dd.iloc[int(len(Dd) * .05):].mean(), "n": len(Dd)})
    return out
