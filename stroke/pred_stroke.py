import pickle
import os

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

def predict_stroke (Age, Hypertension, Heart_Disease, BMI, Avg_Glucose, Diabetes, Gender):

    """
    Prediction function using a pretrained model

    Arguments:
    - Age
    - Hypertension: Enter 0 if no, 1 if yes
    - Heart_Disease: Enter 0 if no, 1 if yes
    - BMI
    - Avg_Glucose
    - Diabetes: Enter 0 if no, 1 if yes
    - Gender: Enter 0 if female, 1 if male

    """
    model_path = os.path.join(ROOT_PATH, 'strokesenseapp', 'models/lreg_model.pkl')

    with open(model_path, 'rb') as file:
        lreg = pickle.load(file)

    with open('/path/to/scaler.pkl', 'rb') as file:
        scaler = pickle.load(file)

    input_data = [[Age, Hypertension, Heart_Disease, BMI, Avg_Glucose, Diabetes, Gender]]
    scaled_input = scaler.transform(input_data)
    prediction = lreg.predict(scaled_input)

    return prediction
