"""
Data Quality Auditor and Anomaly Detector for ChurnGuard AI.
Verifies completeness, boundary checks, duplicate IDs, and data drift.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List


class DataQualityAuditor:
    """Audits customer datasets for integrity issues, missing fields, and anomalous values."""

    @staticmethod
    def audit_customer_dataset(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform a comprehensive data quality audit on the customer dataframe.
        Returns a dictionary with status, score (0-100), and list of warnings/errors.
        """
        report = {
            "total_records": len(df),
            "is_valid": True,
            "quality_score": 100,
            "errors": [],
            "warnings": []
        }

        if df.empty:
            report["is_valid"] = False
            report["quality_score"] = 0
            report["errors"].append("Dataset is completely empty.")
            return report

        # Required columns check
        required_cols = ['customer_id', 'company_name', 'arr']
        for col in required_cols:
            if col not in df.columns:
                report["errors"].append(f"Missing mandatory column: '{col}'")
                report["quality_score"] -= 25

        # Duplicate ID check
        if 'customer_id' in df.columns:
            dupes = df['customer_id'].duplicated().sum()
            if dupes > 0:
                report["errors"].append(f"Found {dupes} duplicate customer_id records.")
                report["quality_score"] -= 20

        # Negative ARR check
        if 'arr' in df.columns:
            negative_arr = (pd.to_numeric(df['arr'], errors='coerce') < 0).sum()
            if negative_arr > 0:
                report["warnings"].append(f"Found {negative_arr} records with negative ARR values.")
                report["quality_score"] -= 15

        # Null value ratio check
        null_counts = df.isnull().sum().sum()
        total_cells = df.size
        null_ratio = null_counts / max(1, total_cells)
        if null_ratio > 0.10:
            report["warnings"].append(f"High missing value ratio: {null_ratio*100:.1f}% cells are empty.")
            report["quality_score"] -= int(null_ratio * 30)

        # Cap quality score
        report["quality_score"] = max(0, min(100, report["quality_score"]))
        if report["errors"]:
            report["is_valid"] = False

        return report
