import numpy as np
import pandas as pd
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    n = len(x)
    if n < 3 or x.std() == 0:
        return pd.Series({"mean": x.mean() if n else np.nan, "t": np.nan, "n": n})
    return pd.Series({"mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)), "n": n})

def explore(data):
    rows = []
    eve = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df[["timestamp", "close", "volume"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            d = d.dropna(subset=["ts", "close"]).reset_index(drop=True)
            n = len(d)
            if n < 300:
                continue
            c = d["close"].values.astype(float)
            v = d["volume"].values.astype(float)
            ts = d["ts"].values.astype("datetime64[h]").astype(np.int64)
            hr = d["ts"].dt.hour.values
            wd = d["ts"].dt.weekday.values
            yr = d["ts"].dt.year.values
            g = c[::12]
            sd12 = np.nanstd(g[1:] / g[:-1] - 1)
            # evening hours: return from close of 19:00 bar to close of 21:00 bar (covers hours 20,21)
            for i in np.where(hr == 19)[0]:
                if i < 20 or i + 2 >= n:
                    continue
                if ts[i + 2] - ts[i] != 2 or ts[i] - ts[i - 20] != 20:
                    continue
                prior = c[i] / c[i - 20] - 1
                eve.append({"coin": coin, "w": w, "yr": yr[i], "wd": wd[i],
                            "r": c[i + 2] / c[i] - 1, "prior": prior,
                            "pz": prior / sd12})
            for i in np.where((hr == 23) & (wd == 6))[0]:
                if i < 168 or i + 48 >= n:
                    continue
                if ts[i] - ts[i - 168] != 168 or ts[i + 48] - ts[i] != 48:
                    continue
                p48 = c[i] / c[i - 48] - 1
                s = np.sign(p48)
                if s == 0:
                    continue
                vr = v[i - 47:i + 1].mean() / max(v[i - 167:i - 47].mean(), 1e-12)
                rows.append({"coin": coin, "w": w, "yr": yr[i], "vr": vr,
                             "lvr": np.log(max(vr, 1e-6)), "z": abs(p48) / (2 * sd12),
                             "s12_36": s * (c[i + 36] / c[i + 12] - 1),
                             "s48": s * (c[i + 48] / c[i] - 1)})
    E = pd.DataFrame(eve)
    R = pd.DataFrame(rows)
    out = {}
    out["A_eve_20_21_by_coin"] = E.groupby("coin")["r"].apply(_t).unstack()
    out["A2_eve_by_year"] = E.groupby("yr")["r"].apply(_t).unstack()
    out["A3_eve_by_weekday"] = E.groupby("wd")["r"].apply(_t).unstack()
    E["sp"] = np.sign(E["prior"]) * E["r"]
    E["pq"] = pd.qcut(E["pz"], 5, labels=False, duplicates="drop")
    out["A4_eve_by_prior20h_quintile"] = E.groupby("pq")["r"].apply(_t).unstack()
    out["A5_share_windows_positive"] = float((E.groupby(["coin", "w"])["r"].mean() > 0).mean())
    L = R[R.vr < 1].copy()
    L["vq"] = pd.qcut(L["vr"], 4, labels=False, duplicates="drop")
    out["B_light_sun_by_vr_quartile_s48"] = L.groupby("vq")["s48"].apply(_t).unstack()
    out["B2_light_sun_by_vr_quartile_s12_36"] = L.groupby("vq")["s12_36"].apply(_t).unstack()
    rr = stats.spearmanr(R["lvr"], R["s48"], nan_policy="omit")
    out["B3_spearman_lvr_s48_all_sundays"] = pd.Series({"rho": rr[0], "p": rr[1], "n": len(R)})
    rl = stats.spearmanr(L["z"], L["s48"], nan_policy="omit")
    out["B4_light_spearman_move_s48"] = pd.Series({"rho": rl[0], "p": rl[1], "n": len(L)})
    Q = R[R.vr <= R.vr.quantile(0.25)]
    out["B5_thinnest_quartile_s48_by_coin"] = Q.groupby("coin")["s48"].apply(_t).unstack()
    out["B6_thinnest_quartile_s48_by_year"] = Q.groupby("yr")["s48"].apply(_t).unstack()
    return out
