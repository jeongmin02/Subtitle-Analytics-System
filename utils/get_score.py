import json
import os


def calculate_composite_scores(input_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for scene in data:
        composite_results = []
        for score in scene.get("emotion_scores", []):
            before = score["before_score"]
            after = score["after_score"]
            delta = after - before

            if before == 0:
                # Division by zero guard
                boost_ratio = 0
                composite_score = 0
            else:
                boost_ratio = delta / before
                composite_score = delta * boost_ratio

            composite_results.append({
                "emotion": score["emotion"],
                "delta": delta,
                "boost_ratio": round(boost_ratio, 2),
                "composite_score": round(composite_score, 2)
            })

        scene["composite_scores"] = composite_results

    return data


def save_output(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    input_file = "/Users/jmrhee/Subtitle-Analytics-System/subtitle/src/data/analysis6.json"
    output_file = "/Users/jmrhee/Subtitle-Analytics-System/subtitle/src/data/analysis6_with_scores.json"

    result = calculate_composite_scores(input_file)
    save_output(result, output_file)
    print(f"Saved composite score results to: {output_file}")