import json
import sys
import os

subject_dir = sys.argv[1]
subject_name = os.path.basename(subject_dir)
terms_file = os.path.join(subject_dir, "terms.json")
md_dir = os.path.join(os.getcwd(), "glossary")
os.makedirs(md_dir, exist_ok=True)
md_file = os.path.join(md_dir, f"{subject_name}.md")

# 1️⃣ Check if JSON exists and is valid
if not os.path.isfile(terms_file):
    print(f"⚠️ No terms.json found for {subject_name}, skipping...")
    sys.exit(0)

if os.path.getsize(terms_file) == 0:
    print(f"⚠️ {terms_file} is empty, skipping...")
    sys.exit(0)

try:
    with open(terms_file, "r", encoding="utf-8") as f:
        terms = json.load(f)
except json.JSONDecodeError:
    print(f"❌ Invalid JSON in {terms_file}, skipping...")
    sys.exit(0)

# 2️⃣ Process terms
total_terms = len(terms)
missing_count = sum(1 for t in terms if t.get("azerbaijani") == "❌ Missing")
revision_count = sum(1 for t in terms if t.get("status") == "⚠️ Revision")
completed_count = sum(1 for t in terms if t.get("status") == "✅ Complete")

# 3️⃣ Write Markdown
with open(md_file, "w", encoding="utf-8") as f:
    f.write(f"# {subject_name} Glossary\n\n")
    f.write(f"- Total terms: **{total_terms}**\n")
    f.write(f"- Missing translations: **{missing_count}**\n")
    f.write(f"- Revisions needed: **{revision_count}**\n\n")
    f.write(f"- Completed translations: **{completed_count}**\n")

    f.write("| Category | English | Azerbaijani | Status |\n")
    f.write("|---------|---------|------------|--------|\n")
    for t in terms:
        f.write(f"| {t.get('category','')} | {t['english']} | {t.get('azerbaijani','')} | {t.get('status', '')} |\n")

print(f"✅ Markdown glossary generated for {subject_name} → {md_file}")