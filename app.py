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

# 사용자 데이터 테이블 출력 및 수정/삭제 기능
st.header("사용자 리스트")

# 선택된 인덱스와 수정 폼을 관리하는 상태 변수
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# 각 사용자 옆에 수정 및 삭제 버튼 추가
def update_user(index, name, probability):
    st.session_state.users.loc[index] = [name, probability]
    st.session_state.edit_index = None
    st.success("사용자가 수정되었습니다.")

def delete_user(index):
    st.session_state.users = st.session_state.users.drop(index).reset_index(drop=True)
    st.session_state.edit_index = None
    st.success("사용자가 삭제되었습니다.")

# 사용자 리스트를 표시하는 데이터프레임
if not st.session_state.users.empty:
    for index, row in st.session_state.users.iterrows():
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"**{row['Name']}**: 확률 {row['Probability']}")
        with col2:
            if st.button("수정", key=f"edit_{index}"):
                st.session_state.edit_index = index
        with col3:
            if st.button("삭제", key=f"delete_{index}"):
                delete_user(index)

# 수정 폼
if st.session_state.edit_index is not None:
    index = st.session_state.edit_index
    user_to_edit = st.session_state.users.loc[index]
    st.header("사용자 수정")
    with st.form("edit_user_form"):
        new_name = st.text_input("이름", user_to_edit["Name"])
        new_probability = st.number_input("확률 (0 - 100)", min_value=0.0, max_value=100.0, value=user_to_edit["Probability"], step=1.0)
        submit_edit = st.form_submit_button("수정 완료")
        
        if submit_edit:
            update_user(index, new_name, new_probability)

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
