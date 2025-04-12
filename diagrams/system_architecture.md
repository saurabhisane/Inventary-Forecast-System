<!-- graph TD
    %% Main Layers
    subgraph "Client Layer"
        A[Web Browser]
        B[User Interface]
    end

    subgraph "Application Layer"
        C[Flask Web Server]
        D[Data Processor]
        E[Prophet Model]
        F[Visualization Engine]
    end

    subgraph "Storage Layer"
        G[Temporary Storage]
    end

    subgraph "Output Layer"
        H[Results Dashboard]
    end

    %% Connections
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> H
    C --> G
    G --> D

    %% Styling
    classDef clientLayer fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef appLayer fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef storageLayer fill:#FFC107,stroke:#FF8F00,stroke-width:2px,color:#000
    classDef outputLayer fill:#FF5722,stroke:#D84315,stroke-width:2px,color:#fff

    class A,B clientLayer
    class C,D,E,F appLayer
    class G storageLayer
    class H outputLayer -->