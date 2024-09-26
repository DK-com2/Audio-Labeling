import streamlit as st
import pandas as pd

# 初期化
if 'segments' not in st.session_state:
    st.session_state.segments = pd.DataFrame(columns=['Start Time', 'End Time', 'Label'])
    st.session_state.last_end_time = 0.0  # 最初の終了時間を0に初期化
    st.session_state.labels = []  # ラベルのリストを初期化

st.title("MP3データラベル付け")

# MP3ファイルのアップロード
uploaded_file = st.file_uploader("MP3ファイルをアップロード", type=["mp3"])

# アップロードされたMP3を再生
if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/mp3')

# 開始時間と終了時間の入力
col1, col2 = st.columns(2)

with col1:
    st.subheader("開始時間")
    start_time_minutes = st.number_input("分", min_value=0, value=0, step=1, key="start_minutes")
    start_time_seconds = st.number_input("秒", min_value=0, value=0, step=1, key="start_seconds")
    
    # フォーマットを整えて表示
    formatted_start_time = f"{int(start_time_minutes)}:{int(start_time_seconds):02d}"
    st.write(f"開始時間: {formatted_start_time}")

with col2:
    st.subheader("終了時間")
    end_time_minutes = st.number_input("分", min_value=0, value=0, step=1, key="end_minutes")
    end_time_seconds = st.number_input("秒", min_value=0, value=0, step=1, key="end_seconds")

    # フォーマットを整えて表示
    formatted_end_time = f"{int(end_time_minutes)}:{int(end_time_seconds):02d}"
    st.write(f"終了時間: {formatted_end_time}")

# ラベル付けの入力
st.subheader("ラベル付けの入力")
label_option = st.selectbox("既存のラベルを選択するか、新しいラベルを追加してください", ["新しいラベルを入力"] + st.session_state.labels)

# 新しいラベルを入力するオプションが選択された場合は、テキスト入力を表示
if label_option == "新しいラベルを入力":
    label = st.text_input("ラベル名を入力")
else:
    label = label_option  # 既存のラベルを使用

# ボタンを押したときの処理
if st.button("追加"):
    if label and (end_time_minutes * 60 + end_time_seconds) > (start_time_minutes * 60 + start_time_seconds):
        # データフレームに追加
        new_segment = pd.DataFrame({'Start Time': [formatted_start_time], 'End Time': [formatted_end_time], 'Label': [label]})
        st.session_state.segments = pd.concat([st.session_state.segments, new_segment], ignore_index=True)

        # 次の開始時間と終了時間のために終了時間を保存
        st.session_state.last_end_time = end_time_minutes * 60 + end_time_seconds

        # 新しいラベルを追加（すでに存在しない場合）
        if label not in st.session_state.labels:
            st.session_state.labels.append(label)

        st.success("セグメントを追加しました！")
    else:
        st.error("終了時間は開始時間より大きくし、ラベル名を空にしないでください。")

# 現在のセグメントの表示
st.subheader("現在のセグメント")
st.dataframe(st.session_state.segments, use_container_width=True)














