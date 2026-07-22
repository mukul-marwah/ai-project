import streamlit as st
import pandas as pd
import json
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import joblib

class SurvivalExplanation(BaseModel):
    risk_level: str
    summary: str
    recommendations: list[str]

final_model = joblib.load("model.pkl")

st.title("🧠 AI Titanic Survival Predictor")
st.caption("ML + LLM powered decision system")

st.sidebar.title("Passenger Inputs")
age = st.sidebar.number_input("Age", min_value=0, max_value=100, value=25)
sex = st.sidebar.selectbox("Sex", ["male", "female"])
pclass = st.sidebar.selectbox("Passenger Class", [1, 2, 3])
fare = st.sidebar.number_input("Fare", min_value=0.0, value=50.0)

def build_prompt(prediction, age, sex, pclass, fare):
    return f"""
You are an AI assistant explaining Titanic survival predictions. 
Input:
- Age: {age}
- Sex: {sex}
- Passenger Class: {pclass}
- Fare: {fare}

Model Prediction:
- Survived = {prediction}

Explain:
1. Risk Level (Low / Medium / High)
2. Short summary (why this prediction happened)
3. 2-3 recommendations for survival improvement (historical context)
"""

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("Missing Gemini API key. Check .env file")
    st.stop()
client = genai.Client(api_key=API_KEY)

def get_llm_response(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SurvivalExplanation
            )
        )
        return json.loads(response.text)
    except Exception as e:
        return {
            "risk_level": "Unknown",
            "summary": "Failed to parse LLM response",
            "recommendations": ["AI explanation failed due to an API error."]
        }

if st.button("Predict Survival"):
    with st.spinner("Analyzing passenger data..."):
        input_data = pd.DataFrame([{
            "Pclass": pclass,
            "Sex": 1 if sex == "male" else 0, 
            "Age": age, 
            "SibSp": 0, 
            "Parch": 0, 
            "Fare": fare,  
            "Embarked_Q": 0, 
            "Embarked_S": 1
        }])
        prediction = final_model.predict(input_data)[0]

        st.markdown("---")
        st.subheader("Prediction Result")
        if prediction == 1:
            st.success("Survived")
        else:
            st.error("Did Not Survive")

        if hasattr(final_model, "predict_proba"):
            prob = final_model.predict_proba(input_data)[0][1]
            st.write(f"**Model Confidence:** {prob:.2%}")

        prompt = build_prompt(prediction, age, sex, pclass, fare)
        llm_output = get_llm_response(prompt)

        st.markdown("---")
        st.subheader("AI Explanation")
        st.info(f"Risk Level: {llm_output.get('risk_level', 'N/A')}")
        
        st.write("**Summary:**")
        st.write(llm_output.get("summary", "N/A"))
        
        st.write("**Recommendations:**")
        for r in llm_output.get("recommendations", []):
            st.write("•", r)
