import pandas as pd
from typing import Dict
from .data_loader import DataLoader
from .revenue_calculator import RevenueCalculator
from .report_generator import ReportGenerator


class RevInsightCore:
    def __init__(self, fp):
        self.fp = fp
        self.data = None

    def load_data(self):
        self.data = DataLoader().load_data(file_path=self.fp)

    @staticmethod
    def export_report(report: Dict[str, pd.DataFrame], file_path: str, report_type: str = 'xlsx') -> bool:
        if not file_path:
            raise ValueError("Please provide a valid file path to save the report.")
        if not report:
            raise ValueError("Please provide a valid report to export.")
        return ReportGenerator(file_path).generate_report(report, report_type)

    def compute(self):
        monthly_revenue = RevenueCalculator.compute_monthly_revenue(self.data)
        product_revenue = RevenueCalculator.compute_product_revenue(self.data)
        customer_revenue = RevenueCalculator.compute_customer_revenue(self.data)
        top_10_customers = RevenueCalculator.top_n_customers(self.data, number_of_customers=10)
        return {
            "Monthly Revenue": monthly_revenue,
            "Product Revenue": product_revenue,
            "Customer Revenue": customer_revenue,
            "Top 10 Customers": top_10_customers
        }

    def run(self, export_format: str = 'xlsx', export_fp: str = None):
        self.load_data()
        report = self.compute()
        self.export_report(report, file_path=export_fp, report_type=export_format)
        return report
