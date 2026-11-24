import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    out = {}
    # build per-bar frame with forward returns on grids
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in (10, 20, 30):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = (np.mean(rs) if rs else np.nan, np.std(rs, ddof=1) if len(rs) > 1 else np.nan)
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            lr = np.log(c)
            r1 = np.r_[np.nan, np.diff(lr)]
            dep = df.get("debug_info.components.depth.last_history_value")
            for i in range(n):
                d = dict(coin=coin, win=w, pos=i, regime=df["regime"].iloc[i],
                         ts=pd.Timestamp(df["timestamp"].iloc[i]),
                         alloc=df["postRebalance_current_allocation"].iloc[i],
                         depth=(dep.iloc[i] if dep is not None else np.nan))
                for h in (10, 20, 30):
                    d[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                for p in (10, 30):
                    d[f"p{p}"] = c[i] / c[i - p] - 1 if i >= p else np.nan
                d["vol20"] = np.nanstd(r1[i - 19:i + 1]) * np.sqrt(365) if i >= 20 else np.nan
                rows.append(d)
    X = pd.DataFrame(rows)
    for h in (10, 20, 30):
        X[f"u{h}"] = X[f"f{h}"] - X["coin"].map(lambda k: drift[(k, h)][0])
        X[f"s{h}"] = X[f"u{h}"] / X["coin"].map(lambda k: drift[(k, h)][1])
    X["day"] = X["ts"].dt.floor("D")

    def summ(sub, h):
        sub = sub[sub["pos"] % h == 0].dropna(subset=[f"u{h}"])
        if len(sub) < 5:
            return pd.Series(dict(n=len(sub)))
        g = sub.groupby("day")[f"u{h}"].sum()
        m = sub[f"u{h}"].mean()
        G = len(g)
        dev = sub.groupby("day")[f"u{h}"].apply(lambda s: (s - m).sum())
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(sub)
        return pd.Series(dict(n=len(sub), days=G, mean_unusual=m, t_day=m / se,
                              total=sub[f"f{h}"].mean(), strength=sub[f"s{h}"].mean()))

    # 1 regime vs not, horizons
    res = {}
    for reg in X["regime"].unique():
        for h in (10, 20, 30):
            res[(reg, h)] = summ(X[X["regime"] == reg], h)
    out["by_regime_horizon"] = pd.DataFrame(res).T
    # 2 depth terciles within regime
    R = X[X["regime"] == "mean_reversion"].copy()
    R["dq"] = pd.qcut(R["depth"], 3, labels=["deep", "mid", "shallow"])
    out["depth_terc_30"] = pd.DataFrame({q: summ(R[R["dq"] == q], 30) for q in ["deep", "mid", "shallow"]}).T
    out["depth_terc_10"] = pd.DataFrame({q: summ(R[R["dq"] == q], 10) for q in ["deep", "mid", "shallow"]}).T
    # 3 within regime, recent 10-day return (fall still going vs turned)
    R2 = R.dropna(subset=["p10"]).copy()
    R2["pq"] = pd.qcut(R2["p10"], 3, labels=["fallingstill", "mid", "bounced"])
    out["regime_by_p10_30"] = pd.DataFrame({q: summ(R2[R2["pq"] == q], 30) for q in ["fallingstill", "mid", "bounced"]}).T
    out["regime_by_p10_10"] = pd.DataFrame({q: summ(R2[R2["pq"] == q], 10) for q in ["fallingstill", "mid", "bounced"]}).T
    # 4 all bars: past 30d return quintile -> next 10/30 (z-score within coin)
    A = X.dropna(subset=["p30"]).copy()
    A["p30z"] = A.groupby("coin")["p30"].transform(lambda s: (s - s.mean()) / s.std())
    A["q"] = pd.qcut(A["p30z"], 5, labels=False)
    out["all_p30q_next30"] = pd.DataFrame({q: summ(A[A["q"] == q], 30) for q in range(5)}).T
    out["all_p30q_next10"] = pd.DataFrame({q: summ(A[A["q"] == q], 10) for q in range(5)}).T
    # 5 vol level
    V = X.dropna(subset=["vol20"]).copy()
    V["vz"] = V.groupby("coin")["vol20"].transform(lambda s: s.rank(pct=True))
    V["q"] = pd.cut(V["vz"], [0, .33, .67, 1], labels=["lowvol", "mid", "highvol"])
    out["all_vol_next30"] = pd.DataFrame({q: summ(V[V["q"] == q], 30) for q in ["lowvol", "mid", "highvol"]}).T
    out["all_vol_next10"] = pd.DataFrame({q: summ(V[V["q"] == q], 10) for q in ["lowvol", "mid", "highvol"]}).T
    # 6 regime by vol
    RV = V[V["regime"] == "mean_reversion"]
    out["regime_vol_next30"] = pd.DataFrame({q: summ(RV[RV["q"] == q], 30) for q in ["lowvol", "mid", "highvol"]}).T
    # 7 by year in regime
    R["yr"] = R["ts"].dt.year
    out["regime_year_30"] = pd.DataFrame({y: summ(R[R["yr"] == y], 30) for y in sorted(R["yr"].unique())}).T
    out["share_regime_bars"] = float((X["regime"] == "mean_reversion").mean())
    return out
