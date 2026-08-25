"""
Export and Reporting Manager for ChurnGuard AI.
Generates structured CSV, JSON, and Markdown executive summaries for leadership.
"""

import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime


class ExportManager:
    """Manages report formatting, data export, and executive briefing dossiers."""

    @staticmethod
    def generate_executive_summary_markdown(
        kpi_dict: Dict[str, Any],
        top_risk_df: pd.DataFrame,
        report_title: str = "ChurnGuard AI Executive Churn & Risk Briefing"
    ) -> str:
        """Generate a clean, styled Markdown report ready for PDF or presentation rendering."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_customers = kpi_dict.get('total_customers', 0)
        avg_risk = kpi_dict.get('avg_risk_score', 0.0)
        rev_at_risk = kpi_dict.get('revenue_at_risk', 0.0)
        churn_rate = kpi_dict.get('churn_rate', 0.0)

        md = [
            f"# {report_title}",
            f"**Generated:** {timestamp} | **Platform:** ChurnGuard AI v1.0",
            "",
            "## 📊 Executive KPI Snapshot",
            f"- **Total Monitored Accounts:** {total_customers}",
            f"- **Portfolio Average Risk Score:** {avg_risk}/100",
            f"- **Total Revenue at Risk:** ${rev_at_risk:,.2f}",
            f"- **Critical Churn Rate:** {churn_rate}%",
            "",
            "## 🚨 Top At-Risk Accounts Requiring Immediate Mitigation",
            "| Customer ID | Company | Risk Score | ARR | Health Status |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ]

        if not top_risk_df.empty:
            for _, row in top_risk_df.head(10).iterrows():
                cid = row.get('customer_id', '')
                cname = row.get('company_name', '')
                rscore = row.get('risk_score', '')
                arr = row.get('arr', 0)
                status = row.get('health_status', '')
                md.append(f"| {cid} | {cname} | {rscore} | ${arr:,.2f} | {status} |")
        else:
            md.append("| - | No critical accounts currently detected | - | - | - |")

        md.extend([
            "",
            "## 🛡️ Recommended CSM Playbook Actions",
            "1. Schedule executive check-in calls with accounts having risk score >= 75.",
            "2. Fast-track critical open support tickets to Tier 3 engineering.",
            "3. Offer customized renewal incentives and roadmap previews to at-risk accounts."
        ])

        return "\n".join(md)

    @staticmethod
    def export_dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
        """Convert a DataFrame to UTF-8 encoded CSV bytes for Streamlit download buttons."""
        return df.to_csv(index=False).encode('utf-8')
