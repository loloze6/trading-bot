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
    hourly = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df[["timestamp", "close", "volume", "forecast"]].copy()
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
            r1 = np.full(n, np.nan)
            r1[:-1] = c[1:] / c[:-1] - 1
            hourly.append(pd.DataFrame({"hr": hr, "wd": wd, "r": r1}))
            g = c[::12]
            sd12 = np.nanstd(g[1:] / g[:-1] - 1)
            for i in np.where(hr == 23)[0]:
                if i < 168 or i + 48 >= n:
                    continue
                if ts[i] - ts[i - 168] != 168 or ts[i + 48] - ts[i] != 48:
                    continue
                p48 = c[i] / c[i - 48] - 1
                s = np.sign(p48)
                if s == 0:
                    continue
                vr = v[i - 47:i + 1].mean() / max(v[i - 167:i - 47].mean(), 1e-12)
                rows.append({
                    "coin": coin, "wd": wd[i], "z": abs(p48) / (2 * sd12),
                    "vr": vr, "heavy": vr >= 1,
                    "s12": s * (c[i + 12] / c[i] - 1),
                    "s12_36": s * (c[i + 36] / c[i + 12] - 1),
                    "s48": s * (c[i + 48] / c[i] - 1),
                    "fc": d["forecast"].iloc[i] != 0,
                })
    R = pd.DataFrame(rows)
    out = {}
    out["A_signed12h_by_weekday_heavy"] = R[R.heavy].groupby("wd")["s12"].apply(_t).unstack()
    out["A2_signed12h_by_weekday_light"] = R[~R.heavy].groupby("wd")["s12"].apply(_t).unstack()
    S = R[R.wd == 6].copy()
    S["vr_q"] = pd.qcut(S["vr"], 4, labels=False, duplicates="drop")
    out["B_sun_by_vr_quartile_s12"] = S.groupby("vr_q")["s12"].apply(_t).unstack()
    out["B2_sun_by_vr_quartile_s12_36"] = S.groupby("vr_q")["s12_36"].apply(_t).unstack()
    out["B3_sun_by_vr_quartile_s48"] = S.groupby("vr_q")["s48"].apply(_t).unstack()
    H = S[S.heavy].copy()
    H["z_q"] = pd.qcut(H["z"], 3, labels=False, duplicates="drop")
    out["C_sun_heavy_by_move_tercile_s12"] = H.groupby("z_q")["s12"].apply(_t).unstack()
    out["C2_sun_heavy_by_move_tercile_s12_36"] = H.groupby("z_q")["s12_36"].apply(_t).unstack()
    out["F_sun_heavy_by_coin_s12"] = H.groupby("coin")["s12"].apply(_t).unstack()
    Hh = pd.concat(hourly)
    out["D_mean_hourly_return_by_hour"] = Hh.groupby("hr")["r"].apply(_t).unstack()
    out["D2_mean_hourly_return_by_weekday"] = Hh.groupby("wd")["r"].apply(_t).unstack()
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df[["day", "book_return", "coin_return"]].copy()
            x["day"] = pd.to_datetime(x["day"], errors="coerce")
            dd.append(x)
    D = pd.concat(dd).dropna()
    D["wd"] = D["day"].dt.weekday
    D["yr"] = D["day"].dt.year
    nz = D[D.book_return != 0]
    out["E_book_return_by_year_nonzero_days"] = nz.groupby("yr")["book_return"].apply(_t).unstack()
    q = nz["book_return"].quantile(0.05)
    out["E2_worst5pct_book_days_count_by_weekday"] = nz[nz.book_return <= q].groupby("wd").size()
    return out
