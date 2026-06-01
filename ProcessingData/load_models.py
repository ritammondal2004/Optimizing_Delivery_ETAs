# Load everything back
import warnings
warnings.filterwarnings('ignore', message=".*numexpr.*")
warnings.filterwarnings('ignore', message=".*XGBoost.*")
warnings.filterwarnings('ignore', category=UserWarning, module='xgboost')

import pickle
import os

# ProcessingData/load_models.py
import pickle
import os

# ── Path to models folder ────────────────────────────────────
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'all_models')

def load_all():
    def load(filename):
        path = os.path.join(MODELS_DIR, filename)
        with open(path, 'rb') as f:
            return pickle.load(f)

    models = {
        'G'                   : load('graph.pkl'),
        'betweenness'         : load('betweenness.pkl'),
        'in_degree'           : load('in_degree.pkl'),
        'out_degree'          : load('out_degree.pkl'),
        'edge_weights'        : load('edge_weights.pkl'),
        'graph_model'         : load('graph_final_model.pkl'),
        'baseline_model'      : load('baseline_final_model.pkl'),
        'le'                  : load('label_encoder.pkl'),
        'train_median'        : load('train_median.pkl'),
        'osrm_speed'          : load('osrm_speed.pkl'),
        'osrm_speed_by_route' : load('osrm_speed_by_route.pkl'),
        'name_to_code'        : load('name_to_code.pkl'),
        'code_to_name'        : load('code_to_name.pkl'),
        'facility_coords'     : load('facility_coords.pkl'),
    }
    print("All models loaded successfully.")
    return models