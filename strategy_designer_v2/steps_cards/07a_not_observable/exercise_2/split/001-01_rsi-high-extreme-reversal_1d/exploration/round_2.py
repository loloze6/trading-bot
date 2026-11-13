def explore(data):
    import numpy as np, pandas as pd
    out = {}
    b = data["bars"]["BTCUSD"]["w1"].reset_index(drop=True)
    f = b["forecast"].astype(float)
    rsi = 50 - b["debug_info.components.rsi_high.last_history_value"].astype(float)
    cl = b["close"].astype(float)
    fwd = cl.shift(-5)/cl - 1
    base = fwd.mean()
    ext = f <= -10
    # cases per grid offset
    offs = []
    for o in range(5):
        g = np.arange(o, len(b), 5)
        m = ext.iloc[g] & fwd.iloc[g].notna()
        ex = (fwd.iloc[g][m] - base)
        offs.append({"offset": o, "cases": int(m.sum()), "mean_excess": ex.mean(),
                     "std_excess": ex.std(), "t": ex.mean()/(ex.std()/np.sqrt(len(ex))) if len(ex) > 1 else np.nan})
    out["by_grid_offset"] = pd.DataFrame(offs)
    # episodes: length, rsi at peak, excess fwd from episode start
    st = ext & ~ext.shift(1, fill_value=False)
    ep = []
    idx = list(np.where(st)[0])
    for i in idx:
        j = i
        while j < len(b) and ext.iloc[j]:
            j += 1
        ep.append({"length_bars": j - i, "rsi_max": rsi.iloc[i:j].max(),
                   "excess_fwd5_start": fwd.iloc[i] - base, "fc_min": f.iloc[i:j].min()})
    out["episodes"] = pd.DataFrame(ep)
    out["all_ext_bars_excess"] = pd.Series({"n": int((ext & fwd.notna()).sum()),
        "mean": (fwd[ext] - base).mean(), "std": (fwd[ext] - base).std()})
    out["bars_before_forecast_possible"] = pd.Series({"first_nonzero_fc": int(np.argmax(f.values != 0)),
        "rsi_gt50_bars_before_34": int((rsi.iloc[:34] > 50).sum())})
    out["fwd5_by_rsi_bin"] = pd.DataFrame({"rsi_bin": pd.cut(rsi, [30,45,50,52,55,60]), "fwd": fwd - base}).groupby("rsi_bin", observed=True)["fwd"].agg(["count", "mean", "std"])
    out["coin_return_window"] = cl.iloc[-1]/cl.iloc[0] - 1
    return out
