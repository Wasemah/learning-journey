# Configuration settings for Student Score Analyzer Project

# Data Configuration
DATA_CONFIG = {
    'data_path': 'data/student_scores.csv',
    'primary_key': 'student_id',
    'score_column': 'score',
    'categorical_columns': ['class', 'subject', 'parent_education', 'extracurricular'],
    'numerical_columns': ['score', 'attendance', 'study_hours']
}

# Analysis Configuration
ANALYSIS_CONFIG = {
    'grade_thresholds': {
        'A': 90,
        'B': 80,
        'C': 70,
        'D': 60,
        'F': 0
    },
    'passing_score': 60,
    'high_performance_threshold': 85,
    'low_performance_threshold': 70,
    'subjects': ['Mathematics', 'Science', 'English', 'History'],
    'classes': ['10A', '10B']
}

# Visualization Configuration
VISUALIZATION_CONFIG = {
    'style': 'seaborn-v0_8',
    'color_palette': {
        'excellent': '#28A745',
        'good': '#20C997',
        'average': '#FFC107',
        'poor': '#FD7E14',
        'failing': '#DC3545'
    },
    'figure_size': (12, 8),
    'dpi': 300,
    'save_format': 'png'
}

# Report Configuration
REPORT_CONFIG = {
    'generate_pdf_report': False,
    'include_student_names': True,
    'include_detailed_stats': True,
    'output_formats': ['json', 'md', 'csv']
}

# Statistical Analysis Configuration
STATS_CONFIG = {
    'confidence_level': 0.95,
    'correlation_threshold': 0.5,
    'outlier_threshold': 2.0  # Standard deviations
}
