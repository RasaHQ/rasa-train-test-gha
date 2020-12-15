# Collect the results of the various model test runs
import json
import os

SUMMARY_FILE = os.environ["SUMMARY_FILE"]
CONFIG = os.environ["CONFIG"]
DATASET = os.environ["DATASET_NAME"]
task_mapping = {
    "story_report.json": "story_prediction",
    "intent_report.json": "intent_classification",
    "CRFEntityExtractor_report.json": "entity_prediction",
    "DIETClassifier_report.json": "entity_prediction",
    "response_selection_report.json": "response_selection",
}


def generate_json(file, task, data):
    if not DATASET in data:
        data = {DATASET: {CONFIG: {}}, **data}
    elif not CONFIG in data[DATASET]:
        data[DATASET] = {CONFIG: {}, **data[DATASET]}

    data[DATASET][CONFIG] = {
        **data[DATASET][CONFIG],
    }

    data[DATASET][CONFIG][task] = {**read_results(file)}

    return data


def read_results(file):
    with open(file) as json_file:
        data = json.load(json_file)

        keys = ["accuracy", "weighted avg", "macro avg", "micro avg"]
        key_mapping = {
            "weighted avg": "weighted_avg",
            "macro avg": "macro_avg",
            "micro avg": "micro_avg",
            "accuracy": "accuracy"
        }
        result = {key_mapping[key]: data[key] for key in keys if key in data}

    return result


if __name__ == "__main__":
    data = {}
    if os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE) as json_file:
            data = json.load(json_file)

    for dirpath, dirnames, files in os.walk(os.environ["RESULT_DIR"]):
        for f in files:
            if f not in task_mapping.keys():
                continue

            data = generate_json(os.path.join(dirpath, f), task_mapping[f], data)

    with open(SUMMARY_FILE, "w") as f:
        json.dump(data, f, sort_keys=True, indent=2)
