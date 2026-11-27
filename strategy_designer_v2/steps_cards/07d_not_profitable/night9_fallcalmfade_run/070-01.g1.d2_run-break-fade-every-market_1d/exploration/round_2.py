def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].astype(float); allr.append((c.shift(-1)/c-1).dropna())
        drift = pd.concat(allr).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); r = c/c.shift(1)-1; nxt = c.shift(-1)/c-1
            run = np.zeros(len(df)); cnt = 0
            for i in range(len(df)):
                run[i] = cnt; cnt = cnt+1 if r.iloc[i] < 0 else 0
            rf = np.full(len(df), np.nan)
            for i in range(len(df)):
                k = int(run[i])
                if k > 0 and i-k-1 >= 0: rf[i] = c.iloc[i-1]/c.iloc[i-k-1]-1
            vol = r.rolling(20, min_periods=10).std()
            t20 = c/c.shift(20)-1
            t10 = c/c.shift(10)-1
            d = pd.DataFrame({"coin": coin, "w": w, "wn": int(w[1:]), "i": np.arange(len(df)),
                              "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                              "run": run, "isup": r > 0, "rf": rf, "vol": vol, "t20": t20, "t10": t10,
                              "nxt": nxt, "u": -(nxt-drift), "alloc": df["postRebalance_current_allocation"].astype(float)})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["case"] = A["isup"] & (A["run"] >= 2)
    A["case1"] = A["isup"] & (A["run"] == 1)
    out = {}
    C = A[A["case"]].copy()
    C["rfq"] = pd.qcut(C["rf"], 4, labels=["deep", "q2", "q3", "shallow"])
    C["t20s"] = np.where(C["t20"] < 0, "t20neg", "t20pos")
    out["u_by_rf_and_t20sign"] = C.dropna(subset=["t20", "rf"]).groupby(["t20s", "rfq"])["u"].agg(["count", "mean", "std"])
    # single-down-day breaks: rf grading too?
    C1 = A[A["case1"]].copy()
    C1["rfq"] = pd.qcut(C1["rf"], 4, labels=["deep", "q2", "q3", "shallow"])
    out["single_run_by_rf"] = C1.dropna(subset=["rf"]).groupby("rfq")["u"].agg(["count", "mean", "std"])
    # condition alone: non-case bars by t10 bucket
    N = A[~A["case"] & ~A["case1"]].copy()
    N["t10b"] = pd.cut(N["t10"], [-9, -0.15, -0.07, 0, 9])
    out["noncase_u_by_t10"] = N.dropna(subset=["t10"]).groupby("t10b")["u"].agg(["count", "mean", "std"])
    C["t10b"] = pd.cut(C["t10"], [-9, -0.15, -0.07, 0, 9])
    out["case_u_by_t10"] = C.dropna(subset=["t10"]).groupby("t10b")["u"].agg(["count", "mean", "std"])
    # variant books
    cost = 0.0019
    def book(sig):
        A2 = A.copy(); A2["pos"] = sig.fillna(0)
        A2["pnl"] = A2["pos"]*A2["nxt"] - cost*A2["pos"].abs()
        A2 = A2.dropna(subset=["nxt"])
        B = A2.groupby(["wn", "day"])["pnl"].mean().reset_index().sort_values(["wn", "day"])
        x = B["pnl"]; v = (1+x).cumprod(); dd = (v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(x))-1
        held = (A2["pos"] != 0).mean()
        return pd.Series({"sharpe": x.mean()/x.std()*np.sqrt(365), "yearly": yr, "maxdd": dd,
                          "calmar": yr/abs(dd), "mean_d": x.mean(), "held_share": held})
    sz = (0.382/np.sqrt(365)/A["vol"]).clip(upper=2)
    res = {}
    res["actual_alloc"] = book(A["alloc"].where(A["alloc"] != 0, 0)*0 + A["alloc"]) if False else None
    res["base_run2"] = book(-sz.where(A["case"], 0))
    res["t20neg"] = book(-sz.where(A["case"] & (A["t20"] < 0), 0))
    rfs = (-A["rf"]/0.10).clip(upper=2)
    res["rf_scaled"] = book(-(sz*rfs).where(A["isup"] & (A["run"] >= 1), 0))
    res["rf_scaled_run2"] = book(-(sz*rfs).where(A["case"], 0))
    res["rf_scaled_t20neg"] = book(-(sz*rfs).where(A["isup"] & (A["run"] >= 1) & (A["t20"] < 0), 0))
    res["rfdeep_only"] = book(-sz.where(A["isup"] & (A["rf"] < -0.076), 0))
    res = {k: v for k, v in res.items() if v is not None}
    out["variant_books"] = pd.DataFrame(res).T
    # holding book
    A2 = A.dropna(subset=["nxt"])
    H = A2.groupby(["wn", "day"])["nxt"].mean()
    out["holding_sharpe"] = float(H.mean()/H.std()*np.sqrt(365))
    # by window for rf_scaled
    A3 = A.copy(); A3["pos"] = -(sz*rfs).where(A["isup"] & (A["run"] >= 1), 0).fillna(0)
    A3["pnl"] = A3["pos"]*A3["nxt"] - cost*A3["pos"].abs()
    out["rf_scaled_by_window"] = A3.dropna(subset=["nxt"]).groupby(["wn", "day"])["pnl"].mean().groupby(level=0).sum()
    return out
