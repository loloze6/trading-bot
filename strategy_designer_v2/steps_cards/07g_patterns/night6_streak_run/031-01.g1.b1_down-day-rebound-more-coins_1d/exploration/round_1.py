import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 3
    rows = []
    for coin, wins in data["bars"].items():
        # drift and usual move per coin: non-overlapping 3-bar grid across windows
        g_all = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            g_all.append(c[idx + H] / c[idx] - 1)
        g_all = np.concatenate(g_all) if g_all else np.array([])
        if len(g_all) < 10:
            continue
        drift, usual = g_all.mean(), g_all.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(60, min_periods=20).std()
            sr = r / vol
            sign = np.sign(r).fillna(0)
            # signed streak length
            streak = np.zeros(len(r))
            for i in range(1, len(r)):
                s = sign.iloc[i]
                if s == 0:
                    streak[i] = 0
                elif streak[i-1] * s > 0:
                    streak[i] = streak[i-1] + s
                else:
                    streak[i] = s
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            vol_rel = vol / r.rolling(180, min_periods=60).std()
            rng = (b["high"] - b["low"]) / c
            rng_s = rng / rng.rolling(60, min_periods=20).mean()
            clv = ((c - b["low"]) - (b["high"] - c)) / (b["high"] - b["low"]).replace(0, np.nan)
            volu = b["volume"].astype(float)
            volu_s = volu / volu.rolling(60, min_periods=20).mean()
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(c) - H, H)
            for i in idx:
                rows.append(dict(coin=coin, win=w, day=ts.iloc[i].normalize(),
                    wd=ts.iloc[i].dayofweek, year=ts.iloc[i].year,
                    sr=sr.iloc[i], streak=streak[i], r5s=r5.iloc[i] / (vol.iloc[i] * np.sqrt(5)) if vol.iloc[i] > 0 else np.nan,
                    r20s=r20.iloc[i] / (vol.iloc[i] * np.sqrt(20)) if vol.iloc[i] > 0 else np.nan,
                    volrel=vol_rel.iloc[i], rng_s=rng_s.iloc[i], clv=clv.iloc[i], volu_s=volu_s.iloc[i],
                    u=(fwd.iloc[i] - drift), z=(fwd.iloc[i] - drift) / usual,
                    pos=b["postRebalance_current_allocation"].iloc[i]))
    d = pd.DataFrame(rows).dropna(subset=["u"])

    def tab(df, col, q=None, bins=None):
        x = df.dropna(subset=[col]).copy()
        if q:
            x["b"] = pd.qcut(x[col], q, duplicates="drop")
        else:
            x["b"] = x[col]
        out = []
        for k, g in x.groupby("b", observed=True):
            dd = g.groupby("day")["u"].sum()
            nd = len(dd)
            t = g["u"].mean() / (dd.std() * np.sqrt(nd) / len(g)) if nd > 2 and dd.std() > 0 else np.nan
            out.append(dict(bin=str(k), n=len(g), days=nd, mean_u_pct=100 * g["u"].mean(),
                            strength=g["z"].mean(), t_day=t))
        return pd.DataFrame(out)

    def slope(df, col):
        x = df.dropna(subset=[col])
        X = x[col].values; Y = x["z"].values
        Xc = X - X.mean()
        b = (Xc * (Y - Y.mean())).sum() / (Xc ** 2).sum()
        e = Y - Y.mean() - b * Xc
        sc = pd.Series(Xc * e).groupby(x["day"].values).sum()
        se = np.sqrt((sc ** 2).sum()) / (Xc ** 2).sum()
        return pd.Series(dict(n=len(x), slope=b, t=b / se))

    d["streak_c"] = d["streak"].clip(-5, 5)
    res = {
        "by_scaled_1d_return": tab(d, "sr", q=10),
        "by_streak": tab(d, "streak_c"),
        "by_5d_scaled": tab(d, "r5s", q=10),
        "by_20d_scaled": tab(d, "r20s", q=10),
        "by_vol_regime": tab(d, "volrel", q=5),
        "by_range": tab(d, "rng_s", q=5),
        "by_close_loc": tab(d, "clv", q=5),
        "by_volume": tab(d, "volu_s", q=5),
        "by_weekday": tab(d, "wd"),
        "by_year": tab(d, "year"),
        "slopes_z": pd.DataFrame({c: slope(d, c) for c in ["sr", "streak", "r5s", "r20s", "volrel", "rng_s", "clv", "volu_s"]}).T,
    }
    return res
