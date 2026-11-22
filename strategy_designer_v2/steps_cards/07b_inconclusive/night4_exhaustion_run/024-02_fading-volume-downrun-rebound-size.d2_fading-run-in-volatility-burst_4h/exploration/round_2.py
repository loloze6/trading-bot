def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 18
    rows = []
    drift = {}
    for coin, wins in bars.items():
        rets = {h: [] for h in (6, 12, 18, 36)}
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            for h in rets:
                idx = np.arange(0, n - h, h)
                rets[h].extend(list(c[idx + h] / c[idx] - 1))
        drift[coin] = {h: np.mean(v) for h, v in rets.items()}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            f = df["forecast"].fillna(0).values
            dfc = np.diff(np.r_[0, f])
            sig = np.where(dfc >= 2)[0]
            seen = set()
            vr = df["debug_info.components.vol_ratio.last_history_value"].values
            sl = df["debug_info.components.streak_loss.last_history_value"].values
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            # streak length: consecutive lower closes ending at t
            down = np.r_[False, c[1:] < c[:-1]]
            slen = np.zeros(n, int)
            for i in range(n):
                slen[i] = slen[i-1] + 1 if (down[i] and i > 0) else 0
            for t in sig:
                cell = t // H
                if cell in seen or t + H >= n:
                    continue
                seen.add(cell)
                rec = {"coin": coin, "year": year[t], "vr": vr[t], "sl": sl[t], "slen": slen[t],
                       "sloss": c[t] / c[max(t - slen[t], 0)] - 1}
                for h in (6, 12, 18, 36):
                    rec["ex%d" % h] = (c[t + h] / c[t] - 1 - drift[coin][h]) if t + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="ex18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    d["sl_dec"] = pd.qcut(d["sl"].rank(method="first"), 10, labels=False)
    out["by_sl_decile"] = d.groupby("sl_dec").apply(summ)
    out["sl_decile_means"] = d.groupby("sl_dec")[["sl", "slen", "sloss", "vr"]].mean()
    top = d[d["sl_dec"] >= 8]
    out["top_sl_by_horizon"] = pd.DataFrame({h: summ(top, "ex%d" % h) for h in (6, 12, 18, 36)}).T
    out["top_sl_by_coin"] = top.groupby("coin").apply(summ)
    out["top_sl_by_year"] = top.groupby("year").apply(summ)
    out["rest_by_year"] = d[d["sl_dec"] < 8].groupby("year").apply(summ)
    vq = pd.qcut(d["vr"].rank(method="first"), 2, labels=["lowvr", "highvr"])
    sq = np.where(d["sl_dec"] >= 8, "topsl", "restsl")
    out["sl_x_vr"] = d.groupby([sq, vq]).apply(summ)
    out["by_slen"] = d.groupby(d["slen"].clip(upper=6)).apply(summ)
    out["corr_sl_ex18_spearman"] = float(d[["sl", "ex18"]].corr(method="spearman").iloc[0, 1])
    return out
