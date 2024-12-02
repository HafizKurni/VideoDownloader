
# Streamlit Video Downloader

This app allows you to download a video from a URL and replace the previously downloaded video for efficient storage.

## Features

1. **Video Downloading**:
   - Downloads videos from YouTube or other supported platforms using `yt_dlp`.
   - Saves the downloaded video as a fixed file (`latest_video.mp4`), replacing any existing file.

2. **Efficient Storage**:
   - Ensures only one video is stored at a time, minimizing storage usage.

3. **Video Playback and Download**:
   - Displays the most recently downloaded video in the app.
   - Provides a download button for users to download the video locally.

## Usage

1. **Install Dependencies**:
   Make sure you have the required Python packages installed:

   ```bash
   pip install streamlit yt-dlp
   ```

2. **Run the App**:
   Run the app using Streamlit:

   ```bash
   streamlit run app.py
   ```

3. **Download a Video**:
   - Enter a video URL in the input box.
   - Click the "Download" button to download the video.
   - The app will display the video and provide a download button.

4. **Replace the Video**:
   - To download a new video, enter a new URL and click "Download".
   - The new video will replace the old one.

## How It Works

1. **Temporary File Name**:
   - Downloads the video with a unique temporary file name to avoid conflicts.

2. **Renaming After Download**:
   - After the download completes, the temporary file is renamed to `latest_video.mp4`.
   - The old file is deleted before renaming.

3. **Streamlit Integration**:
   - Uses Streamlit's `st.video` to display the video.
   - Provides a download button with a fixed file name (`latest_video.mp4`).

## Notes

- Ensure the `Output` directory has appropriate permissions for file creation and deletion.
- Streamlit's `st.video` automatically updates when a new video is downloaded.
