# Video-to-Emotion Frame Extractor 🎥🙂

This repository provides a pipeline to process video files by extracting frames, detecting human faces, and tagging the detected emotions. The output is a chronologically ordered set of frames that contain human faces and their corresponding emotions.

---

## 🚀 Features
1. **Frame Extraction**  
   - Takes a video file and breaks it into frames at a user-defined interval.
2. **Face Detection**  
   - Identifies human faces in each frame.
   - Discards frames without faces.
3. **Emotion Recognition**  
   - Tags each detected face with its corresponding emotion (e.g., happy, sad, angry, surprised, etc.).
4. **Chronological Output**  
   - Saves only the relevant frames (with faces) in chronological order.
   - Filenames are annotated with the detected emotion.

---

## 📂 Project Structure
```
├── sample/                 # Example videos & outputs
│   ├── input/              # Raw input videos
│   ├── frames_output/      # Extracted frames
│   └── processed/          # Frames with detected faces & emotions
├── scripts/
│   ├── extract_frames.py   # Script for frame extraction
│   ├── detect_faces.py     # Script for face detection
│   ├── detect_emotions.py  # Script for emotion recognition
│   └── pipeline.py         # Main pipeline combining all steps
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## ⚙️ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/video-emotion-extractor.git
   cd video-emotion-extractor
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

### 1. Extract frames from a video
```bash
python scripts/extract_frames.py --video sample/input/video.mp4 --output sample/frames_output --interval 10
```
- `--interval`: Extract every Nth frame (e.g., 10 = every 10th frame).

### 2. Detect faces from frames
```bash
python scripts/detect_faces.py --input sample/frames_output --output sample/processed
```

### 3. Detect emotions
```bash
python scripts/detect_emotions.py --input sample/processed --output sample/processed
```

### 4. Run the entire pipeline
```bash
python scripts/pipeline.py --video sample/input/video.mp4 --output sample/processed --interval 10
```

---

## 🧠 Emotion Categories
The current model can detect the **7 basic emotions**:
- Happy 😀  
- Sad 😢  
- Angry 😡  
- Surprised 😲  
- Fearful 😨  
- Disgusted 🤢  
- Neutral 😐  

---

## 🔧 Dependencies
- Python 3.8+
- [OpenCV](https://opencv.org/)
- [TensorFlow / PyTorch](https://pytorch.org/) (for emotion detection model)
- Pre-trained emotion recognition model (to be configured in `detect_emotions.py`)

Install them with:
```bash
pip install -r requirements.txt
```

---

## 📊 Example Output
For an input video of 60 seconds at 30 FPS (≈1800 frames):
- Extracted frames: 180 (interval = 10)
- Frames with faces: 120
- Final saved frames with emotions: 120, named like:
  ```
  frame_001_happy.jpg
  frame_002_sad.jpg
  frame_003_neutral.jpg
  ```

---

## 🌟 Roadmap
- [ ] Add support for multiple faces per frame  
- [ ] Store results in CSV (frame → emotion mapping)  
- [ ] Provide visualization dashboard (e.g., workflow, emotion timeline)  
- [ ] Optimize for real-time streaming  

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 🙏 Acknowledgments

Sample video used in this repository:
- ["The 7 Basic Emotions - Do you recognise all facial expressions?"](https://www.youtube.com/watch?v=YOUR_VIDEO_ID) on YouTube.  
All rights belong to the original creator.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
