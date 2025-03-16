from fastapi import FastAPI
import pickle

from stroke.pred_stroke import predict_stroke

# FastAPI instance
app = FastAPI()

# Root endpoint
@app.get("/")
def root():
    return {'greeting':"hello"}

# Prediction endpoint
@app.get("/predict")
def predict(Age: float, Hypertension: int, Heart_Disease: int, BMI: float, Avg_Glucose: float, Diabetes: int, Gender: int):
    prediction = predict_stroke(
        float(Age),
        int(Hypertension),
        int(Heart_Disease),
        float(BMI),
        float(Avg_Glucose),
        int(Diabetes),
        int(Gender)
    )
    return {"prediction": int(prediction[0])}
