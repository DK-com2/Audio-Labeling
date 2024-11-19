import streamlit as st
import pandas as pd
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

# アプリのタイトル
st.title("スペクトログラム表示とCSVによる範囲ハイライト")

# ファイルアップロード
audio_file = st.file_uploader("音声ファイルをアップロードしてください (MP3/WAV形式対応)", type=["mp3", "wav"])
csv_file = st.file_uploader("対応するCSVファイルをアップロードしてください", type=["csv"])

if audio_file and csv_file:
    # 音声ファイルを読み込む
    y, sr = librosa.load(audio_file, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)

    # スペクトログラムを計算
    S = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)

    # CSVデータを読み込む
    df = pd.read_csv(csv_file)

    # スペクトログラムをプロット
    fig, ax = plt.subplots(figsize=(duration / 2, 10))  # 横幅を音声の長さに比例
    img = librosa.display.specshow(S_db, sr=sr, x_axis="time", y_axis="log", cmap="viridis", ax=ax)
    fig.colorbar(img, ax=ax, format="%+2.0f dB")
    ax.set_title("Spectrogram with Annotations")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")

    # CSVの範囲に基づきハイライトを追加
    for _, row in df.iterrows():
        start_time = row["Start (s)"]
        end_time = row["End (s)"]
        ax.axvspan(start_time, end_time, color="red", alpha=0.2)  # 半透明の赤色で範囲をハイライト

    # Streamlitでプロットを表示
    st.pyplot(fig)

    st.write("CSVデータで指定された範囲を赤色でハイライトしています。")
