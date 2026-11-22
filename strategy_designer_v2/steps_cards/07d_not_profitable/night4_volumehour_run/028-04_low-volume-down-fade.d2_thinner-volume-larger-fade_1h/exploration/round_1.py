import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H = [6, 12, 24, 48]
    drift = {}
    for coin, ws in data["bars"].items():
        for h in H:
            rs = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.concatenate(rs).mean()
    rows = []
    gross, net, turn = [], [], []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            ret1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            al = b["postRebalance_current_allocation"].fillna(0).values
            gross.append(np.nansum(al * ret1))
            pv = b["postRebalance_total_value"].values
            net.append(np.log(pv[-1] / pv[0]))
            turn.append(np.abs(b["allocation_change"].fillna(0)).sum())
            f = b["forecast"].fillna(0).values
            z = b["debug_info.components.fall.last_history_value"].values
            zv = b["debug_info.components.fall_x_volume.last_history_value"].values
            v = np.where(np.abs(z) > 1e-12, zv / z, np.nan)
            lr = np.log(c)
            for cell in range(0, n, 6):
                seg = np.where(f[cell:cell + 6] >= 2)[0]
                if len(seg) == 0:
                    continue
                t = cell + seg[0]
                r = {"coin": coin, "window": w, "year": b["timestamp"].iloc[t].year,
                     "f": f[t], "z": z[t], "v": v[t],
                     "p24": c[t] / c[t - 24] - 1 if t >= 24 else np.nan,
                     "p168": c[t] / c[t - 168] - 1 if t >= 168 else np.nan,
                     "hr": b["timestamp"].iloc[t].hour}
                for h in H:
                    r[f"u{h}"] = (c[t + h] / c[t] - 1 - drift[(coin, h)]) if t + h < n else np.nan
                    r[f"t{h}"] = (c[t + h] / c[t] - 1) if t + h < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    out["book_gross_vs_net"] = pd.Series({"sum_gross_bar_gain": np.sum(gross), "sum_log_net": np.sum(net),
                                          "sum_turnover": np.sum(turn), "turnover_x_0.0011/2?": np.sum(turn) * 0.00055})
    def summ(g):
        s = {"n": len(g)}
        for h in H:
            x = g[f"u{h}"].dropna()
            s[f"u{h}"] = x.mean(); s[f"t{h}_t"] = x.mean() / (x.std() / np.sqrt(len(x)))
            s[f"tot{h}"] = g[f"t{h}"].mean()
        return pd.Series(s)
    out["all"] = summ(d)
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 5, labels=False)
    out["by_forecast_q"] = d.groupby("fq").apply(summ)
    d["zq"] = pd.qcut(d["z"].rank(method="first"), 5, labels=False)
    out["by_fall_q(0=deepest)"] = d.groupby("zq").apply(summ)
    d["vq"] = pd.qcut(d["v"].rank(method="first"), 5, labels=False)
    out["by_vol_ratio_q(0=thinnest)"] = d.groupby("vq").apply(summ)
    dd = d.dropna(subset=["p168"]).copy()
    dd["pq"] = pd.qcut(dd["p168"].rank(method="first"), 5, labels=False)
    out["by_prior7d_q(0=most down)"] = dd.groupby("pq").apply(summ)
    dd = d.dropna(subset=["p24"]).copy()
    dd["pq"] = pd.qcut(dd["p24"].rank(method="first"), 5, labels=False)
    out["by_prior24h_q"] = dd.groupby("pq").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["vq_mean_v"] = d.groupby("vq")["v"].mean()
    out["zq_mean_z"] = d.groupby("zq")["z"].mean()
    return out
