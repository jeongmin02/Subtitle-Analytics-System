
# 🎞️ Video Frame Extractor

Extract frames from a video at a fixed interval and generate a metadata JSON file with frame information.

---

## 📥 Input Command

```bash
python3 extract_frames.py /path/to/video.mp4 /path/to/output_dir --interval 1.0
```

### Arguments

- `input_video` (required): Path to the input `.mp4` video file.
- `output_dir` (optional): Directory to save the extracted frames and metadata (default: `./frames`).
- `--interval` or `-i` (optional): Time interval in seconds between frames (default: `1.0`).

---

## 📤 Output

For every interval (e.g., 1.0 second), the script:
- Extracts a single frame from the video.
- Saves it as a JPEG image.
- Records the metadata for each frame in a JSON file.

### Example Output Files:
- `frame_000000.jpg`
- `frame_000001.jpg`
- ...
- `frame_metadata.json`

---

## 📁 Directory Structure

Assuming the command:

```bash
python3 extract_frames.py input.mp4 output_frames --interval 1.0
```

The resulting directory will look like this:

```
output_frames/
├── frame_000000.jpg
├── frame_000001.jpg
├── frame_000002.jpg
├── ...
└── frame_metadata.json
```

### `frame_metadata.json` example:

```json
[
    {
        "id": 0,
        "start_time": 0.0,
        "end_time": 1.0,
        "frame_name": "frame_000000.jpg"
    },
    {
        "id": 1,
        "start_time": 1.0,
        "end_time": 2.0,
        "frame_name": "frame_000001.jpg"
    }
]
```

---

## 🛠️ Requirements

- Python 3.x
- OpenCV (`cv2`)

Install OpenCV if you haven't already:

```bash
pip install opencv-python
```

---

## 🧾 License

MIT License
