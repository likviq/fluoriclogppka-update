"""Утиліти для роботи з молекулами"""

import io
import base64
from typing import Optional
import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw, Descriptors
from constants import MOLECULE_IMAGE_SIZE, MESSAGES


def validate_smiles(smiles: str) -> bool:
    """Перевіряє валідність SMILES рядка"""
    if not smiles or not isinstance(smiles, str):
        return False
    
    smiles = smiles.strip()
    
    if not smiles:
        return False
    
    try:
        mol = Chem.MolFromSmiles(smiles)
        
        if mol is None:
            return False
        
        if mol.GetNumAtoms() == 0:
            return False
        
        canonical_smiles = Chem.MolToSmiles(mol)
        if not canonical_smiles:
            return False
        
        test_mol = Chem.MolFromSmiles(canonical_smiles)
        if test_mol is None:
            return False
        
        return True
        
    except Exception:
        return False


def sdf_to_smiles(sdf_content: str) -> Optional[str]:
    """Конвертує SDF файл в SMILES"""
    try:
        mol_supplier = Chem.SDMolSupplier()
        mol_supplier.SetData(sdf_content)
        
        for mol in mol_supplier:
            if mol is not None:
                return Chem.MolToSmiles(mol)
        return None
    except Exception as e:
        st.error(MESSAGES["ERROR_SDF_PROCESSING"].format(error=str(e)))
        return None


def draw_molecule(smiles: str) -> str:
    """Малює молекулу та повертає HTML"""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return "<p>Не вдалося намалювати молекулу</p>"
        
        img = Draw.MolToImage(mol, size=MOLECULE_IMAGE_SIZE)
        
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f'<img src="data:image/png;base64,{img_str}" style="max-width: 100%; height: auto;">'
    except Exception as e:
        return f"<p>{MESSAGES['ERROR_MOLECULE_DRAW'].format(error=str(e))}</p>"


def get_molecule_properties(smiles: str) -> dict:
    """Отримує основні властивості молекули"""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            return {}
        
        return {
            "molecular_weight": Descriptors.MolWt(mol),
            "num_atoms": mol.GetNumAtoms(),
            "num_bonds": mol.GetNumBonds()
        }
    except Exception:
        return {}


def process_editor_molecule(molecule) -> Optional[str]:
    """Processes molecule from Ketcher editor"""
    try:
        editor_smiles = None
        
        if hasattr(molecule, 'smiles') and molecule.smiles:
            editor_smiles = molecule.smiles
        elif isinstance(molecule, str):
            if validate_smiles(molecule):
                editor_smiles = molecule
        elif isinstance(molecule, dict):
            if 'smiles' in molecule:
                editor_smiles = molecule['smiles']
            elif 'molfile' in molecule:
                try:
                    mol = Chem.MolFromMolBlock(molecule['molfile'])
                    if mol:
                        editor_smiles = Chem.MolToSmiles(mol)
                except:
                    pass
        
        if editor_smiles and validate_smiles(editor_smiles):
            return editor_smiles
        
        return None
        
    except Exception as e:
        st.error(MESSAGES["ERROR_EDITOR_PROCESSING"].format(error=str(e)))
        return None