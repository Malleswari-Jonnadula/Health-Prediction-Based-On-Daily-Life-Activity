# 🩺Health-Prediction-Based-On-Daily-Life-Activity-Using-Machine-Learning
This project uses Machine Learning to predict a person’s health risk level based on their daily activity patterns such as step count, heart rate, and sleep hours. By applying unsupervised clustering techniques like K-Means and Agglomerative Clustering, the model groups users into three health categories like Normal,Mild and Severe. It helps users understand their overall lifestyle health and take preventive actions early.

## 🔗Live Demo


👉[Click here to open the deployed Streamlit app](https://health-prediction-based-on-life-activity.streamlit.app/)


## 🧠Problem Statement
Most existing systems focus only on specific illnesses and ignore key health indicators like blood pressure, stress, and heart activity. This limits their ability to give a complete view of a person’s well-being.
This project aims to build a smarter, more comprehensive health prediction system. It analyzes multiple health parameters together to identify risk levels and give users actionable insights. 

## 🛠️Technologies & Libraries Used:
### 🤖 Machine Learning & Data Processing
- **Python** – Core language for data processing, ML and backend development
- **Scikit-learn** – K-Means and Agglomerative Clustering , StandardScaler
- **Pandas & NumPy** – Data handling, analysis and data manipulation
- **Silhouette Score** – Clustering performance evaluation

### 📊 Data Visualization & Analytics
- **Matplotlib & Seaborn** – For generating cluster plots, heatmaps, and correlation analysis
- **Plotly** – To build interactive graphs for real-time user insights

### 🧑‍💻 User Interface
- **Streamlit** – Built the user-friendly interactive web UI 
- **HTML & CSS** – Used for customizing frontend elements inside the Streamlit app

### 🗃️ Database
- **SQLite** – Stores user profiles, prediction results, and daily health data locally

