def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    allb = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["nxt"] = b["close"].shift(-1) / b["close"] - 1
            b["prev"] = b["close"] / b["close"].shift(1) - 1
            b["oc_next"] = b["close"].shift(-1) / b["open"].shift(-1) - 1
            b["gap_next"] = b["open"].shift(-1) / b["close"] - 1
            b["raw"] = b["debug_info.components.sma_cross_spread.last_history_value"]
            b["inst"] = b["forecast"] > 0
            b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            # run position
            r = (b["inst"] != b["inst"].shift()).cumsum()
            b["runpos"] = b.groupby(r).cumcount()
            allb.append(b)
            i = b[b.inst]["nxt"].dropna(); o = b[~b.inst]["nxt"].dropna()
            rows.append(dict(win=w, n_in=len(i), n_out=len(o), mean_in=i.mean(), mean_out=o.mean(),
                             up_in=(i > 0).mean() if len(i) else np.nan, up_out=(o > 0).mean() if len(o) else np.nan,
                             raw_pos_share=(b["raw"] > 0).mean(), coin_ret=b.close.iloc[-1]/b.close.iloc[0]-1))
    A = pd.concat(allb)
    out["per_window"] = pd.DataFrame(rows)
    A = A.dropna(subset=["nxt"])
    out["by_year"] = A.groupby(["year", "inst"])["nxt"].agg(["count", "mean", lambda x: (x > 0).mean()])
    fi = A[A.inst]
    fi = fi.assign(fbin=pd.qcut(fi["forecast"], 4, duplicates="drop"))
    out["in_by_forecast_q"] = fi.groupby("fbin")["nxt"].agg(["count", "mean", "median", lambda x: (x > 0).mean()])
    # raw>0 but forecast 0 vs raw<=0
    A["grp"] = np.where(A.inst, "fc>0", np.where(A.raw > 0, "raw>0,fc=0", "raw<=0"))
    out["by_grp"] = A.groupby("grp")[["nxt", "prev", "oc_next", "gap_next"]].mean()
    out["by_grp_n"] = A.groupby("grp")["nxt"].agg(["count", "std", lambda x: (x > 0).mean()])
    out["in_runpos"] = A[A.inst].assign(rp=pd.cut(A[A.inst].runpos, [-1, 5, 20, 60, 1000])).groupby("rp")["nxt"].agg(["count", "mean", lambda x: (x > 0).mean()])
    # distribution: in-stretch next returns quantiles vs out
    out["quantiles"] = A.groupby("inst")["nxt"].quantile([0.05, 0.25, 0.5, 0.75, 0.95]).unstack()
    t = stats.ttest_ind(A[A.inst].nxt, A[~A.inst].nxt, equal_var=False)
    out["welch"] = f"t={t.statistic:.2f}"
    # same-bar return in vs out
    out["samebar"] = A.groupby("inst")["prev"].agg(["mean", lambda x: (x > 0).mean()])
    return out
