def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    coin = list(data["bars"].keys())[0]
    allb = []
    for w, b in data["bars"][coin].items():
        b = b.copy()
        b["nr"] = b["close"].shift(-1) / b["close"] - 1
        b["cr"] = b["close"] / b["close"].shift(1) - 1
        b["nlr"] = b["close"].shift(-1) / b["open"].shift(-1) - 1
        b["gap"] = b["open"].shift(-1) / b["close"] - 1
        b["raw"] = b["debug_info.components.sma_cross_spread.last_history_value"]
        b["inst"] = b["forecast"] > 0
        b["w"] = w
        ts = pd.to_datetime(b["timestamp"])
        b["year"] = ts.dt.year
        b["wd"] = ts.dt.weekday
        grp = (b["inst"] != b["inst"].shift()).cumsum()
        b["age"] = b.groupby(grp).cumcount()
        b["past20"] = b["close"] / b["close"].shift(20) - 1
        allb.append(b.dropna(subset=["nr"]))
    a = pd.concat(allb)
    def summ(g):
        return pd.Series({"n": len(g), "mean": g["nr"].mean(), "up": (g["nr"] > 0).mean(),
                          "sd": g["nr"].std(), "med": g["nr"].median()})
    out = {}
    out["by_window_inst"] = a.groupby(["w", "inst"]).apply(summ)
    out["by_year_inst"] = a.groupby(["year", "inst"]).apply(summ)
    ins = a[a.inst].copy()
    ins["fq"] = pd.qcut(ins["forecast"].rank(method="first"), 4, labels=False)
    out["inst_by_forecast_q"] = ins.groupby("fq").apply(summ)
    ins["ageq"] = pd.cut(ins["age"], [-1, 10, 30, 60, 1000])
    out["inst_by_age"] = ins.groupby("ageq").apply(summ)
    out["raw_pos_fc0"] = summ(a[(a.raw > 0) & (~a.inst)])
    out["raw_neg"] = summ(a[a.raw <= 0])
    out["inst_by_wd"] = ins.groupby("wd").apply(summ)
    a["p20"] = np.sign(a["past20"])
    out["by_inst_past20sign"] = a.groupby(["inst", "p20"]).apply(summ)
    out["samebar_by_inst"] = a.groupby("inst")["cr"].agg(["mean", "count"])
    out["gap_and_intrabar_next"] = a.groupby("inst")[["gap", "nlr"]].mean()
    out["t_ins_vs_out"] = float(stats.ttest_ind(a[a.inst]["nr"], a[~a.inst]["nr"], equal_var=False).statistic)
    out["ret_quantiles_inst"] = a.groupby("inst")["nr"].quantile([0.05, 0.25, 0.5, 0.75, 0.95]).unstack()
    out["corr_fc_nr_inst"] = float(ins[["forecast", "nr"]].corr().iloc[0, 1])
    t = data["trades"][coin]
    out["trades_cols"] = ", ".join(map(str, list(t.values())[0].columns)) if len(t) else "none"
    out["trades_n"] = int(sum(len(x) for x in t.values()))
    return out
