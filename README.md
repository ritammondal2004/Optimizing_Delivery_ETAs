# 👨‍💻 Author

## Ritam Mondal

*  IIT Kharagpur
*  ML & Data Analytics Enthusiast
*  Optimization & Graph Intelligence Research

### 📬 Contact

* Email: [ritamm134@gmail.com](mailto:ritamm134@gmail.com)
* LinkedIn: https://www.linkedin.com/in/ritam-mondal-86a369287/
* GitHub: https://github.com/ritammondal2004

````markdown
<h1 align="center">🚚 Graph-Based Network Intelligence for Delivery Time Prediction</h1>

<p align="center">
  Intelligent ETA prediction system using Machine Learning, Graph Analytics, and Real-Time Route Intelligence
</p>

<br>

<p align="center">
  <a href="https://www.linkedin.com/in/ritam-mondal-86a369287/" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-blue?logo=linkedin&logoColor=white&style=for-the-badge"/>
  </a>

  <a href="mailto:ritamm134@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-red?logo=gmail&logoColor=white&style=for-the-badge"/>
  </a>

  <a href="https://github.com/ritammondal2004" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-black?logo=github&logoColor=white&style=for-the-badge"/>
  </a>
</p>

---

#  Overview

This project is an advanced **ETA (Estimated Time of Arrival) Prediction System** designed for intelligent logistics and delivery optimization.

The system combines:

-  Machine Learning
-  Graph-Based Network Intelligence
-  Route Optimization
-  Real-Time Distance Analysis
-  Interactive Geospatial Visualization

to accurately estimate delivery times between facilities and cities.

The application is fully deployed using **Streamlit Cloud** and provides an interactive web interface for live ETA prediction.

---

# 🚀 Live Demo

🔗 **Deployed Application:**  
https://optimizingdeliveryetas-g6gq58lfhiwt4d83aj5zox.streamlit.app/

---

# ✨ Features

-  Intelligent ETA prediction
-  Graph-based route intelligence
-  Facility resolution using fuzzy matching
-  Real-time map visualization
-  Interactive Folium maps
-  Machine learning powered predictions
-  Distance-aware route estimation
-  Clean Streamlit dashboard
-  Public cloud deployment

---

# 🧠 Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Core backend |
| Streamlit | Web application |
| Scikit-Learn | ML modeling |
| XGBoost | Advanced prediction |
| NetworkX | Graph analytics |
| Folium | Interactive maps |
| Pandas | Data processing |
| NumPy | Numerical computations |

---

# 📂 Project Structure

```bash
├── app.py
├── requirements.txt
├── runtime.txt
├── delivery_data.csv
├── df_train.csv
├── df_test.csv
│
├── ProcessingData/
│   ├── ETA_prediction.py
│   ├── Resolve_Facility.py
│   ├── load_models.py
│   ├── OsrmApiDistance.py
│
├── all_models/
│   ├── graph.pkl
│   ├── model.pkl
│   ├── encoder.pkl
│   └── ...
├── Notebooks/
│   ├── ETA_prediction_map.ipynb
│   ├── ETA_project_data_observation.ipynb
│   
│   

````

---

# ⚙️ Installation

## 1️. Clone Repository

```bash
git clone https://github.com/ritammondal2004/optimizing_delivery_etas.git
```

---

## 2️. Navigate to Project Folder

```bash
cd optimizing_delivery_etas
```

---

## 3️. Create Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 4️. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# 🌍 Deployment

This project is deployed using:

* Streamlit Community Cloud
* GitHub Integration
* Public Cloud Hosting

---

#  Core Functionalities

##  ETA Prediction

Predicts estimated delivery time using:

* source location
* destination location
* route type
* graph intelligence
* historical delivery patterns

---

##  Graph Analytics

Uses graph-based metrics such as:

* betweenness centrality
* in-degree
* out-degree
* route connectivity

to improve ETA accuracy.

---

##  Interactive Mapping

The application visualizes:

* delivery locations
* route paths
* source/destination mapping
* geographical insights

using Folium maps.

---

#  Machine Learning Pipeline

The system uses:

* feature engineering
* graph-based features
* preprocessing pipelines
* trained regression models

for intelligent delivery prediction.

---

# 🧪 Requirements

```txt
streamlit==1.45.1
streamlit-folium==0.26.2
folium==0.20.0
pandas==2.2.3
numpy==2.2.6
scikit-learn==1.7.0
xgboost==3.0.2
networkx==3.4.2
joblib==1.5.1
requests==2.32.4
```

---



---

#  Future Improvements

* Live traffic integration
* Real-time GPS tracking
* Advanced route optimization
* Multi-vehicle scheduling
* Deep learning based ETA estimation
* API deployment using FastAPI

---





