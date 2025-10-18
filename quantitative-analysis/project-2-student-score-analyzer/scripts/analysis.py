import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json
import os

class StudentScoreAnalyzer:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.results = {}
    
    def load_data(self):
        """Load and display basic info about the dataset"""
        print("=== Student Score Data Overview ===")
        print(f"Dataset shape: {self.data.shape}")
        print("\nFirst 5 rows:")
        print(self.data.head())
        print("\nData types:")
        print(self.data.dtypes)
        print("\nMissing values:")
        print(self.data.isnull().sum())
        print("\nBasic statistics:")
        print(self.data['score'].describe())
        
        return self.data
    
    def subject_performance(self):
        """Analyze performance by subject"""
        subject_stats = self.data.groupby('subject').agg({
            'score': ['mean', 'median', 'std', 'count'],
            'attendance': 'mean',
            'study_hours': 'mean'
        }).round(2)
        
        print("\n=== Subject Performance ===")
        print(subject_stats)
        
        self.results['subject_performance'] = subject_stats
        return subject_stats
    
    def class_comparison(self):
        """Compare performance between classes"""
        class_stats = self.data.groupby('class').agg({
            'score': ['mean', 'median', 'std'],
            'attendance': 'mean',
            'study_hours': 'mean'
        }).round(2)
        
        print("\n=== Class Comparison ===")
        print(class_stats)
        
        self.results['class_comparison'] = class_stats
        return class_stats
    
    def correlation_analysis(self):
        """Analyze correlations between variables"""
        numeric_columns = ['score', 'attendance', 'study_hours']
        correlation_matrix = self.data[numeric_columns].corr()
        
        print("\n=== Correlation Analysis ===")
        print(correlation_matrix)
        
        # Convert to regular Python types for JSON serialization
        self.results['correlations'] = correlation_matrix.round(4).to_dict()
        return correlation_matrix
    
    def grade_distribution(self):
        """Calculate grade distribution"""
        def assign_grade(score):
            if score >= 90: return 'A'
            elif score >= 80: return 'B'
            elif score >= 70: return 'C'
            elif score >= 60: return 'D'
            else: return 'F'
        
        self.data['grade'] = self.data['score'].apply(assign_grade)
        grade_dist = self.data['grade'].value_counts().sort_index()
        
        print("\n=== Grade Distribution ===")
        print(grade_dist)
        
        self.results['grade_distribution'] = grade_dist.to_dict()
        return grade_dist
    
    def factor_analysis(self):
        """Analyze impact of various factors on scores"""
        # Parent education impact
        education_impact = self.data.groupby('parent_education')['score'].mean().sort_values(ascending=False)
        
        # Extracurricular impact
        extracurricular_impact = self.data.groupby('extracurricular')['score'].mean()
        
        print("\n=== Factor Analysis ===")
        print("Impact of Parent Education:")
        print(education_impact)
        print("\nImpact of Extracurricular Activities:")
        print(extracurricular_impact)
        
        self.results['education_impact'] = education_impact.round(2).to_dict()
        self.results['extracurricular_impact'] = extracurricular_impact.round(2).to_dict()
        
        return education_impact, extracurricular_impact
    
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # 1. Score distribution histogram
        axes[0,0].hist(self.data['score'], bins=10, color='skyblue', edgecolor='black', alpha=0.7)
        axes[0,0].set_title('Score Distribution')
        axes[0,0].set_xlabel('Score')
        axes[0,0].set_ylabel('Frequency')
        
        # 2. Subject comparison
        subject_means = self.data.groupby('subject')['score'].mean()
        axes[0,1].bar(subject_means.index, subject_means.values, color='lightcoral')
        axes[0,1].set_title('Average Scores by Subject')
        axes[0,1].set_ylabel('Average Score')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # 3. Class comparison
        class_means = self.data.groupby('class')['score'].mean()
        axes[0,2].bar(class_means.index, class_means.values, color='lightgreen')
        axes[0,2].set_title('Average Scores by Class')
        axes[0,2].set_ylabel('Average Score')
        
        # 4. Study hours vs Score scatter plot
        axes[1,0].scatter(self.data['study_hours'], self.data['score'], alpha=0.6, color='purple')
        axes[1,0].set_xlabel('Study Hours')
        axes[1,0].set_ylabel('Score')
        axes[1,0].set_title('Study Hours vs Score')
        
        # 5. Attendance vs Score
        axes[1,1].scatter(self.data['attendance'], self.data['score'], alpha=0.6, color='orange')
        axes[1,1].set_xlabel('Attendance (%)')
        axes[1,1].set_ylabel('Score')
        axes[1,1].set_title('Attendance vs Score')
        
        # 6. Grade distribution
        grade_dist = self.data['grade'].value_counts().sort_index()
        axes[1,2].pie(grade_dist.values, labels=grade_dist.index, autopct='%1.1f%%')
        axes[1,2].set_title('Grade Distribution')
        
        plt.tight_layout()
        plt.savefig('results/student_performance_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_results(self):
        """Save analysis results to files"""
        os.makedirs('results', exist_ok=True)
        
        # Save statistical results
        with open('results/statistical_analysis.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Save detailed report
        self.generate_report()
        
        print("✅ Results saved to 'results/' folder")
    
    def generate_report(self):
        """Generate a comprehensive analysis report"""
        report = f"""
# Student Score Analysis Report

## Executive Summary
- **Total Students Analyzed**: {len(self.data)}
- **Average Score**: {self.data['score'].mean():.2f}
- **Highest Score**: {self.data['score'].max()}
- **Lowest Score**: {self.data['score'].min()}

## Key Findings

### 📊 Performance by Subject
{self.results.get('subject_performance', {}).to_string() if 'subject_performance' in self.results else 'N/A'}

### 🏫 Class Performance Comparison
{self.results.get('class_comparison', {}).to_string() if 'class_comparison' in self.results else 'N/A'}

### 📈 Correlation Insights
- Study Hours vs Score: {self.results.get('correlations', {}).get('score', {}).get('study_hours', 'N/A')}
- Attendance vs Score: {self.results.get('correlations', {}).get('score', {}).get('attendance', 'N/A')}

### 🎯 Recommendations
1. Focus on improving performance in lower-scoring subjects
2. Encourage consistent study habits
3. Monitor attendance patterns
4. Provide additional support for students from certain educational backgrounds

---
*Report generated on: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}*
"""
        
        with open('results/performance_report.md', 'w') as f:
            f.write(report)

def main():
    # Initialize analyzer
    analyzer = StudentScoreAnalyzer('data/student_scores.csv')
    
    # Run analyses
    analyzer.load_data()
    analyzer.subject_performance()
    analyzer.class_comparison()
    analyzer.correlation_analysis()
    analyzer.grade_distribution()
    analyzer.factor_analysis()
    
    # Save results
    analyzer.save_results()
    
    print("\n=== Student Score Analysis Complete ===")
    print("📊 Check the 'results' folder for generated files!")

if __name__ == "__main__":
    main()
