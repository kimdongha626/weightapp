import streamlit as st
import pandas as pd
import joblib

# 1. 웹앱 제목 및 설명
st.title("🏋️‍♂️ 신체 치수 기반 몸무게 예측 앱")
st.write("엉덩이, 허리, 가슴둘레를 입력하면 예상 몸무게를 예측해줍니다.")

# 2. 모델 로드 함수 (weight_model.pkl 로드)
@st.cache_resource  
def load_my_model():
    return joblib.load("weight_model_.pkl") 

try:
    # 변수명을 요청하신 rf_model로 지정했습니다.
    rf_model = load_my_model()
except FileNotFoundError:
    st.error("🚨 'weight_model.pkl' 파일을 찾을 수 없습니다. 파일이 weight_app.py와 같은 폴더에 있는지 확인해주세요!")
    rf_model = None

st.divider() # 구분선

# 3. 사용자 입력 받기 (Streamlit UI 컴포넌트)
st.subheader("📏 신체 치수 입력")

col1, col2, col3 = st.columns(3)

with col1:
    hip = st.number_input("엉덩이둘레 (cm)", min_value=30.0, max_value=150.0, value=90.0, step=0.1)
with col2:
    waist = st.number_input("허리둘레 (cm)", min_value=30.0, max_value=150.0, value=75.0, step=0.1)
with col3:
    chest = st.number_input("가슴둘레 (cm)", min_value=30.0, max_value=150.0, value=85.0, step=0.1)

st.divider()

# 4. 예측 버튼 및 결과 출력
if st.button("몸무게 예측하기", type="primary"):
    if rf_model is not None:
        # 제공해주신 DataFrame 변환 방식 그대로 적용
        input_data = pd.DataFrame([[hip, waist, chest]], columns=['엉덩이둘레', '허리둘레', '젖가슴둘레'])
        
        # rf_model을 사용하여 예측 진행
        predicted_weight = rf_model.predict(input_data)
        
        # 결과 시각화
        st.balloons() # 축하 풍선 효과 🎉
        st.success(f"🔮 예측된 몸무게는 **{predicted_weight[0]:.1f} kg** 입니다.")
    else:
        st.error("모델이 정상적으로 로드되지 않아 예측할 수 없습니다.")