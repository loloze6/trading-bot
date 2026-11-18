import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True).copy()
            r = b["close"].pct_change()
            s20 = r.rolling(20).std()
            vr = s20 / s20.rolling(60).mean()
            ret20 = b["close"] / b["close"].shift(20) - 1
            vol20 = s20 * np.sqrt(20)
            nxt = b["close"].shift(-1) / b["close"] - 1
            pos = b["postRebalance_current_allocation"]
            prev = b["previous_allocation"]
            net = b["total_portfolio_value"].shift(-1) / b["total_portfolio_value"] - 1
            df = pd.DataFrame({"coin": c, "w": w, "wn": int(w[1:]), "i": np.arange(len(b)), "pos": pos,
                               "dpos": (pos - prev).abs(), "nxt": nxt, "net": net, "r": r, "vr": vr,
                               "ret20": ret20, "tz": ret20 / vol20, "regime": b["regime"]})
            rows.append(df.iloc[:-1])
    d = pd.concat(rows).dropna(subset=["nxt", "net"])
    d["gross"] = d["pos"] * d["nxt"]
    fee = d["gross"] - d["net"]
    rate = fee.sum() / d["dpos"].sum()
    out["fee_rate_per_unit_turnover"] = float(rate)

    def book(df, posc):
        g = df.copy()
        g["p"] = posc
        g = g.sort_values(["coin", "wn", "i"])
        g["dp"] = g.groupby(["coin", "w"])["p"].diff().abs().fillna(g["p"].abs())
        g["n2"] = g["p"] * g["nxt"] - rate * g["dp"]
        p = g.groupby(["wn", "i"])["n2"].mean().sort_index()
        sh = p.mean() / p.std() * np.sqrt(365)
        eq = (1 + p).cumprod().values
        dd = (eq / np.maximum.accumulate(eq) - 1).min()
        yr = eq[-1] ** (365 / len(p)) - 1
        return pd.Series({"sharpe": sh, "mean": p.mean(), "maxdd": dd, "calmar": yr / -dd})

    hold = d.groupby(["wn", "i"])["nxt"].mean()
    out["hold_sharpe"] = float(hold.mean() / hold.std() * np.sqrt(365))
    eqh = (1 + hold.sort_index()).cumprod().values
    out["hold_maxdd"] = float((eqh / np.maximum.accumulate(eqh) - 1).min())
    v = {}
    v["actual_recomputed"] = book(d, d["pos"].values)
    v["scale_by_(vr-1)x2"] = book(d, (d["pos"] * (2 * (d["vr"] - 1)).clip(0, 2)).values)
    v["scale_by_abs_tz/2"] = book(d, (d["pos"] * (d["tz"].abs() / 2).clip(0, 2)).values)
    v["drop_shorts_when_tz>0"] = book(d, np.where((d["pos"] < 0) & (d["tz"] > 0), 0, d["pos"]))
    v["both"] = book(d, (d["pos"] * (2 * (d["vr"] - 1)).clip(0, 2) * (d["tz"].abs() / 2).clip(0, 2)).values)
    out["variants"] = pd.DataFrame(v).T

    # drawdown composition
    p = d.groupby(["wn", "i"])["net"].mean().sort_index()
    eq = (1 + p).cumprod().values
    ddv = eq / np.maximum.accumulate(eq) - 1
    tr = int(np.argmin(ddv)); pk = int(np.argmax(eq[:tr + 1]))
    idx = p.index[pk:tr + 1]
    dd = d.set_index(["wn", "i"]).loc[lambda x: x.index.isin(idx)].reset_index()
    dd["side"] = np.sign(dd["pos"]).map({1: "long", -1: "short", 0: "flat"})
    dd["tzs"] = np.sign(dd["tz"]).map({1: "up20", -1: "down20", 0: "z"})
    out["dd_by_side_trend"] = dd.groupby(["side", "tzs"]).agg(n=("net", "size"), sum_net=("net", "sum"),
                                                             mean_net=("net", "mean"), vr=("vr", "mean"),
                                                             abspos=("pos", lambda x: x.abs().mean()))
    out["dd_hold_return_mean"] = float(dd["nxt"].mean())
    a = d[d["pos"] != 0].copy()
    a["tz_q"] = pd.qcut(a["tz"], 5, labels=False)
    a["side"] = np.sign(a["pos"])
    out["active_by_tz_q_side"] = a.groupby(["tz_q", "side"]).agg(n=("net", "size"), mean_net=("net", "mean"),
        t=("gross", lambda x: x.mean() / x.std() * np.sqrt(len(x))), tz=("tz", "mean"))
    a["vrq"] = pd.qcut(a["vr"], 4, labels=False)
    out["active_vrq_mean_vr_turnover"] = a.groupby("vrq").agg(vr=("vr", "mean"), dpos=("dpos", "mean"),
        gross=("gross", "mean"), net=("net", "mean"))
    return out
