import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    fc_desc = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std()
            mv = v.rolling(720, min_periods=240).mean()
            z = r / sd; vr = v / mv
            x = z * vr
            fc = b["forecast"].astype(float)
            fc_desc.append(fc)
            lh = b.get("debug_info.components.vol_surge_up.last_history_value")
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in (2, 4, 6):
                pos = np.arange(0, len(b) - h, h)
                fr = c.shift(-h).iloc[pos].values / c.iloc[pos].values - 1
                df = pd.DataFrame({"coin": coin, "w": w, "h": h, "fr": fr,
                                   "z": z.iloc[pos].values, "vr": vr.iloc[pos].values,
                                   "x": x.iloc[pos].values, "fc": fc.iloc[pos].values,
                                   "yr": yr.iloc[pos].values})
                rows.append(df)
    d = pd.concat(rows)
    d["drift"] = d.groupby(["coin", "h"])["fr"].transform("mean")
    d["u"] = d["fr"] - d["drift"]
    allfc = pd.concat(fc_desc)
    out["forecast_dist"] = allfc.describe(percentiles=[.5, .75, .9, .95, .99])
    out["share_fc_eq20"] = float((allfc >= 19.99).mean())
    out["share_fc_pos"] = float((allfc > 0).mean())

    def summ(g):
        n = len(g); m = g["u"].mean(); s = g["u"].std()
        return pd.Series({"n": n, "mean_u_%": 100 * m, "t": m / (s / np.sqrt(n)) if n > 1 else np.nan,
                          "mean_z": g["z"].mean(), "mean_vr": g["vr"].mean()})
    dd = d.dropna(subset=["z", "vr", "u"]).copy()
    # surge up / down, by z bucket and volume bucket
    dd["zb"] = pd.cut(dd["z"], [-np.inf, -4, -3, -2, 2, 3, 4, np.inf])
    dd["vb"] = pd.cut(dd["vr"], [0, 1.5, 3, np.inf])
    out["h6_by_z_vol"] = dd[dd.h == 6].groupby(["zb", "vb"], observed=True).apply(summ)
    out["h2_by_z_vol"] = dd[dd.h == 2].groupby(["zb", "vb"], observed=True).apply(summ)
    # forecast bands at h6
    dd["fb"] = pd.cut(dd["fc"], [-0.01, 0.0001, 2, 10, 19.99, 20.01])
    out["h6_by_forecast"] = dd[dd.h == 6].groupby("fb", observed=True).apply(summ)
    # strong up & heavy vol by coin and year, h6
    s = dd[(dd.h == 6) & (dd.z > 3) & (dd.vr > 3)]
    out["h6_zgt3_vgt3_by_coin"] = s.groupby("coin").apply(summ)
    out["h6_zgt3_vgt3_by_year"] = s.groupby("yr").apply(summ)
    sd_ = dd[(dd.h == 6) & (dd.z < -3) & (dd.vr > 3)]
    out["h6_zlt-3_vgt3_by_year"] = sd_.groupby("yr").apply(summ)
    return out
