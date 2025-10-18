import pandas as pd
import numpy as np
import json
from datetime import datetime

class FinancialDataProcessor:
    """Process and validate financial data for analysis"""
    
    def __init__(self):
        self.cleaning_log = []
    
    def load_financial_data(self, file_path):
        """Load financial statements data"""
        try:
            df = pd.read_csv(file_path)
            self.cleaning_log.append(f"✅ Loaded data with {len(df)} rows")
            return df
        except Exception as e:
            self.cleaning_log.append(f"❌ Error loading data: {str(e)}")
            return None
    
    def validate_data_quality(self, df):
        """Validate data quality and completeness"""
        validation_results = {
            'total_rows': len(df),
            'missing_values': {},
            'data_types': {},
            'outliers': {}
        }
        
        # Check for missing values
        missing_data = df.isnull().sum()
        validation_results['missing_values'] = missing_data[missing_data > 0].to_dict()
        
        # Validate data types
        for column in df.columns:
            validation_results['data_types'][column] = str(df[column].dtype)
        
        # Check for outliers in numerical columns
        numerical_columns = df.select_dtypes(include=[np.number]).columns
        for column in numerical_columns:
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR))]
            validation_results['outliers'][column] = len(outliers)
        
        return validation_results
    
    def clean_financial_data(self, df):
        """Clean and preprocess financial data"""
        # Create a copy to avoid modifying original
        cleaned_df = df.copy()
        
        # Handle missing values
        numerical_columns = ['revenue', 'cogs', 'gross_profit', 'operating_income', 'net_income',
                           'total_assets', 'current_assets', 'inventory', 'accounts_receivable', 
                           'cash', 'total_liabilities', 'current_liabilities', 'long_term_debt',
                           'shareholders_equity']
        
        for column in numerical_columns:
            if column in cleaned_df.columns and cleaned_df[column].isnull().any():
                median_value = cleaned_df[column].median()
                cleaned_df[column].fillna(median_value, inplace=True)
                self.cleaning_log.append(f"✅ Filled missing values in {column} with median: {median_value}")
        
        # Ensure positive values for certain columns
        positive_columns = ['revenue', 'total_assets', 'shareholders_equity']
        for column in positive_columns:
            if column in cleaned_df.columns:
                negative_count = (cleaned_df[column] < 0).sum()
                if negative_count > 0:
                    cleaned_df[column] = cleaned_df[column].abs()
                    self.cleaning_log.append(f"✅ Converted {negative_count} negative values to positive in {column}")
        
        # Validate financial relationships
        self._validate_financial_relationships(cleaned_df)
        
        return cleaned_df
    
    def _validate_financial_relationships(self, df):
        """Validate logical relationships in financial data"""
        # Check if gross profit = revenue - COGS
        gross_profit_check = abs(df['gross_profit'] - (df['revenue'] - df['cogs'])) < 1
        if not gross_profit_check.all():
            self.cleaning_log.append("⚠️  Gross profit doesn't match revenue - COGS for some records")
        
        # Check if assets = liabilities + equity
        balance_sheet_check = abs(df['total_assets'] - (df['total_liabilities'] + df['shareholders_equity'])) < 1
        if not balance_sheet_check.all():
            self.cleaning_log.append("⚠️  Balance sheet equation doesn't balance for some records")
    
    def calculate_growth_metrics(self, df):
        """Calculate growth rates and trends"""
        growth_data = {}
        
        for company_id in df['company_id'].unique():
            company_data = df[df['company_id'] == company_id].sort_values('period')
            company_name = company_data['company_name'].iloc[0]
            
            if len(company_data) > 1:
                # Calculate quarter-over-quarter growth
                latest = company_data.iloc[-1]
                previous = company_data.iloc[-2]
                
                revenue_growth = (latest['revenue'] - previous['revenue']) / previous['revenue']
                net_income_growth = (latest['net_income'] - previous['net_income']) / previous['net_income']
                
                growth_data[company_id] = {
                    'company_name': company_name,
                    'revenue_growth_qoq': revenue_growth,
                    'net_income_growth_qoq': net_income_growth,
                    'latest_period': latest['period'],
                    'previous_period': previous['period']
                }
        
        return growth_data
    
    def generate_data_quality_report(self, validation_results):
        """Generate data quality assessment report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_records': validation_results['total_rows'],
                'columns_with_missing_data': len(validation_results['missing_values']),
                'columns_with_outliers': len([k for k, v in validation_results['outliers'].items() if v > 0])
            },
            'detailed_findings': validation_results,
            'cleaning_actions': self.cleaning_log,
            'data_quality_score': self._calculate_quality_score(validation_results)
        }
        
        return report
    
    def _calculate_quality_score(self, validation_results):
        """Calculate overall data quality score (0-100)"""
        total_penalty = 0
        
        # Penalty for missing values
        missing_penalty = sum(validation_results['missing_values'].values()) * 5
        total_penalty += min(missing_penalty, 50)  # Cap at 50
        
        # Penalty for outliers
        outlier_penalty = sum(validation_results['outliers'].values()) * 2
        total_penalty += min(outlier_penalty, 30)  # Cap at 30
        
        quality_score = max(0, 100 - total_penalty)
        return quality_score
    
    def export_processed_data(self, df, output_path):
        """Export cleaned and processed data"""
        try:
            df.to_csv(output_path, index=False)
            self.cleaning_log.append(f"✅ Exported processed data to {output_path}")
            return True
        except Exception as e:
            self.cleaning_log.append(f"❌ Error exporting data: {str(e)}")
            return False

# Example usage
if __name__ == "__main__":
    processor = FinancialDataProcessor()
    
    # Load and process data
    df = processor.load_financial_data('data/financial_statements.csv')
    
    if df is not None:
        # Validate data quality
        validation = processor.validate_data_quality(df)
        
        # Clean data
        cleaned_df = processor.clean_financial_data(df)
        
        # Calculate growth metrics
        growth_metrics = processor.calculate_growth_metrics(cleaned_df)
        
        # Generate report
        quality_report = processor.generate_data_quality_report(validation)
        
        print("📊 Data Processing Complete!")
        print(f"Data Quality Score: {quality_report['data_quality_score']}/100")
        print(f"Cleaning Actions: {len(processor.cleaning_log)}")
        
        # Export processed data
        processor.export_processed_data(cleaned_df, 'data/processed_financials.csv')
        
        # Save quality report
        with open('results/data_quality_report.json', 'w') as f:
            json.dump(quality_report, f, indent=2)
