import streamlit as st
import os
import yt_dlp
import time
import subprocess

tabs = st.tabs(["Download Video", "Tutorial"])

# Set up the title of the app
with tabs[0]:
    st.title("Video Downloader 🎥")

    # Create a folder to save downloaded videos
    download_folder = os.path.join("Output")
    os.makedirs(download_folder, exist_ok=True)

    # Define the final fixed file name for the downloaded video
    fixed_file_name = "latest_video.mp4"
    fixed_file_path = os.path.join(download_folder, fixed_file_name)

    # Initialize session state to track download status and available formats
    if "download_clicked" not in st.session_state:
        st.session_state["download_clicked"] = False
    if "formats" not in st.session_state:
        st.session_state["formats"] = []

    # Get video URL input from user
    url = st.text_input("Enter the video URL:")

    # Fetch video formats if URL is provided
    if st.button("Fetch Formats", use_container_width=True):
        if url:
            try:
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    formats = [
                        {
                            "format_id": fmt["format_id"],
                            "quality": fmt.get("format_note", "unknown"),
                            "ext": fmt["ext"],
                            "resolution": fmt.get("resolution", "audio only"),
                            "has_audio": "audio" in fmt.get("acodec", "") and fmt.get("acodec", "") != "none",
                        }
                        for fmt in info["formats"]
                    ]
                    st.session_state["formats"] = formats
                    st.success("Available formats fetched successfully.")
            except Exception as e:
                st.error(f"An error occurred while fetching formats: {e}")
        else:
            st.warning("Please enter a valid URL.")

    # Display available formats
    if st.session_state["formats"]:
        st.subheader("Available Formats:")
        selected_format = st.selectbox(
            "Choose a format to download:",
            st.session_state["formats"],
            format_func=lambda x: f"{x['quality']} ({x['resolution']}) - {x['ext']}{' [Audio]' if x['has_audio'] else ''}",
        )

    # Download the video if URL is valid and download button is clicked
    if st.button("Download" , use_container_width=True):
        if url and "selected_format" in locals():
            try:
                # Create a temporary unique file name using timestamp
                temp_file_name = f"temp_{int(time.time())}.mp4"
                temp_file_path = os.path.join(download_folder, temp_file_name)
                audio_file_path = os.path.join(download_folder, f"temp_audio_{int(time.time())}.m4a")

                # Set download options
                ydl_opts = {
                    'format': selected_format["format_id"],
                    'outtmpl': temp_file_path,  # Save video with temporary file name
                }

                if not selected_format["has_audio"]:
                    # Download video and audio separately if necessary
                    ydl_opts_audio = {
                        'format': 'bestaudio',
                        'outtmpl': audio_file_path,  # Save audio
                    }
                    with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl_audio:
                        st.write("Downloading audio...")
                        ydl_audio.download([url])

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    st.write("Downloading video...")
                    ydl.download([url])

                # Merge video and audio if needed
                if not selected_format["has_audio"] and os.path.exists(audio_file_path):
                    merged_file_path = os.path.join(download_folder, "merged_output.mp4")
                    ffmpeg_command = [
                        "ffmpeg",
                        "-i", temp_file_path,
                        "-i", audio_file_path,
                        "-c:v", "copy",
                        "-c:a", "aac",
                        "-strict", "experimental",
                        merged_file_path
                    ]
                    subprocess.run(ffmpeg_command, check=True)
                    os.rename(merged_file_path, fixed_file_path)
                    os.remove(audio_file_path)
                    os.remove(temp_file_path)
                else:
                    os.rename(temp_file_path, fixed_file_path)

                st.session_state["download_clicked"] = True
                st.success(f"The video has been downloaded and saved as '{fixed_file_name}'.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid URL and select a format.")

    # Display and provide a download button for the latest video only if the download button was clicked
    if st.session_state["download_clicked"] and os.path.exists(fixed_file_path):
        st.subheader("Latest Downloaded Video:")
        st.video(fixed_file_path)
        with open(fixed_file_path, "rb") as f:
            st.download_button(
                label="Download Latest Video",
                data=f,
                file_name=fixed_file_name,
                mime="video/mp4"
            )

    st.text("This app is powered by yt-dlp and inspired by the amazing open-source community. ❤️")

with tabs[1]:
    st.title("Tutorial")
    st.write("### How to Use This Video Downloader")
    st.markdown("""
    1. **Enter the Video URL**: Copy the URL of the video you want to download and paste it into the input box on the "Video Downloader" tab.
    2. **Fetch Formats**: Click on the "Fetch Formats" button to retrieve the available download options for the video.
    3. **Select Format**: Choose the desired video format from the dropdown list. Each option displays quality, resolution, and whether it includes audio.
    4. **Download Video**: Click on the "Download" button. The selected video will be downloaded and saved in the `Output` folder.
    5. **View & Download**: After the download is complete, you can view the video directly or download it to your device.
    """)
    st.write("Enjoy using this downloader!")