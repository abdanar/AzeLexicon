# AzeLexicon – Azerbaijani Word List & Terminology

![GitHub Repo Size](https://img.shields.io/github/repo-size/abdanar/AzeLexicon)
![GitHub Issues](https://img.shields.io/github/issues/abdanar/AzeLexicon)
![License](https://img.shields.io/github/license/abdanar/AzeLexicon)

**AzeLexicon** is a structured, open-source repository of Azerbaijani words and terminology. Its main purpose is to serve as the **primary source for the Azerbaijani word list, its hyphenated version, and academic/scientific terminology**, supporting anyone producing **academic or scientific work in Azerbaijani**.

## 📚 Project Scope

The repository includes:

- **General word list**  
  A plain list of Azerbaijani words (`txt` format). It contains only words, without translations. Some cleanup and refinement are still needed.  

- **Hyphenated words**  
  A hyphenated version of the general word list. This list is not yet complete, as the **hyphenation algorithm** is under active development.  

- **Academic and scientific terminology**  
  Organized by subject (mathematics, physics, computer science, etc.).  
  Each subject has a main file (`terms.json`) containing the **translations of English terms into Azerbaijani**.  
  Subfields (e.g., linear algebra, topology) are used for **initial collection of terms**, which are then consolidated into the main `terms.json`.

This project aims to be the **authoritative reference** for Azerbaijani in scientific and academic contexts.


## Repository Structure

```text
AzeLexicon/
├── data/
│   ├── general/
│   │   ├── words.txt                  # plain list of Azerbaijani words (no translations)
│   │   └── words-hyphenated.txt      # hyphenated version of the general word list
│   │
│   ├── scripts/
│   │   ├── generate_markdown.py       # utility to generate markdown docs from terms
│   │   └── hyphenation.py             # experimental hyphenation algorithm
│   │
│   └── subjects/
│       ├── math/
│       │   ├── terms.json             # glossary of math terms (EN ↔ AZ)
│       │   ├── subfields/
│       │   │   ├── linalg.txt         # collected linear algebra terms
│       │   │   ├── topology.txt       # collected topology terms
│       │   │   └── ...                # more subfields to be added
│       │   └── scripts/sort_validate.py
│       │
│       └── ...                        # other subjects (physics, CS, chemistry, biology, etc.)
│
├── glossary/
│   ├── general.md                     # curated general Azerbaijani word list (human-readable)
│   ├── math.md                        # curated glossary (Markdown) from terms.json
│   └── ...                            # other subject glossaries
│
├── .github/workflows/
│   └── sort-validate.yml              # 🛠 Automated Term Standardization workflow
│
├── LICENSE
├── README.md
├── CONTRIBUTING.md
└── CODE_OF_CONDUCT.md
```

## ⚙️ Automation

To maintain consistency and quality across the repository, all `terms.json` files are automatically sorted alphabetically and checked for duplicates by the **🛠 Automated Term Standardization workflow** (`sort-validate.yml`). Contributors are expected to update the status for each term **they are contributing** in the JSON file. The workflow automatically flags missing translations with `❌ Missing`, so there is no need to add this manually.

Valid statuses are:  
- `❌ Missing` – automatically flagged by the workflow for missing translations.  
- `⚠️ Revision` – use this if the translation needs review or you are unsure.  
- `✅ Complete` – use this if the translation is verified and fully correct.

The workflow can be triggered manually in the **GitHub Actions** tab.

> [!CAUTION]
> Before submitting a PR, ensure that the **🛠 Automated Term Standardization workflow** completes successfully and that each contributed term’s status is updated appropriately.
