# 🔒 Malicious URL Classifier - Learning Project

> **⚠️ Educational Purpose Notice**: This is a **learning project** developed to understand ML application development. It demonstrates core concepts but has limitations in real-world accuracy.

A machine learning web application that detects potentially malicious URLs using classification algorithms and rule-based analysis. **Built for educational purposes to showcase full-stack ML development skills.**

## 🎯 Project Purpose & Scope

**This project was created to learn:**
- End-to-end machine learning application development
- Flask web API development and deployment  
- Frontend-backend integration patterns
- Model serialization and serving
- Building user feedback systems
- Web security concepts and threat detection methodologies

**🔬 Important Note**: This is a **demonstration project** with known accuracy limitations. Not recommended for production security use.

## 🚀 Features

- **Real-time URL Analysis** - Instant scanning with educational purpose
- **Dual Detection System** - Combines machine learning and rule-based methods
- **Confidence Scoring** - Probability-based certainty indicators
- **User Feedback System** - Report inaccurate classifications
- **Clean Web Interface** - Simple, intuitive design for demonstration

## 📊 Current Implementation Status

### ✅ What's Implemented (Learning Goals Achieved)
- Complete full-stack application architecture
- Real-time URL classification system
- Dual-layer detection (ML + rule-based)
- User feedback collection system
- Web interface with responsive design

### 🔧 Known Limitations & Learning Points
- **Training Data**: Model trained on limited historical dataset for learning purposes
- **Accuracy**: Performance varies - demonstrates the importance of quality data
- **Feature Engineering**: Basic features used to understand ML pipeline concepts
- **Scope**: Best suited for educational demonstration and portfolio purposes

## 🖥️ Demo Output
**Sample Classification Results:**
🟢 Safe | Confidence: 99.00% | Method: rule_based_safe
🔴 Malicious | Confidence: 85.00% | Method: ml_classification

## 🏗️ Project Structure
MALICIOUSURLCLASSIFIER/
├── backend/ # Flask API & ML model
│ ├── app.py # Main application server
│ ├── url_classifier.pkl # Trained ML model (learning model)
│ └── feedback_data.json # User reporting data
├── frontend/ # Web interface
│ ├── index.html # Main page
│ ├── style.css # Styling
│ └── script.js # Client-side logic
├── requirements.txt # Python dependencies
├── test_request.py # API testing utility
└── README.md # Project documentation

## ⚡ Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/DG-ROHITHA/malicious-url-classifier
   cd malicious-url-classifier
   
**2. Install dependencies:**

pip install -r requirements.txt

**3. Run the application:**

cd backend
python app.py