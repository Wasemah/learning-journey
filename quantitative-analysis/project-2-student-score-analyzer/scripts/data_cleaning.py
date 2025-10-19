import pandas as pd

class DataMapper:
    def __init__(self, data):
        self.data = data
    
    def data_fast(self):
        # Method for fast data processing
        pass
    
    def add_value(self, value):
        # Method to add values
        pass
    
    def new_data_info(self):
        """Displays information about the dataset"""
        print("Dataset shape:", self.data.shape)
        print("Column names:", self.data.columns.tolist())
        print("Data types:")
        print(self.data.dtypes)
        print("Basic statistics:")
        print(self.data.describe())
        print("Missing values:")
        print(self.data.isnull().sum())

if __name__ == "__main__":
    # Create sample data for testing
    sample_data = pd.DataFrame({
        'name': ['John', 'Jane', 'Bob'],
        'score': [85, 92, 78],
        'age': [25, 30, 35]
    })
    
    program = DataMapper(sample_data)
    program.new_data_info()
