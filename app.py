import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import io

def compress_image(uploaded_file):
    image = Image.open(uploaded_file)
    image.thumbnail((512, 512))
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG', quality=80)
    return img_byte_arr.getvalue()

# 1. 페이지 설정 및 보안 (API Key)
st.set_page_config(page_title="AI 관상가", page_icon="🎭")
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

st.title("🎭 AI 관상가")
st.write("얼굴 사진을 올리면 관상을 분석해 드립니다.")

# 2. 이미지 입력 (카메라 또는 파일 업로드)
img_file = st.file_uploader("사진 업로드", type=['jpg', 'jpeg', 'png'])
camera_file = st.camera_input("또는 직접 촬영하기")

target_file = img_file if img_file else camera_file

if target_file:
    # 이미지 표시
    img = Image.open(target_file)
    compressed_bytes = compress_image(target_file)
    st.image(img, caption="분석할 사진", width=300)
    
    # 중요: 바이트를 그대로 넣지 말고 딕셔너리로 감싸기!
    image_blob = {
        "mime_type": "image/jpeg",
        "data": compressed_bytes
    }
    
    if st.button("관상 분석 시작"):
        try:
            with st.spinner("전문 관상가가 분석 중입니다..."):
                # 모델 로드 (Gemini 3 Flash)
                model = genai.GenerativeModel('gemini-1.5-flash') # 현재 안정적 사용 가능 버전
                
                # 분석 프롬프트
                prompt = """
                # Role (역할)
                당신은 60년 동안 인간의 운명을 연구한 '대관상가(Grand Physiognomist)'이자, 현대 심리학과 빅데이터를 통합한 '운명 분석가'입니다. 당신은 사진 한 장에서 한 사람의 인생 전체를 꿰뚫어 보는 통찰력을 가졌습니다. 당신의 분석은 단순한 요약이 아니라, 한 편의 '전기(Biography)'처럼 구체적이고 방대해야 합니다.
                
                # Task (임무)
                제공된 인물의 이미지를 '현미경'처럼 세밀하게 분석하여, 최소 10,000자 분량에 도전한다는 마음가짐으로 매우 상세한 **[초정밀 관상 운명 보고서]**를 작성하세요. 단답형이나 개조식 요약을 지양하고, 서술형으로 깊이 있게 풀어서 설명해야 합니다.
                
                # Analytical Framework (분석 프레임워크: 십이궁 및 정밀 분석)
                분량을 확보하고 깊이를 더하기 위해 아래의 관상학적 '십이궁(十二宮)'과 세부 주제를 반드시 모두 다루십시오.
                
                1. **명궁(命宮 - 인당):** 선천적인 운명, 생명력, 기질의 근본.
                2. **재백궁(財帛宮 - 코):** 재물의 획득 방식, 소비 패턴, 평생의 부(Wealth).
                3. **형제궁(兄弟宮 - 눈썹):** 대인관계, 인복, 형제/동료와의 협력 혹은 갈등.
                4. **전택궁(田龍宮 - 눈두덩):** 부동산 운, 가정의 평화, 유산 상속.
                5. **남녀궁(男女宮 - 눈밑):** 자녀운, 스태미나, 창의력, 애정의 깊이.
                6. **노복궁(奴僕宮 - 턱):** 리더십, 부하 직원 운, 말년의 사회적 영향력.
                7. **처첩궁(妻妾宮 - 눈꼬리):** 배우자 운, 결혼 생활의 디테일, 연애 스타일.
                8. **질액궁(疾厄宮 - 콧대):** 건강, 잠재적 질병, 스트레스 저항력.
                9. **천이궁(遷移宮 - 이마 양옆):** 이동수, 여행, 유학, 이직, 변화에 대한 적응력.
                10. **관록궁(官祿宮 - 이마 중앙):** 직업적 성공, 승진, 명예, 사회적 지위.
                11. **복덕궁(福德宮 - 이마 상단 양옆):** 전생의 업(Karma), 정신적 만족도, 재테크 감각.
                12. **부모궁(父母宮 - 이마 상단):** 윗사람의 덕, 유년기 환경, 학업운.
                
                # Output Format (출력 형식)
                반드시 다음 목차를 준수하며, 각 항목마다 **최소 3~4개의 긴 문단**으로 상세하게 서술하세요.
                
                ## 📖 [인물의 이름/특징] 관상학적 대서사시
                
                ### 1. 서론: 첫인상과 기운의 형상화
                (얼굴에서 풍기는 오라(Aura), 찰색, 음양의 조화, 동물에 비유한 물형 관상 등을 포함하여 서술)
                
                ### 2. 정밀 분석: 삼정(三停)과 오관(五官)의 미학
                (이마, 눈, 코, 입, 귀 각각의 생김새를 mm 단위로 뜯어보듯 묘사하고 의미를 부여)
                
                ### 3. 십이궁(十二宮)으로 보는 운명의 지도
                (위 프레임워크의 12가지 궁을 하나도 빠짐없이 상세히 분석. 각 궁마다 긍정적 측면과 주의할 점을 모두 서술)
                
                ### 4. 심층 종합 운세 (Specific Deep Dive)
                *이 섹션은 특히 구체적이어야 합니다.*
                
                #### A. 직업 및 성취 (Career & Ambition)
                - **최적의 직업군:** (구체적인 직무 예시 5가지 이상 나열 및 이유)
                - **리더십 스타일:** (카리스마형인지, 관리형인지, 참모형인지 분석)
                - **위기 관리 능력:** (역경이 닥쳤을 때 돌파하는 힘)
                
                #### B. 재물과 경제관 (Wealth & Assets)
                - **돈을 버는 스타일:** (사업가형, 전문직형, 투자형 등)
                - **재물 리스크:** (사기를 조심해야 하는지, 과소비를 조심해야 하는지)
                - **부의 축적 시기:** (인생 중 언제 가장 큰 부가 들어오는지)
                
                #### C. 애정과 인간관계 (Love & Relationships)
                - **연애/결혼 패턴:** (상대에게 헌신하는지, 리드하는지, 갈등의 원인은 무엇인지)
                - **이상적인 배우자상:** (관상학적으로 합이 맞는 파트너의 특징)
                - **사회적 평판:** (타인이 보는 나의 모습과 실제 나의 모습의 괴리)
                
                #### D. 건강과 에너지 (Vitality)
                - **취약한 신체 부위:** (관상학적으로 약해 보이는 장기나 부위)
                - **에너지 관리법:** (활동적인 취미가 맞는지, 정적인 휴식이 맞는지)
                
                ### 5. 인생의 타임라인 (Chronological Flow)
                - **초년기 (10대~20대):** 성장 배경과 학업, 자아 형성 과정.
                - **중년기 (30대~50대):** 사회적 투쟁, 성취, 가정 형성, 인생의 하이라이트.
                - **말년기 (60대 이후):** 자아실현, 재물의 결과, 자녀복, 건강.
                
                ### 6. 대관상가의 최종 제언 (Master's Advice)
                (운명을 개척하기 위한 구체적인 행동 지침, 마음가짐, 행운의 아이템이나 색상 등 실질적인 개운법(開運法) 제시)
                
                # Writing Rules (작성 수칙)
                1. **절대 요약하지 마십시오.** 독자가 지루해할까 걱정하지 말고 최대한 상세하게 묘사하십시오.
                2. 문학적이고 은유적인 표현을 사용하여 글의 품격을 높이십시오.
                3. 전문 용어(와잠, 산근, 법령 등)를 사용하되, 반드시 풀어서 설명하십시오.
                4. **분량이 끊기면 "계속해서 작성해줘"라고 요청받을 것을 가정하고, 최대한 길게 작성하십시오.**
                """
                
                # 이미지와 프롬프트 전송
                response = model.generate_content([prompt, image_blob])
                
                st.subheader("🔮 분석 결과")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
