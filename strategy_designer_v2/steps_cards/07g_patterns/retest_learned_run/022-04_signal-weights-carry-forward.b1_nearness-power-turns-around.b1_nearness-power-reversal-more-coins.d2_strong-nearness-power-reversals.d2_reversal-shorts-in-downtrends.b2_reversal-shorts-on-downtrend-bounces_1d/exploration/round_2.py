import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            f5 = c.shift(-5) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            idx = np.arange(0, len(df), 5)
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "r5": r5.values[idx], "r20": r20.values[idx],
                "f5": f5.values[idx], "fc": df["forecast"].values[idx],
                "wd": ts.dt.weekday.values[idx], "year": ts.dt.year.values[idx],
                "dkey": ts.dt.floor("D").values[idx].astype("int64"),
            }))
    g = pd.concat(rows, ignore_index=True).dropna(subset=["f5"])
    g["ex"] = g.f5 - g.groupby("coin")["f5"].transform("mean")
    g["z"] = g.ex / g.groupby("coin")["f5"].transform("std")
    out = {}
    # date-clustered weekday: mean per date then t across dates
    d = g.groupby(["dkey", "wd"])["z"].mean().reset_index()
    a = d.groupby("wd")["z"].agg(["mean", "count", "std"])
    a["t_dates"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["weekday_date_clustered"] = a.drop(columns="std")
    yy = g[g.wd.isin([1, 6])].groupby(["wd", "year"])["z"].agg(["mean", "count"])
    out["tue_sun_by_year"] = yy.unstack(0)
    out["tue_sun_by_coin"] = g[g.wd.isin([1, 6])].groupby(["coin", "wd"])["z"].mean().unstack(1)
    # bounce gate: slope of z on r5 (standardized by coin r5 std)
    gg = g.dropna(subset=["r5", "r20"]).copy()
    gg["r5s"] = gg.r5 / gg.groupby("coin")["r5"].transform("std")
    gg["r20s"] = gg.r20 / gg.groupby("coin")["r20"].transform("std")
    b = gg[(gg.r20 < 0) & (gg.r5 > 0)].copy()
    out["bounce_n"] = len(b)
    sl = stats.linregress(b.r5s, b.z)
    out["bounce_slope_z_on_r5s"] = f"slope {sl.slope:.3f} t {sl.slope/sl.stderr:.2f}"
    # date-clustered bounce slope: products per date
    b["prod"] = (b.r5s - b.r5s.mean()) * b.z
    pdk = b.groupby("dkey")["prod"].mean()
    out["bounce_prod_t_dates"] = f"mean {pdk.mean():.4f} t {pdk.mean()/(pdk.std()/np.sqrt(len(pdk))):.2f} n_dates {len(pdk)}"
    b["q"] = pd.qcut(b.r5s.rank(method="first"), 3, labels=False)
    out["bounce_r5_tercile_by_year"] = b.groupby(["year", "q"])["z"].mean().unstack(1)
    b["inactive"] = b.fc >= 0
    bi = b[b.inactive]
    sl2 = stats.linregress(bi.r5s, bi.z)
    out["bounce_inactive_slope"] = f"slope {sl2.slope:.3f} t {sl2.slope/sl2.stderr:.2f} n {len(bi)}"
    # mirror: dip inside uptrend, slope on r5
    u = gg[(gg.r20 > 0) & (gg.r5 < 0)]
    sl3 = stats.linregress(u.r5s, u.z)
    out["dip_in_up_slope"] = f"slope {sl3.slope:.3f} t {sl3.slope/sl3.stderr:.2f} n {len(u)}"
    # interaction across all: z on r5s * (r20<0)
    dn = gg[gg.r20 < 0]
    sl4 = stats.linregress(dn.r5s, dn.z)
    out["down20_all_r5_slope"] = f"slope {sl4.slope:.3f} t {sl4.slope/sl4.stderr:.2f} n {len(dn)}"
    # bounce by r5 tercile by coin count negative
    out["bounce_top_tercile_by_coin"] = b[b.q == 2].groupby("coin")["z"].agg(["mean", "count"])
    # book: daily returns by weekday
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df.copy(); x["wd"] = pd.to_datetime(x["day"]).dt.weekday; x["coin"] = coin
            dd.append(x)
    dd = pd.concat(dd).dropna(subset=["book_return"])
    out["book_by_weekday_bp"] = dd.groupby("wd")["book_return"].agg(lambda s: s.mean() * 1e4)
    return out
