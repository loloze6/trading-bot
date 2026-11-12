def explore(data):
    import numpy as np, pandas as pd
    out = {}
    b = data["bars"]["BTCUSD"]["w1"].copy()
    raw = b["debug_info.components.sma_cross_spread.last_history_value"]
    post = b["debug_info.components.sma_cross_spread.post_pipeline_value"]
    f = b["forecast"]
    b["ret_next"] = b["close"].shift(-1) / b["close"] - 1
    out["n_bars"] = len(b)
    out["raw_spread_desc"] = raw.describe()
    out["forecast_desc"] = f.describe()
    out["share_raw_pos"] = float((raw > 0).mean())
    out["share_forecast_pos"] = float((f > 0).mean())
    out["share_post_pos"] = float((post > 0).mean())
    out["n_raw_pos_forecast_zero"] = int(((raw > 0) & (f <= 0)).sum())
    # runs of raw > 0
    s = (raw > 0).astype(int)
    runs = (s.diff().fillna(s.iloc[0]) != 0).cumsum()
    rl = s.groupby(runs).agg(["first", "size"])
    out["runs_sign_length"] = rl.rename(columns={"first": "raw_pos", "size": "len"}).reset_index(drop=True)
    # position of runs in window (bar index)
    idx = np.arange(len(b))
    out["first_raw_pos_bar"] = int(idx[raw.values > 0][0]) if (raw > 0).any() else -1
    out["first_f_pos_bar"] = int(idx[f.values > 0][0]) if (f > 0).any() else -1
    out["last_f_pos_bar"] = int(idx[f.values > 0][-1]) if (f > 0).any() else -1
    # raw spread by thirds of window
    b["third"] = pd.cut(idx, 3, labels=["t1", "t2", "t3"])
    out["raw_by_third"] = b.groupby("third")["debug_info.components.sma_cross_spread.last_history_value"].agg(["mean", "min", "max"])
    # returns
    g = np.where(f > 0, "in", "out")
    out["ret_by_group"] = b.groupby(g)["ret_next"].agg(["count", "mean", "std", lambda x: (x > 0).mean()])
    out["ret_std_all"] = float(b["ret_next"].std())
    out["coin_total_ret"] = float(b["close"].iloc[-1] / b["close"].iloc[0] - 1)
    out["n_trades"] = len(data["trades"]["BTCUSD"]["w1"])
    return out
