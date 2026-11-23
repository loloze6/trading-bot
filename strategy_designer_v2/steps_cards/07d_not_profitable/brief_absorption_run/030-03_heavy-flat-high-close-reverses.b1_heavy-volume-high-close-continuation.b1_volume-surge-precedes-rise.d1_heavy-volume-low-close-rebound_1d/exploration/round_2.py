def explore(data):
    import pandas as pd, numpy as np
    out = {}
    br = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            b["coin"] = c; b["wn"] = int(w[1:])
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["ret60"] = b["close"] / b["close"].shift(60) - 1
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["pos"] = np.arange(len(b))
            b["ad"] = b["previous_allocation"].abs() if "previous_allocation" in b else np.nan
            # hold signal for 10 days: max forecast over last 10 bars
            b["fc10"] = b["forecast"].rolling(10, min_periods=1).max()
            b["dn60"] = (b["ret60"] < 0).astype(float)
            b["dn20"] = (b["ret20"] < 0).astype(float)
            br.append(b)
    A = pd.concat(br, ignore_index=True)
    al = A["postRebalance_current_allocation"]
    sv = A["sizing_target_allocation"]
    out["alloc_vs_forecast_corr"] = pd.Series({"corr_alloc_fc": al.corr(A["forecast"]),
        "corr_alloc_fc10": al.corr(A["fc10"]), "mean_alloc_fc10_lt1": al[A["fc10"] < 1].mean(),
        "share_fc10_lt1": (A["fc10"] < 1).mean(), "mean_target_alloc": sv.mean()})
    # variants: daily gain series pooled by (wn, timestamp) mean over coins
    vol = A.groupby(["coin", "wn"])["r1"].transform(lambda x: x.rolling(60, min_periods=20).std() * np.sqrt(365))
    scale = (0.382 / vol).clip(upper=2)
    A["v_actual"] = al * A["r1"]
    A["v_hold"] = A["r1"]
    A["v_fc"] = (A["fc10"] / 20).clip(0, 1) * scale * A["r1"]
    A["v_fc_dn60"] = (A["fc10"] / 20).clip(0, 1) * scale * A["dn60"] * A["r1"]
    A["v_fc_up60"] = (A["fc10"] / 20).clip(0, 1) * scale * (1 - A["dn60"]) * A["r1"]
    A["v_fc_ge10"] = (A["fc10"] >= 10).astype(float) * scale * A["r1"]
    A["inpos_fc"] = (A["fc10"] > 0.5).astype(float)
    A["t"] = A["timestamp"].astype(str)
    res = {}
    for v in ["v_actual", "v_hold", "v_fc", "v_fc_dn60", "v_fc_up60", "v_fc_ge10"]:
        S = A.dropna(subset=[v]).groupby(["wn", "t"])[v].mean().sort_index()
        val = (1 + S).cumprod()
        dd = (val / val.cummax() - 1).min()
        yr = val.iloc[-1] ** (365 / len(S)) - 1
        res[v] = {"sharpe": S.mean() / S.std() * np.sqrt(365), "yearly": yr, "maxdd": dd,
                  "calmar": yr / abs(dd), "mean": S.mean()}
    out["variants"] = pd.DataFrame(res).T.round(4)
    # in deepest drawdown: allocation and forecast state
    S = A.groupby(["wn", "t"]).agg(g=("v_actual", "mean"), fc=("forecast", "mean"),
                                   al=("postRebalance_current_allocation", "mean"),
                                   r=("r1", "mean"), dn=("dn60", "mean")).dropna().sort_index()
    val = (1 + S["g"]).cumprod(); dd = val / val.cummax() - 1
    S["indd"] = np.where(dd < -0.3, "dd>30%", "other")
    out["state_in_falls"] = S.groupby("indd").agg(n=("g", "size"), mean_alloc=("al", "mean"),
        mean_fc=("fc", "mean"), share_dn60=("dn", "mean"), mean_coin_r=("r", "mean"), mean_gain=("g", "mean")).round(4)
    # grid check, ge10 x dn60 by window halves for stability
    drift = A[A["pos"] % 10 == 0].groupby("coin").apply(
        lambda x: (x["close"].shift(-1)).mean() * 0)  # placeholder
    G = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            f = b["close"].shift(-10) / b["close"] - 1
            r60 = b["close"] / b["close"].shift(60) - 1
            g = pd.DataFrame({"coin": c, "wn": int(w[1:]), "f": f, "r60": r60, "fc": b["forecast"]}).iloc[::10]
            G.append(g)
    G = pd.concat(G).dropna()
    G["ex"] = G["f"] - G.groupby("coin")["f"].transform("mean")
    G["half"] = np.where(G["wn"] <= 12, "w1-12", "w13-24")
    G["dn"] = np.where(G["r60"] < 0, "down60", "up60")
    G["s"] = np.where(G["fc"] >= 10, "fc>=10", "fc<10")
    out["grid_half"] = G.groupby(["s", "dn", "half"])["ex"].agg(["size", "mean"]).round(4)
    G["r60q"] = pd.qcut(G["r60"], 4, labels=["q1low", "q2", "q3", "q4high"])
    out["grid_r60q"] = G.groupby(["s", "r60q"], observed=True)["ex"].agg(["size", "mean"]).round(4)
    return out
