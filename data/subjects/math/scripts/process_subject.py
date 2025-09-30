import os
import sys
import json

# -----------------------
# CONFIGURATION
# -----------------------

# Mapping: filename -> id/category
category_info = {
    "algtop.txt":      {"id": "math.AT", "category": "Algebraic Topology"},
    "comalg.txt":      {"id": "math.AC", "category": "Commutative Algebra"},
    "diffeqn.txt":     {"id": "math.DE", "category": "Differential Equations"},
    "funcanalysis.txt":{"id": "math.FA", "category": "Functional Analysis"},
    "geotop.txt":      {"id": "math.GT", "category": "Geometric Topology"},
    "grouptheory.txt": {"id": "math.GR", "category": "Group Theory"},
    "histmath.txt":    {"id": "math.HM", "category": "History of Mathematics"},
    "linalg.txt":      {"id": "math.LA", "category": "Linear Algebra"},
    "mathgeneral.txt": {"id": "math.GM", "category": "General Mathematics"},
    "numanalysis.txt": {"id": "math.NA", "category": "Numerical Analysis"},
    "numtheory.txt":   {"id": "math.NT", "category": "Number Theory"},
    "opalg.txt":       {"id": "math.OP", "category": "Operator Algebra"},
    "prob.txt":        {"id": "math.PR", "category": "Probability"},
    "qalg.txt":        {"id": "math.QA", "category": "Quantum Algebra"},
    "spectheory.txt":  {"id": "math.ST", "category": "Spectral Theory"}
}

allowed_statuses = ["✅ Complete", "❌ Missing", "⚠️ Revision"]

# -----------------------
# HELPERS
# -----------------------

def clean_sort_txt(file_path):
    """
    Remove duplicates and sort words in a txt file.
    Preserves any header lines that start with '#'.
    Returns the list of cleaned words.
    """
    if not os.path.isfile(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Separate header lines
    headers = [line for line in lines if line.startswith("#")]
    words = [line for line in lines if not line.startswith("#")]

    # Remove duplicates and sort
    unique_sorted = sorted(set(words), key=str.lower)

    # Write back to the file, preserving headers
    with open(file_path, "w", encoding="utf-8") as f:
        for header in headers:
            f.write(header + "\n")
        for word in unique_sorted:
            f.write(word + "\n")

    return unique_sorted

def update_terms_json(terms_json_path, words_by_file):
    """Update terms.json with new words and update id/category if needed."""

    # Load existing terms.json if available
    if os.path.isfile(terms_json_path):
        with open(terms_json_path, "r", encoding="utf-8") as f:
            try:
                terms_data = json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️ Failed to parse {terms_json_path}, starting fresh.")
                terms_data = []
    else:
        terms_data = []

    # Build lookup dict for quick access
    terms_lookup = {term["english"]: term for term in terms_data}

    for file_name, words in words_by_file.items():
        info = category_info.get(file_name)
        if not info:
            print(f"⚠️ No category info for {file_name}, skipping...")
            continue

        for word in words:
            if word in terms_lookup:
                # Update id/category only if different
                term = terms_lookup[word]
                if term.get("id") != info["id"]:
                    term["id"] = info["id"]
                if term.get("category") != info["category"]:
                    term["category"] = info["category"]
            else:
                # Add new term with default fields
                new_term = {
                    "english": word,
                    "azerbaijani": "",
                    "status": "❌ Missing",
                    "part_of_speech": "",
                    "id": info["id"],
                    "category": info["category"]
                }
                terms_data.append(new_term)
                terms_lookup[word] = new_term

    # Sort terms.json by category then english
    terms_data_sorted = sorted(terms_data, key=lambda x: (x["category"].lower(), x["english"].lower()))

    # Save back to terms.json
    with open(terms_json_path, "w", encoding="utf-8") as f:
        json.dump(terms_data_sorted, f, ensure_ascii=False, indent=2)

    print(f"✅ Updated {terms_json_path} with {len(words_by_file)} category files.")

    return terms_data_sorted

def validate_terms_json(subject_name, terms):
    """Validate terms.json fields (categories, statuses, duplicates)."""
    errors = []
    seen_english = set()
    seen_azerbaijani = set()

    math_categories = {info["category"] for info in category_info.values()}

    for i, term in enumerate(terms, start=1):
        english = term.get("english", "").strip()
        azerbaijani = term.get("azerbaijani", "").strip()
        category = term.get("category", "").strip()
        status = term.get("status")

        if not english:
            errors.append(f"Term #{i} missing English field.")
            continue

        if not azerbaijani:
            term["status"] = "❌ Missing"

        if status and status not in allowed_statuses:
            errors.append(f"Invalid status '{status}' in Term #{i}")

        if english in seen_english:
            errors.append(f"Duplicate English '{english}' in Term #{i}")
            continue
        if azerbaijani in seen_azerbaijani and term["status"] != "❌ Missing":
            errors.append(f"Duplicate Azerbaijani '{azerbaijani}' in Term #{i}")
            continue
        if category and category not in math_categories:
            errors.append(f"Invalid category '{category}' in Term #{i}. Allowed: {math_categories}")
            continue

        seen_english.add(english)
        seen_azerbaijani.add(azerbaijani)

    if errors:
        print(f"⚠️ {subject_name}: Validation issues found:")
        for e in errors:
            print(" - " + e)
        sys.exit(1)
    else:
        print(f"✅ {subject_name}: terms.json validated successfully.")

# -----------------------
# MAIN
# -----------------------

def main(subject_dir):
    categories_dir = os.path.join(subject_dir, "categories")
    if not os.path.isdir(categories_dir):
        print(f"❌ Categories folder not found: {categories_dir}")
        return

    # Process each category txt file
    words_by_file = {}
    for file_name in os.listdir(categories_dir):
        if file_name.endswith(".txt"):
            file_path = os.path.join(categories_dir, file_name)
            words = clean_sort_txt(file_path)
            words_by_file[file_name] = words

    # Merge all words into <subject>_terms.txt
    all_words = sorted({word for words in words_by_file.values() for word in words}, key=str.lower)
    subject_name = os.path.basename(subject_dir)
    subject_terms_file = os.path.join(subject_dir, f"{subject_name}_terms.txt")
    with open(subject_terms_file, "w", encoding="utf-8") as f:
        for word in all_words:
            f.write(word + "\n")
    print(f"✅ Generated {subject_terms_file} with {len(all_words)} words.")

    # Update terms.json
    terms_json_path = os.path.join(subject_dir, "terms.json")
    terms = update_terms_json(terms_json_path, words_by_file)

    # Validate terms.json
    validate_terms_json(subject_name, terms)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_subject.py <subject_folder>")
        sys.exit(1)

    main(sys.argv[1])
