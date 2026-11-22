import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    coins = list(bars.keys())
    # coin normal 84-bar drift and usual move, per coin, non-overlapping grid
    drift = {}; usual = {}
    for c in coins:
        rs = []
        for w, b in bars[c].items():
            cl = b["close"].reset_index(drop=True)
            g = cl.iloc[::84]
            rr = (g.shift(-1) / g - 1).dropna()
            rs.append(rr)
        rs = pd.concat(rs); drift[c] = rs.mean(); usual[c] = rs.std()
    out["drift_usual"] = pd.DataFrame({"drift": drift, "usual": usual}).round(4)
    # time in market
    st = []
    allrows = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            a = b["postRebalance_current_allocation"].fillna(0)
            f = b["forecast"].fillna(0)
            st.append(dict(coin=c, wi=int(w[1:]), in_mkt=(a > 0).mean(), fc_pos=(f > 0).mean(),
                           in_mkt_fc0=((a > 0) & (f == 0)).mean(), mean_alloc=a.mean(),
                           ntrade=(b["allocation_change"].fillna(0).abs() > 1e-9).sum()))
            cl = b["close"]; lr = np.log(cl).diff()
            r180 = cl / cl.shift(180) - 1
            v42 = lr.rolling(42).std(); v360 = lr.rolling(360, min_periods=180).std()
            fwd = cl.shift(-84) / cl - 1
            df = pd.DataFrame(dict(coin=c, wi=int(w[1:]), pos=np.arange(len(b)), f=f, a=a,
                                   r180=r180, vr=v42 / v360, fwd=fwd))
            df["cell"] = df["pos"] // 84
            allrows.append(df)
    S = pd.DataFrame(st)
    out["time_in_market"] = S[["in_mkt", "fc_pos", "in_mkt_fc0", "mean_alloc", "ntrade"]].describe().round(3)
    out["in_mkt_by_window"] = S.groupby("wi")[["in_mkt", "fc_pos", "mean_alloc"]].mean().round(3)
    A = pd.concat(allrows)
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    # cases: first bar in each cell with forecast >= 2
    C = A[A["f"] >= 2].dropna(subset=["fwd"]).groupby(["coin", "wi", "cell"]).head(1)
    out["n_cases"] = len(C)
    def grp(col, q=4):
        G = C.dropna(subset=[col])
        k = pd.qcut(G[col], q, labels=False, duplicates="drop")
        t = G.groupby(k).agg(lo=(col, "min"), hi=(col, "max"), n=("ex", "size"), ex=("ex", "mean"),
                             sd=("ex", "std"), fwd=("fwd", "mean"))
        t["t"] = t["ex"] / (t["sd"] / np.sqrt(t["n"]))
        return t.round(4)
    out["cases_by_r180"] = grp("r180")
    out["cases_by_vr"] = grp("vr")
    out["cases_by_f"] = grp("f")
    # bars not in signal (f==0) but long: excess fwd
    nonsig = A[(A["f"] == 0)].dropna(subset=["fwd"])
    nonsig = nonsig[nonsig["pos"] % 84 == 0]
    out["grid_f0_long_vs_flat"] = nonsig.groupby(nonsig["a"] > 0).agg(n=("ex", "size"), ex=("ex", "mean")).round(4)
    # during the deep fall windows 12-14: allocation, forecast pos share
    out["fall_windows_alloc"] = A[A["wi"].isin([12, 13, 14])].groupby("coin").agg(
        in_mkt=("a", lambda x: (x > 0).mean()), alloc=("a", "mean"), fc_pos=("f", lambda x: (x > 0).mean())).round(3)
    # trades table durations
    T = pd.concat([t.assign(coin=c) for c in coins for w, t in data["trades"][c].items()])
    out["trade_duration_days"] = (T["duration_minutes"] / 1440).describe().round(2)
    return out
