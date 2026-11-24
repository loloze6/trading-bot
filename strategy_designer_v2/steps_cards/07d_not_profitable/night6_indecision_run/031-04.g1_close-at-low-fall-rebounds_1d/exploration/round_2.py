def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r = c.pct_change()
            sd20 = r.rolling(20, min_periods=20).std()
            b["z"] = r / sd20.shift(1)
            b["nxt"] = c.shift(-1) / c - 1
            b["ret5"] = c / c.shift(5) - 1
            b["ret5z"] = b["ret5"] / (sd20.shift(1) * np.sqrt(5))
            b["ret5prev"] = c.shift(1) / c.shift(6) - 1
            b["ret5prevz"] = b["ret5prev"] / (sd20.shift(1) * np.sqrt(5))
            b["cl"] = (b["high"] - c) / (b["high"] - b["low"])
            b["prevz"] = b["z"].shift(1)
            b["coin"] = coin; b["win"] = int(w[1:])
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    drift = B.groupby("coin")["nxt"].mean()
    B["ex"] = B["nxt"] - B["coin"].map(drift)
    B["case"] = B["regime"] == "mean_reversion"
    B["gain"] = B["postRebalance_current_allocation"] * B["nxt"]
    V = B.dropna(subset=["nxt", "ret5prevz"]).copy()
    def summ(g):
        return pd.Series({"n": len(g), "mean_ex": g["ex"].mean(),
                          "t_ex": stats.ttest_1samp(g["ex"], 0).statistic if len(g) > 2 else np.nan,
                          "mean_gain": g["gain"].mean(), "alloc": g["postRebalance_current_allocation"].mean()})
    # prior run before today (5-day return up to yesterday, in vol units)
    edges = [-np.inf, -2, -1, 0, 1, np.inf]
    V["runq"] = pd.cut(V["ret5prevz"], edges)
    out["cases_by_prior_run_z"] = V[V["case"]].groupby("runq").apply(summ)
    out["noncases_by_prior_run_z"] = V[~V["case"]].groupby("runq").apply(summ)
    # condition alone: prior sharp down day without today's sharp fall
    out["prevsharp_noncase"] = V[(~V["case"]) & (V["prevz"] < -1)].pipe(summ)
    out["prevsharp_noncase_z_lt_minus2"] = V[(~V["case"]) & (V["prevz"] < -2)].pipe(summ)
    # interaction: prior run x close location within cases
    C = V[V["case"]].copy()
    C["run_down"] = C["ret5prevz"] < -1
    C["cl_hi"] = C["cl"] > C["cl"].median()
    out["cases_run_x_cl"] = C.groupby(["run_down", "cl_hi"]).apply(summ)
    # graded slope within run-down cases
    for k, g in C.groupby("run_down"):
        s = stats.linregress(g["cl"], g["ex"])
        out[f"slope_cl_rundown_{k}"] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(g)}"
    s = stats.linregress(C["ret5prevz"], C["ex"])
    out["slope_ex_on_prior_run_z"] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(C)}"
    # by year for run_down cases
    out["rundown_cases_by_year"] = C[C["run_down"]].groupby("year").apply(summ)
    out["notrun_cases_by_year"] = C[~C["run_down"]].groupby("year").apply(summ)
    # simulated book share of gain from run-down cases
    out["gain_sum_by_run_down"] = C.groupby("run_down")["gain"].agg(["count", "sum", "mean", "std"])
    # nxt2..nxt5 path for run-down cases (longer horizon)
    return out
