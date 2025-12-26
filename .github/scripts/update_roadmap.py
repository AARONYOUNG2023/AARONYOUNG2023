#!/usr/bin/env python3
from datetime import datetime, date
import re

# Define projects with their timelines
PROJECTS = [
    {"name": "H1B Master", "start": date(2025, 12, 1), "end": date(2026, 3, 31), "status": "Active"},
    {"name": "GitBridge", "start": date(2025, 12, 1), "end": date(2026, 5, 31), "status": "Active"},
    {"name": "Chinese High School Selection Tool", "start": date(2026, 3, 1), "end": date(2026, 6, 30), "status": "Planned"},
    {"name": "Python ETL Bootcamp", "start": date(2025, 12, 1), "end": date(2026, 12, 31), "status": "Teaching"},
]

def get_status_emoji(status, start_date, end_date, today):
    if today > end_date:
        return "✅ Completed"
    elif today < start_date:
        return "🟡 Planned"
    elif status == "Teaching":
        return "📚 Teaching"
    else:
        return "🟢 Active"

def generate_gantt_chart(today):
    # Determine the range of months to show (current month to 6 months ahead)
    current_month = today.replace(day=1)
    
    # Generate month headers
    months = []
    month_names = []
    for i in range(7):
        m = date(current_month.year + (current_month.month + i - 1) // 12, 
                 ((current_month.month + i - 1) % 12) + 1, 1)
        months.append(m)
        month_names.append(m.strftime("%b"))
    
    year_header = f"            {months[0].year}"
    if months[-1].year != months[0].year:
        year_header += f"                              {months[-1].year}"
    
    month_header = "         " + "    ".join(f"{m:^3}" for m in month_names)
    divider = "          " + "|------" * 7 + "|"
    
    lines = [year_header, month_header, divider]
    
    # Generate bars for each active/upcoming project
    for proj in PROJECTS:
        if proj["end"] >= today:  # Only show if not completed
            bar = ""
            name = proj["name"][:10].ljust(10)
            
            for m in months:
                month_end = date(m.year, m.month + 1, 1) if m.month < 12 else date(m.year + 1, 1, 1)
                month_end = date(month_end.year, month_end.month, 1)
                
                if proj["start"] <= m and proj["end"] >= m:
                    bar += "███████"
                elif proj["start"] < month_end and proj["end"] >= m:
                    bar += "███████"
                else:
                    bar += "       "
            
            lines.append(f"{name} {bar}")
    
    lines.append(divider)
    
    return "\n".join(lines)

def generate_table(today):
    rows = []
    rows.append("| Project | Timeline | Status |")
    rows.append("|:--------|:---------|:------:|")
    
    for proj in PROJECTS:
        if proj["end"] >= today:  # Only show if not completed
            start_str = proj["start"].strftime("%b %Y")
            end_str = proj["end"].strftime("%b %Y")
            status = get_status_emoji(proj["status"], proj["start"], proj["end"], today)
            rows.append(f"| **{proj['name']}** | {start_str} - {end_str} | {status} |")
    
    return "\n".join(rows)

def generate_roadmap_section(today):
    gantt = generate_gantt_chart(today)
    table = generate_table(today)
    
    section = f"""## 📅 Project Roadmap

<div align="center">

*Last updated: {today.strftime("%B %d, %Y")}*

```
{gantt}
```

{table}

</div>

---"""
    return section

def update_readme():
    today = date.today()
    
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Pattern to match the roadmap section
    pattern = r"## 📅.*?(?=## 🌟 Current Focus)"
    
    new_section = generate_roadmap_section(today)
    
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, new_section + "\n\n", content, flags=re.DOTALL)
    else:
        # Insert before Current Focus if pattern not found
        new_content = content.replace("## 🌟 Current Focus", new_section + "\n\n## 🌟 Current Focus")
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"Roadmap updated for {today}")

if __name__ == "__main__":
    update_readme()
