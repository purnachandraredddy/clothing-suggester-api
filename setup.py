#!/usr/bin/env python3
"""
Setup script for the Clothing Recommendation System

This script allows easy installation and distribution of the project.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    """Read the README.md file."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Clothing Recommendation System"

# Read requirements
def read_requirements():
    """Read the requirements.txt file."""
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="clothing-recommender",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered clothing suggestions based on weather conditions",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/clothing-recommender",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docker": [
            "gunicorn>=20.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "train-clothing-model=train_model:main",
            "run-clothing-api=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.joblib", "*.csv", "*.json"],
    },
    keywords="machine-learning, flask, api, clothing, weather, recommendation",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/clothing-recommender/issues",
        "Source": "https://github.com/yourusername/clothing-recommender",
        "Documentation": "https://github.com/yourusername/clothing-recommender#readme",
    },
) 