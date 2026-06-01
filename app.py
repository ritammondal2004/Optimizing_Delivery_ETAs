
# app.py
import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd                                
import numpy as np                                  
from math import radians, sin, cos, sqrt, atan2       
from datetime import datetime                          
from difflib import get_close_matches                  
import requests    
from ProcessingData.RoadDistance.OsrmApiDistance import get_road_distance
from ProcessingData.Resolve_Facility import resolve_facility
from ProcessingData.RoadDistance.haversine_distance import haversine_distance                                     
import re                                           
                                                         
from ProcessingData.load_models import load_all              
                                                      
# ── Page config ──────────────────────────────────────────────
st.set_page_config(            
    page_title = "Delhivery ETA Predictor", 
    page_icon  = "🚚",                          
    layout     = "wide"                
)                                        
                                                       
# ── Load all models once (cached) ────────────────────────────
@st.cache_resource
def get_models():
    return load_all()  

models = get_models()

# ── Unpack ───────────────────────────────────────────────────
betweenness         = models['betweenness']
in_degree           = models['in_degree']
out_degree          = models['out_degree']
edge_weights        = models['edge_weights']
graph_model         = models['graph_model']
baseline_model      = models['baseline_model']
le                  = models['le']
train_median        = models['train_median']
osrm_speed          = models['osrm_speed']
osrm_speed_by_route = models['osrm_speed_by_route']
name_to_code        = models['name_to_code']
code_to_name        = models['code_to_name'] 
facility_coords     = models['facility_coords']

# ── Feature lists ────────────────────────────────────────────
  # ──────── Define baseline features (NO graph features) ────────
baseline_features = [
                'segment_osrm_time',
                'segment_osrm_distance',
                'route_type_encoded',
                'hour_of_day',
                'day_of_week',
                'month'
            ]

 # Graph-enhanced features (adds graph info on top)
graph_features = baseline_features + [
                'src_betweenness',
                'dst_betweenness',
                'src_in_degree',
                'src_out_degree',
                'dst_in_degree',
                'dst_out_degree',
                'corridor_median_delay'
            ]

# ── Helpers ──────────────────────────────────────────────────
#code_to_name     = {v: k.title() for k, v in name_to_code.items()}
all_names_sorted = sorted([
    k.title() for k in name_to_code.keys()
    if isinstance(k, str)
])  

def match_route_type(route):
    for cls in le.classes_:
        if cls.lower() == route.strip().lower():
            return cls
    return None


# ── UI ───────────────────────────────────────────────────────
st.title("🚚 Delhivery ETA Predictor")
st.markdown("Graph-Based Network Intelligence for Delivery Time Prediction")

# ── Sidebar controls ─────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Prediction Settings")

    src_input = st.selectbox(
        "Source Facility",
        options  = [""] + all_names_sorted,
        index    = 0,
        help     = "Type to search facility"
    )
    dst_input = st.selectbox(
        "Destination Facility",
        options  = [""] + all_names_sorted,
        index    = 0,
        help     = "Type to search facility"
    )
    route_type = st.selectbox(
        "Route Type",
        options = ['FTL', 'Carting']
    )
    model_choice = st.selectbox(
        "Model",
        options = ['Graph-Enhanced Model', 'Baseline Model']
    )

    predict_btn = st.button("🔍 Predict ETA", use_container_width=True)

# ── Main area: Map ───────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Facility Network Map")
                           
    # Build base map  
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5,
                   tiles='OpenStreetMap')

    # Top 5 bottleneck hubs
    top5 = list(betweenness.keys())[:5]

    for code, (lat, lng) in facility_coords.items():
        is_top     = code in top5
        place_name = code_to_name.get(code, code)

        folium.CircleMarker(
            location     = [lat, lng],
            radius       = 7 if is_top else 3,
            color        = '#E24B4A' if is_top else '#378ADD',
            fill         = True,
            fill_opacity = 0.8,
            tooltip      = f"{'⚠️ ' if is_top else ''}{place_name}"
        ).add_to(m)

    result_data = None

    # ── Run prediction ───────────────────────────────────────
    if predict_btn and src_input and dst_input:

        src_code, src_name = resolve_facility(src_input)
        dst_code, dst_name = resolve_facility(dst_input)

        if src_code and dst_code:
            src_coords = facility_coords.get(src_code)
            dst_coords = facility_coords.get(dst_code)

            if src_coords and dst_coords:

                # Road distance
                dist_km, osrm_time = get_road_distance(
                    src_coords[0], src_coords[1],
                    dst_coords[0], dst_coords[1]
                )
                if dist_km is None:
                    dist_km   = haversine_distance(
                                    src_coords[0], src_coords[1],
                                    dst_coords[0], dst_coords[1]
                                )
                    osrm_time = dist_km / osrm_speed_by_route.get(
                                    route_type, osrm_speed
                                )

                # Encode
                matched_route = match_route_type(route_type)
                route_encoded = le.transform([matched_route])[0]
                now           = datetime.now()

                row = {
                    'segment_osrm_time'     : osrm_time,
                    'segment_osrm_distance' : dist_km,
                    'route_type_encoded'    : route_encoded,
                    'hour_of_day'           : now.hour,
                    'day_of_week'           : now.weekday(),
                    'month'                 : now.month,
                    'src_betweenness'       : betweenness.get(src_code, 0),
                    'dst_betweenness'       : betweenness.get(dst_code, 0),
                    'src_in_degree'         : in_degree.get(src_code, 0),
                    'src_out_degree'        : out_degree.get(src_code, 0),
                    'dst_in_degree'         : in_degree.get(dst_code, 0),
                    'dst_out_degree'        : out_degree.get(dst_code, 0),
                    'corridor_median_delay' : edge_weights.get(
                                                (src_code, dst_code),
                                                train_median
                                             )
                }

                if model_choice == 'Baseline Model':
                    pred = baseline_model.predict(
                               pd.DataFrame([row])[baseline_features]
                           )[0]
                else:
                    pred = graph_model.predict(
                               pd.DataFrame([row])[graph_features]
                           )[0]

                result_data = {
                    'eta'      : pred,
                    'osrm'     : osrm_time,
                    'delay'    : pred / osrm_time,
                    'distance' : dist_km,
                    'src_code' : src_code,
                    'dst_code' : dst_code,
                    'src_name' : src_name,
                    'dst_name' : dst_name,
                }

                # Draw route on map
                line_color = "#CD3434" if result_data['delay'] > 1.5 else '#1D9E75'

                folium.Marker(
                    src_coords,
                    popup = src_name,
                    icon  = folium.Icon(color='green', icon='play')
                ).add_to(m)

                folium.Marker(
                    dst_coords,
                    popup = dst_name,
                    icon  = folium.Icon(color='red', icon='flag')
                ).add_to(m)

                folium.PolyLine(
                    [src_coords, dst_coords],
                    color   = line_color,
                    weight  = 4,
                    opacity = 0.8
                ).add_to(m)

                mid = [(src_coords[0]+dst_coords[0])/2,
                       (src_coords[1]+dst_coords[1])/2]

                folium.Marker(
                    mid,
                    icon = folium.DivIcon(
                        html = f"<div style='background:{line_color};"
                               f"color:white;padding:4px 8px;"
                               f"border-radius:4px;font-weight:bold;"
                               f"font-size:12px'>{pred:.0f} mins</div>"
                    )
                ).add_to(m)

    st_folium(m, width=900, height=550)

# ── Results panel ────────────────────────────────────────────
with col2:
    st.subheader("📊 Prediction Result")

    if result_data:
        delay = result_data['delay']
        color = "🔴" if delay > 1.5 else "🟡" if delay > 1.2 else "🟢"

        st.metric("Predicted ETA",
                  f"{result_data['eta']:.0f} mins",
                  f"{result_data['eta']/60:.1f} hrs")

        st.metric("OSRM Estimate",
                  f"{result_data['osrm']:.0f} mins")

        st.metric("Delay Factor",
                  f"{delay:.2f}x  {color}")

        st.metric("Road Distance",
                  f"{result_data['distance']:.0f} km")

        st.divider()
        st.write(f"**From:** {result_data['src_name']}")
        st.write(f"**To:** {result_data['dst_name']}")
        st.write(f"**Route:** {route_type}")
        st.write(f"**Model:** {model_choice}")

    else:
        st.info("Select source, destination and click Predict ETA")

        # Show top 5 bottleneck hubs
        st.subheader("⚠️ Top 5 Bottleneck Hubs")
        top5_df = pd.DataFrame([
            {
                'Hub'         : code_to_name.get(code, code),
                'Betweenness' : f"{score:.3f}"
            }
            for code, score in list(betweenness.items())[:5]
        ])
        st.dataframe(top5_df, use_container_width=True)

