import questionary

def get_reference_input(reference_data=None):
    fields = [
        ("authors", "text"), ("year", "text"), ("title", "text"), 
        ("journal_conference", "text"), ("doi_url", "text")
    ]

    data = reference_data if reference_data else {}
    for field_name, field_type in fields:
        default_value = data.get(field_name, "")
        if field_type == "text":
            answer = questionary.text(f"Enter {field_name.replace('_', ' ').title()}:", default=default_value).ask()
        
        if answer is not None:
            data[field_name] = answer
    return data

def get_chapter_input(chapter_data=None):
    fields = [
        ("chapter_title", "text"), ("content_summary", "text"), 
        ("key_concepts", "text"), ("status", "select", ["Outline", "Drafting", "Review", "Completed"])
    ]

    data = chapter_data if chapter_data else {}
    for field_name, field_type, *options in fields:
        default_value = data.get(field_name, "")
        if field_type == "text":
            answer = questionary.text(f"Enter {field_name.replace('_', ' ').title()}:", default=default_value).ask()
        elif field_type == "select":
            answer = questionary.select(f"Select {field_name.replace('_', ' ').title()}:", choices=options[0], default=default_value).ask()
        
        if answer is not None:
            data[field_name] = answer
    return data
