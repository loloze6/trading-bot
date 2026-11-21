import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    coins = list(bars.keys())
    G = []; A = []
    for c in coins:
        # coin normal 48h drift and usual move over all windows
        gr = []
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 48, 48)
            gr.append(cl[idx + 48] / cl[idx] - 1)
        gr = np.concatenate(gr); drift = gr.mean(); usual = gr.std()
        for w, b in bars[c].items():
            cl = b["close"]
            r1 = cl.pct_change()
            f = b["forecast"]
            fwd = cl.shift(-48) / cl - 1
            ret30 = cl / cl.shift(720) - 1
            ret7 = cl / cl.shift(168) - 1
            vr = r1.rolling(168).std() / r1.rolling(720).std()
            ret24 = cl / cl.shift(24) - 1
            df = pd.DataFrame({"f": f, "fwd": fwd - drift, "tot": fwd, "ret30": ret30, "ret7": ret7, "vr": vr,
                               "ret24": ret24, "alloc": b["postRebalance_current_allocation"],
                               "gain": b["postRebalance_current_allocation"] * (cl.shift(-1) / cl - 1)})
            df["coin"] = c; df["w"] = w
            g = df.iloc[np.arange(0, len(df), 48)]
            G.append(g); A.append(df)
    G = pd.concat(G).dropna(subset=["fwd", "ret30", "vr", "ret7"])
    A = pd.concat(A).dropna(subset=["gain", "ret30"])
    pos = G[G.f > 0].copy()
    # slope t of fwd on f, within ret30 terciles
    pos["t30"] = pd.qcut(pos.ret30, 3, labels=["down30", "mid30", "up30"])
    pos["t7"] = pd.qcut(pos.ret7, 3, labels=["down7", "mid7", "up7"])
    pos["tvr"] = pd.qcut(pos.vr, 3, labels=["calm", "mid", "agitated"])
    def slope(g):
        s = stats.linregress(g.f, g.fwd)
        return pd.Series({"n": len(g), "slope_bps_per_unit": s.slope * 1e4, "t": s.slope / s.stderr,
                          "mean_excess_bps": g.fwd.mean() * 1e4, "mean_total_bps": g.tot.mean() * 1e4})
    for k in ["t30", "t7", "tvr"]:
        out["slope_by_" + k] = pos.groupby(k).apply(slope)
    # flat (f==0) grid vs pos grid
    out["fwd_by_forecast_sign"] = G.assign(s=np.sign(G.f)).groupby("s").agg(n=("fwd", "size"), excess_bps=("fwd", lambda x: x.mean()*1e4), total_bps=("tot", lambda x: x.mean()*1e4))
    # f quintiles among pos
    pos["fq"] = pd.qcut(pos.f, 5, labels=False, duplicates="drop")
    out["fwd_by_f_quintile"] = pos.groupby("fq").agg(flo=("f", "min"), fhi=("f", "max"), n=("fwd", "size"),
        excess_bps=("fwd", lambda x: x.mean()*1e4), total_bps=("tot", lambda x: x.mean()*1e4))
    # book exposure and gain by 30d return tercile on all bars
    A["t30"] = pd.qcut(A.ret30, 5, labels=False)
    out["alloc_gain_by_ret30_quint_all"] = A.groupby("t30").agg(lo=("ret30","min"), hi=("ret30","max"),
        alloc=("alloc", "mean"), share_in=("alloc", lambda x: (x.abs() > 1e-6).mean()),
        gain_bps=("gain", lambda x: x.mean()*1e4), sd_gain_bps=("gain", lambda x: x.std()*1e4))
    # interaction: f quintile x ret30 sign
    pos["up30"] = pos.ret30 > 0
    out["excess_by_fq_and_trend"] = pos.groupby(["up30", "fq"]).agg(n=("fwd","size"), excess_bps=("fwd", lambda x: x.mean()*1e4)).unstack(0)
    return out
