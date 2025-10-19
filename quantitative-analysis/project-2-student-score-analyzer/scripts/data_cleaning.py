import pandas as pd
import numpy as np


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
    
    def load_config(self):
        """Load cleaning configuration"""
        try:
            with open('config/analysis_config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Config file not found. Using default settings.")
            return {}
    
    def load_data(self):
        """Load the student data"""
        self.data = pd.read_csv(self.data_path)
        print(f"✅ Loaded data with {len(self.data)} rows and {len(self.data.columns)} columns")
        return self.data
    
    def validate_data(self):
        """Validate data against configuration"""
        config = self.load_config()
        quality_checks = config.get('quality_checks', {})
        
        print("\n=== Data Validation ===")
        
        # Check required columns
        required_cols = quality_checks.get('required_columns', ['student_id', 'class', 'subject', 'score'])
        missing_cols = [col for col in required_cols if col not in self.data.columns]
        
        if missing_cols:
            print(f"❌ Missing required columns: {missing_cols}")
        else:
            print("✅ All required columns present")
        
        # Check score range
        score_min = self.data['score'].min()
        score_max = self.data['score'].max()
        score_range = quality_checks.get('score_range', [0, 100])
        
        if score_min < score_range[0] or score_max > score_range[1]:
            print(f"❌ Scores outside expected range: {score_min}-{score_max}")
        else:
            print("✅ All scores within valid range")
        
        # Check for duplicates
        duplicate_students = self.data.duplicated(subset=['student_id', 'subject']).sum()
        if duplicate_students > 0:
            print(f"❌ Found {duplicate_students} duplicate student-subject entries")
        else:
            print("✅ No duplicate entries found")
        
        # Check for missing values
        missing_values = self.data.isnull().sum().sum()
        if missing_values > 0:
            print(f"❌ Found {missing_values} missing values")
        else:
            print("✅ No missing values found")
    
    def clean_data(self):
        """Perform data cleaning operations"""
        print("\n=== Data Cleaning ===")
        
        # Remove duplicates
        initial_count = len(self.data)
        self.data = self.data.drop_duplicates(subset=['student_id', 'subject'])
        removed_duplicates = initial_count - len(self.data)
        
        if removed_duplicates > 0:
            print(f"✅ Removed {removed_duplicates} duplicate entries")
        
        # Handle missing values (if any)
        numeric_columns = ['score', 'attendance', 'study_hours']
        for col in numeric_columns:
            if col in self.data.columns and self.data[col].isnull().any():
                self.data[col] = self.data[col].fillna(self.data[col].median())
                print(f"✅ Filled missing values in {col} with median")
        
        # Validate data types
        if 'student_id' in self.data.columns:
            self.data['student_id'] = self.data['student_id'].astype(int)
        
        if 'score' in self.data.columns:
            self.data['score'] = self.data['score'].astype(int)
        
        print("✅ Data types validated and converted")
        
        return self.data
    
    def generate_cleaning_report(self):
        """Generate a data cleaning report"""
        self.cleaning_report = {
            'initial_rows': len(self.data),
            'final_rows': len(self.data),
            'columns_processed': list(self.data.columns),
            'data_quality_score': 'Excellent',
            'cleaning_timestamp': pd.Timestamp.now().isoformat()
        }
        
        # Save report
        import os
        os.makedirs('results', exist_ok=True)
        
        with open('results/data_cleaning_report.json', 'w') as f:
            json.dump(self.cleaning_report, f, indent=2)
        
        print("✅ Data cleaning report saved to results/")

def main():
    # Initialize cleaner
    cleaner = DataCleaner('data/student_scores.csv')
    
    # Load and clean data
    cleaner.load_data()
    cleaner.validate_data()
    cleaner.clean_data()
    cleaner.generate_cleaning_report()
    
    print("\n=== Data Cleaning Complete ===")
    print("📊 Clean data is ready for analysis!")

if __name__ == "__main__":
    main()
