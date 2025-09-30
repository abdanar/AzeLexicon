# Contributor Guide: Adding Translations to `terms.json`

This guide explains how to correctly add translations for English terms into `terms.json` and maintain consistency across the repository. It is highly recommended for all contributors to read this before making changes.

To add a translation, for example, the Azerbaijani translation of **“equation”**, first check whether the word already exists in `math_terms.txt`. If it does, it has already been added automatically to `terms.json`. Next, verify whether a translation exists by looking at the **`status`** field.  

- `❌ Missing` → translation is missing and can be added.  
- `⚠️ Revision` → translation needs review or verification.  
- `✅ Complete` → translation is verified and complete.  

If the translation is missing, add it in the `azerbaijani` field (e.g., `"tənlik"`) and specify its part of speech in `part_of_speech` (e.g., `"noun"`). Including the `status` field is optional, but it is highly appreciated to maintain consistency and quality across the repository.

> [!CAUTION]
> The `id` and `category` fields are already filled and **must not be changed**. If you notice any problem, please open an issue with a detailed description.

If the word is not in `math_terms.txt`, first add the English term to the respective category `.txt` file (not directly in `math_terms.txt`). In this example, `"equation"` should be added to `mathgeneral.txt`. Then, manually trigger the **🛠 Automated Term Standardization** workflow in the **GitHub Actions** tab. The term will appear in `terms.json` with `❌ Missing` status, after which you can add the translation as described above.

The final JSON entry should have the following form:

```json
{
  "english": "equation",
  "azerbaijani": "tənlik",
  "status": "✅ Complete",
  "part_of_speech": "noun",
  "id": "math.LA",
  "category": "Linear Algebra"
}
```

> [!NOTE]
> For the **`id`** field, we primarily use the category IDs from [arxiv.org](https://arxiv.org/category_taxonomy) for mathematics. If needed, additional IDs may be added. For categories not included in arxiv.org, you can check the **`category`** field for the full category name.

