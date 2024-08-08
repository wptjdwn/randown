import streamlit as st
import pandas as pd
import numpy as np

# 초기 사용자 데이터프레임 설정
if "users" not in st.session_state:
    st.session_state.users = pd.DataFrame(columns=["Name", "Probability"])

# 페이지 제목 설정
st.title("랜덤 뽑기 사이트")

st.header("사용자 추가")

# 사용자 이름과 확률을 입력받는 폼
with st.form("add_user_form"):
    name = st.text_input("이름", "")
    probability = st.number_input("확률 (0 - 100)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
    submitted = st.form_submit_button("추가")

    if submitted:
        # 유효성 검사
        if name.strip() == "":
            st.error("이름을 입력해야 합니다.")
        elif probability < 0 or probability > 100:
            st.error("확률은 0 이상 100 이하의 값이어야 합니다.")
        else:
            # 사용자 추가
            new_user = pd.DataFrame({"Name": [name], "Probability": [probability]})
            st.session_state.users = pd.concat([st.session_state.users, new_user], ignore_index=True)
            st.success(f"사용자 '{name}'이(가) 추가되었습니다.")

# 사용자 데이터 테이블 출력 및 편집 기능
st.header("사용자 리스트")

# 데이터프레임을 편집할 수 있는 에디터
edited_users = st.data_editor(st.session_state.users, key="user_editor")
# 데이터프레임을 업데이트하는 버튼
if st.button("저장"):
    st.session_state.users = edited_users
    st.success("변경사항이 저장되었습니다.")

# 랜덤 뽑기 기능
st.header("랜덤 뽑기")
if st.button("뽑기"):
    if not st.session_state.users.empty:
        # 확률에 따라 사용자 뽑기
        probabilities = st.session_state.users["Probability"].astype(float)
        if probabilities.sum() == 0:
            st.error("확률의 총합이 0입니다. 각 사용자의 확률을 설정해주세요.")
        else:
            winner = np.random.choice(st.session_state.users["Name"], p=probabilities / probabilities.sum())
            st.success(f"당첨자: {winner}")
    else:
        st.warning("사용자가 없습니다. 먼저 사용자를 추가해주세요.")

# 사용자 리스트 초기화 기능
st.header("리스트 초기화")
if st.button("리스트 초기화"):
    st.session_state.users = pd.DataFrame(columns=["Name", "Probability"])
    st.success("모든 사용자가 초기화되었습니다.")

