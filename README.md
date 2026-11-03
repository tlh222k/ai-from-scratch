# AI From Scratch

**A structured journey into Artificial Intelligence, Machine Learning, and Deep Learning — from mathematical foundations to practical implementations.**

[![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-013243?logo=numpy)](https://numpy.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Visualization-3F4F75?logo=plotly)](https://plotly.com/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Learning](https://img.shields.io/badge/Status-Actively%20Learning-success)]()

---

## Overview

**AI From Scratch** is a personal learning repository dedicated to understanding the foundations of Artificial Intelligence through mathematics, programming, experimentation, and practical implementation.

Rather than simply using existing AI libraries and frameworks, this project focuses on understanding how things work internally — from mathematical operations and fundamental machine learning algorithms to neural networks and deep learning architectures.

The repository combines:

- **Mathematical Foundations:** Linear Algebra, Calculus, Probability, and Statistics.
- **Programming Foundations:** Python, NumPy, and scientific computing.
- **Machine Learning:** Fundamental algorithms, optimization, and model evaluation.
- **Deep Learning:** Neural networks, backpropagation, and deep learning architectures.
- **Interactive Visualizations:** Visual explanations of mathematical and machine learning concepts.
- **Hands-on Implementations:** Experiments, notebooks, and implementations from scratch.

The ultimate goal is to develop strong theoretical foundations and practical engineering skills for building AI systems.

## Learning Roadmap

The repository is organized into progressive learning phases.

### Phase 00 — Math Foundations

Build the mathematical intuition required to understand Machine Learning and Deep Learning.

Topics:

- Linear Algebra
- Vectors and Matrices
- Matrix Operations
- Functions and Graphs
- Calculus
- Derivatives and Gradients
- Probability and Statistics

### Phase 01 — Setup and Tooling

Establish a reliable development environment and become familiar with the tools used in AI development.

Topics:

- Python Environment Setup
- Virtual Environments
- Python Package Management
- NumPy
- Jupyter Notebook
- Development Tools and Workflow

### Phase 02 — Machine Learning Fundamentals

Understand the fundamental principles behind machine learning algorithms.

Topics:

- Introduction to Machine Learning
- Supervised Learning
- Regression
- Classification
- Loss Functions
- Gradient Descent
- Model Evaluation
- Overfitting and Underfitting

### Phase 03 — Deep Learning Core

Explore how neural networks learn representations and solve complex problems.

Topics:

- Artificial Neural Networks
- Perceptrons
- Multi-Layer Perceptrons (MLPs)
- Activation Functions
- Forward Propagation
- Backpropagation
- Optimization Algorithms
- Training Neural Networks

> The roadmap is continuously evolving as new concepts, experiments, and learning materials are added.

## Repository Structure

```text
ai-from-scratch/
│
├── images/
│   └── # Images and learning illustrations
│
├── phases/
│   ├── 00-math-foundations/
│   │   └── # Mathematical foundations
│   │
│   ├── 01-setup-and-tooling/
│   │   └── # Development environment and tools
│   │
│   ├── 02-ml-fundamentals/
│   │   └── # Machine Learning fundamentals
│   │
│   └── 03-deep-learning-core/
│       └── # Deep Learning concepts and implementations
│
├── visualizations/
│   ├── notebooks/
│   │   └── function_visualization.ipynb
│   │
│   ├── index.html
│   ├── linear_function.html
│   └── quadratic_function.html
│
├── .venv/
│
├── requirements.txt
│
└── README.md
```

## Interactive Visualizations

Visual intuition is an important part of understanding mathematical and machine learning concepts.

This repository includes interactive visualizations built with **Plotly**, allowing learners to explore mathematical functions and understand how inputs affect outputs.

### Current Visualizations

| Visualization | Description |
|---|---|
| Linear Function | Explore the behavior of \(f(x) = 2x + 1\). |
| Quadratic Function | Explore the behavior of \(g(x) = x^2\). |

### Explore the Visualizations

If GitHub Pages is enabled for this repository, access the interactive visualizations here:

**[Open Interactive Visualizations](https://tlh222k.github.io/ai-from-scratch/visualizations/)**

Individual visualizations:

- [Linear Function](https://tlh222k.github.io/ai-from-scratch/visualizations/linear_function.html)
- [Quadratic Function](https://tlh222k.github.io/ai-from-scratch/visualizations/quadratic_function.html)

## Getting Started

### Prerequisites

Make sure you have installed:

- Python 3.13 or a compatible Python version.
- Git.
- Visual Studio Code (recommended).
- Jupyter Notebook or JupyterLab.

### 1. Clone the Repository

```bash
git clone https://github.com/tlh222k/ai-from-scratch.git

cd ai-from-scratch
```

### 2. Create a Virtual Environment

**Windows:**

```powershell
python -m venv .venv

.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```

### 4. Register the Jupyter Kernel

```bash
python -m ipykernel install --user --name ai-from-scratch --display-name "Python (AI From Scratch)"
```

### 5. Launch Jupyter

```bash
jupyter lab
```

Open the notebooks inside the repository and select the **Python (AI From Scratch)** kernel.

## Technologies and Tools

| Technology | Purpose |
|---|---|
| Python | Primary programming language |
| NumPy | Numerical computing and linear algebra |
| Plotly | Interactive data visualization |
| Jupyter Notebook | Experiments and interactive learning |
| Git & GitHub | Version control and project management |
| GitHub Pages | Hosting interactive HTML visualizations |

Additional libraries and frameworks will be introduced as the learning roadmap progresses.

## Learning Philosophy

This repository follows a learning approach built around understanding rather than memorization.

**1. Understand the fundamentals**

Learn the mathematical and theoretical foundations before relying on high-level abstractions.

**2. Build mathematical intuition**

Use equations, examples, and visualizations to understand why algorithms work.

**3. Implement from scratch**

Reimplement fundamental algorithms using Python and NumPy to understand their internal mechanisms.

**4. Experiment and analyze**

Change parameters, observe results, investigate errors, and understand model behavior.

**5. Connect theory with practice**

Progress from mathematical concepts to working implementations and practical AI applications.

## Learning Progress

The repository is continuously updated as new topics and implementations are completed.

- [x] Initial repository structure
- [x] Interactive Linear Function visualization
- [x] Interactive Quadratic Function visualization
- [ ] Complete Mathematical Foundations
- [ ] Complete Machine Learning Fundamentals
- [ ] Implement fundamental ML algorithms from scratch
- [ ] Complete Deep Learning Core
- [ ] Implement neural networks from scratch

---

**Learn deeply. Build from scratch. Understand how AI works.**
