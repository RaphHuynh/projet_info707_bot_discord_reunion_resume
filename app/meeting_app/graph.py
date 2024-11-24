from datetime import datetime, timedelta
import numpy as np

def generate_heatmap(meeting_dates):
    today = datetime.today()
    start_date = datetime(today.year, 1, 1)
    end_date = datetime(today.year, 12, 31)

    num_days = (end_date - start_date).days + 1
    all_dates = [start_date + timedelta(days=i) for i in range(num_days)]

    weeks = np.zeros((53, 7), dtype=int)

    date_counts = {date.date(): 0 for date in all_dates} 
    for date in meeting_dates:
        date_only = date.date() 
        if date_only in date_counts:
            date_counts[date_only] += 1

    for i, date in enumerate(all_dates):
        week_idx = i // 7
        day_idx = i % 7
        weeks[week_idx][day_idx] = date_counts[date.date()]

    return weeks, start_date
