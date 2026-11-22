import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    H = 84
    # normal drift per coin (non-overlapping 84-bar returns over all windows)
    drift = {}; usual = {}
    for c, ws in data["bars"].items():
        rs = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - H, H)
            rs += list(cl[idx + H] / cl[idx] - 1)
        drift[c] = np.mean(rs); usual[c] = np.std(rs)
    # cases: first active bet per 84-bar grid cell
    cases = []
    gains = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(cl)
            f = b["forecast"].values
            wn = int(w[1:])
            p30 = b["close"] / b["close"].shift(180) - 1
            p7 = b["close"] / b["close"].shift(42) - 1
            for g0 in range(0, n - H, H):
                seg = np.where(f[g0:g0 + H] != 0)[0]
                if len(seg) == 0: continue
                i = g0 + seg[0]
                if i + H >= n: continue
                r = cl[i + H] / cl[i] - 1
                cases.append(dict(coin=c, wn=wn, f=f[i], ex=r - drift[c], r=r,
                                  p30=p30.iloc[i], p7=p7.iloc[i]))
            a = b["postRebalance_current_allocation"].values
            rr = np.append(cl[1:] / cl[:-1] - 1, np.nan)
            gains.append(pd.DataFrame({"wn": wn, "coin": c, "g": a * rr, "side": np.sign(a)}))
    C = pd.DataFrame(cases)
    C["fs"] = np.sign(C["f"])
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["case_ex_by_sign"] = C.groupby("fs")["ex"].apply(tt).unstack().round(4)
    C["per"] = pd.cut(C["wn"], [0, 17, 24], labels=["w1-17", "w18-24"])
    out["case_ex_by_sign_period"] = C.groupby(["per", "fs"])["ex"].apply(tt).unstack().round(4)
    neg = C[C["fs"] < 0].dropna(subset=["p30"]).copy()
    neg["p30q"] = pd.qcut(neg["p30"], 3, labels=False)
    out["neg_cases_ex_by_prior30d_tercile"] = neg.groupby("p30q")["ex"].apply(tt).unstack().round(4)
    pos = C[C["fs"] > 0].dropna(subset=["p30"]).copy()
    pos["p30q"] = pd.qcut(pos["p30"], 3, labels=False)
    out["pos_cases_ex_by_prior30d_tercile"] = pos.groupby("p30q")["ex"].apply(tt).unstack().round(4)
    # slope of ex on f within positive cases only
    s = stats.linregress(pos["f"], pos["ex"])
    out["pos_slope"] = f"slope {s.slope:.5f} t {s.slope/s.stderr:.2f} n {len(pos)}"
    # bar gains by side, per window group
    G = pd.concat(gains).dropna()
    G["per"] = pd.cut(G["wn"], [0, 17, 20, 24], labels=["w1-17", "w18-20", "w21-24"])
    out["bar_gain_by_side_period"] = G.groupby(["per", "side"])["g"].agg(["count", "sum", "mean"]).round(5)
    # long-only book: daily-ish approx via bar gains, chained per coin-mean per bar index
    G["g_long"] = np.where(G["side"] > 0, G["g"], 0.0)
    out["sum_gain_long_only_vs_all_by_window_grp"] = G.groupby("per")[["g", "g_long"]].sum().round(3)
    return out
