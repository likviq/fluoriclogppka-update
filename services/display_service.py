"""Сервіс для відображення результатів та візуалізації"""

import json
import pandas as pd
import streamlit as st
from fluoriclogppka.ml_part.constants import Target

from utils.molecule_utils import draw_molecule, get_molecule_properties
from constants import (
    FEATURE_SECTIONS, FEATURE_NAMES, FLOAT_PRECISION, 
    EXTENDED_PRECISION, MESSAGES, FEATURE_IMPORTANCE
)


class DisplayService:
    """Сервіс для відображення результатів та візуалізації"""
    
    def display_molecule_info(self, smiles: str, input_method: str):
        """Відображає інформацію про молекулу"""
        st.success(f"Використовується молекула з: {input_method}")
        st.code(f"SMILES: {smiles}")
        
        # Відображення структури молекули
        mol_html = draw_molecule(smiles)
        st.markdown(mol_html, unsafe_allow_html=True)
        
        # Основні властивості
        properties = get_molecule_properties(smiles)
        if properties:
            st.subheader("Основні властивості молекули:")
            prop_col1, prop_col2, prop_col3 = st.columns(3)
            
            with prop_col1:
                st.metric("Молекулярна вага", f"{properties.get('molecular_weight', 0):.2f}")
            with prop_col2:
                st.metric("Кількість атомів", properties.get('num_atoms', 0))
            with prop_col3:
                st.metric("Кількість зв'язків", properties.get('num_bonds', 0))
        else:
            st.warning(MESSAGES["ERROR_PROPERTIES"].format(error="невідома помилка"))
    
    def display_prediction_result(self, prediction_data: dict):
        """Відображає результати передбачення"""
        st.header("📈 Останнє передбачення")
        
        result = prediction_data.get("result", {})
        
        if 'parameters' in prediction_data and 'target_value' in prediction_data['parameters']:
            predicted_value_type = prediction_data['parameters']['target_value']
            
            if predicted_value_type == Target.logP:
                value = result if isinstance(result, (int, float)) else result.get('logP', 'N/A')
                st.header(f"🌊 logP: {value:.4f}" if isinstance(value, (int, float)) else f"🌊 logP: {value}")
            
            if predicted_value_type == Target.pKa:
                value = result if isinstance(result, (int, float)) else result.get('pKa', 'N/A')
                st.header(f"🧪 pKa: {value:.4f}" if isinstance(value, (int, float)) else f"🧪 pKa: {value}")
        
        with st.expander("Показати деталі"):
            st.json(prediction_data)
    
    def display_3d_features(self, features_dict: dict, target_value: str):
        """Відображає 3D характеристики молекули в зручному форматі"""
        if not features_dict:
            return
        
        st.subheader("🧬 3D Характеристики молекули")
        
        col1, col2, col3 = st.columns(3)
        
        # Групуємо характеристики за категоріями
        for i, (section_key, section_info) in enumerate(FEATURE_SECTIONS.items()):
            column = [col1, col2, col3][i]
            
            with column:
                st.markdown(section_info["title"])
                self._display_feature_group(features_dict, section_info["features"], section_key)
        
        # Детальна таблиця
        with st.expander("Детальна таблиця всіх характеристик"):
            self._display_detailed_table(features_dict, target_value)
        
        # Кнопка завантаження
        st.download_button(
            key="download_3d_features",
            label="📥 Завантажити 3D характеристики (JSON)",
            data=json.dumps(features_dict, ensure_ascii=False, indent=4, default=str),
            file_name="3d_features.json",
            mime="application/json"
        )
    
    def _display_feature_group(self, features_dict: dict, feature_keys: list, section_key: str):
        """Відображає групу характеристик"""
        for feature_key in feature_keys:
            value = features_dict.get(feature_key)
            if value is not None:
                display_name = FEATURE_NAMES.get(feature_key, feature_key)
                
                if isinstance(value, (int, float)):
                    if section_key == "ANGLES":
                        display_value = round(value, FLOAT_PRECISION)
                    else:
                        display_value = round(value, FLOAT_PRECISION) if isinstance(value, float) else str(value)
                else:
                    display_value = str(value)
                
                st.metric(display_name, display_value)
    
    def _display_detailed_table(self, features_dict: dict, target_value: str):
        """Відображує детальну таблицю характеристик"""
        df_data = []
        for key, value in features_dict.items():
            if value is not None:
                display_name = FEATURE_NAMES.get(key, key)
                formatted_value = (
                    f"{value:.{FLOAT_PRECISION}f}" if isinstance(value, float) else value
                )
                importance = f"{FEATURE_IMPORTANCE[target_value.value.lower()].get(key, key) * 100}%"
                
                df_data.append({
                    "Характеристика": display_name,
                    "Значення": formatted_value,
                    "Важливість": importance,
                })
        
        if df_data:
            df = pd.DataFrame(df_data)
            st.dataframe(df, width="stretch")
        else:
            st.info(MESSAGES["INFO_NO_FEATURES"])
    
    def display_parameters_section(self):
        """Displays prediction parameters section"""        
        col_params1, col_params2 = st.columns(2)
        
        with col_params1:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            target_options = {
                "pKa": "pKa",
                "logP": "logP"
            }
            target_value = st.selectbox(
                "Target Property:",
                options=list(target_options.keys()),
                help="Select property for prediction"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        return target_value