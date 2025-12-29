import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# 1. 페이지 설정 및 보안 (API Key)
st.set_page_config(page_title="AI 관상가", page_icon="🎭")
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

st.title("🎭 AI 관상 도우미 (Gemini 3 Flash)")
st.write("얼굴 사진을 올리면 관상을 분석해 드립니다.")

# 2. 이미지 입력 (카메라 또는 파일 업로드)
img_file = st.file_uploader("사진 업로드", type=['jpg', 'jpeg', 'png'])
camera_file = st.camera_input("또는 직접 촬영하기")

target_file = img_file if img_file else camera_file

if target_file:
    # 이미지 표시
    img = Image.open(target_file)
    st.image(img, caption="분석할 사진", width=300)

    if st.button("관상 분석 시작"):
        try:
            with st.spinner("전문 관상가가 분석 중입니다..."):
                # 모델 로드 (Gemini 3 Flash)
                model = genai.GenerativeModel('gemini-3-flash-preview') # 현재 안정적 사용 가능 버전
                
                # 분석 프롬프트
                prompt = """
                당신은 30년 경력의 관상가입니다.
                첨부된 사진 속 인물의 눈, 코, 입, 이마, 턱을 정밀하게 분석하세요.
                1. 성격적 특징
                2. 재물운 및 직업운
                3. 전반적인 운세 총평
                친절하면서도 신뢰감 있는 어조로 한국어로 작성해 주세요.
                """
                
                # 이미지와 프롬프트 전송
                response = model.generate_content([prompt, img])
                
                st.subheader("🔮 분석 결과")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
