import pandas as pd
import numpy as np

class RatioCalculator:
    """Advanced financial ratio calculations with validation"""
    
    @staticmethod
    def calculate_all_ratios(financial_data):
        """Calculate comprehensive set of financial ratios"""
        ratios = {}
        
        # Profitability Ratios
        ratios.update(RatioCalculator.calculate_profitability_ratios(financial_data))
        
        # Liquidity Ratios
        ratios.update(RatioCalculator.calculate_liquidity_ratios(financial_data))
        
        # Leverage Ratios
        ratios.update(RatioCalculator.calculate_leverage_ratios(financial_data))
        
        # Efficiency Ratios
        ratios.update(RatioCalculator.calculate_efficiency_ratios(financial_data))
        
        # Valuation Ratios
        ratios.update(RatioCalculator.calculate_valuation_ratios(financial_data))
        
        return ratios
    
    @staticmethod
    def calculate_profitability_ratios(data):
        """Calculate profitability ratios"""
        ratios = {}
        
        try:
            # Basic profitability ratios
            ratios['gross_margin'] = data['gross_profit'] / data['revenue']
            ratios['operating_margin'] = data['operating_income'] / data['revenue']
            ratios['net_margin'] = data['net_income'] / data['revenue']
            ratios['roa'] = data['net_income'] / data['total_assets']
            ratios['roe'] = data['net_income'] / data['shareholders_equity']
            
            # Advanced profitability ratios
            ratios['ebitda_margin'] = (data['operating_income'] + data.get('depreciation', 0)) / data['revenue']
            ratios['operating_cash_flow_margin'] = data.get('operating_cash_flow', data['net_income']) / data['revenue']
            
        except ZeroDivisionError:
            print("Warning: Division by zero in profitability ratios")
        
        return ratios
    
    @staticmethod
    def calculate_liquidity_ratios(data):
        """Calculate liquidity and solvency ratios"""
        ratios = {}
        
        try:
            # Current liquidity ratios
            ratios['current_ratio'] = data['current_assets'] / data['current_liabilities']
            ratios['quick_ratio'] = (data['current_assets'] - data['inventory']) / data['current_liabilities']
            ratios['cash_ratio'] = data['cash'] / data['current_liabilities']
            
            # Working capital metrics
            ratios['working_capital'] = data['current_assets'] - data['current_liabilities']
            ratios['working_capital_ratio'] = data['current_assets'] / data['current_liabilities']
            
        except ZeroDivisionError:
            print("Warning: Division by zero in liquidity ratios")
        
        return ratios
    
    @staticmethod
    def calculate_leverage_ratios(data):
        """Calculate leverage and solvency ratios"""
        ratios = {}
        
        try:
            # Debt ratios
            ratios['debt_to_equity'] = data['total_liabilities'] / data['shareholders_equity']
            ratios['debt_ratio'] = data['total_liabilities'] / data['total_assets']
            ratios['equity_ratio'] = data['shareholders_equity'] / data['total_assets']
            
            # Coverage ratios
            ebit = data['operating_income']
            interest_expense = data.get('interest_expense', data['long_term_debt'] * 0.05)
            ratios['interest_coverage'] = ebit / interest_expense if interest_expense > 0 else float('inf')
            
            # Financial leverage
            ratios['financial_leverage'] = data['total_assets'] / data['shareholders_equity']
            
        except ZeroDivisionError:
            print("Warning: Division by zero in leverage ratios")
        
        return ratios
    
    @staticmethod
    def calculate_efficiency_ratios(data):
        """Calculate efficiency and activity ratios"""
        ratios = {}
        
        try:
            # Turnover ratios (annualized for quarterly data)
            ratios['asset_turnover'] = (data['revenue'] * 4) / data['total_assets']
            ratios['inventory_turnover'] = (data['cogs'] * 4) / data['inventory']
            ratios['receivables_turnover'] = (data['revenue'] * 4) / data['accounts_receivable']
            
            # Days ratios
            ratios['days_inventory'] = 365 / ratios['inventory_turnover'] if ratios['inventory_turnover'] > 0 else float('inf')
            ratios['days_receivables'] = 365 / ratios['receivables_turnover'] if ratios['receivables_turnover'] > 0 else float('inf')
            
            # Fixed asset turnover
            fixed_assets = data['total_assets'] - data['current_assets']
            ratios['fixed_asset_turnover'] = data['revenue'] / fixed_assets if fixed_assets > 0 else float('inf')
            
        except ZeroDivisionError:
            print("Warning: Division by zero in efficiency ratios")
        
        return ratios
    
    @staticmethod
    def calculate_valuation_ratios(data):
        """Calculate market valuation ratios"""
        ratios = {}
        
        try:
            # Basic valuation ratios
            eps = data['net_income'] / data['shares_outstanding']
            ratios['pe_ratio'] = data['stock_price'] / eps if eps > 0 else float('inf')
            
            book_value_per_share = data['shareholders_equity'] / data['shares_outstanding']
            ratios['pb_ratio'] = data['stock_price'] / book_value_per_share
            
            sales_per_share = data['revenue'] / data['shares_outstanding']
            ratios['ps_ratio'] = data['stock_price'] / sales_per_share
            
            # Advanced valuation ratios
            ratios['ev_to_ebitda'] = RatioCalculator.calculate_ev_to_ebitda(data)
            ratios['dividend_yield'] = data.get('dividends', 0) / data['stock_price'] if data['stock_price'] > 0 else 0
            
        except ZeroDivisionError:
            print("Warning: Division by zero in valuation ratios")
        
        return ratios
    
    @staticmethod
    def calculate_ev_to_ebitda(data):
        """Calculate Enterprise Value to EBITDA ratio"""
        try:
            market_cap = data['shares_outstanding'] * data['stock_price']
            debt = data['long_term_debt']
            cash = data['cash']
            ebitda = data['operating_income'] + data.get('depreciation', data['operating_income'] * 0.1)
            
            enterprise_value = market_cap + debt - cash
            return enterprise_value / ebitda if ebitda > 0 else float('inf')
        except:
            return float('inf')
    
    @staticmethod
    def validate_ratios(ratios, industry_benchmarks):
        """Validate ratios against reasonable ranges and benchmarks"""
        warnings = []
        
        # Profitability validation
        if ratios.get('net_margin', 0) < 0:
            warnings.append("Negative net profit margin detected")
        
        if ratios.get('roe', 0) > 1:
            warnings.append("Extremely high ROE (possible financial engineering)")
        
        # Liquidity validation
        if ratios.get('current_ratio', 0) < 1:
            warnings.append("Current ratio below 1 - potential liquidity issues")
        
        if ratios.get('quick_ratio', 0) < 0.5:
            warnings.append("Quick ratio very low - limited liquid assets")
        
        # Leverage validation
        if ratios.get('debt_to_equity', 0) > 2:
            warnings.append("High debt-to-equity ratio - elevated financial risk")
        
        if ratios.get('interest_coverage', float('inf')) < 1.5:
            warnings.append("Low interest coverage - difficulty servicing debt")
        
        return warnings

# Example usage
if __name__ == "__main__":
    # Sample data for testing
    sample_data = {
        'revenue': 10000000,
        'cogs': 6000000,
        'gross_profit': 4000000,
        'operating_income': 2000000,
        'net_income': 1500000,
        'total_assets': 50000000,
        'current_assets': 12000000,
        'inventory': 3000000,
        'accounts_receivable': 4000000,
        'cash': 2000000,
        'total_liabilities': 30000000,
        'current_liabilities': 8000000,
        'long_term_debt': 22000000,
        'shareholders_equity': 20000000,
        'shares_outstanding': 1000000,
        'stock_price': 25.0
    }
    
    calculator = RatioCalculator()
    ratios = calculator.calculate_all_ratios(sample_data)
    
    print("📊 Calculated Financial Ratios:")
    for category, ratio_dict in ratios.items():
        print(f"\n{category.upper()}:")
        for ratio, value in ratio_dict.items():
            print(f"  {ratio}: {value:.4f}")
