from datetime import datetime, timedelta
import dateutil.parser
def round_to_nearest_30_minutes(dt):
    new_minute = round(dt.minute // 30) * 30
    new  = dt.replace(minute=new_minute, second=0, microsecond=0)
    return new

def standardize_date(date_str, time_str= ""):
    date_str = date_str.lower()
    total_string = f"{date_str} {time_str}"
    if "live" in date_str:
        return "Live"
    elif "today" in date_str:
        if time_str == "":
            today_datetime = datetime.now().strftime('%Y-%m-%d')
            today_datetime = total_string.replace("today", today_datetime)
            today_datetime  = dateutil.parser.parse(today_datetime)
            today_datetime = round_to_nearest_30_minutes(today_datetime)    
            return today_datetime.strftime("%Y-%m-%d %H:%M:%S")
        else:
            today_datetime = datetime.combine(datetime.today().date(), dateutil.parser.parse(time_str).time())
            rounded = round_to_nearest_30_minutes(today_datetime)
            rounded = rounded.strftime("%Y-%m-%d %H:%M:%S")
            return rounded
    elif "tomorrow" in date_str:
        if time_str == "":
            tomorrow_datetime = datetime.today().date() + timedelta(days=1)
            tomorrow_datetime = tomorrow_datetime.strftime('%Y-%m-%d')
            tomorrow_datetime = total_string.replace("tomorrow", tomorrow_datetime)
            tomorrow_datetime  = dateutil.parser.parse(tomorrow_datetime)
            tomorrow_datetime = round_to_nearest_30_minutes(tomorrow_datetime)    
            return tomorrow_datetime.strftime("%Y-%m-%d %H:%M:%S")
        else:
            tomorrow_datetime = datetime.combine((datetime.today().date() + timedelta(days=1)), dateutil.parser.parse(time_str).time())
            rounded = round_to_nearest_30_minutes(tomorrow_datetime)
            rounded = rounded.strftime("%Y-%m-%d %H:%M:%S")
            return rounded
    try :
        date = dateutil.parser.parse(total_string)
        rounded = round_to_nearest_30_minutes(date)
        rounded = rounded.strftime("%Y-%m-%d %H:%M:%S")
        return rounded
    except:
        pass


    formats_to_try = [
            "%Y-%m-%d %H:%M:%S",
            "%m/%d/%Y %H:%M:%S",
            "%d-%m-%Y %H:%M:%S",
            "%a, %b %d, %Y %H:%M:%S"#,  # Format for "Sun, Jan 28, 2024"
        
    ]
    for date_format in formats_to_try:
        try:
            # Try parsing the date with the current format
            parsed_date = datetime.strptime(total_string, date_format)
            rounded = round_to_nearest_30_minutes(parsed_date)

            # If successful, return the date in the desired format
            return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
        except :
            # If parsing fails, try the next format
            pass

    # If none of the formats work, return None or raise an error
    return date_str