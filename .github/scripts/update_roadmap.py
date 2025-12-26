#!/usr/bin/env python3
from datetime import datetime, date
import re

# Define projects with their timelines
PROJECTS = [
    {"name": "H1B Master", "start": date(2025, 12, 1), "end": date(2026, 3, 31)},
    {"name": "GitBridge", "start": date(2025, 12, 1), "end": date(2026, 5, 31)},
    {"name": "CHSS Tool", "start": date(2026, 3, 1), "end": date(2026, 6, 30)},
    {"name": "ETL Bootcamp", "start": date(2025, 12, 1), "end": date(2026, 12, 31)},
]

def generate_roadmap_section(today):
    # Generate 7 months starting from current month
    months = []
    current = today.replace(day=1)
    for i in range(7):
        year = current.year + (current.month + i - 1) // 12
        month = ((current.month + i - 1) % 12) + 1
        months.append(date(year, month, 1))
    
    # Header row
    month_headers = [m.strftime("%b") for m in months]
    header = "| Project | " + " | ".join(month_headers) + " |"
    separator = "|:--------|" + "|".join([":---:" for _ in months]) + "|"
    
    # Project rows
    rows = []
    for proj in PROJECTS:
        if proj["end"] >= today:  # Only show active/future projects
            cells = []
            for m in months:
                month_start = m
                month_end = date(m.year + (m.month // 12), (m.month % 12) + 1, 1)
                
                # Check if project is active in this month
                if proj["start"] <= month_end and proj["end"] >= month_start:
                    if today >= month_start and today < month_end:
                        cells.append("🔵")  # Current month
                    elif proj["start"] <= month_start:
                        cells.append("🟢")  # Active
                    else:
                        cells.append("🟡")  # Planned
                else:
                    cells.append("")
            
            row = f"| **{proj['name']}** | " + " | ".join(cells) + " |"
            rows.append(row)
    
    table = "\n".join([header, separator] + rows)
    
    # Legend
    legend = "🔵 Current | 🟢 Active | 🟡 Planned"
    
    section = f"""## 📅 Project Roadmap

<div align="center">

*Updated: {today.strftime("%b %d, %Y")}*

{table}

{legend}

</div>

---"""
    return section

def update_readme():
    today = date.today()
    
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Pattern to match the roadmap section
    pattern = r"## 📅 .*?Roadmap.*?(?=## 🌟 Current Focus)"
    
    new_section = generate_roadmap_section(today)
    
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, new_section + "\n\n", content, flags=re.DOTALL)
    else:
        new_content = content.replace("## 🌟 Current Focus", new_section + "\n\n## 🌟 Current Focus")
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"Roadmap updated for {today}")

if __name__ == "__main__":
    update_readme()
