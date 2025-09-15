import streamlit as st

from constants import PAGE_CONFIG, MESSAGES, CUSTOM_CSS
from services.input_handlers import InputManager
from services.prediction_service import PredictionService
from services.display_service import DisplayService

st.set_page_config(**PAGE_CONFIG)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

input_manager = InputManager()
prediction_service = PredictionService()
display_service = DisplayService()


def main():
    """Головна функція додатку"""
    
    st.title("🧪 Fluoriclogppka Prediction")
    st.markdown("Додаток для передбачення властивостей молекул за допомогою fluoriclogppka")
    
    final_smiles, input_method = input_manager.get_molecule_input()
    
    if final_smiles and input_method:
        display_service.display_molecule_info(final_smiles, input_method)
    
    target_value = display_service.display_parameters_section()
    
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
    
    if 'last_prediction' in st.session_state:
        display_service.display_prediction_result(st.session_state['last_prediction'])
        
        if st.button("🧬 Розрахувати 3D характеристики"):
            with st.spinner("Розраховуємо 3D характеристики..."):
                prediction = st.session_state['last_prediction']
                features_3d = prediction_service.get_3d_features(
                    smiles=prediction['smiles'],
                    target_value=prediction['parameters']["target_value"],
                    convert_to_basic_type=True,
                )
                if features_3d:
                    st.session_state['last_prediction']['3d_features'] = features_3d
        
        if '3d_features' in st.session_state['last_prediction']:
            display_service.display_3d_features(st.session_state['last_prediction']['3d_features'])


if __name__ == "__main__":
    main()