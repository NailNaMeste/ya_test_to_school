import datetime


def parse_string(string_time: str):
    print("time", string_time)
    start_time, end_time = string_time.split("-")
    start_time = datetime.datetime.now().replace(
        hour=int(start_time.split(":")[0]), minute=int(start_time.split(":")[1])
    )
    end_time = datetime.datetime.now().replace(
        hour=int(end_time.split(":")[0]), minute=int(end_time.split(":")[1])
    )
    return start_time, end_time


def str_hours_to_datetime(hours: list[str] | str):
    result = []
    start_hours = []
    end_hours = []
    if isinstance(hours, list):
        for pairs in hours:
            start_time, end_time = parse_string(pairs)
            start_hours.append(start_time)
            end_hours.append(end_time)
    elif isinstance(hours, str):
        start_time, end_time = parse_string(hours)
        start_hours.append(start_time)
        end_hours.append(end_time)

    return start_hours, end_hours


def str_to_datetime(hour: str) -> tuple[datetime.datetime, datetime.datetime]:
    return parse_string(hour)
