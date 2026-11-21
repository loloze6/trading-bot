import numpy as np, pandas as pd
from scipy import stats

def _grp(df, var, val="unusual", q=3):
    d = df[[var, val]].dropna()
    if len(d) < 15:
        return pd.DataFrame()
    d = d.copy()
    d["g"] = pd.qcut(d[var].rank(method="first"), q, labels=False)
    g = d.groupby("g")[val].agg(["count", "mean", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    g["var_mean"] = d.groupby("g")[var].mean()
    rho, p = stats.spearmanr(d[var], d[val])
    g["spearman_rho"] = rho
    g["spearman_p"] = p
    return g.round(4)

def explore(data):
    bars = data["bars"]; days = data["days"]; out = {}
    H = 26
    drift = {}; usual = {}
    for c, ws in bars.items():
        r = []
        for w, df in ws.items():
            cl = df["close"].values
            idx = np.arange(0, len(cl) - H, H)
            r += list(cl[idx + H] / cl[idx] - 1)
        drift[c] = np.mean(r); usual[c] = np.std(r)
    rows = []; grid = []; daily = []; agerows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values.astype(float); n = len(cl)
            hi = df["high"].values.astype(float); lo = df["low"].values.astype(float)
            vol = df["volume"].values.astype(float)
            ret1 = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
            ts = pd.to_datetime(df["timestamp"])
            reg = df["regime"].values
            raw = df.get("debug_info.components.thin_cloud.last_history_value")
            def feats(i):
                return dict(
                    past26=cl[i] / cl[i - 26] - 1 if i >= 26 else np.nan,
                    past7=cl[i] / cl[i - 7] - 1 if i >= 7 else np.nan,
                    vol20=np.nanstd(ret1[max(1, i - 19):i + 1]) if i >= 10 else np.nan,
                    ret0=ret1[i],
                    dist_hi26=cl[i] / hi[max(0, i - 25):i + 1].max() - 1 if i >= 25 else np.nan,
                    volratio=vol[i] / np.nanmean(vol[max(0, i - 20):i]) if i >= 10 else np.nan,
                )
            tr = np.where(reg == "trending")[0]
            used = set()
            for i in tr:
                if i + H >= n: continue
                cell = i // H
                if cell in used: continue
                used.add(cell)
                fwd = cl[i + H] / cl[i] - 1
                d = dict(coin=c, win=w, unusual=fwd - drift[c], fwd=fwd,
                         f13=cl[i + 13] / cl[i] - 1 - drift[c] / 2,
                         f52=(cl[i + 52] / cl[i] - 1 - 2 * drift[c]) if i + 52 < n else np.nan,
                         raw=float(raw.iloc[i]) if raw is not None and pd.notna(raw.iloc[i]) else np.nan,
                         year=ts.iloc[i].year)
                d.update(feats(i)); rows.append(d)
            for i in np.arange(0, n - H, H):
                d = dict(coin=c, win=w, unusual=cl[i + H] / cl[i] - 1 - drift[c],
                         strength=(cl[i + H] / cl[i] - 1 - drift[c]) / usual[c])
                d.update(feats(i)); grid.append(d)
            for i in range(1, n - 1):
                daily.append(dict(coin=c, r0=ret1[i], r1=ret1[i + 1], wd=ts.iloc[i + 1].weekday(),
                                  vol20=np.nanstd(ret1[max(1, i - 19):i + 1]) if i >= 10 else np.nan))
            # position gain by age since last cross
            pos = df["postRebalance_current_allocation"].values.astype(float)
            last = -999
            for i in range(n - 1):
                if reg[i] == "trending": last = i
                if pos[i] > 0 and last >= 0:
                    agerows.append(dict(age=i - last, gain=pos[i] * ret1[i + 1],
                                        mkt=pos[i] * (drift[c] / H)))
    cs = pd.DataFrame(rows); gr = pd.DataFrame(grid); dy = pd.DataFrame(daily); ag = pd.DataFrame(agerows)
    out["cases_n_mean_unusual_f13_f52"] = cs[["unusual", "f13", "f52"]].agg(["count", "mean", "std"]).round(4)
    for v in ["past26", "past7", "vol20", "ret0", "dist_hi26", "volratio", "raw"]:
        out["cases_by_" + v] = _grp(cs, v)
    out["cases_by_coin"] = cs.groupby("coin")["unusual"].agg(["count", "mean", "std"]).round(4)
    out["cases_by_year"] = cs.groupby("year")["unusual"].agg(["count", "mean"]).round(4)
    # plain momentum on the grid, same horizon
    out["grid_by_past26"] = _grp(gr, "past26", q=5)
    out["grid_by_vol20"] = _grp(gr, "vol20", q=3)
    out["grid_by_dist_hi26"] = _grp(gr, "dist_hi26", q=5)
    # daily: next-day after large moves (z by coin vol)
    dy["z0"] = dy["r0"] / dy["vol20"]
    out["daily_next_by_z0"] = _grp(dy, "z0", val="r1", q=5)
    w = dy.groupby("wd")["r1"].agg(["count", "mean", "std"]); w["t"] = w["mean"] / (w["std"] / np.sqrt(w["count"]))
    out["daily_by_weekday"] = w.round(5)
    ag["ab"] = pd.cut(ag["age"], [-1, 0, 3, 7, 13, 19, 26, 200])
    a = ag.groupby("ab")[["gain", "mkt"]].agg(["count", "mean"]); out["pos_gain_by_age"] = a.round(5)
    return out
