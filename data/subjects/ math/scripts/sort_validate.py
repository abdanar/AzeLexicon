import json
import sys
import os

# Get subject folder from argument
subject_dir = sys.argv[1]
subject_name = os.path.basename(subject_dir)
terms_file = os.path.join(subject_dir, "terms.json")

# Predefined allowed categories
math_categories = ["Arithmetic", "Algebra", "Calculus", "Geometry", "Statistics"]

# Check if JSON exists
if not os.path.isfile(terms_file):
    print(f"❌ Error: terms.json not found for {subject_name}")
    sys.exit(1)

# Load JSON
try:
    with open(terms_file, "r", encoding="utf-8") as f:
        terms = json.load(f)
except json.JSONDecodeError as e:
    print(f"❌ Error: Failed to parse JSON - {e}")
    sys.exit(1)

# Validation + strict duplicate removal
errors = []
seen_english = set()
seen_azerbaijani = set()
clean_terms = []

for i, term in enumerate(terms, start=1):
    english = term.get("english", "").strip()
    azerbaijani = term.get("azerbaijani", "").strip()
    category = term.get("category", "").strip()

    if not english or not azerbaijani:
        errors.append(f"Term #{i} missing English/Azerbaijani field. Skipped.")
        continue

    if category and category not in math_categories:
        errors.append(f"Invalid category '{category}' in Term #{i}. Allowed: {math_categories}")
        continue

    # Strict duplicate check: skip if either exists
    if english in seen_english or azerbaijani in seen_azerbaijani:
        errors.append(f"Duplicate detected (English: '{english}' / Azerbaijani: '{azerbaijani}') Term #{i} skipped.")
        continue

    clean_terms.append(term)
    seen_english.add(english)
    seen_azerbaijani.add(azerbaijani)

# Sort by category then English
clean_terms = sorted(clean_terms, key=lambda x: (x.get("category", "").lower(), x["english"].lower()))

# Save cleaned JSON
with open(terms_file, "w", encoding="utf-8") as f:
    json.dump(clean_terms, f, ensure_ascii=False, indent=2)

# Report
print(f"✅ {subject_name}: terms.json validated, duplicates removed, sorted!")
if errors:
    print("⚠️ Warnings / skipped entries:")
    for e in errors:
        print(f" - {e}")
    print("❌ Validation failed. Please fix duplicates or invalid categories.")
    sys.exit(1)
