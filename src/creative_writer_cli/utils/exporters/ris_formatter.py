def format_to_ris(reference):
    # Basic RIS formatting
    ris_entry = ""
    ris_entry += "TY  - JOUR\n"
    for author in reference.get("authors", "").split(" and "): # Assuming "and" separates authors
        ris_entry += f"AU  - {author.strip()}\n"
    ris_entry += f"PY  - {reference.get("year", "")}\n"
    ris_entry += f"TI  - {reference.get("title", "")}\n"
    ris_entry += f"JO  - {reference.get("journal_conference", "")}\n"
    ris_entry += f"DO  - {reference.get("doi_url", "")}\n"
    ris_entry += "ER  - \n"
    return ris_entry
