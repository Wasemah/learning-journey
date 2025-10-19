import pandas as pd
import numpy as np
import pandas as pd



class DataAnalyzer:
    def __init__(self, data):
        self.data = data
    
    def show_data_info(self):
        """Show basic information about the dataset"""
        print(f"Dataset shape: {self.data.shape}")
        print("\nFirst 5 rows:")
        print(self.data.head())
        print("\nData types:")
        print(self.data.dtypes)
        print("\nMissing values:")
        print(self.data.isnull().sum())

# Example of how to use it:
if __name__ == "__main__":
    # Create sample data for testing
    sample_data = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'score': [85, 92, 78],
        'age': [20, 21, 19]
    })
    
    analyzer = DataAnalyzer(sample_data)
    analyzer.show_data_info()
