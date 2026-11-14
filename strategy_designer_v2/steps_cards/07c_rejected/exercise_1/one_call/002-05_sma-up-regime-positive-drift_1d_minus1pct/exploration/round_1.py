def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    coin = list(data["bars"].keys())[0]
    rows = []
    allb = []
    for w, b in data["bars"][coin].items():
        b = b.copy()
        b["nr"] = b["close"].shift(-1) / b["close"] - 1
        b["raw"] = b["debug_info.components.sma_cross_spread.last_history_value"]
        b["inst"] = b["forecast"] > 0
        b["w"] = w
        b["year"] = pd.to_datetime(b["timestamp"]).dt.year
        b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
        # bars since stretch start
        grp = (b["inst"] != b["inst"].shift()).cumsum()
        b["age"] = b.groupby(grp).cumcount()
        b["past20"] = b["close"] / b["close"].shift(20) - 1
        allb.append(b.dropna(subset=["nr"]))
    a = pd.concat(allb)
    def summ(g):
        return pd.Series({"n": len(g), "mean": g["nr"].mean(), "up": (g["nr"] > 0).mean(), "sd": g["nr"].std()})
    out = {}
    out["by_window_inst"] = a.groupby(["w", "inst"]).apply(summ)
    out["by_year_inst"] = a.groupby(["year", "inst"]).apply(summ)
    ins = a[a.inst]
    ins = ins.assign(fq=pd.qcut(ins["forecast"].rank(method="first"), 4, labels=False))
    out["inst_by_forecast_q"] = ins.groupby("fq").apply(summ)
    ins = ins.assign(ageq=pd.cut(ins["age"], [-1, 10, 30, 60, 1000]))
    out["inst_by_age"] = ins.groupby("ageq").apply(summ)
    out["raw_pos_fc0"] = summ(a[(a.raw > 0) & (~a.inst)])
    out["raw_neg"] = summ(a[a.raw <= 0])
    out["inst_by_wd"] = ins.groupby("wd").apply(summ)
    a = a.assign(p20=np.sign(a["past20"]))
    out["by_inst_past20sign"] = a.groupby(["inst", "p20"]).apply(summ)
    # check same-bar return in-stretch
    a["cr"] = a.groupby("w")["close"].pct_change()
    out["samebar_by_inst"] = a.groupby("inst")["cr"].agg(["mean", "count"])
    # intrabar
    a["oc"] = a["close"] / a["open"] - 1
    out["oc_nextbar"] = a.groupby("inst")["nr"].describe()
    out["t_ins_vs_out"] = float(stats.ttest_ind(a[a.inst]["nr"], a[~a.inst]["nr"], equal_var=False).statistic)
    out["trades"] = pd.concat(data["trades"][coin].values())[["net_profit_loss_percent", "duration_minutes"]].describe()
    return out
