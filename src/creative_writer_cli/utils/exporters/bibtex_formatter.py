def format_to_bibtex(reference):
    # Basic BibTeX formatting for an article
    # Assumes 'journal_conference' is the journal title
    # You might need to refine this based on specific BibTeX entry types and fields
    authors = reference.get("authors", "").replace(" and ", " and ")
    title = reference.get("title", "")
    year = reference.get("year", "")
    journal = reference.get("journal_conference", "")
    doi = reference.get("doi_url", "")

    bibtex_entry = f"""@article{{{reference.get("title", "").replace(" ", "").replace(":", "")}{year},
    author = {{{authors}}},
    title = {{{title}}},
    journal = {{{journal}}},
    year = {{{year}}},
    doi = {{{doi}}}
}}"""
    return bibtex_entry