import json
import sys
import os

subject_dir = sys.argv[1]
subject_name = os.path.basename(subject_dir)
terms_file = os.path.join(subject_dir, "terms.json")
md_dir = "glossary"
os.makedirs(md_dir, exist_ok=True)
md_file = os.path.join(md_dir, f"{subject_name}.md")

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

with open(md_file, "w", encoding="utf-8") as f:
    f.write(f"# {subject_name} Glossary\n\n")
    f.write("| Category | English | Azerbaijani |\n")
    f.write("|---------|---------|------------|\n")
    for t in terms:
        f.write(f"| {t.get('category','')} | {t['english']} | {t.get('azerbaijani','')} |\n")

print(f"✅ Markdown glossary generated for {subject_name} → {md_file}")