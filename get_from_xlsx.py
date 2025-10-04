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

columns = ["Title", "Author", "My Rating", "Average Rating", "Exclusive Shelf", "Date Read"]
df = df[columns]
df['Date Read'] = pd.to_datetime(df['Date Read'], errors='coerce').dt.date
read_df = df[df['Date Read'].notna()]  # Keep only books with a read date
df = df.fillna("")
read_df=read_df[read_df['Exclusive Shelf'] == 'read']


read_books = []
read_books.append(f"# Bash Books\n")
read_books.append(f"_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n")
read_books.append("\n")

read_books.append("| Title | Author | My Rating | Avg Rating |  Date Read |")
read_books.append("|-------|--------|-----------|------------|------------|")

for _, row in read_df.iterrows():
    read_books.append(
        f"| {row['Title']} | {row['Author']} | {row['My Rating']} | {row['Average Rating']} "
        f"| {row['Date Read']} |"
    )

md_content = "\n".join(read_books)

output_path = os.path.join(REPO_DIR, OUTPUT_FILE)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(md_content)


to_read_df = df[df['Exclusive Shelf'] == 'to-read']
if not to_read_df.empty:
    to_read_books = []
    to_read_books.append(f"\n# To Read\n")
    to_read_books.append("| Title | Author | My Rating | Avg Rating |")
    to_read_books.append("|-------|--------|-----------|------------|")

    for _, row in to_read_df.iterrows():
        to_read_books.append(
            f"| {row['Title']} | {row['Author']} | {row['My Rating']} | {row['Average Rating']} |"
        )

    md_to_read_content = "\n".join(to_read_books)
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(md_to_read_content)

print(f"Markdown file generated at {output_path}")
repo = Repo(REPO_DIR)

relative_path = os.path.relpath(output_path, repo.working_tree_dir)
