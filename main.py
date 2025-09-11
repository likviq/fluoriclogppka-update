"""Головний файл Streamlit додатку для передбачення властивостей молекул"""

import streamlit as st

from constants import PAGE_CONFIG, MESSAGES
from services.input_handlers import InputManager
from services.prediction_service import PredictionService
from services.display_service import DisplayService

# Налаштування сторінки
st.set_page_config(**PAGE_CONFIG)

# Ініціалізація сервісів
input_manager = InputManager()
prediction_service = PredictionService()
display_service = DisplayService()


def main():
    """Головна функція додатку"""
    
    # Заголовок
    st.title("🧪 Fluoriclogppka Prediction")
    st.markdown("Додаток для передбачення властивостей молекул за допомогою fluoriclogppka")
    
    # Отримання молекули від користувача
    final_smiles, input_method = input_manager.get_molecule_input()
    
    # Відображення інформації про молекулу
    if final_smiles and input_method:
        display_service.display_molecule_info(final_smiles, input_method)
    
    # Параметри передбачення
    target_value = display_service.display_parameters_section()
    
    # Кнопка запуску передбачення
    if st.button("🚀 Запустити передбачення", type="primary"):
        if final_smiles:
            with st.spinner("Виконується передбачення..."):
                result = prediction_service.predict(final_smiles, target_value)
                
                if result.get('success'):
                    st.session_state['last_prediction'] = result
                    st.success(MESSAGES["SUCCESS_PREDICTION"])
                else:
                    st.error(f"Помилка: {result.get('error', 'Невідома помилка')}")
        else:
            st.error(MESSAGES["ERROR_NO_MOLECULE"])
    
    # Display results
    if 'last_prediction' in st.session_state:
        st.markdown('<div class="section-header">📈 Prediction Results</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="results-container">', unsafe_allow_html=True)
            display_service.display_prediction_result(st.session_state['last_prediction'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 3D features button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            features_button = st.button("🧬 Calculate 3D Features", use_container_width=True)
        
        if features_button:
            with st.spinner("Calculating 3D features..."):
                prediction = st.session_state['last_prediction']
                features_3d = prediction_service.get_3d_features(
                    smiles=prediction['smiles'],
                    target_value=prediction['parameters']["target_value"]
                )
                if features_3d:
                    st.session_state['last_prediction']['3d_features'] = features_3d
        
        # Display 3D features if available
        if '3d_features' in st.session_state['last_prediction']:
            st.markdown('<div class="section-header">🧬 3D Molecular Features</div>', unsafe_allow_html=True)
            display_service.display_3d_features(st.session_state['last_prediction']['3d_features'])


if __name__ == "__main__":
    main()