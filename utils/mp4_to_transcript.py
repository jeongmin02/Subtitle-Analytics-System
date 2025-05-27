import whisper
import os
import json

def transcribe_mp4(mp4_path, output_prefix="transcript"):
    # base/small/medium/large 
    model = whisper.load_model("large") 
    print("Transcribing...")
    result = model.transcribe(mp4_path, verbose=True)

    simple_segments = []
    for idx, seg in enumerate(result['segments']):
        simple_segments.append({
            "id": idx,
            "subtitle": seg['text'].strip(),
            "start_time": format_timestamp(seg['start']),
            "end_time": format_timestamp(seg['end'])
        })

    # ✅ JSON 저장 (간결한 형식)
    json_path = f"{output_prefix}.json"
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(simple_segments, jf, ensure_ascii=False, indent=2)

    # ✅ 텍스트도 병렬 저장
    txt_path = f"{output_prefix}.txt"
    with open(txt_path, "w", encoding="utf-8") as tf:
        for s in simple_segments:
            tf.write(f"[{s['start_time']} --> {s['end_time']}]\n{s['subtitle']}\n\n")

    print(f"Saved to {json_path} and {txt_path}")

def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("mp4_path", help="Path to the input MP4 file")
    parser.add_argument("--output", default="transcript", help="Output filename prefix")
    args = parser.parse_args()

    transcribe_mp4(args.mp4_path, args.output)
