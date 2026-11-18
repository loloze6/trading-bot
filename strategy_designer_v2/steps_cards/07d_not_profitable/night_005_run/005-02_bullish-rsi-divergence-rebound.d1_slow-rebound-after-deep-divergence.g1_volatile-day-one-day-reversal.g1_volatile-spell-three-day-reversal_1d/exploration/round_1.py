import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    coins = list(data["bars"].keys())
    rows = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True).copy()
            r = b["close"].pct_change()
            s20 = r.rolling(20).std()
            vr = s20 / s20.rolling(60).mean()
            ret20 = b["close"] / b["close"].shift(20) - 1
            ret5 = b["close"] / b["close"].shift(5) - 1
            nxt = b["close"].shift(-1) / b["close"] - 1
            pos = b["postRebalance_current_allocation"]
            net = b["total_portfolio_value"].shift(-1) / b["total_portfolio_value"] - 1
            df = pd.DataFrame({"coin": c, "w": w, "pos": pos, "nxt": nxt, "gross": pos * nxt, "net": net,
                               "r": r, "vr": vr, "ret20": ret20, "ret5": ret5, "fc": b["forecast"],
                               "regime": b["regime"], "i": np.arange(len(b))})
            rows.append(df.iloc[:-1])
    d = pd.concat(rows)
    d = d.dropna(subset=["nxt", "net"])
    mu = d.groupby("coin")["nxt"].mean()
    d["mu"] = d["coin"].map(mu)
    d["mkt"] = d["pos"] * d["mu"]
    d["timing"] = d["gross"] - d["mkt"]
    d["side"] = np.sign(d["pos"]).map({1: "long", -1: "short", 0: "flat"})
    def summ(g):
        return pd.Series({"n": len(g), "mean_net": g["net"].mean(), "sum_net": g["net"].sum(),
                          "mean_gross": g["gross"].mean(), "mean_timing": g["timing"].mean(),
                          "t_gross": g["gross"].mean() / (g["gross"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "mean_abs_pos": g["pos"].abs().mean()})
    out["by_side"] = d.groupby("side").apply(summ)
    out["by_coin"] = d.groupby("coin").apply(lambda g: pd.Series({
        "sharpe_book": g["net"].mean() / g["net"].std() * np.sqrt(365),
        "sharpe_hold": g["nxt"].mean() / g["nxt"].std() * np.sqrt(365),
        "mean_net": g["net"].mean(), "mkt": g["mkt"].mean(), "timing": g["timing"].mean()}))
    a = d[d["side"] != "flat"].copy()
    a["trend_q"] = pd.qcut(a["ret20"], 5, labels=False, duplicates="drop")
    out["active_by_ret20_quintile_x_side"] = a.groupby(["trend_q", "side"]).apply(summ)
    a["vr_q"] = pd.qcut(a["vr"], 4, labels=False, duplicates="drop")
    out["active_by_volratio_q"] = a.groupby("vr_q").apply(summ)
    a["fc_q"] = pd.qcut(a["fc"].abs(), 3, labels=False, duplicates="drop")
    out["active_by_absfc_tercile"] = a.groupby(["fc_q", "side"]).apply(summ)
    out["flat_share"] = float((d["side"] == "flat").mean())
    out["fee_drag_mean"] = float((d["gross"] - d["net"]).mean())
    # portfolio drawdown
    p = d.groupby(["w", "i"])["net"].mean().reset_index()
    p["wn"] = p["w"].str[1:].astype(int)
    p = p.sort_values(["wn", "i"])
    eq = (1 + p["net"]).cumprod().values
    peak = np.maximum.accumulate(eq)
    dd = eq / peak - 1
    trough = int(np.argmin(dd)); pk = int(np.argmax(eq[:trough + 1]))
    out["max_dd"] = float(dd.min())
    out["dd_span_days"] = trough - pk
    out["dd_windows"] = ",".join(p.iloc[pk:trough + 1]["w"].unique())
    # per window book return vs hold
    pw = d.groupby("w").agg(net=("net", "sum"), hold=("nxt", "mean"), longshare=("pos", lambda x: (x > 0).mean()),
                           shortshare=("pos", lambda x: (x < 0).mean()))
    pw["hold"] = d.groupby("w")["nxt"].sum() / d.groupby("w")["coin"].nunique()
    pw["net"] = pw["net"] / d.groupby("w")["coin"].nunique()
    out["per_window"] = pw.sort_values("net")
    return out
