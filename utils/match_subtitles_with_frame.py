import json
import re
from datetime import datetime
from pathlib import Path
from PIL import Image
import pytesseract


def timestamp_to_seconds(ts):
    h, m, s_ms = ts.split(":")
    s, ms = s_ms.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_overlapping_frames(sub_start, sub_end, frame_meta):
    frames = []
    for frame in frame_meta:
        f_start = frame["start_time"]
        f_end = frame["end_time"]
        if f_end > sub_start and f_start < sub_end:
            frames.append(frame["frame_name"])
    return frames

def ocr_contains_subtitle(frame_path, subtitle_text):
    try:
        img = Image.open(frame_path).convert("L") 
        img = img.point(lambda x: 0 if x < 170 else 255, "1") 

        ocr_text = pytesseract.image_to_string(img, lang="kor+eng")
        
        ocr_text_clean = re.sub(r"\s+", "", ocr_text)
        subtitle_clean = re.sub(r"\s+", "", subtitle_text)

        return subtitle_clean in ocr_text_clean
    except Exception as e:
        print(f"OCR error in {frame_path}: {e}")
        return False

def process_subtitles(result_path, frame_meta_path, frame_dir, output_path):
    subtitles = load_json(result_path)
    frames = load_json(frame_meta_path)

    for sub in subtitles:
        sub_start = timestamp_to_seconds(sub["start_time"])
        sub_end = timestamp_to_seconds(sub["end_time"])

        matched_frames = get_overlapping_frames(sub_start, sub_end, frames)
        sub["frames"] = matched_frames

        sub["is_displayed"] = False
        for fname in matched_frames:
            if ocr_contains_subtitle(Path(frame_dir) / fname, sub["subtitle"]):
                sub["is_displayed"] = True
                break

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(subtitles, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    process_subtitles(
        result_path="./result.json",
        frame_meta_path="./frame_metadata.json",
        frame_dir="./frames", 
        output_path="./result_augmented.json"
    )
