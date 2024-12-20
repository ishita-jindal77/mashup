import streamlit as st
import os
import yt_dlp
from pydub import AudioSegment
import shutil

# Downloads the videos
def download_videos(singer_name, num_videos):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': 'True',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{singer_name}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as youtube_dl:
        query = f'{singer_name} songs'
        youtube_dl.download([f'ytsearch{num_videos}:{query}'])

# Converts videos to audio
def converting_videos_to_audio(singer_name):
    audio_files = []
    for root, dirs, files in os.walk(singer_name):
        for file in files:
            if file.endswith(".mp3"):
                audio_files.append(os.path.join(root, file))
    return audio_files

# Edits audio according to the given duration
def cutting_the_audio(audio_files, duration):
    for audio_file in audio_files:
        audio = AudioSegment.from_mp3(audio_file)
        audio_cut = audio[:duration * 1000]
        audio_cut.export(audio_file, format="mp3")

# Merges the audio files
def merging_the_audios(audio_files, output_file):
    combined_audios = AudioSegment.from_mp3(audio_files[0])
    for audio_file in audio_files[1:]:
        combined_audios += AudioSegment.from_mp3(audio_file)
    combined_audios.export(output_file, format="mp3")

st.title("Mashup Generator")

singer_name = st.text_input("Singer Name")
num_videos = st.number_input("Number of Videos", min_value=1, step=1)
audio_duration = st.number_input("Audio Duration in Seconds (greater than 20)", min_value=21)
output_file = st.text_input("Output File Name", value="mashup-output.mp3")

if st.button("Create the Mashup"):
    if not singer_name or not output_file:
        st.error("Please fill all the fields before proceeding.")
    else:
        try:
            # Remove existing directory if it exists
            if os.path.exists(singer_name):
                shutil.rmtree(singer_name)
            os.makedirs(singer_name)

            # Download videos
            with st.spinner("Downloading videos..."):
                download_videos(singer_name, num_videos)
            st.success(f"Downloaded {num_videos} videos of {singer_name}.")

            # Convert videos to audio
            audio_files = converting_videos_to_audio(singer_name)
            with st.spinner("Cutting audio files..."):
                cutting_the_audio(audio_files, audio_duration)
            st.success(f"Cut the first {audio_duration} seconds of each audio file.")

            # Merge audio files
            with st.spinner("Merging audio files..."):
                merging_the_audios(audio_files, output_file)
            st.success(f"Audio files merged and saved as {output_file}.")

        except Exception as e:
            st.error(f"An error occurred: {e}")