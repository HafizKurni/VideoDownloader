import streamlit as st
import os
import yt_dlp
import time

# Set up the title of the app
st.title("Video Downloader")

# Create a folder to save downloaded videos
download_folder = os.path.join("Output")
os.makedirs(download_folder, exist_ok=True)

# Define the final fixed file name for the downloaded video
fixed_file_name = "latest_video.mp4"
fixed_file_path = os.path.join(download_folder, fixed_file_name)

# Get video URL input from user
url = st.text_input("Enter the video URL:")

# Download the video if URL is valid and download button is clicked
if st.button("Download"):
    if url:
        try:
            # Create a temporary unique file name using timestamp
            temp_file_name = f"temp_{int(time.time())}.mp4"
            temp_file_path = os.path.join(download_folder, temp_file_name)

            # Set download options
            ydl_opts = {
                'format': 'best',
                'outtmpl': temp_file_path,  # Save with temporary file name
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                st.write("Downloading video...")
                ydl.download([url])

            # Rename the temporary file to the fixed file name
            if os.path.exists(temp_file_path):
                if os.path.exists(fixed_file_path):
                    os.remove(fixed_file_path)  # Remove the old file
                os.rename(temp_file_path, fixed_file_path)
                st.success(f"The video has been downloaded and saved as '{fixed_file_name}'.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid URL.")

# Display and provide a download button for the latest video
if os.path.exists(fixed_file_path):
    st.subheader("Latest Downloaded Video:")
    st.video(fixed_file_path)
    with open(fixed_file_path, "rb") as f:
        st.download_button(
            label="Download Latest Video",
            data=f,
            file_name=fixed_file_name,
            mime="video/mp4"
        )
