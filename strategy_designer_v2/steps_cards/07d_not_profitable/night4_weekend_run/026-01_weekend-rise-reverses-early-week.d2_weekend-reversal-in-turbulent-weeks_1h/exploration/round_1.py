import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = c; t["win"] = w
            tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    T["dur_h"] = T["duration_minutes"] / 60
    out["trades_by_coin"] = T.groupby("coin").agg(n=("side", "size"), short_share=("side", lambda s: (s == "SHORT").mean()),
        dur_h=("dur_h", "mean"), pnl=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        comm=("total_commission", "mean"))
    T["entry_wd"] = pd.to_datetime(T["entry_time"]).dt.weekday
    T["entry_hr"] = pd.to_datetime(T["entry_time"]).dt.hour
    out["trades_by_entry_wd"] = T.groupby("entry_wd").agg(n=("side", "size"), dur_h=("dur_h", "mean"),
        pnl=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    out["dur_quantiles"] = T["dur_h"].describe()
    # bar-level gain by position
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["g"] = b["pos"] * b["r1"]
            b["vr"] = b["postRebalance_total_value"].shift(-1) / b["postRebalance_total_value"] - 1
            ts = pd.to_datetime(b["timestamp"])
            b["wd"] = ts.dt.weekday; b["hr"] = ts.dt.hour
            b["coin"] = c
            b["fc_nz"] = b["forecast"] != 0
            b["regime_mr"] = b["regime"] == "mean_reversion"
            rows.append(b[["coin", "wd", "hr", "pos", "g", "vr", "r1", "fc_nz", "regime_mr", "forecast"]])
    B = pd.concat(rows, ignore_index=True)
    B["inpos"] = B["pos"].abs() > 1e-9
    out["pos_by_wd"] = B.groupby("wd").agg(share_in=("inpos", "mean"), mean_pos=("pos", "mean"),
        gain=("g", "mean"), book=("vr", "mean"), coin=("r1", "mean"), nz_fc=("fc_nz", "sum"))
    out["inpos_share_all"] = float(B["inpos"].mean())
    out["fc_nz_by_hr_wd0"] = B[B.fc_nz].groupby(["wd", "hr"]).size().head(20)
    out["mean_abs_pos_inpos"] = float(B.loc[B.inpos, "pos"].abs().mean())
    out["sum_gain_vs_book"] = pd.Series({"sum_g": B["g"].sum(), "sum_vr": B["vr"].sum()})
    return out
