def generate_final_output(filtered_text, verification_report, links):
    """
    Combines the filtered text, verification report, and links into the final output.
    Returns a dictionary suitable for JSON output.
    """
    final_output = {
        "filtered_text": filtered_text,
        "verification_report": verification_report,
        "links": links
    }
    return final_output
