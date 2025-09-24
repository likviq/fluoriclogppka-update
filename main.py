from services.prediction_service import PredictionService

from fluoriclogppka.ml_part.constants import Identificator, Target

prediction_service = PredictionService()


def main(smiles, target_value):
    features_3d = prediction_service.get_3d_features(
        smiles=smiles,
        target_value=target_value
    )  

    print("Features:")
    print(features_3d) 


if __name__ == "__main__":
    SMILES = "FC1(F)CCC(C(O)=O)CC1"
    target_value = Target.logP
    main(SMILES, target_value)