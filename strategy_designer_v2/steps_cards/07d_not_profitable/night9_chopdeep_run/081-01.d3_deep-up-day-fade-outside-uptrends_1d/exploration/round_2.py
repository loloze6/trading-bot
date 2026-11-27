def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=20).std()
            hi20 = c.rolling(20, min_periods=20).max()
            depth = (c / hi20 - 1) / sd20
            tr60 = c / c.shift(60) - 1
            sd30 = r1.rolling(30, min_periods=30).std()
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "r1": r1, "depth": depth, "tr60": tr60, "sd30": sd30, "sd20": sd20,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "prev": b["previous_allocation"].astype(float),
                "f1": c.shift(-1) / c - 1,
            })
            # agitation proxy inside window: sd30 vs expanding median of sd30 within window
            df["agit"] = (sd30 > sd30.expanding(30).median()).astype(float)
            df.loc[sd30.isna(), "agit"] = np.nan
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    dr = A.groupby("coin")["f1"].mean()
    A["u1"] = -(A["f1"] - A["coin"].map(dr))
    A["pnl"] = A["alloc"] * A["f1"]
    A["fee_turn"] = (A["alloc"] - A["prev"]).abs()
    def summ(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    held = A[A["alloc"].abs() > 1e-9]
    out["held bars: signal on vs off"] = pd.DataFrame({
        "on": pd.Series({"n": (held["fc"] < 0).sum(), "pnl%": 100 * held[held["fc"] < 0]["pnl"].mean(), "abs_alloc": held[held["fc"] < 0]["alloc"].abs().mean(), "turn": held[held["fc"] < 0]["fee_turn"].mean()}),
        "off": pd.Series({"n": (held["fc"] >= 0).sum(), "pnl%": 100 * held[held["fc"] >= 0]["pnl"].mean(), "abs_alloc": held[held["fc"] >= 0]["alloc"].abs().mean(), "turn": held[held["fc"] >= 0]["fee_turn"].mean()})})
    # pnl net of approximate cost 0.11% per unit turnover side
    A["net"] = A["pnl"] - 0.0011 * A["fee_turn"]
    act = A[A["fc"] < 0].copy()
    act["dq"] = pd.qcut(act["fc"], 5, labels=False)
    out["book pnl by fc quintile (0 deepest), per active bar"] = act.groupby("dq").agg(n=("pnl", "size"), gross_pnl_bp=("pnl", lambda x: 1e4 * x.mean()), net_pnl_bp=("net", lambda x: 1e4 * x.mean()), abs_alloc=("alloc", lambda x: x.abs().mean()), turn=("fee_turn", "mean"))
    out["book pnl on held off-signal bars"] = pd.Series({"gross_bp": 1e4 * held[held["fc"] >= 0]["pnl"].mean(), "net_bp": 1e4 * A[(A["alloc"].abs() > 1e-9) & (A["fc"] >= 0)]["net"].mean(), "sum_share_of_total_gross": held[held["fc"] >= 0]["pnl"].sum() / A["pnl"].sum()})
    # condition-alone checks for agitation
    cand = A[(A["r1"] > 0) & (A["tr60"] <= 0.10)].dropna(subset=["u1", "depth", "agit"]).copy()
    cand["deep"] = cand["depth"] < cand["depth"].median()
    out["up days outside rising: depth half x agitation, unusual short"] = cand.groupby(["deep", "agit"]).apply(lambda g: summ(g["u1"]))
    allb = A.dropna(subset=["u1", "agit"])
    out["all bars by agitation (condition alone, no signal)"] = allb.groupby("agit").apply(lambda g: summ(g["u1"]))
    dn = A[(A["r1"] <= 0) & (A["tr60"] <= 0.10)].dropna(subset=["u1", "depth"]).copy()
    dn["deep"] = dn["depth"] < cand["depth"].median()
    out["down days outside rising by depth half"] = dn.groupby("deep").apply(lambda g: summ(g["u1"]))
    # depth deepest third x agit inside active
    act2 = act.dropna(subset=["agit"]).copy()
    act2["deep3"] = pd.qcut(act2["fc"], 3, labels=["deep", "mid", "shallow"])
    out["active: depth tercile x agit, unusual short"] = act2.groupby(["deep3", "agit"]).apply(lambda g: summ(g["u1"]))
    # worst book days: pnl on the coin days in the worst 5% of pnl
    hp = held.dropna(subset=["pnl"])
    lo = hp["pnl"] < hp["pnl"].quantile(0.02)
    out["worst 2% held bars vs rest"] = pd.DataFrame({"worst": hp[lo][["fc", "depth", "r1", "tr60", "agit", "sd20"]].mean(), "rest": hp[~lo][["fc", "depth", "r1", "tr60", "agit", "sd20"]].mean()})
    out["worst 2% share of total gross pnl"] = hp[lo]["pnl"].sum() / hp["pnl"].sum()
    return out
