from pypdf import PdfReader
import re
from datetime import datetime

def extract_eaf_text(pdf_path):
    reader = PdfReader(pdf_path)

    extracted_text = []

    for page in reader.pages:
        text = page.extract_text() or ""
        extracted_text.append(text)

    return "\n".join(extracted_text)

DAY_MAP = {
    "SUN": 0,
    "MON": 1,
    "TUE": 2,
    "WED": 3,
    "THU": 4,
    "FRI": 5,
    "SAT": 6
}

DAY_PATTERN = r"SUN|MON|TUE|WED|THU|FRI|SAT"

def parse_time(time_string):
    return datetime.strptime(
        time_string.strip().upper(),
        "%I:%M %p"
    ).strftime("%H:%M:%S")


def parse_eaf_text(extracted_text):
    if "CLASS SCHEDULE:" not in extracted_text:
        raise ValueError("Class schedule section was not found.")

    
    schedule_section = extracted_text.split(
        "CLASS SCHEDULE:", 1
    )[1]

    schedule_section = schedule_section.split(
        "TOTAL UNITS", 1
    )[0]

    rows = re.split(
        r"(?m)(?=^[A-Z0-9]{5,10}\s+[A-Z0-9]{5,10}-)",
        schedule_section.strip()
    )

    courses = []
    course_pattern = re.compile(
        r"^([A-Z0-9]{5,10})\s+"
        r"\1-(.*?)\s+"
        r"([A-Z]{2}\s+\d{3}-[A-Z]{2})\s+"
        r"(.*)$",
        re.IGNORECASE
    )

    meeting_pattern = re.compile(
        rf"\b({DAY_PATTERN})\s*\|\s*"
        r"(\d{1,2}:\d{2}\s*[AP]M)\s*-\s*"
        r"(\d{1,2}:\d{2}\s*[AP]M)\s*\|\s*"
        rf"(.+?)(?=,\s*(?:{DAY_PATTERN})\s*\|"
        r"|\s+\d+\.\d{2}\s*$)",
        re.IGNORECASE
    )

    for row in rows:
        row = re.sub(r"\s+", " ", row).strip()

        if not row:
            continue

        match = course_pattern.match(row)

        if not match:
            continue

        course_code = match.group(1).upper()
        course_name = match.group(2).strip()
        section = match.group(3).strip()

        meeting_text = match.group(4)

        units_match = re.search(
            r"(\d+(?:\.\d{1,2})?)\s*$",
            meeting_text
        )

        units = float(units_match.group(1)) if units_match else None

        meetings = []

        for meeting_match in meeting_pattern.finditer(meeting_text):
            day = meeting_match.group(1).upper()
            start_time = meeting_match.group(2)
            end_time = meeting_match.group(3)
            room = meeting_match.group(4).strip()

            meetings.append({
                "day_of_week": DAY_MAP[day],
                "day": day,
                "start_time": parse_time(start_time),
                "end_time": parse_time(end_time),
                "room": room
            })

        if not meetings:
            raise ValueError(
                f"No valid class meetings found for {course_code}."
            )

        courses.append({
            "course_code": course_code,
            "course_name": course_name,
            "section": section,
            "units": units,
            "meetings": meetings
        })

    if not courses:
        raise ValueError(
            "No subjects could be extracted from this EAF."
        )

    academic_info = re.search(
        r"\b(20\d{2}-20\d{2})\s+"
        r"(First|Second|Summer)\s+Term\b",
        extracted_text,
        re.IGNORECASE
    )

    academic_year = academic_info.group(1) if academic_info else None
    term = academic_info.group(2).title() if academic_info else None

    year_match = re.search(
        r"YEAR LEVEL\s*:\s*(.+?)(?:CLASS SCHEDULE|$)",
        extracted_text,
        re.IGNORECASE | re.DOTALL
    )

    year_level = (
        re.sub(r"\s+", " ", year_match.group(1)).strip()
        if year_match else None
    )

    room_groups = {}

    for course in courses:
        for meeting in course["meetings"]:
            key = (
                course["course_code"],
                meeting["day_of_week"],
                meeting["start_time"],
                meeting["end_time"]
            )

            room_groups.setdefault(key, [])

            if meeting["room"] not in room_groups[key]:
                room_groups[key].append(meeting["room"])

    room_conflicts = []

    for key, rooms in room_groups.items():
        if len(rooms) > 1:
            course_code, day, start, end = key

            room_conflicts.append({
                "course_code": course_code,
                "day_of_week": day,
                "start_time": start,
                "end_time": end,
                "rooms": rooms
            })

    time_conflicts = []

    all_meetings = []

    for course in courses:
        for meeting in course["meetings"]:
            all_meetings.append({
                "course_code": course["course_code"],
                "course_name": course["course_name"],
                **meeting
            })

    for index, first in enumerate(all_meetings):
        for second in all_meetings[index + 1:]:
            if first["course_code"] == second["course_code"]:
                continue
            if first["day_of_week"] != second["day_of_week"]:
                continue
            if (
                first["start_time"] < second["end_time"]
                and second["start_time"] < first["end_time"]
            ):
                time_conflicts.append({
                    "first_course": first["course_code"],
                    "second_course": second["course_code"],
                    "day_of_week": first["day_of_week"],
                    "first_start": first["start_time"],
                    "first_end": first["end_time"],
                    "second_start": second["start_time"],
                    "second_end": second["end_time"]
                })
    return {
        "academic_year": academic_year,
        "term": term,
        "year_level": year_level,
        "courses": courses,
        "room_conflicts": room_conflicts,
        "time_conflicts": time_conflicts
    }
