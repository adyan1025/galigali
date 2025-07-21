import matplotlib.pyplot as plt
import calendar
import numpy as np
import os
import cal_api

events_list = cal_api.calendar_api

events = {
    (2023, 10, 31): ["Halloween Party", "Dinner with Friends"],
    (2023, 10, 25): ["Project Deadline"],
    # Add more events here
}

def calendar_draw(year, month):
    cal = calendar.monthcalendar(year, month)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, 7)
    ax.set_ylim(0, max(len(cal), 5))
    ax.axis('off')
    
    for i, day in enumerate(days):
        ax.text(i + 0.5, len(cal) + 0.5, day, ha='center')
    
    for week_index, week in enumerate(cal):
        for day_index, day in enumerate(week):
            if day != 0:
                ax.text(day_index + 0.5, len(cal) - week_index - 0.5, str(day), ha='center')
            if (year, month, day) in events:
                    # Get the events for the specific day
                    event_texts = events[(year, month, day)]
                    # List events under the day number
                    for event_index, event in enumerate(event_texts):
                        ax.text(day_index + 0.5, len(cal) - week_index - 0.5 - 0.3 * (event_index + 1), event, ha='center', va='top', fontsize=10, color='red')


    output_dir = './images/'
    output_filename = 'cal_img.png'
    output_file = os.path.join(output_dir, output_filename)
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close(fig)
    

calendar_draw(2023, 10)