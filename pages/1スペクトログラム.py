import streamlit as st
import pandas as pd
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# サンプルファイルのパス
SAMPLE_AUDIO_PATH = "test_sample/uguisu.mp3"
SAMPLE_CSV_PATH = "test_sample/uguisu.BirdNET.results.csv"


# アプリのタイトルと設定
st.set_page_config(page_title="Spectrogram Generator", layout="wide")
st.title("Audio File Analysis Tool")

# サイドバー
st.sidebar.header("Settings")
st.sidebar.write("Choose options below:")

# Step 1: 音声ファイルの選択
st.header("Step 1: Select Audio File")
use_sample_audio = st.sidebar.checkbox("Use Sample Audio", value=True)
uploaded_audio = None if use_sample_audio else st.sidebar.file_uploader("Upload an audio file", type=["mp3", "wav"])

# Step 2: CSVファイルの選択
st.header("Step 2: Select CSV File")
use_sample_csv = st.sidebar.checkbox("Use Sample CSV", value=True)
uploaded_csv = None if use_sample_csv else st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# Step 3: ハイライトオプション
highlight_option = st.sidebar.checkbox("Highlight CSV Ranges on Spectrogram", value=True)

# ロード中のメッセージ
if use_sample_audio:
    audio_file = SAMPLE_AUDIO_PATH
else:
    audio_file = uploaded_audio

if audio_file:
    with st.spinner("Loading audio file..."):
        # 音声ファイルを読み込む
        y, sr = librosa.load(audio_file, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)

        # スペクトログラムを計算 (解像度調整)
        n_fft = 1024
        hop_length = 512
        S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
        S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)

        # スペクトログラムをプロット (音声の長さに応じて横幅を動的に設定)
        width_per_second = 2  # 秒ごとの横幅（調整可能）
        fig, ax = plt.subplots(figsize=(duration * width_per_second, 20))  # 高さを少し小さく設定
        img = librosa.display.specshow(S_db, sr=sr, x_axis="time", y_axis="log", cmap="viridis", ax=ax)
        fig.colorbar(img, ax=ax, format="%+2.0f dB")
        ax.set_title("Spectrogram", fontsize=16)
        ax.set_xlabel("Time (s)", fontsize=14)
        ax.set_ylabel("Frequency (Hz)", fontsize=14)

        # ハイライトオプションが有効ならば、CSVファイルを読み込んで範囲をハイライト
        if highlight_option:
            if use_sample_csv:
                csv_file = SAMPLE_CSV_PATH
            else:
                csv_file = uploaded_csv

            if csv_file:
                with st.spinner("Loading CSV file..."):
                    # CSVファイルを読み込む
                    df = pd.read_csv(csv_file)

                    # CSVの範囲に基づきハイライトを追加
                    for _, row in df.iterrows():
                        start_time = row["Start (s)"]
                        end_time = row["End (s)"]
                        ax.axvspan(start_time, end_time, color="red", alpha=0.2)  # 半透明の赤色で範囲をハイライト

                    # データフレームを表示
                    st.subheader("Uploaded CSV Data")
                    st.dataframe(df)

        # プロットを表示
        st.pyplot(fig)

        st.success(f"Audio file loaded successfully! Duration: {duration:.2f} seconds.")


