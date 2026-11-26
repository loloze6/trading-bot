import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        grid_rets = []
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30).std()
            r7 = c / c.shift(7) - 1
            z = r7 / (sd30 * np.sqrt(7))
            ch = (c - c.shift(30)).abs()
            path = c.diff().abs().rolling(30).sum()
            er = ch / path
            volr = sd30 / sd30.rolling(60).mean()
            fwd = c.shift(-7) / c - 1
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for i in range(0, len(b), 7):
                if i + 7 < len(b):
                    grid_rets.append(fwd.iloc[i])
                    recs.append(dict(coin=coin, win=w, year=yr.iloc[i], z=z.iloc[i], er=er.iloc[i],
                                     volr=volr.iloc[i], reg=b["regime"].iloc[i],
                                     fc=b["forecast"].iloc[i], fwd=fwd.iloc[i], r7=r7.iloc[i]))
        drift = np.nanmean(grid_rets)
        for d in recs:
            d["unus"] = d["fwd"] - drift
        rows += recs
    df = pd.DataFrame(rows).dropna(subset=["z", "unus"])
    df["rev"] = -np.sign(df["z"]) * df["unus"]  # reversal direction gain

    def summ(g):
        n = len(g)
        m = g["rev"].mean()
        t = m / (g["rev"].std() / np.sqrt(n)) if n > 2 else np.nan
        sl = np.polyfit(g["z"], g["unus"], 1)[0] if n > 5 else np.nan
        return pd.Series(dict(n=n, mean_rev=m, t_rev=t, slope_unus_on_z=sl))

    out = {}
    df["mr"] = df["reg"] == "mean_reversion"
    df["side"] = np.where(df["z"] > 0, "up", "down")
    out["by_regime_side"] = df.groupby(["mr", "side"]).apply(summ)
    df["erbin"] = pd.cut(df["er"], [0, 0.15, 0.3, 0.45, 1.0])
    out["by_er_side"] = df.groupby(["erbin", "side"]).apply(summ)
    dv = df.dropna(subset=["volr"])
    dv["agit"] = dv["volr"] >= 1
    dv["trend"] = dv["er"] >= 0.3
    out["by_agit_trend_volr_known"] = dv.groupby(["agit", "trend"]).apply(summ)
    df["zbin"] = pd.cut(df["z"], [-10, -1.5, -0.5, 0.5, 1.5, 10])
    out["by_zbin_all"] = df.groupby("zbin").apply(summ)
    out["by_zbin_mr"] = df[df["mr"]].groupby("zbin").apply(summ)
    out["mr_up_by_coin"] = df[df["mr"] & (df["z"] > 0)].groupby("coin").apply(summ)
    out["mr_up_by_year"] = df[df["mr"] & (df["z"] > 0)].groupby("year").apply(summ)
    out["chop_by_coin"] = df[df["er"] < 0.3].groupby("coin").apply(summ)
    out["chop_by_year"] = df[df["er"] < 0.3].groupby("year").apply(summ)
    out["regime_share"] = df["reg"].value_counts(normalize=True)
    return out
