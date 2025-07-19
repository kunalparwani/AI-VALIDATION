import json
def aggregate_results_all(ml_results, non_ml_results):
    """
    Aggregates ML model results and non-ML tool results into a structured final output.
    """

    final_output = {
        "ml_results_summary": [],
        "non_ml_results_summary": []
    }

    # 🔷 ✅ Process ML results
    for vuln_type, result in ml_results.items():
        final_output["ml_results_summary"].append({
            "vulnerability": vuln_type,
            "status": result["label"]
        })

    # 🔷 ✅ Process Non-ML tool results (Bandit findings)
    if isinstance(non_ml_results, str):
        # If Bandit returns raw JSON string, parse if needed
        import json
        try:
            non_ml_results = json.loads(non_ml_results)
        except Exception as e:
            non_ml_results = [{"error": f"Failed to parse Bandit output: {str(e)}"}]

    final_output["non_ml_results_summary"] = non_ml_results

    # 🔷 ✅ Add any overall aggregation logic here
    # For example, flag code as vulnerable if any model or tool detected issues
    overall_status = "secure"
    for ml in final_output["ml_results_summary"]:
        if ml["status"] == "vulnerable":
            overall_status = "vulnerable"
            break
    if len(non_ml_results) > 0:
        overall_status = "vulnerable"

    final_output["overall_status"] = overall_status

    return final_output
