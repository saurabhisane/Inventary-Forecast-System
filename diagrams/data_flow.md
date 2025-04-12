<!-- ```mermaid
flowchart LR
    subgraph UI[User Interface]
        A[Web Browser] --> B[File Upload]
    end

    subgraph Processing[Data Processing]
        C[Data Validation] --> D[Data Cleaning]
        D --> E[Feature Engineering]
    end

    subgraph ML[Machine Learning]
        F[Prophet Model] --> G[Forecast Generation]
        G --> H[Pattern Analysis]
    end

    subgraph VIS[Visualization]
        I[Chart Generation] --> J[Interactive Display]
        J --> K[Report Generation]
    end

    B --> C
    E --> F
    H --> I

    style UI fill:#2196F3,stroke:#fff,stroke-width:2px
    style Processing fill:#4CAF50,stroke:#fff,stroke-width:2px
    style ML fill:#FFC107,stroke:#fff,stroke-width:2px
    style VIS fill:#FF5722,stroke:#fff,stroke-width:2px
```

# Data Flow Description

## 1. User Interface Layer
Input: CSV files with historical inventory/sales data
Output: File transfer to processing layer

## 2. Data Processing Layer
Input: Raw CSV data
Process: 
- Data validation
- Cleaning
- Feature engineering
Output: Processed dataset

## 3. Machine Learning Layer
Input: Processed dataset
Process:
- Prophet model training
- Forecast generation
- Pattern recognition
Output: Predictions and patterns

## 4. Visualization Layer
Input: Analysis results
Process:
- Chart generation
- Interactive visualization
- Report compilation
Output: User-friendly insights  -->