import cv2
import os
import math
import zipfile
import io
from pathlib import Path

# ---------------------------
# Video utilities
# ---------------------------
def get_video_info(video_path: str) -> dict:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"error": "Cannot open video file"}
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps and fps > 0 else 0
    cap.release()
    return {
        "fps": fps,
        "total_frames": total_frames,
        "duration_seconds": duration,
        "duration_hms": f"{int(duration // 3600):02}:{int((duration % 3600) // 60):02}:{int(duration % 60):02}",
    }

# ------------------------------------------------

def extract_frames_by_rate(video_path, output_folder, frames_per_second=1.0):
    """
    Extract frames at a target rate (can be fractional). Picks frames at times:
      t = 0, 1/fps_target, 2/fps_target, ... < duration
    Converts times to frame indices via round(t * fps). Uses seeking for efficiency.
    Returns info dict + list of saved file paths.
    """
    os.makedirs(output_folder, exist_ok=True)

    info = get_video_info
    
    (video_path)
    if "error" in info:
        return info

    fps = info["fps"]
    duration = info["duration_seconds"]
    total_frames = info["total_frames"]
    if not fps or fps <= 0 or total_frames == 0 or duration == 0:
        return {"error": "Video has invalid metadata (fps/frames/duration).", **info}

    if frames_per_second <= 0:
        return {"error": "frames_per_second must be > 0.", **info}

    num_samples = math.ceil(duration * frames_per_second)
    target_times = [(i / frames_per_second) for i in range(num_samples)]
    frame_indices = sorted(
        {min(int(round(t * fps)), total_frames - 1) for t in target_times if t < duration}
    )
    if 0 not in frame_indices:
        frame_indices = [0] + frame_indices

    cap = cv2.VideoCapture(video_path)
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    extracted_count = 0
    saved_files = []

    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret or frame is None:
            continue
        extracted_count += 1
        ts_sec = idx / fps
        frame_filename = f"{base_name}_{extracted_count:04d}_t{ts_sec:.2f}s.jpg"
        out_path = os.path.join(output_folder, frame_filename)
        cv2.imwrite(out_path, frame)
        saved_files.append(out_path)

    cap.release()

    return {
        **info,
        "frames_requested_per_second": frames_per_second,
        "frames_planned": len(frame_indices),
        "frames_extracted": extracted_count,
        "output_folder": output_folder,
        "saved_files": saved_files,
        "sampling_rule": "t = 0, 1/fps_target, 2/fps_target, … < duration; index = round(t * fps)",
    }

# ------------------------------------------------

def extract_frames_by_count(video_path, output_folder, num_images: int):
    """
    Uniformly pick `num_images` frames from the whole video [0, total_frames-1].
    Returns info dict + list of saved file paths.
    """
    os.makedirs(output_folder, exist_ok=True)

    info = get_video_info(video_path)
    if "error" in info:
        return info

    fps = info["fps"]
    total_frames = info["total_frames"]
    duration = info["duration_seconds"]

    if not fps or fps <= 0 or total_frames == 0 or duration == 0:
        return {"error": "Video has invalid metadata (fps/frames/duration).", **info}

    if not num_images or num_images <= 0:
        return {"error": "Number of images must be > 0.", **info}

    # If num_images > total_frames, cap it (or allow duplicates).
    num_images = min(num_images, total_frames)

    # Evenly spaced indices across [0, total_frames-1]
    # Using round to distribute nicely
    indices = sorted({int(round(i * (total_frames - 1) / (num_images - 1))) for i in range(num_images)}) if num_images > 1 else [0]

    cap = cv2.VideoCapture(video_path)
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    saved_files = []

    for i, idx in enumerate(indices, start=1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret or frame is None:
            continue
        ts_sec = idx / fps
        frame_filename = f"{base_name}_{i:04d}_t{ts_sec:.2f}s.jpg"
        out_path = os.path.join(output_folder, frame_filename)
        cv2.imwrite(out_path, frame)
        saved_files.append(out_path)

    cap.release()

    return {
        **info,
        "frames_requested": num_images,
        "frames_extracted": len(saved_files),
        "output_folder": output_folder,
        "saved_files": saved_files,
        "sampling_rule": "Uniform spacing over [0 .. last frame].",
    }

# ------------------------------------------------

def make_zip_bytes(paths, zip_basename="frames_bundle"):
    """
    Create an in-memory zip from a list of file paths. Returns (zip_bytes, zip_filename)
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in paths:
            arcname = Path(p).name
            zf.write(p, arcname=arcname)
    zip_buffer.seek(0)
    return zip_buffer.read(), f"{zip_basename}.zip"

# ------------------------------------------------