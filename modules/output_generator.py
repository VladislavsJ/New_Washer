def generate_final_output(filtered_text, verification_report):
    """
    Combines the filtered text and the verification report into the final output.
    Returns a dictionary suitable for JSON output.
    """
    final_text = f"{filtered_text}\n\n---\nVerification Result: {verification_report['result']}\nDetails: {verification_report['details']}"
    
    return {
        "refined_content": filtered_text,
        "verification_report": verification_report,
        "final_output": final_text
    }
