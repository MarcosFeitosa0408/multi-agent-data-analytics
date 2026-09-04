"""
Quality Agent
-------------
Responsável por avaliar a qualidade de datasets de vendas.

Versão inicial:
- execução determinística;
- Python + Pandas;
- sem LLM;
- sem alteração do dataset original.
"""

from pathlib import Path
import json
import pandas as pd


class QualityAgent:
    """Agente responsável pela avaliação da qualidade dos dados."""

    REQUIRED_COLUMNS = [
        "order_id",
        "order_date",
        "store",
        "product",
        "category",
        "quantity",
        "unit_price",
        "total_sales",
        "customer_state",
        "payment_method",
    ]

    VALID_CATEGORIES = {
        "Eletrônicos",
        "Periféricos",
        "Escritório",
    }

    VALID_PAYMENT_METHODS = {
        "PIX",
        "Cartão",
        "Boleto",
    }

      def __init__(self, dataset_path: str, task_id: str = "task_001"):
        self.dataset_path = Path(dataset_path)
        self.task_id = task_id

    def load_data(self) -> pd.DataFrame:
        """Carrega o dataset sem modificar o arquivo original."""

        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset não encontrado: {self.dataset_path}"
            )

        return pd.read_csv(self.dataset_path)

    def validate_structure(self, df: pd.DataFrame) -> list:
        """Verifica se todas as colunas obrigatórias existem."""

        issues = []

        missing_columns = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing_columns:
            issues.append(
                {
                    "rule": "Q00",
                    "severity": "CRITICAL",
                    "type": "missing_columns",
                    "message": "Colunas obrigatórias ausentes.",
                    "columns": missing_columns,
                }
            )

        return issues

    def check_missing_values(self, df: pd.DataFrame) -> list:
        """Identifica valores ausentes em campos obrigatórios."""

        issues = []

        for column in self.REQUIRED_COLUMNS:
            if column not in df.columns:
                continue

            missing_count = int(df[column].isna().sum())

            if missing_count > 0:
                issues.append(
                    {
                        "rule": "Q02",
                        "severity": "HIGH",
                        "type": "missing_values",
                        "column": column,
                        "count": missing_count,
                        "message": (
                            f"A coluna '{column}' possui "
                            f"{missing_count} valor(es) ausente(s)."
                        ),
                    }
                )

        return issues

    def check_duplicates(self, df: pd.DataFrame) -> list:
        """Verifica duplicidades de order_id."""

        issues = []

        if "order_id" not in df.columns:
            return issues

        duplicate_count = int(df["order_id"].duplicated().sum())

        if duplicate_count > 0:
            issues.append(
                {
                    "rule": "Q01",
                    "severity": "HIGH",
                    "type": "duplicate_order_id",
                    "count": duplicate_count,
                    "message": (
                        f"Foram encontrados {duplicate_count} "
                        "registro(s) com order_id duplicado."
                    ),
                }
            )

        return issues

    def check_numeric_rules(self, df: pd.DataFrame) -> list:
        """Valida quantidade, preço e total da venda."""

        issues = []

        if "quantity" in df.columns:
            invalid_quantity = int(
                (df["quantity"].notna() & (df["quantity"] <= 0)).sum()
            )

            if invalid_quantity > 0:
                issues.append(
                    {
                        "rule": "Q03",
                        "severity": "HIGH",
                        "type": "invalid_quantity",
                        "count": invalid_quantity,
                        "message": (
                            f"Foram encontrados {invalid_quantity} "
                            "valor(es) inválido(s) em quantity."
                        ),
                    }
                )

        if "unit_price" in df.columns:
            invalid_price = int(
                (df["unit_price"].notna() & (df["unit_price"] <= 0)).sum()
            )

            if invalid_price > 0:
                issues.append(
                    {
                        "rule": "Q04",
                        "severity": "HIGH",
                        "type": "invalid_unit_price",
                        "count": invalid_price,
                        "message": (
                            f"Foram encontrados {invalid_price} "
                            "valor(es) inválido(s) em unit_price."
                        ),
                    }
                )

        if "total_sales" in df.columns:
            invalid_total = int(
                (df["total_sales"].notna() & (df["total_sales"] < 0)).sum()
            )

            if invalid_total > 0:
                issues.append(
                    {
                        "rule": "Q05",
                        "severity": "HIGH",
                        "type": "invalid_total_sales",
                        "count": invalid_total,
                        "message": (
                            f"Foram encontrados {invalid_total} "
                            "valor(es) negativo(s) em total_sales."
                        ),
                    }
                )

        return issues

    def check_business_values(self, df: pd.DataFrame) -> list:
        """Valida categorias e métodos de pagamento."""

        issues = []

        if "category" in df.columns:
            invalid_categories = sorted(
                set(df["category"].dropna()) - self.VALID_CATEGORIES
            )

            if invalid_categories:
                issues.append(
                    {
                        "rule": "Q08",
                        "severity": "MEDIUM",
                        "type": "invalid_category",
                        "values": invalid_categories,
                        "message": "Foram encontradas categorias não reconhecidas.",
                    }
                )

        if "payment_method" in df.columns:
            invalid_methods = sorted(
                set(df["payment_method"].dropna())
                - self.VALID_PAYMENT_METHODS
            )

            if invalid_methods:
                issues.append(
                    {
                        "rule": "Q09",
                        "severity": "MEDIUM",
                        "type": "invalid_payment_method",
                        "values": invalid_methods,
                        "message": (
                            "Foram encontrados métodos de pagamento "
                            "não reconhecidos."
                        ),
                    }
                )

        return issues

    def check_sales_consistency(self, df: pd.DataFrame) -> list:
        """Verifica quantity x unit_price x total_sales."""

        issues = []

        required = {
            "quantity",
            "unit_price",
            "total_sales",
        }

        if not required.issubset(df.columns):
            return issues

        valid_rows = df[
            df["quantity"].notna()
            & df["unit_price"].notna()
            & df["total_sales"].notna()
        ].copy()

        if valid_rows.empty:
            return issues

        expected_total = (
            valid_rows["quantity"] * valid_rows["unit_price"]
        )

        inconsistent = (
            (valid_rows["total_sales"] - expected_total).abs() > 0.01
        )

        inconsistent_count = int(inconsistent.sum())

        if inconsistent_count > 0:
            issues.append(
                {
                    "rule": "Q06",
                    "severity": "HIGH",
                    "type": "sales_calculation_inconsistency",
                    "count": inconsistent_count,
                    "message": (
                        f"Foram encontrados {inconsistent_count} "
                        "registro(s) com inconsistência matemática."
                    ),
                }
            )

        return issues

    def calculate_quality_score(
        self,
        df: pd.DataFrame,
        issues: list,
    ) -> float:
        """Calcula um score inicial de qualidade entre 0 e 100."""

        if df.empty:
            return 0.0

        total_cells = len(df) * len(self.REQUIRED_COLUMNS)

        missing_cells = int(
            df[self.REQUIRED_COLUMNS]
            .isna()
            .sum()
            .sum()
        )

        duplicate_rows = (
            int(df["order_id"].duplicated().sum())
            if "order_id" in df.columns
            else 0
        )

        invalid_issue_count = sum(
            int(issue.get("count", 0))
            for issue in issues
        )

        total_problems = missing_cells + duplicate_rows + invalid_issue_count

        if total_cells == 0:
            return 0.0

        score = 100 - ((total_problems / total_cells) * 100)

        return round(max(0.0, min(100.0, score)), 2)

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

    def export_report(
        self,
        report: dict,
        output_path: str,
    ) -> None:
        """Exporta o relatório em JSON."""

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open("w", encoding="utf-8") as file:
            json.dump(
                report,
                file,
                ensure_ascii=False,
                indent=2,
            )


if __name__ == "__main__":
    agent = QualityAgent("data/sales.csv")

    report = agent.run()

    agent.export_report(
        report,
        "outputs/quality_report.json",
    )

    print(json.dumps(
        report,
        ensure_ascii=False,
        indent=2,
    ))
