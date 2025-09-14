# streamlit_app.py
import streamlit as st
import tempfile
from pathlib import Path

from src.utils import (
    extract_frames_by_count,
    extract_frames_by_rate,
    make_zip_bytes,
    get_video_info
)

# ---------------------------
# Page & Style
# ---------------------------
st.set_page_config(
    page_title="Video Frame Splitter",
    page_icon="🎬",
    layout="centered",
)

st.markdown("""
<style>
/* Tweak metrics cards */
[data-testid="stMetricValue"] {
    font-size: 28px;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}
div.stButton > button:first-child {
    border-radius: 12px;
    padding: 0.6rem 1.1rem;
    font-weight: 600;
}
.download-area {
    border: 1px dashed #bbb;
    border-radius: 12px;
    padding: 1rem;
    background: #fafafa;
}
.note {
    font-size: 0.9rem;
    color: #666;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Session helpers
# ---------------------------
if "uploaded_video_path" not in st.session_state:
    st.session_state.uploaded_video_path = None
if "last_zip" not in st.session_state:
    st.session_state.last_zip = None
if "last_zip_name" not in st.session_state:
    st.session_state.last_zip_name = None

# ---------------------------
# UI: Tabs
# ---------------------------
tab1, tab2 = st.tabs(["🖼️ Image Generation", "😊 Emotion Detection"])

with tab1:
    st.title("🎬 Video → Image Splitter")
    st.caption("Upload a video, inspect its properties, then split into a fixed number of images and download as a zip.")

    uploaded = st.file_uploader("Select a video file", type=["mp4", "mov", "avi", "mkv", "webm"])
    temp_video_path = None

    if uploaded:
        # Save to a temporary file so OpenCV can read it
        suffix = Path(uploaded.name).suffix or ".mp4"
        tmpf = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmpf.write(uploaded.read())
        tmpf.flush()
        tmpf.close()
        temp_video_path = tmpf.name
        st.session_state.uploaded_video_path = temp_video_path

        # Show the video preview
        with st.expander("Preview video"):
            st.video(temp_video_path)

        # Video info
        info = get_video_info(temp_video_path)
        if "error" in info:
            st.error(info["error"])
        else:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("FPS", f"{info['fps']:.2f}")
            with c2:
                st.metric("Total Frames", f"{info['total_frames']}")
            with c3:
                st.metric("Duration", info["duration_hms"])

            st.markdown("<div class='note'>Tip: The frames will be spaced uniformly across the full duration.</div>", unsafe_allow_html=True)

            # Number-only input
            num_images = st.number_input(
                "Number of images to extract",
                min_value=1,
                max_value=info["total_frames"] if info["total_frames"] > 0 else None,
                value=min(30, info["total_frames"]) if info["total_frames"] > 0 else 30,
                step=1,
                help="Uniformly spaced frames from start to end."
            )

            # Split button
            if st.button("Split to Images", type="primary", use_container_width=False):
                with st.spinner("Extracting frames..."):
                    with tempfile.TemporaryDirectory() as outdir:
                        result = extract_frames_by_count(temp_video_path, outdir, int(num_images))
                        if "error" in result:
                            st.error(result["error"])
                        else:
                            st.success(f"Extracted {result['frames_extracted']} images.")
                            st.caption(f"Sampling rule: {result['sampling_rule']}")
                            # Build a zip in memory
                            zip_bytes, zip_name = make_zip_bytes(result["saved_files"], zip_basename=f"{Path(uploaded.name).stem}_frames")
                            st.session_state.last_zip = zip_bytes
                            st.session_state.last_zip_name = zip_name

            # Download area
            if st.session_state.last_zip:
                st.markdown("### Download")
                with st.container():
                    st.markdown("<div class='download-area'>", unsafe_allow_html=True)
                    st.download_button(
                        label="⬇️ Download images as ZIP",
                        data=st.session_state.last_zip,
                        file_name=st.session_state.last_zip_name,
                        mime="application/zip",
                        use_container_width=True
                    )
                    st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info("Upload a video to begin.")

with tab2:
    st.header("😊 Emotion Detection")
    st.write("""tbd    
    """)
    st.divider()
    st.write("For now, upload any images to preview how you'd stage inputs:")

    imgs = st.file_uploader("Select extracted image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if imgs:
        cols = st.columns(3)
        for i, img in enumerate(imgs):
            with cols[i % 3]:
                st.image(img, caption=img.name, use_column_width=True)
        st.info("🔧 tbd")
