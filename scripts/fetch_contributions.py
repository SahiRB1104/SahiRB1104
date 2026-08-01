import os
import json
import re
import requests
from bs4 import BeautifulSoup

def fetch_contributions(username="SahiRB1104", output_path="data/contributions.json"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html"
    }
    
    print(f"Fetching contributions from {url}...")
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise RuntimeError(f"Failed to fetch contributions HTML: HTTP {res.status_code}")
        
    soup = BeautifulSoup(res.text, "html.parser")
    
    days = []
    # Find all td elements with class ContributionCalendar-day
    day_tds = soup.find_all("td", class_="ContributionCalendar-day")
    
    # Also look for tooltips or aria labels if available
    tooltips = {t.get("for"): t.text.strip() for t in soup.find_all("tool-tip") if t.get("for")}
    
    total_contributions = 0
    
    for td in day_tds:
        date = td.get("data-date")
        if not date:
            continue
        
        level = int(td.get("data-level", 0))
        td_id = td.get("id")
        
        count = 0
        tooltip_text = tooltips.get(td_id, "")
        
        if tooltip_text:
            # Match e.g. "15 contributions on August 1, 2025" or "No contributions on..."
            match = re.search(r"(\d+)\s+contribution", tooltip_text)
            if match:
                count = int(match.group(1))
        else:
            # Fallback level estimation if exact count isn't in tooltip
            count = level * 2 if level > 0 else 0
            
        days.append({
            "date": date,
            "level": level,
            "count": count
        })
        total_contributions += count

    # Try to extract total contributions count from header if present
    header = soup.find("h2", class_=re.compile(r"content-signin|f4"))
    if header:
        h_match = re.search(r"([\d,]+)\s+contributions", header.text)
        if h_match:
            total_contributions = int(h_match.group(1).replace(",", ""))

    # Calculate streaks
    current_streak = 0
    max_streak = 0
    temp_streak = 0
    
    # Sort days chronologically
    days.sort(key=lambda d: d["date"])
    
    for d in days:
        if d["count"] > 0 or d["level"] > 0:
            temp_streak += 1
            if temp_streak > max_streak:
                max_streak = temp_streak
        else:
            temp_streak = 0
            
    # Calculate current streak working backwards from latest day
    for d in reversed(days):
        if d["count"] > 0 or d["level"] > 0:
            current_streak += 1
        else:
            # Break if zero on a past day
            if current_streak > 0:
                break

    data = {
        "username": username,
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "max_streak": max_streak,
        "days_recorded": len(days),
        "days": days
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    print(f"Successfully saved {len(days)} days of contribution data to {output_path}")
    print(f"Total Contributions: {total_contributions} | Max Streak: {max_streak} days | Current Streak: {current_streak} days")

if __name__ == "__main__":
    fetch_contributions("SahiRB1104", "data/contributions.json")
