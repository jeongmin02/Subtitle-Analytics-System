# extract_frames.py

import cv2
import os
import sys
import argparse

def extract_frames(input_path: str, output_dir: str, interval: float = 0.5):
    """
    :param input_path:  입력 비디오 파일 경로
    :param output_dir:  추출된 프레임을 저장할 디렉토리
    :param interval:    저장 간격(초 단위), 기본 0.5s
    """
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"[Error] Cannot open video file: {input_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    # 다음 저장 시점을 0초부터 시작
    next_save_time = 0.0
    saved_count   = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 현재 재생 시간 (초 단위)
        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

        # 저장 시점을 지났으면 dump
        if current_time >= next_save_time:
            fname = os.path.join(output_dir, f"frame_{saved_count:06d}.jpg")
            cv2.imwrite(fname, frame)
            saved_count += 1
            next_save_time += interval

    cap.release()
    print(f"[Info] Extracted {saved_count} frames (every {interval}s) to {output_dir}")

def main():
    parser = argparse.ArgumentParser(
        description="Extract video frames at a fixed time interval")
    parser.add_argument("input_video", help="Path to input video file")
    parser.add_argument("output_dir", nargs="?",
                        default="frames",
                        help="Directory to save frames")
    parser.add_argument("--interval", "-i", type=float, default=0.5,
                        help="Time interval between frames in seconds (default: 0.5)")
    args = parser.parse_args()

    extract_frames(args.input_video, args.output_dir, args.interval)

if __name__ == "__main__":
    main()
