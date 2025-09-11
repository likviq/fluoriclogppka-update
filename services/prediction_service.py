"""Сервіс для виконання передбачень молекулярних властивостей"""

import streamlit as st
import fluoriclogppka
from constants import MESSAGES


class PredictionService:
    """Сервіс для виконання передбачень властивостей молекул"""
    
    def __init__(self):
        pass
    
    def predict(self, smiles: str, target_value: str) -> dict:
        """
        Виконує передбачення для заданої молекули
        
        Args:
            smiles: SMILES рядок молекули
            target_value: Цільова властивість для передбачення
            
        Returns:
            dict: Результат передбачення
        """
        try:
            inference_params = {
                "SMILES": smiles,
                "target_value": getattr(fluoriclogppka.Target, target_value),
                "model_type": getattr(fluoriclogppka.ModelType, "gnn")
            }

            inference = fluoriclogppka.Inference(**inference_params)
            result = inference.predict()

            return {
                'smiles': smiles,
                'result': result,
                'parameters': inference_params,
                'success': True
            }

        except Exception as e:
            st.error(MESSAGES["ERROR_PREDICTION"].format(error=str(e)))
            return {
                'smiles': smiles,
                'error': str(e),
                'success': False
            }
    
    def get_3d_features(self, smiles: str, target_value) -> dict:
        """
        Gets 3D features of the molecule
        
        Args:
            smiles: SMILES string of the molecule
            target_value: Target property
            
        Returns:
            dict: 3D features of the molecule
        """
        try:
            from fluoriclogppka.ml_part.services.molecule_3d_features_service import Molecule3DFeaturesService
            
            service = Molecule3DFeaturesService(
                smiles=smiles,
                target_value=target_value,
                conformers_limit=None
            )
            
            return service.features_3d_dict
        except Exception as e:
            st.error(MESSAGES["ERROR_3D_FEATURES"].format(error=str(e)))
            return None