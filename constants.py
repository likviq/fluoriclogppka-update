"""Константи та конфігурація для додатку"""

# Streamlit configuration
PAGE_CONFIG = {
    "page_title": "Fluoriclogppka Prediction",
    "page_icon": "🧪",
    "layout": "wide"
}

# Target property options
TARGET_OPTIONS = {
    "pKa": "pKa",
    "logP": "logP"
}

# Molecule input methods
INPUT_METHODS = {
    "SMILES": "📝 SMILES Input",
    "SDF": "📁 SDF File Upload", 
    "EDITOR": "🎨 Molecule Editor"
}

# Visualization parameters
MOLECULE_IMAGE_SIZE = (400, 400)
EDITOR_HEIGHT = 400

# Messages
MESSAGES = {
    "SUCCESS_PREDICTION": "Prediction completed successfully!",
    "ERROR_NO_MOLECULE": "Please enter a valid molecule",
    "ERROR_SDF_PROCESSING": "Error processing SDF file: {error}",
    "ERROR_MOLECULE_DRAW": "Error drawing molecule: {error}",
    "ERROR_3D_FEATURES": "Error calculating 3D features: {error}",
    "ERROR_PREDICTION": "Error performing prediction: {error}",
    "ERROR_SDF_READ": "Error reading SDF file: {error}",
    "ERROR_EDITOR_PROCESSING": "Error processing molecule from editor: {error}",
    "ERROR_PROPERTIES": "Could not calculate properties: {error}",
    "INFO_DRAW_MOLECULE": "Draw a molecule in the editor above",
    "INFO_NO_FEATURES": "No features available for display"
}

# File extensions
ALLOWED_FILE_EXTENSIONS = ['sdf']

# Section headers for 3D features
FEATURE_SECTIONS = {
    "BASIC": {
        "title": "**Basic Properties:**",
        "features": [
            "identificator", "dipole_moment", "mol_volume", 
            "mol_weight", "sasa", "tpsa+f"
        ]
    },
    "ANGLES": {
        "title": "**Angles:**",
        "features": [
            "angle_X1X2R2", "angle_X2X1R1", "angle_R2X2R1",
            "angle_R1X1R2", "dihedral_angle"
        ]
    },
    "DISTANCES": {
        "title": "**Distances and Conformation:**",
        "features": [
            "f_to_fg", "f_freedom", "distance_between_atoms_in_cycle_and_f_group",
            "distance_between_atoms_in_f_group_centers", "cis/trans"
        ]
    }
}

# Feature names in English
FEATURE_NAMES = {
    "identificator": "Identifier",
    "dipole_moment": "Dipole Moment",
    "mol_volume": "Molecular Volume", 
    "mol_weight": "Molecular Weight",
    "sasa": "SASA",
    "tpsa+f": "TPSA+F",
    "angle_X1X2R2": "Angle X1X2R2",
    "angle_X2X1R1": "Angle X2X1R1",
    "angle_R2X2R1": "Angle R2X2R1",
    "angle_R1X1R2": "Angle R1X1R2",
    "dihedral_angle": "Dihedral Angle",
    "f_to_fg": "F to FG",
    "f_freedom": "F Freedom",
    "distance_between_atoms_in_cycle_and_f_group": "Distance Between Atoms in Cycle",
    "distance_between_atoms_in_f_group_centers": "Distance Between F-Group Centers",
    "cis/trans": "Cis/Trans"
}

# Value formatting
FLOAT_PRECISION = 4
EXTENDED_PRECISION = 6

# Custom CSS styles
CUSTOM_CSS = """
<style>
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        margin: 1.5rem 0 1rem 0;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Card styling */
    .info-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Success messages */
    .success-card {
        background: linear-gradient(45deg, #56ab2f, #a8e6cf);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Error messages */
    .error-card {
        background: linear-gradient(45deg, #ff416c, #ff4b2b);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric cards */
    div[data-testid="metric-container"] {
        background: white;
        border: 1px solid #e1e5e9;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease-in-out;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Radio button styling */
    .stRadio > div {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: #f8f9fa;
        border: 2px dashed #667eea;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #e1e5e9;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    /* Molecule structure container */
    .molecule-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    /* Results container */
    .results-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Feature table styling */
    .feature-table {
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Download button styling */
    .download-button {
        background: linear-gradient(45deg, #11998e, #38ef7d);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        margin-top: 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    /* Spinner overlay */
    .stSpinner > div {
        border-color: #667eea !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""