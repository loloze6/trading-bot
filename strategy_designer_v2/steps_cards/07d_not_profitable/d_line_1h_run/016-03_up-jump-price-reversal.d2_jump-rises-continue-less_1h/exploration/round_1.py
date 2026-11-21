def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    allb = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["fwd72"] = b["close"].shift(-72) / b["close"] - 1
            b["past72"] = b["close"] / b["close"].shift(72) - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gross"] = b["pos"] * b["ret1"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["turn"] = (b["pos"] - b["previous_allocation"]).abs()
            b["coin"] = coin; b["win"] = w
            b["idx"] = np.arange(len(b))
            allb.append(b[["coin","win","idx","ret1","fwd72","past72","pos","gross","fee","turn","forecast",
                           "debug_info.components.grind.last_history_value",
                           "debug_info.components.grind.post_pipeline_value"]])
    A = pd.concat(allb, ignore_index=True)
    A = A.rename(columns={"debug_info.components.grind.last_history_value":"raw",
                          "debug_info.components.grind.post_pipeline_value":"post"})
    g = A.groupby("coin")
    out["per_coin_hourly"] = pd.DataFrame({
        "gross_mean_bp": g["gross"].mean()*1e4,
        "fee_mean_bp": g["fee"].mean()*1e4,
        "pos_mean": g["pos"].mean(),
        "share_in": g["pos"].apply(lambda s: (s.abs()>1e-6).mean()),
        "turn_per_day": g["turn"].mean()*24,
        "coin_ret_bp": g["ret1"].mean()*1e4,
        "mkt_part_bp": g["pos"].mean()*g["ret1"].mean()*1e4,
    })
    # forecast / raw relation
    out["forecast_desc"] = A[["raw","post","forecast","pos"]].describe().T
    out["corr_raw_post"] = float(A[["raw","post"]].corr().iloc[0,1])
    # gross by state: risen vs not
    A["risen"] = A["past72"] > 0
    out["by_risen"] = A.groupby("risen").agg(n=("gross","size"), pos=("pos","mean"),
        gross_bp=("gross", lambda s: s.mean()*1e4), coin_bp=("ret1", lambda s: s.mean()*1e4))
    # grid: fwd72 by raw bucket and by post bucket on risen bars
    G = A[(A["idx"] % 72 == 0) & A["risen"] & A["fwd72"].notna()].copy()
    G["rawq"] = pd.qcut(G["raw"], 5, labels=False, duplicates="drop")
    out["grid_by_rawq"] = G.groupby("rawq").agg(n=("fwd72","size"), fwd72=("fwd72","mean"),
                                                 pos=("pos","mean"), post=("post","mean"))
    G["postq"] = pd.qcut(G["post"].rank(method="first"), 5, labels=False)
    out["grid_by_postq"] = G.groupby("postq").agg(n=("fwd72","size"), fwd72=("fwd72","mean"),
                                                   raw=("raw","mean"), pos=("pos","mean"))
    # all grid bars by pos bucket
    H = A[(A["idx"] % 72 == 0) & A["fwd72"].notna()].copy()
    H["posq"] = pd.cut(H["pos"], [-0.01,1e-6,0.5,1,1.5,2.5])
    out["grid_by_pos"] = H.groupby("posq").agg(n=("fwd72","size"), fwd72=("fwd72","mean"), risen=("risen","mean"))
    # days
    d = []
    for coin in data["days"]:
        for w, x in data["days"][coin].items():
            x = x.copy(); x["win"] = w; d.append(x)
    D = pd.concat(d)
    dd = D.groupby(["win","day"])[["book_return","coin_return"]].mean().reset_index()
    out["by_window"] = dd.groupby("win").agg(book=("book_return","mean"), coin=("coin_return","mean")).T
    return out
