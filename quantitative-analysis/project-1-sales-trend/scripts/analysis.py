import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class SalesAnalyzer:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.data['date'] = pd.to_datetime(self.data['date'])
    
    def load_data(self):
        """Load and display basic info about the dataset"""
        print("=== Sales Data Overview ===")
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

def main():
    # Initialize analyzer
    analyzer = SalesAnalyzer('data/sales_data.csv')
    
    # Run analyses
    analyzer.load_data()
    analyzer.monthly_trend_analysis()
    analyzer.product_performance()
    analyzer.regional_analysis()
    
    print("\n=== Analysis Complete ===")
    print("Check the 'results' folder for visualizations!")

if __name__ == "__main__":
    main()
