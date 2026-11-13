def explore(data):
    import numpy as np, pandas as pd
    out = {}
    tr = []
    for c, ws in data["trades"].items():
        for w, df in ws.items():
            if df is None or len(df) == 0: continue
            d = df.copy(); d["coin"] = c; d["win"] = w
            tr.append(d)
    tr = pd.concat(tr, ignore_index=True)
    tr["dur_d"] = tr["duration_minutes"] / 1440.0
    tr["yr"] = pd.to_datetime(tr["entry_time"]).dt.year
    tr["ef"] = pd.cut(tr["entry_forecast"], [0, 1, 2.5, 5, 100])
    out["trades_by_entry_forecast"] = tr.groupby("ef", observed=True).agg(n=("dur_d", "size"), gross=("profit_loss_percent", "mean"),
        med=("profit_loss_percent", "median"), dur=("dur_d", "mean"))
    out["trades_by_year"] = tr.groupby("yr").agg(n=("dur_d", "size"), gross=("profit_loss_percent", "mean"),
        win=("profit_loss_percent", lambda x: (x > 0).mean()), dur=("dur_d", "mean"))
    # exit reason from bars: at exit bar, was regime unknown (vol rise) or forecast 0 in trending (ret20<=0)
    rows = []; daily = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r1 = cl.pct_change()
            vol20 = r1.rolling(20).std()
            vmed = vol20.rolling(100, min_periods=40).median()
            a = b["postRebalance_current_allocation"].fillna(0)
            inpos = a.abs() > 1e-6
            v = b["postRebalance_total_value"]
            br = v.pct_change()
            prev_in = inpos.shift(1, fill_value=False)
            ret20 = cl / cl.shift(20) - 1
            for i in range(1, len(b)):
                if prev_in.iloc[i] and not inpos.iloc[i]:
                    rows.append(dict(reg=b["regime"].iloc[i], r20pos=ret20.iloc[i] > 0))
                if prev_in.iloc[i]:
                    daily.append(dict(br=br.iloc[i], cr=r1.iloc[i], volhi=vol20.iloc[i-1] > vmed.iloc[i-1] if not np.isnan(vmed.iloc[i-1]) else np.nan,
                                      regexit=b["regime"].iloc[i]))
    E = pd.DataFrame(rows)
    out["exit_reason"] = E.groupby(["reg", "r20pos"]).size()
    D = pd.DataFrame(daily).dropna(subset=["br"])
    out["invested_days_by_next_regime"] = D.groupby("regexit")["br"].agg(["size", "mean", "std", "sum"])
    out["invested_days_by_sign"] = D.groupby(D["cr"] > 0)["br"].agg(["size", "mean", "sum"])
    q = D["br"].quantile([0.02, 0.98])
    out["tails"] = pd.Series({"sum_all": D["br"].sum(), "sum_worst2pct": D.loc[D["br"] <= q.iloc[0], "br"].sum(),
        "sum_best2pct": D.loc[D["br"] >= q.iloc[1], "br"].sum(), "n_worst2pct": (D["br"] <= q.iloc[0]).sum(),
        "share_worst_on_unknown_bar": (D.loc[D["br"] <= q.iloc[0], "regexit"] == "unknown").mean()})
    # Trades: losers' path; short trades exit cause
    tr["short"] = tr["dur_d"] <= 3.5
    out["short_vs_long_trades"] = tr.groupby("short").agg(n=("dur_d", "size"), gross=("profit_loss_percent", "mean"),
        sum=("profit_loss_percent", "sum"), exitf0=("exit_forecast", lambda x: (x.abs() < 1e-9).mean()))
    return out
