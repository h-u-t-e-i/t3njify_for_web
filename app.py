import streamlit as st
import csv
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
import moviepy.config as mpy_config
mpy_config.change_settings({"FFMPEG_BINARY": "ffmpeg"})

def braille_to_binary_groups(text):
    binary_list = []
    for char in text:
        if '\u2800' <= char <= '\u28FF':
            dot_bits = ord(char) - 0x2800
            dot_order = [0, 3, 1, 4, 2, 5]
            bit_str = ''.join('1' if dot_bits & (1 << pos) else '0' for pos in dot_order)
            binary_list.append(bit_str)
    joined = ''.join(binary_list)
    return [joined[i:i+3] for i in range(0, len(joined), 3)]

st.title("t3njify うぇぶ！")

# 入力
braille_text = st.text_area("点字を入力してください（漢点字には非対応です。）", height=200)
bpm = st.number_input("BPMを入力してください（15以上を推奨します。）", min_value=1.0, value=60.0, step=1.0)

if st.button("生成！"):
    groups = braille_to_binary_groups(braille_text)

    if not groups:
        st.error("点字が見つかりません。")
    else:
        st.success(f"{len(groups)} 個のクリップを生成しています…")

        base_path = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
        video_dir = os.path.join(base_path, "tenjis")
        speed_factor = bpm / 15
        all_clips = []

        # プログレスバー初期化
        progress_bar = st.progress(0)
        status_placeholder = st.empty()

        total = len(groups)

        for i, group in enumerate(groups):
            filename = group.strip() + ".mp4"
            video_path = os.path.join(video_dir, filename)

            # 現在のステータス表示
            status_placeholder.markdown(f"`{filename}` を処理中…")

            if not os.path.isfile(video_path):
                st.warning(f"見つかりません…: {filename}")
                progress_bar.progress((i + 1) / total)
                continue

            try:
                clip = VideoFileClip(video_path).fx(vfx.speedx, factor=speed_factor).without_audio()
                all_clips.append(clip)
            except Exception as e:
                st.error(f"{filename} 読込エラー: {e}")

            # プログレスバー更新
            progress_bar.progress((i + 1) / total)

        status_placeholder.markdown("すべてのクリップ処理が完了しました！")

        if all_clips:
            final_clip = concatenate_videoclips(all_clips, method="compose")
            output_path = os.path.join(base_path, "tenjified.mp4")
            final_clip.write_videofile(output_path, codec="libx264", fps=min(60, int(final_clip.fps * speed_factor)))

            st.video(output_path)

            with open(output_path, "rb") as f:
                st.download_button(
                    label="tenjified.mp4 をダウンロード！",
                    data=f.read(),
                    file_name="tenjified.mp4",
                    mime="video/mp4"
                )
        else:
            st.error("動画クリップが読み込まれませんでした。")
