import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import os
import sys




# Add config to path and import settings
sys.path.append('config')
from settings import DATA_CONFIG, ANALYSIS_CONFIG, VISUALIZATION_CONFIG, OUTPUT_CONFIG

class SalesAnalyzer:
    def __init__(self, data_path=None):
        # Use config path or provided path
        self.data_path = data_path or DATA_CONFIG['data_path']
        self.data = pd.read_csv(self.data_path)
        self.data[DATA_CONFIG['date_column']] = pd.to_datetime(self.data[DATA_CONFIG['date_column']])
        
        # Apply visualization settings
        plt.style.use(VISUALIZATION_CONFIG['style'])
        
    def load_config(self, config_file='config/analysis_config.json'):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file {config_file} not found. Using default settings.")
            return {}
    
    
    
    def load_data(self):
        """Load and display basic info about the dataset"""
        config = self.load_config()
        
        print("=== Sales Data Overview ===")
        print(f"Project: {config.get('project', {}).get('name', 'Sales Analysis')}")
        print(f"Dataset shape: {self.data.shape}")
        print("\nFirst 5 rows:")
        print(self.data.head())
        print("\nData types:")
        print(self.data.dtypes)
        print("\nMissing values:")
        print(self.data.isnull().sum())
        
        return self.data
    
    def monthly_trend_analysis(self):
        """Analyze monthly sales trends"""
        monthly_data = self.data.groupby(self.data['date'].dt.to_period('M')).agg({
            'units_sold': 'sum',
            'revenue': 'sum'
        }).reset_index()
        
        monthly_data['date'] = monthly_data['date'].dt.to_timestamp()
        
        print("\n=== Monthly Sales Trends ===")
        print(monthly_data)
        
        return monthly_data
    
    def product_performance(self):
        """Analyze product performance"""
        product_stats = self.data.groupby('product').agg({
            'units_sold': ['sum', 'mean'],
            'revenue': ['sum', 'mean']
        }).round(2)
        
        print("\n=== Product Performance ===")
        print(product_stats)
        
        return product_stats
    
    def regional_analysis(self):
        """Analyze sales by region"""
        region_stats = self.data.groupby('region').agg({
            'units_sold': 'sum',
            'revenue': 'sum'
        }).sort_values('revenue', ascending=False)
        
        print("\n=== Regional Performance ===")
        print(region_stats)
        
        return region_stats
    
    def create_visualizations(self):
        """Create basic visualizations"""
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Monthly revenue trend
        monthly_data = self.monthly_trend_analysis()
        axes[0,0].plot(monthly_data['date'], monthly_data['revenue'], marker='o', linewidth=2)
        axes[0,0].set_title('Monthly Revenue Trend')
        axes[0,0].set_ylabel('Revenue ($)')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Product sales
        product_sales = self.data.groupby('product')['units_sold'].sum()
        axes[0,1].bar(product_sales.index, product_sales.values, color='skyblue')
        axes[0,1].set_title('Total Units Sold by Product')
        axes[0,1].set_ylabel('Units Sold')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Regional revenue
        region_revenue = self.data.groupby('region')['revenue'].sum()
        axes[1,0].pie(region_revenue.values, labels=region_revenue.index, autopct='%1.1f%%')
        axes[1,0].set_title('Revenue Distribution by Region')
        
        # Category performance
        category_sales = self.data.groupby('category')['revenue'].sum()
        axes[1,1].barh(category_sales.index, category_sales.values, color='lightgreen')
        axes[1,1].set_title('Revenue by Category')
        axes[1,1].set_xlabel('Revenue ($)')
        
        plt.tight_layout()
        plt.savefig('results/sales_analysis_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()

    def save_results(self):
        """Save analysis results to files using config settings"""
        # Create results directory if it doesn't exist
        os.makedirs(OUTPUT_CONFIG['results_directory'], exist_ok=True)
        
        # Save product performance
        product_stats = self.data.groupby('product').agg({
            'units_sold': 'sum',
            'revenue': 'sum'
        }).round(2)
        product_stats.to_csv(f"{OUTPUT_CONFIG['results_directory']}/product_performance.csv")
        
        # Save regional analysis
        region_stats = self.data.groupby('region').agg({
            'units_sold': 'sum',
            'revenue': 'sum'
        }).sort_values('revenue', ascending=False)
        
        regional_data = {
            'regional_performance': region_stats.reset_index().to_dict('records'),
            'summary': {
                'highest_revenue_region': region_stats['revenue'].idxmax(),
                'lowest_revenue_region': region_stats['revenue'].idxmin(),
                'total_revenue_across_regions': float(region_stats['revenue'].sum()),
                'analysis_date': str(pd.Timestamp.now().date()),
                'currency': ANALYSIS_CONFIG['currency']
            }
        }
        
        with open(f"{OUTPUT_CONFIG['results_directory']}/regional_analysis.json", 'w') as f:
            json.dump(regional_data, f, indent=2)
        
        print("✅ Results saved using configuration settings!")
        print(f"📁 Location: {OUTPUT_CONFIG['results_directory']}/")

def main():
    # Initialize analyzer (will use config settings)
    analyzer = SalesAnalyzer()
    
    # Run analyses
    analyzer.load_data()
    analyzer.monthly_trend_analysis()
    analyzer.product_performance()
    analyzer.regional_analysis()
    
    # Save results
    analyzer.save_results()
    
    print("\n=== Analysis Complete ===")
    print("📊 Check the results folder for generated files!")
    print("⚙️  All settings loaded from config files")

if __name__ == "__main__":
    main()
