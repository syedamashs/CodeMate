import time


def run_evaluation(provider, dataset_name: str, samples: int, dataset_service):
    dataset = dataset_service.sample(dataset_name, samples)
    if not dataset or not dataset["available"]:
        return {"available": False, "message": dataset["message"] if dataset else "Dataset not found."}
    try:
        rows = dataset_service.load_samples(dataset_name, samples)
    except Exception as exc:
        return {"available": False, "message": f"Could not load {dataset_name}: {exc}"}
    successful = 0
    latencies = []
    results = []
    for index, row in enumerate(rows, start=1):
        code = row.get("code") or row.get("canonical_solution") or row.get("prompt", "")
        if not code.strip():
            continue
        started = time.perf_counter()
        try:
            result = provider.analyze("Python", code, "")
            latency = round(time.perf_counter() - started, 3)
            successful += 1
            latencies.append(latency)
            results.append({"test_id": row.get("task_id", f"sample-{index}"), "bug_type": result.get("bug_type", "N/A"), "latency": latency})
        except Exception:
            continue
    average_latency = round(sum(latencies) / len(latencies), 3) if latencies else "N/A"
    return {"available": True, "message": "Evaluation completed. Generated code was not executed; bug and fix accuracy require labelled expectations.",
            "samples_evaluated": len(rows), "successful_responses": successful, "bug_detection": "N/A", "fix_success": "N/A", "average_latency": average_latency, "results": results}
