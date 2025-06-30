def format_to_zotero_rdf(reference):
    # Zotero RDF is more complex and typically involves XML/RDF serialization.
    # For a simple text export, we'll provide a basic representation.
    # A full implementation would require an RDF library.
    rdf_entry = f"""<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:bib="http://purl.org/net/biblio#"
    xmlns:dc="http://purl.org/dc/elements/1.1/">
  <bib:Article rdf:about="urn:doi:{reference.get("doi_url", "")}">
    <dc:title>{reference.get("title", "")}</dc:title>
    <dc:creator>{reference.get("authors", "")}</dc:creator>
    <dc:date>{reference.get("year", "")}</dc:date>
    <bib:journal>{reference.get("journal_conference", "")}</bib:journal>
    <bib:doi>{reference.get("doi_url", "")}</bib:doi>
  </bib:Article>
</rdf:RDF>"""
    return rdf_entry