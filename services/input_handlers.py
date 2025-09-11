"""Обробники різних методів введення молекул"""

from typing import Optional, Tuple
import streamlit as st
from streamlit_ketcher import st_ketcher

from utils.molecule_utils import validate_smiles, sdf_to_smiles, process_editor_molecule
from constants import INPUT_METHODS, EDITOR_HEIGHT, ALLOWED_FILE_EXTENSIONS, MESSAGES


class InputHandler:
    """Базовий клас для обробників введення"""
    
    def process_input(self) -> Tuple[Optional[str], Optional[str]]:
        """Обробляє введення та повертає SMILES і назву методу"""
        raise NotImplementedError


class SMILESInputHandler(InputHandler):
    """Обробник введення SMILES"""
    
    def process_input(self) -> Tuple[Optional[str], Optional[str]]:
        st.header("📝 Введення SMILES")
        smiles_input = st.text_area(
            "Введіть SMILES рядок:",
            value="FC1(F)CC(C(O)=O)C1",
            height=100,
            help="Введіть SMILES представлення молекули"
        )
        
        if smiles_input and validate_smiles(smiles_input):
            return smiles_input, "Введення SMILES"
        
        return None, None


class SDFInputHandler(InputHandler):
    """Обробник завантаження SDF файлів"""
    
    def process_input(self) -> Tuple[Optional[str], Optional[str]]:
        st.header("📁 Завантаження SDF")
        uploaded_file = st.file_uploader(
            "Завантажте SDF файл:",
            type=ALLOWED_FILE_EXTENSIONS,
            help="Завантажте файл з молекулою в форматі SDF"
        )
        
        if uploaded_file is not None:
            try:
                sdf_content = uploaded_file.read().decode('utf-8')
                sdf_smiles = sdf_to_smiles(sdf_content)
                if sdf_smiles:
                    return sdf_smiles, "SDF файл"
            except Exception as e:
                st.error(MESSAGES["ERROR_SDF_READ"].format(error=str(e)))
        
        return None, None


class EditorInputHandler(InputHandler):
    """Обробник редактора молекул"""
    
    def process_input(self) -> Tuple[Optional[str], Optional[str]]:
        st.header("🎨 Редактор молекул")
        
        molecule = st_ketcher(
            height=EDITOR_HEIGHT,
            key="molecule_editor"
        )
        
        if molecule:
            editor_smiles = process_editor_molecule(molecule)
            if editor_smiles:
                st.success(f"Отримано SMILES з редактора: {editor_smiles}")
                return editor_smiles, "Редактор молекул"
            else:
                st.info(MESSAGES["INFO_DRAW_MOLECULE"])
        else:
            st.info(MESSAGES["INFO_DRAW_MOLECULE"])
        
        return None, None


class InputManager:
    """Manager for handling different input methods"""
    
    def __init__(self):
        self.handlers = {
            INPUT_METHODS["SMILES"]: SMILESInputHandler(),
            INPUT_METHODS["SDF"]: SDFInputHandler(),
            INPUT_METHODS["EDITOR"]: EditorInputHandler()
        }
    
    def get_molecule_input(self) -> Tuple[Optional[str], Optional[str]]:
        """Gets molecule from user"""
        input_method_choice = st.radio(
            "Choose molecule input method:",
            list(INPUT_METHODS.values()),
            index=0,
            horizontal=True
        )
        
        handler = self.handlers.get(input_method_choice)
        if handler:
            return handler.process_input()
        
        return None, None