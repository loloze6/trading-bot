import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    FC = "forecast"
    RAW_D = "debug_info.components.dist_high.last_history_value"
    PP_D = "debug_info.components.dist_high.post_pipeline_value"

    reading = (
        "The situation is graded and centred on the coin's usual distance, as the Fidelity states, so each active bar's "
        "expected side is the sign of (dist_high after standardise + the plan's +10 offset): long when the close is nearer "
        "its 52-week high than usual, short when it is farther; a bar counts only if its raw distance is valid (<= 0); "
        "the top and fourth quintiles are cut at the 80th and 60th percentiles of the pooled grid forecasts (top: >= q80, "
        "fourth: q60 <= f < q80); holding is the coin's mean 7-bar return over all its grid bars in all windows; "
        "fewer than 100 top-quintile cases gives 'not observable'."
    )

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or FC not in df.columns:
                continue
            f = pd.to_numeric(df[FC], errors="coerce")
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            if RAW_D not in df.columns or PP_D not in df.columns:
                continue
            raw = pd.to_numeric(df[RAW_D], errors="coerce")
            pp = pd.to_numeric(df[PP_D], errors="coerce")
            centred = pp + 10.0
            valid = raw.notna() & pp.notna() & (raw <= 1e-12) & (pp <= 1e-9)
            exp_sign = np.sign(centred)
            ok = active & valid & (exp_sign != 0) & (np.sign(f) == exp_sign)
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "top-quintile mean 7-bar excess return over holding"
    threshold = "t >= 2 confirms (with supporting check), t <= -2 rejects; at least 100 top-quintile cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "top-quintile cases": 0},
            "decided_by": (
                f"Only {agreement:.1%} of the {n_active} active bars carry the sign of the plan's centred closeness to the "
                "52-week high (long nearer than usual, short farther), below the 90% required."
            ),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            for t in range(0, n - H, H):
                c0, c1 = c[t], c[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, w, f[t], c1 / c0 - 1.0))
    grid = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])

    if len(grid) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": passed},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"top-quintile cases": 0},
            "decided_by": "No 7-bar grid cases exist, below the 100 top-quintile cases required.",
            "reading": reading,
        }

    hold = grid.groupby("coin")["ret"].mean()
    grid["excess"] = grid["ret"] - grid["coin"].map(hold)

    g = grid.dropna(subset=["forecast", "ret"])
    q60 = float(np.quantile(g["forecast"], 0.6))
    q80 = float(np.quantile(g["forecast"], 0.8))
    top = g[g["forecast"] >= q80]
    fourth = g[(g["forecast"] >= q60) & (g["forecast"] < q80)]
    n_top = int(len(top))
    n_fourth = int(len(fourth))

    mean_ex = float(top["excess"].mean()) if n_top > 0 else None
    if n_top > 1:
        sd = float(top["excess"].std(ddof=1))
        t_main = float(mean_ex / (sd / np.sqrt(n_top))) if sd > 0 else None
    else:
        t_main = None

    if n_top > 1 and n_fourth > 1:
        tw = stats.ttest_ind(top["ret"].to_numpy(), fourth["ret"].to_numpy(), equal_var=False).statistic
        tw = float(tw) if np.isfinite(tw) else None
    else:
        tw = None
    sup_pass = (tw is not None and tw > 0)

    counts = {
        "top-quintile cases": n_top,
        "fourth-quintile cases": n_fourth,
        "grid cases": int(len(g)),
        "active bars": int(n_active),
    }

    def result(status, decided):
        return {
            "status": status,
            "situation_check": {"agreement": agreement, "passed": passed},
            "main_measure": {
                "name": main_name,
                "value": mean_ex,
                "statistic": {"name": "t of the mean", "value": t_main} if t_main is not None else None,
                "threshold": threshold,
            },
            "supporting_check": {
                "name": "top minus fourth quintile mean 7-bar return, Welch t > 0",
                "value": tw,
                "passed": bool(sup_pass) if tw is not None else None,
            },
            "counts": counts,
            "decided_by": decided,
            "reading": reading,
        }

    if n_top < 100:
        return result("not observable",
                      f"Only {n_top} independent top-quintile cases, below the 100 the plan requires.")
    if t_main is None:
        return result("inconclusive", "The top-quintile excess return has no defined t, so neither rule is met.")
    if t_main >= 2:
        if sup_pass:
            return result("confirmed",
                          f"The top-quintile mean excess over holding has t = {t_main:.2f} >= 2 and the top quintile beats the fourth (Welch t = {tw:.2f} > 0).")
        return result("inconclusive",
                      f"t = {t_main:.2f} >= 2 but the supporting check fails (Welch t top minus fourth = {tw}).")
    if t_main <= -2:
        return result("rejected",
                      f"The top-quintile mean excess over holding has t = {t_main:.2f} <= -2.")
    return result("inconclusive", f"The top-quintile mean excess over holding has t = {t_main:.2f}, between -2 and 2.")
