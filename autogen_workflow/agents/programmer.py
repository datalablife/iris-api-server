"""
Programmer Agent for AutoGen Programming Workflow

This module implements the Programmer agent responsible for writing clean,
efficient, and maintainable code based on architectural designs and requirements.
"""

from typing import List, Dict, Any, Optional
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient


class ProgrammerAgent:
    """
    Programmer Agent responsible for code implementation and development.
    
    This agent writes clean, efficient, and well-documented code following
    best practices and coding standards established by the architecture team.
    """
    
    def __init__(self, model_client: ChatCompletionClient, config: Dict[str, Any]):
        """
        Initialize the Programmer Agent.
        
        Args:
            model_client: The AI model client for generating responses
            config: Configuration dictionary containing agent settings
        """
        self.config = config
        self.agent = AssistantAgent(
            name=config["name"],
            model_client=model_client,
            description=config["description"],
            system_message=config["system_message"],
            handoffs=config["handoffs"]
        )
        
        # Code generation tracking
        self.code_artifacts = {
            "modules": [],
            "tests": [],
            "documentation": [],
            "configurations": []
        }
    
    def get_agent(self) -> AssistantAgent:
        """Get the underlying AutoGen AssistantAgent instance."""
        return self.agent
    
    def generate_project_structure(self, architecture: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate project structure based on architecture design.
        
        Args:
            architecture: Architecture design specifications
            
        Returns:
            Project structure with files and directories
        """
        structure = {
            "root": "data_analysis_api",
            "directories": {
                "app": {
                    "description": "Main application code",
                    "subdirectories": {
                        "api": "API endpoints and routes",
                        "core": "Core business logic",
                        "models": "Data models and schemas",
                        "services": "Business services",
                        "utils": "Utility functions",
                        "db": "Database related code"
                    }
                },
                "tests": {
                    "description": "Test files",
                    "subdirectories": {
                        "unit": "Unit tests",
                        "integration": "Integration tests",
                        "e2e": "End-to-end tests"
                    }
                },
                "docs": "Documentation files",
                "scripts": "Utility scripts",
                "config": "Configuration files",
                "requirements": "Dependency files"
            },
            "key_files": [
                "main.py",
                "requirements.txt",
                "Dockerfile",
                "docker-compose.yml",
                "README.md",
                ".env.example",
                "pytest.ini",
                ".gitignore"
            ]
        }
        
        return structure
    
    def create_fastapi_application(self) -> str:
        """Create the main FastAPI application code."""
        return '''"""
Data Analysis API Server - Main Application

This module contains the main FastAPI application with all routes,
middleware, and configuration for the data analysis API server.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn
import logging
from typing import AsyncGenerator

from app.core.config import settings
from app.core.database import database
from app.core.security import verify_token
from app.api.routes import data, analysis, visualization, auth
from app.core.logging import setup_logging


# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    logger.info("Starting Data Analysis API Server...")
    await database.connect()
    logger.info("Database connected successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Data Analysis API Server...")
    await database.disconnect()
    logger.info("Database disconnected")


# Create FastAPI application
app = FastAPI(
    title="Data Analysis API Server",
    description="High-performance API for data analysis and visualization",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)


# Dependency for authentication
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and return current user."""
    try:
        payload = verify_token(credentials.credentials)
        return payload
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "data-analysis-api",
        "version": "1.0.0"
    }


# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(
    data.router, 
    prefix="/api/v1/data", 
    tags=["Data Management"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    analysis.router, 
    prefix="/api/v1/analysis", 
    tags=["Data Analysis"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    visualization.router, 
    prefix="/api/v1/visualization", 
    tags=["Data Visualization"],
    dependencies=[Depends(get_current_user)]
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower()
    )
'''
    
    def create_database_models(self) -> str:
        """Create SQLAlchemy database models."""
        return '''"""
Database Models for Data Analysis API

This module contains SQLAlchemy models for the data analysis API,
including user management, data storage, and analysis results.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional

Base = declarative_base()


class User(Base):
    """User model for authentication and authorization."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    datasets = relationship("Dataset", back_populates="owner")
    analysis_jobs = relationship("AnalysisJob", back_populates="user")


class Dataset(Base):
    """Dataset model for storing uploaded data information."""
    
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(50), nullable=False)
    columns_info = Column(JSON, nullable=True)
    row_count = Column(Integer, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="datasets")
    analysis_jobs = relationship("AnalysisJob", back_populates="dataset")


class AnalysisJob(Base):
    """Analysis job model for tracking data analysis tasks."""
    
    __tablename__ = "analysis_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    analysis_type = Column(String(100), nullable=False)
    parameters = Column(JSON, nullable=True)
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    result = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="analysis_jobs")
    dataset = relationship("Dataset", back_populates="analysis_jobs")
    visualizations = relationship("Visualization", back_populates="analysis_job")


class Visualization(Base):
    """Visualization model for storing chart and graph information."""
    
    __tablename__ = "visualizations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    chart_type = Column(String(100), nullable=False)
    configuration = Column(JSON, nullable=False)
    file_path = Column(String(500), nullable=True)
    analysis_job_id = Column(Integer, ForeignKey("analysis_jobs.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    analysis_job = relationship("AnalysisJob", back_populates="visualizations")


class APIKey(Base):
    """API Key model for API access management."""
    
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    key_hash = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
'''
    
    def create_api_routes(self) -> Dict[str, str]:
        """Create API route modules."""
        routes = {}
        
        # Data management routes
        routes["data.py"] = '''"""
Data Management API Routes

This module contains API endpoints for data upload, management,
and basic operations on datasets.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
import os
import uuid
from datetime import datetime

from app.core.database import get_db
from app.models.database import Dataset, User
from app.schemas.data import DatasetCreate, DatasetResponse, DatasetList
from app.services.data_service import DataService
from app.core.config import settings

router = APIRouter()
data_service = DataService()


@router.post("/upload", response_model=DatasetResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    name: Optional[str] = None,
    description: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a new dataset file."""
    
    # Validate file type
    allowed_types = [".csv", ".xlsx", ".json", ".parquet"]
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_extension} not supported. Allowed types: {allowed_types}"
        )
    
    try:
        # Save file
        file_id = str(uuid.uuid4())
        file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{file_extension}")
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Analyze file
        dataset_info = await data_service.analyze_dataset(file_path, file_extension)
        
        # Create dataset record
        dataset = Dataset(
            name=name or file.filename,
            description=description,
            file_path=file_path,
            file_size=len(content),
            file_type=file_extension,
            columns_info=dataset_info["columns"],
            row_count=dataset_info["row_count"],
            owner_id=current_user["user_id"]
        )
        
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        
        return DatasetResponse.from_orm(dataset)
        
    except Exception as e:
        # Clean up file if database operation fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload dataset: {str(e)}"
        )


@router.get("/datasets", response_model=List[DatasetList])
async def list_datasets(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all datasets for the current user."""
    
    datasets = db.query(Dataset).filter(
        Dataset.owner_id == current_user["user_id"]
    ).offset(skip).limit(limit).all()
    
    return [DatasetList.from_orm(dataset) for dataset in datasets]


@router.get("/datasets/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(
    dataset_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific dataset."""
    
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.owner_id == current_user["user_id"]
    ).first()
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    return DatasetResponse.from_orm(dataset)


@router.delete("/datasets/{dataset_id}")
async def delete_dataset(
    dataset_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a dataset and its associated file."""
    
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.owner_id == current_user["user_id"]
    ).first()
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    # Delete file
    if os.path.exists(dataset.file_path):
        os.remove(dataset.file_path)
    
    # Delete database record
    db.delete(dataset)
    db.commit()
    
    return {"message": "Dataset deleted successfully"}
'''
        
        return routes
    
    def create_data_service(self) -> str:
        """Create data processing service."""
        return '''"""
Data Service for Data Analysis API

This module contains business logic for data processing,
analysis, and manipulation operations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import json
import os
from pathlib import Path

from app.core.config import settings


class DataService:
    """Service class for data processing operations."""
    
    def __init__(self):
        self.supported_formats = {
            ".csv": self._read_csv,
            ".xlsx": self._read_excel,
            ".json": self._read_json,
            ".parquet": self._read_parquet
        }
    
    async def analyze_dataset(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """
        Analyze a dataset and return metadata information.
        
        Args:
            file_path: Path to the dataset file
            file_type: Type of the file (.csv, .xlsx, etc.)
            
        Returns:
            Dictionary containing dataset metadata
        """
        try:
            # Read the dataset
            df = await self._read_dataset(file_path, file_type)
            
            # Basic information
            info = {
                "row_count": len(df),
                "column_count": len(df.columns),
                "columns": [],
                "memory_usage": df.memory_usage(deep=True).sum(),
                "has_null_values": df.isnull().any().any(),
                "duplicate_rows": df.duplicated().sum()
            }
            
            # Column analysis
            for column in df.columns:
                col_info = {
                    "name": column,
                    "dtype": str(df[column].dtype),
                    "null_count": df[column].isnull().sum(),
                    "unique_count": df[column].nunique(),
                    "sample_values": df[column].dropna().head(5).tolist()
                }
                
                # Add statistics for numeric columns
                if df[column].dtype in ['int64', 'float64']:
                    col_info.update({
                        "min": float(df[column].min()) if not pd.isna(df[column].min()) else None,
                        "max": float(df[column].max()) if not pd.isna(df[column].max()) else None,
                        "mean": float(df[column].mean()) if not pd.isna(df[column].mean()) else None,
                        "std": float(df[column].std()) if not pd.isna(df[column].std()) else None
                    })
                
                info["columns"].append(col_info)
            
            return info
            
        except Exception as e:
            raise Exception(f"Failed to analyze dataset: {str(e)}")
    
    async def _read_dataset(self, file_path: str, file_type: str) -> pd.DataFrame:
        """Read dataset based on file type."""
        if file_type not in self.supported_formats:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        return self.supported_formats[file_type](file_path)
    
    def _read_csv(self, file_path: str) -> pd.DataFrame:
        """Read CSV file."""
        return pd.read_csv(file_path)
    
    def _read_excel(self, file_path: str) -> pd.DataFrame:
        """Read Excel file."""
        return pd.read_excel(file_path)
    
    def _read_json(self, file_path: str) -> pd.DataFrame:
        """Read JSON file."""
        return pd.read_json(file_path)
    
    def _read_parquet(self, file_path: str) -> pd.DataFrame:
        """Read Parquet file."""
        return pd.read_parquet(file_path)
    
    async def get_dataset_preview(self, file_path: str, file_type: str, rows: int = 10) -> Dict[str, Any]:
        """Get a preview of the dataset."""
        try:
            df = await self._read_dataset(file_path, file_type)
            
            preview = {
                "columns": df.columns.tolist(),
                "data": df.head(rows).to_dict('records'),
                "total_rows": len(df),
                "preview_rows": min(rows, len(df))
            }
            
            return preview
            
        except Exception as e:
            raise Exception(f"Failed to generate dataset preview: {str(e)}")
    
    async def validate_dataset(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Validate dataset for common issues."""
        try:
            df = await self._read_dataset(file_path, file_type)
            
            validation = {
                "is_valid": True,
                "issues": [],
                "warnings": [],
                "recommendations": []
            }
            
            # Check for empty dataset
            if len(df) == 0:
                validation["is_valid"] = False
                validation["issues"].append("Dataset is empty")
            
            # Check for columns with all null values
            null_columns = df.columns[df.isnull().all()].tolist()
            if null_columns:
                validation["warnings"].append(f"Columns with all null values: {null_columns}")
            
            # Check for duplicate rows
            duplicate_count = df.duplicated().sum()
            if duplicate_count > 0:
                validation["warnings"].append(f"Found {duplicate_count} duplicate rows")
                validation["recommendations"].append("Consider removing duplicate rows")
            
            # Check for mixed data types in columns
            for column in df.columns:
                if df[column].dtype == 'object':
                    # Try to identify mixed types
                    sample = df[column].dropna().head(100)
                    if len(sample) > 0:
                        types = set(type(x).__name__ for x in sample)
                        if len(types) > 1:
                            validation["warnings"].append(f"Column '{column}' has mixed data types: {types}")
            
            return validation
            
        except Exception as e:
            return {
                "is_valid": False,
                "issues": [f"Failed to validate dataset: {str(e)}"],
                "warnings": [],
                "recommendations": []
            }
'''
    
    def create_unit_tests(self) -> str:
        """Create unit test template."""
        return '''"""
Unit Tests for Data Analysis API

This module contains comprehensive unit tests for the data analysis API,
covering all major functionality and edge cases.
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os
import pandas as pd

from main import app
from app.core.database import get_db, Base
from app.models.database import User, Dataset
from app.core.security import create_access_token


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    """Set up test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user():
    """Create a test user."""
    db = TestingSessionLocal()
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password",
        full_name="Test User"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.delete(user)
    db.commit()
    db.close()


@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers."""
    token = create_access_token(data={"sub": test_user.email, "user_id": test_user.id})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_csv_file():
    """Create a sample CSV file for testing."""
    data = {
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "salary": [50000, 60000, 70000]
    }
    df = pd.DataFrame(data)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        yield f.name
    
    os.unlink(f.name)


class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test health check endpoint returns correct response."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_login_success(self, setup_database, test_user):
        """Test successful login."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": test_user.email, "password": "password"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    def test_login_invalid_credentials(self, setup_database):
        """Test login with invalid credentials."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "invalid@example.com", "password": "wrong"}
        )
        assert response.status_code == 401


class TestDataUpload:
    """Test data upload functionality."""
    
    def test_upload_csv_success(self, setup_database, auth_headers, sample_csv_file):
        """Test successful CSV file upload."""
        with open(sample_csv_file, 'rb') as f:
            response = client.post(
                "/api/v1/data/upload",
                files={"file": ("test.csv", f, "text/csv")},
                headers=auth_headers
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "test.csv"
        assert data["file_type"] == ".csv"
        assert data["row_count"] == 3
    
    def test_upload_unsupported_file_type(self, setup_database, auth_headers):
        """Test upload of unsupported file type."""
        with tempfile.NamedTemporaryFile(suffix='.txt') as f:
            f.write(b"test content")
            f.seek(0)
            
            response = client.post(
                "/api/v1/data/upload",
                files={"file": ("test.txt", f, "text/plain")},
                headers=auth_headers
            )
        
        assert response.status_code == 400
        assert "not supported" in response.json()["detail"]
    
    def test_upload_without_auth(self, sample_csv_file):
        """Test upload without authentication."""
        with open(sample_csv_file, 'rb') as f:
            response = client.post(
                "/api/v1/data/upload",
                files={"file": ("test.csv", f, "text/csv")}
            )
        
        assert response.status_code == 401


class TestDataService:
    """Test data service functionality."""
    
    @pytest.mark.asyncio
    async def test_analyze_dataset(self, sample_csv_file):
        """Test dataset analysis."""
        from app.services.data_service import DataService
        
        service = DataService()
        result = await service.analyze_dataset(sample_csv_file, ".csv")
        
        assert result["row_count"] == 3
        assert result["column_count"] == 3
        assert len(result["columns"]) == 3
        
        # Check column information
        name_column = next(col for col in result["columns"] if col["name"] == "name")
        assert name_column["dtype"] == "object"
        assert name_column["unique_count"] == 3
    
    @pytest.mark.asyncio
    async def test_dataset_preview(self, sample_csv_file):
        """Test dataset preview generation."""
        from app.services.data_service import DataService
        
        service = DataService()
        preview = await service.get_dataset_preview(sample_csv_file, ".csv", rows=2)
        
        assert preview["total_rows"] == 3
        assert preview["preview_rows"] == 2
        assert len(preview["data"]) == 2
        assert "name" in preview["columns"]
    
    @pytest.mark.asyncio
    async def test_dataset_validation(self, sample_csv_file):
        """Test dataset validation."""
        from app.services.data_service import DataService
        
        service = DataService()
        validation = await service.validate_dataset(sample_csv_file, ".csv")
        
        assert validation["is_valid"] is True
        assert len(validation["issues"]) == 0


if __name__ == "__main__":
    pytest.main([__file__])
'''
    
    def get_code_templates(self) -> Dict[str, str]:
        """Get various code templates for different components."""
        return {
            "fastapi_app": self.create_fastapi_application(),
            "database_models": self.create_database_models(),
            "data_routes": self.create_api_routes()["data.py"],
            "data_service": self.create_data_service(),
            "unit_tests": self.create_unit_tests()
        }

    def create_dockerfile(self) -> str:
        """Create Dockerfile for the application."""
        return '''# Multi-stage Dockerfile for Data Analysis API
FROM python:3.9-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Create and set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set work directory
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Change ownership to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

    def create_docker_compose(self) -> str:
        """Create docker-compose.yml for development."""
        return '''version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/dataapi
      - REDIS_URL=redis://redis:6379
      - ENVIRONMENT=development
    depends_on:
      - db
      - redis
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=dataapi
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  worker:
    build: .
    command: celery -A app.core.celery worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/dataapi
      - REDIS_URL=redis://redis:6379
      - ENVIRONMENT=development
    depends_on:
      - db
      - redis
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
'''
