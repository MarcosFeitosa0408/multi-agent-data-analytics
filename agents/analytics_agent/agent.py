def run(self) -> dict:
    """Executa todas as verificações de qualidade."""

    try:
        df = self.load_data()

        issues = []

        issues.extend(self.validate_structure(df))
        issues.extend(self.check_missing_values(df))
        issues.extend(self.check_duplicates(df))
        issues.extend(self.check_numeric_rules(df))
        issues.extend(self.check_business_values(df))
        issues.extend(self.check_sales_consistency(df))

        quality_score = self.calculate_quality_score(df, issues)

        status = "COMPLETED"

        critical_issues = [
            issue
            for issue in issues
            if issue.get("severity") == "CRITICAL"
        ]

        if critical_issues:
            status = "ERROR"

        return {
            "agent": "quality_agent",
            "status": status,
            "task_id": self.task_id,
            "dataset": str(self.dataset_path),
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "quality_score": quality_score,
            "issues": issues,
        }

    except Exception as exc:
        return {
            "agent": "quality_agent",
            "status": "ERROR",
            "task_id": self.task_id,
            "dataset": str(self.dataset_path),
            "error": {
                "type": type(exc).__name__,
                "message": str(exc),
            },
        }
