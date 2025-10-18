import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

class FinancialAnalyzer:
    def __init__(self, data_path, benchmarks_path):
        self.data = pd.read_csv(data_path)
        self.benchmarks = self.load_benchmarks(benchmarks_path)
        self.analysis_results = {}
        
    def load_benchmarks(self, benchmarks_path):
        """Load industry benchmarks"""
        with open(benchmarks_path, 'r') as f:
            return json.load(f)
    
    def calculate_profitability_ratios(self, company_data):
        """Calculate profitability ratios"""
        ratios = {}
        
        # Gross Margin
        ratios['gross_margin'] = company_data['gross_profit'] / company_data['revenue']
        
        # Operating Margin
        ratios['operating_margin'] = company_data['operating_income'] / company_data['revenue']
        
        # Net Profit Margin
        ratios['net_margin'] = company_data['net_income'] / company_data['revenue']
        
        # Return on Assets (ROA)
        ratios['roa'] = company_data['net_income'] / company_data['total_assets']
        
        # Return on Equity (ROE)
        ratios['roe'] = company_data['net_income'] / company_data['shareholders_equity']
        
        return ratios
    
    def calculate_liquidity_ratios(self, company_data):
        """Calculate liquidity ratios"""
        ratios = {}
        
        # Current Ratio
        ratios['current_ratio'] = company_data['current_assets'] / company_data['current_liabilities']
        
        # Quick Ratio (Acid-Test)
        quick_assets = company_data['current_assets'] - company_data['inventory']
        ratios['quick_ratio'] = quick_assets / company_data['current_liabilities']
        
        # Cash Ratio
        ratios['cash_ratio'] = company_data['cash'] / company_data['current_liabilities']
        
        return ratios
    
    def calculate_leverage_ratios(self, company_data):
        """Calculate leverage/solvency ratios"""
        ratios = {}
        
        # Debt to Equity
        ratios['debt_to_equity'] = company_data['total_liabilities'] / company_data['shareholders_equity']
        
        # Debt Ratio
        ratios['debt_ratio'] = company_data['total_liabilities'] / company_data['total_assets']
        
        # Interest Coverage (simplified)
        ebit = company_data['operating_income']
        interest_expense = company_data['long_term_debt'] * 0.05  # Assume 5% interest
        ratios['interest_coverage'] = ebit / interest_expense if interest_expense > 0 else float('inf')
        
        return ratios
    
    def calculate_efficiency_ratios(self, company_data):
        """Calculate efficiency ratios"""
        ratios = {}
        
        # Asset Turnover
        ratios['asset_turnover'] = company_data['revenue'] / company_data['total_assets']
        
        # Inventory Turnover (annualized)
        ratios['inventory_turnover'] = (company_data['cogs'] * 4) / company_data['inventory']
        
        # Receivables Turnover (annualized)
        ratios['receivables_turnover'] = (company_data['revenue'] * 4) / company_data['accounts_receivable']
        
        return ratios
    
    def calculate_valuation_ratios(self, company_data):
        """Calculate valuation ratios"""
        ratios = {}
        
        # P/E Ratio
        eps = company_data['net_income'] / company_data['shares_outstanding']
        ratios['pe_ratio'] = company_data['stock_price'] / eps if eps > 0 else float('inf')
        
        # P/B Ratio
        book_value_per_share = company_data['shareholders_equity'] / company_data['shares_outstanding']
        ratios['pb_ratio'] = company_data['stock_price'] / book_value_per_share
        
        # P/S Ratio
        sales_per_share = company_data['revenue'] / company_data['shares_outstanding']
        ratios['ps_ratio'] = company_data['stock_price'] / sales_per_share
        
        return ratios
    
    def analyze_company(self, company_id):
        """Comprehensive analysis for a single company"""
        company_data = self.data[self.data['company_id'] == company_id].iloc[-1]  # Latest quarter
        company_name = company_data['company_name']
        industry = company_data['industry']
        
        print(f"\n=== Financial Analysis: {company_name} ({industry}) ===")
        
        # Calculate all ratios
        ratios = {}
        ratios['profitability'] = self.calculate_profitability_ratios(company_data)
        ratios['liquidity'] = self.calculate_liquidity_ratios(company_data)
        ratios['leverage'] = self.calculate_leverage_ratios(company_data)
        ratios['efficiency'] = self.calculate_efficiency_ratios(company_data)
        ratios['valuation'] = self.calculate_valuation_ratios(company_data)
        
        # Compare with benchmarks
        industry_benchmarks = self.benchmarks['industry_benchmarks'][industry]
        comparison = self.compare_with_benchmarks(ratios, industry_benchmarks)
        
        # Store results
        self.analysis_results[company_id] = {
            'company_name': company_name,
            'industry': industry,
            'period': company_data['period'],
            'ratios': ratios,
            'benchmark_comparison': comparison,
            'financial_health': self.assess_financial_health(ratios, industry_benchmarks)
        }
        
        return ratios
    
    def compare_with_benchmarks(self, ratios, benchmarks):
        """Compare company ratios with industry benchmarks"""
        comparison = {}
        
        for category in ratios:
            comparison[category] = {}
            for ratio_name, ratio_value in ratios[category].items():
                benchmark_value = benchmarks[category].get(ratio_name, None)
                if benchmark_value:
                    difference = ratio_value - benchmark_value
                    percentage_diff = (difference / benchmark_value) * 100
                    comparison[category][ratio_name] = {
                        'company_value': ratio_value,
                        'benchmark_value': benchmark_value,
                        'difference': difference,
                        'percentage_diff': percentage_diff,
                        'status': 'Above' if difference > 0 else 'Below'
                    }
        
        return comparison
    
    def assess_financial_health(self, ratios, benchmarks):
        """Assess overall financial health"""
        health_score = 0
        total_metrics = 0
        insights = []
        
        # Profitability assessment
        profitability_metrics = ['net_margin', 'roe', 'roa']
        for metric in profitability_metrics:
            if metric in ratios['profitability']:
                company_val = ratios['profitability'][metric]
                benchmark_val = benchmarks['profitability'][metric]
                if company_val >= benchmark_val:
                    health_score += 1
                    insights.append(f"✅ Strong {metric.replace('_', ' ').title()}")
                else:
                    insights.append(f"⚠️  Weak {metric.replace('_', ' ').title()}")
                total_metrics += 1
        
        # Liquidity assessment
        liquidity_metrics = ['current_ratio', 'quick_ratio']
        for metric in liquidity_metrics:
            if metric in ratios['liquidity']:
                company_val = ratios['liquidity'][metric]
                benchmark_val = benchmarks['liquidity'][metric]
                if company_val >= benchmark_val:
                    health_score += 1
                    insights.append(f"✅ Good {metric.replace('_', ' ').title()}")
                else:
                    insights.append(f"⚠️  Poor {metric.replace('_', ' ').title()}")
                total_metrics += 1
        
        # Overall health rating
        health_percentage = (health_score / total_metrics) * 100
        if health_percentage >= 80:
            rating = "Excellent"
        elif health_percentage >= 60:
            rating = "Good"
        elif health_percentage >= 40:
            rating = "Fair"
        else:
            rating = "Poor"
        
        return {
            'score': health_percentage,
            'rating': rating,
            'insights': insights
        }
    
    def generate_dashboard_data(self):
        """Generate data for dashboard visualization"""
        dashboard_data = {}
        
        for company_id in self.data['company_id'].unique():
            company_analysis = self.analyze_company(company_id)
            dashboard_data[company_id] = self.analysis_results[company_id]
        
        return dashboard_data
    
    def save_analysis_results(self):
        """Save analysis results to files"""
        os.makedirs('results', exist_ok=True)
        
        # Save detailed analysis
        with open('results/company_comparison.json', 'w') as f:
            json.dump(self.analysis_results, f, indent=2)
        
        # Generate report
        self.generate_financial_report()
        
        print("✅ Financial analysis results saved to 'results/' folder")
    
    def generate_financial_report(self):
        """Generate a comprehensive financial report"""
        report = "# Financial Ratio Analysis Report\n\n"
        report += f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
        
        for company_id, analysis in self.analysis_results.items():
            report += f"## {analysis['company_name']} ({analysis['industry']})\n\n"
            report += f"**Period:** {analysis['period']}\n"
            report += f"**Financial Health:** {analysis['financial_health']['rating']} ({analysis['financial_health']['score']:.1f}%)\n\n"
            
            report += "### Key Ratios vs Industry Benchmarks\n\n"
            for category, ratios in analysis['benchmark_comparison'].items():
                report += f"#### {category.title()}\n\n"
                for ratio_name, comparison in ratios.items():
                    status_icon = "✅" if comparison['status'] == 'Above' else "⚠️"
                    report += f"- {status_icon} **{ratio_name.replace('_', ' ').title()}**: {comparison['company_value']:.3f} "
                    report += f"(Industry: {comparison['benchmark_value']:.3f}) "
                    report += f"**{comparison['status']} benchmark by {abs(comparison['percentage_diff']):.1f}%**\n"
                report += "\n"
            
            report += "### Financial Health Insights\n\n"
            for insight in analysis['financial_health']['insights']:
                report += f"- {insight}\n"
            
            report += "\n---\n\n"
        
        with open('results/ratio_analysis_report.md', 'w') as f:
            f.write(report)

def main():
    # Initialize analyzer
    analyzer = FinancialAnalyzer(
        'data/financial_statements.csv',
        'data/industry_benchmarks.json'
    )
    
    # Analyze all companies
    print("=== Financial Ratio Dashboard ===")
    print("Analyzing company financial statements...")
    
    for company_id in [1, 2, 3]:
        analyzer.analyze_company(company_id)
    
    # Save results
    analyzer.save_analysis_results()
    
    print("\n=== Financial Analysis Complete ===")
    print("📊 Check the 'results/' folder for detailed analysis and reports!")
    print("💡 Use the generated data to create interactive dashboards")

if __name__ == "__main__":
    main()
