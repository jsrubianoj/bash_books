import pandas as pd
from git import Repo
import os
from datetime import datetime

# -----------------------------
# CONFIGURATION
# -----------------------------
XLSX_FILE = "goodreads_library_export.xlsx"   # path to your Goodreads export
REPO_DIR = r"C:\Python\bash_books"             # local clone of your GitHub repo
OUTPUT_FILE = "books.md"                    # output file name in repo
COMMIT_MSG = "Update books list from Goodreads export"
print("Repo dir:", REPO_DIR)
print("Is dir?", os.path.isdir(REPO_DIR))
df = pd.read_excel(XLSX_FILE)

columns = ["Title", "Author", "My Rating", "Average Rating", "Publisher", "Year Published", "Bookshelves", "Date Read"]
df = df[columns]
df['Date Read'] = pd.to_datetime(df['Date Read'], errors='coerce').dt.date
df = df[df['Date Read'].notna()]  # Keep only books with a read date
df = df.fillna("")

md_lines = []
md_lines.append(f"# My Books\n")
md_lines.append(f"_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n")
md_lines.append("\n")

md_lines.append("| Title | Author | My Rating | Avg Rating |  Date Read |")
md_lines.append("|-------|--------|-----------|------------|------------|")

for _, row in df.iterrows():
    md_lines.append(
        f"| {row['Title']} | {row['Author']} | {row['My Rating']} | {row['Average Rating']} "
        f"| {row['Date Read']} |"
    )

md_content = "\n".join(md_lines)

output_path = os.path.join(REPO_DIR, OUTPUT_FILE)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"Markdown file generated at {output_path}")
repo = Repo(REPO_DIR)

relative_path = os.path.relpath(output_path, repo.working_tree_dir)
