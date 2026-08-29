"""
Forecast-Centric Strategy Analysis
Extracts forecasts as primary entities from completed trades
Analyzes forecast accuracy and links to trade outcomes
"""

import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Any
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
import os

logger = logging.getLogger("trading_bot")


def calc_range_metrics(df: pd.DataFrame) -> dict:
    """Calculate metrics for forecasts grouped by range bin."""
    if len(df) == 0 or "forecast" not in df.columns:
        return {}

    bins = [-np.inf, -15, -10, -5, 0, 5, 10, 15, np.inf]
    labels = [
        "very_negative_lt_minus_15",
        "minus_15_to_minus_10",
        "minus_10_to_minus_5",
        "minus_5_to_0",
        "0_to_5",
        "5_to_10",
        "10_to_15",
        "15_to_very_positive",
    ]

    df = df.copy()
    df["forecast_bin"] = pd.cut(df["forecast"], bins=bins, labels=labels)

    metrics = {}
    for bin_label in labels:
        bin_trades = df[df["forecast_bin"] == bin_label]
        if len(bin_trades) == 0:
            continue
        metrics[bin_label] = {
            "total_forecasts": len(bin_trades),
            "profitable_trades": int(bin_trades["profitable_net"].sum()),
            "success_rate_pct": round(bin_trades["profitable_net"].mean() * 100, 2),
            "total_net_pnl_usd": round(bin_trades["net_profit_loss_absolute"].sum(), 4),
            "avg_pnl_per_trade_usd": round(bin_trades["net_profit_loss_absolute"].mean(), 4),
        }
    return metrics


class ForecastAnalyzer:
    """
    Analyzes trading strategy through forecast lens.
    Each trade generates 2 forecast records: ENTRY and EXIT.
    Links forecasts to outcomes for accuracy analysis.
    """

    def __init__(self, output_path: str = "forecast_analysis.xlsx"):
        performance_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(performance_dir)
        self.output_path = os.path.join(project_dir, output_path)

    def analyze(self, completed_trades: List["CompletedTrade"]):
        """
        Main analysis entry point.

        Args:
            completed_trades: List of CompletedTrade objects from metrics tracker
        """
        if not completed_trades:
            logger.warning("No completed trades to analyze.")
            return

        logger.debug(f"Starting forecast-centric analysis on {len(completed_trades)} trades...")

        # Step 1: Extract forecast records from trades
        forecast_records = self._extract_forecasts(completed_trades)

        if not forecast_records:
            logger.warning("No forecast data found in trades.")
            return

        df_forecasts = pd.DataFrame(forecast_records)
        logger.debug(f"✓ Extracted {len(df_forecasts)} forecast decision points")

        # Step 2: Calculate metrics
        metrics_tables = self._calculate_metrics(df_forecasts)

        # Step 3: Export to Excel
        self._export_excel(df_forecasts, metrics_tables)

        logger.debug(f"✓ Forecast analysis exported to {self.output_path}")

    def _extract_forecasts(self, trades: List["CompletedTrade"]) -> List[Dict]:
        """
        STEP 1: Extract forecast records.
        Each trade → 2 records (ENTRY + EXIT)
        """
        records = []

        for idx, trade in enumerate(trades, 1):
            trade_id = f"T{idx:04d}"

            # === ENTRY FORECAST ===
            entry_rec = self._build_entry_record(trade, trade_id, idx)
            records.append(entry_rec)

            # === EXIT FORECAST ===
            exit_rec = self._build_exit_record(trade, trade_id, idx, entry_rec.get("forecast"))
            records.append(exit_rec)

        return records

    def _build_entry_record(self, trade, trade_id: str, idx: int) -> Dict:
        """Build ENTRY forecast record."""
        record = {
            "forecast_id": f"F{idx * 2 - 1:05d}",  # F00001, F00003, F00005...
            "forecast": trade.entry_forecast,
            "regime": trade.entry_regime,
            "confidence": trade.entry_confidence,
            "decision_type": "ENTRY",
            "side": trade.side,
            "trade_id": trade_id,
            "timestamp": trade.entry_time,
            "net_profit_loss_absolute": trade.net_profit_loss_absolute,
            "profitable_net": trade.profitable_net,
            "ope_commission": trade.entry_commission,
        }

        # Extract from entry_debug_info
        if trade.entry_debug_info:
            # Add all other debug fields dynamically (flexible for future strategies)
            for key, val in trade.entry_debug_info.items():
                if key not in ["forecast", "regime", "confidence"]:
                    record[f"{key}"] = val

        return record

    def _build_exit_record(self, trade, trade_id: str, idx: int, entry_forecast) -> Dict:
        """Build EXIT forecast record."""
        record = {
            "forecast_id": f"F{idx * 2:05d}",  # F00002, F00004, F00006...
            "forecast": trade.exit_forecast,
            "regime": trade.exit_regime,
            "confidence": trade.exit_confidence,
            "decision_type": "EXIT",
            "side": trade.side,
            "trade_id": trade_id,
            "timestamp": trade.exit_time,
            "net_profit_loss_absolute": trade.net_profit_loss_absolute,
            "profitable_net": trade.profitable_net,
            "ope_commission": trade.exit_commission,
        }

        # Extract from exit_debug_info
        if trade.exit_debug_info:
            # Add all other debug fields
            for key, val in trade.exit_debug_info.items():
                if key not in ["forecast", "regime", "confidence"]:
                    record[f"{key}"] = val

        return record

    def _calculate_metrics(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        STEP 2: Calculate metrics tables.
        Returns dict of metric DataFrames for different tabs.
        """
        metrics_dict = {}

        # Copy forecasts (wby entry type)
        df_exit = df[df["decision_type"] == "EXIT"].copy()
        df_entry = df[df["decision_type"] == "ENTRY"].copy()

        # === CATEGORY 1: Overall Summary ===
        metrics_dict["Overall Forecast Summary"] = self._calc_overall_metrics(df_exit)

        # === CATEGORY 2: Entry Forecasts by Range ===
        metrics_dict["Entry Forecasts By Range"] = self._calc_range_metrics(df_entry)

        # === CATEGORY 3: Exit Forecasts by Range ===
        metrics_dict["Exit Forecasts By Range"] = self._calc_range_metrics(df_exit)

        # === CATEGORY 4: Regime Performance ===
        if "regime" in df_exit.columns:
            metrics_dict["Performance By Regime"] = {}

        return metrics_dict

    def _calc_overall_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate overall forecast metrics."""
        if len(df) == 0 or "forecast" not in df.columns:
            return {}

        corr = df["forecast"].corr(df["net_profit_loss_absolute"]) if "net_profit_loss_absolute" in df.columns else None
        winners = df[df["profitable_net"] == True]
        losers = df[df["profitable_net"] == False]

        return {
            "Total Forecasts": len(df),
            "Positive Forecasts (>0)": int((df["forecast"] > 0).sum()),
            "Negative Forecasts (<0)": int((df["forecast"] < 0).sum()),
            "Forecast-PnL Correlation": round(corr, 4) if corr is not None else "N/A",
            "Avg Forecast (Winners)": round(winners["forecast"].mean(), 4) if len(winners) > 0 else "N/A",
            "Avg Forecast (Losers)": round(losers["forecast"].mean(), 4) if len(losers) > 0 else "N/A",
        }

    def _calc_range_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        return calc_range_metrics(df)

    def _export_excel(self, df_forecasts: pd.DataFrame, metrics_dict: Dict[str, Dict]):
        """
        STEP 3: Export to Excel with two tabs.
        Tab 1: Forecast Records
        Tab 2: Forecast Metrics (dict-based like PerformanceMetrics)
        """
        with pd.ExcelWriter(self.output_path, engine="openpyxl") as writer:
            # Tab 1: All Forecast Records
            df_forecasts.to_excel(writer, sheet_name="Forecast Records", index=False)

            # Tab 2: Metrics (write dict-based structure)
            self._write_metrics_to_sheet(writer, metrics_dict)

        # Apply formatting
        self._format_excel(self.output_path)

    def _write_metrics_to_sheet(self, writer, metrics_dict: Dict[str, Dict]):
        """Write metrics dict to Excel sheet like metrics.py does."""
        wb = writer.book
        ws = wb.create_sheet("Forecast Metrics")

        row = 1

        for category, metrics in metrics_dict.items():
            # Category header
            ws.cell(row=row, column=1, value=category)
            ws.cell(row=row, column=1).font = Font(bold=True, size=12)
            row += 2  # blank line after header

            # Metrics of this category
            for metric_name, metric_value in metrics.items():
                # Case 1: nested dict (e.g. one entry per forecast_bin)
                if isinstance(metric_value, dict):
                    # write sub‑section title (the bin label)
                    ws.cell(row=row, column=1, value=metric_name)
                    ws.cell(row=row, column=1).font = Font(bold=True)
                    row += 1

                    # write sub‑metrics (keys of inner dict)
                    for sub_name, sub_val in metric_value.items():
                        # convert numpy scalars etc. to plain Python types
                        if hasattr(sub_val, "item"):
                            sub_val = sub_val.item()

                        ws.cell(row=row, column=1, value=f"  {sub_name}")
                        ws.cell(row=row, column=2, value=sub_val)
                        row += 1

                    row += 1  # extra blank line between bins

                # Case 2: simple scalar metric (overall summary)
                else:
                    val = metric_value
                    if hasattr(val, "item"):
                        val = val.item()

                    ws.cell(row=row, column=1, value=metric_name)
                    ws.cell(row=row, column=2, value=val)
                    row += 1

            row += 1  # blank line between categories

        # Auto‑adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if cell.value is not None:
                        max_length = max(max_length, len(str(cell.value)))
                except Exception:
                    pass
            adjusted_width = min(max_length + 3, 60)
            ws.column_dimensions[column_letter].width = adjusted_width

    def _format_excel(self, filepath: str):
        """Apply professional formatting to Excel file."""
        wb = openpyxl.load_workbook(filepath)

        # Define styles
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF", size=11)
        header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        border_side = Side(style="thin", color="CCCCCC")
        border = Border(left=border_side, right=border_side, top=border_side, bottom=border_side)

        # Format Forecast Records sheet
        if "Forecast Records" in wb.sheetnames:
            ws = wb["Forecast Records"]

            # Format header row
            for cell in ws[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = header_alignment
                cell.border = border

            # Freeze top row
            ws.freeze_panes = "A2"

        wb.save(filepath)
        logger.debug(f"✓ Excel formatting applied")
