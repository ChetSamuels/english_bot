from prompts.scenarios.airport import SYSTEM_PROMPT as AIRPORT
from prompts.scenarios.hotel import SYSTEM_PROMPT as HOTEL
from prompts.scenarios.celeb import SYSTEM_PROMPT as CELEB
from prompts.scenarios.choosing_prof import SYSTEM_PROMPT as PROFESSION
from prompts.scenarios.clothes_shop import SYSTEM_PROMPT as CLOTHES
from prompts.scenarios.doctor import SYSTEM_PROMPT as DOCTOR
from prompts.scenarios.ecology import SYSTEM_PROMPT as ECOLOGY
from prompts.scenarios.exam import SYSTEM_PROMPT as EXAM
from prompts.scenarios.family_rules import SYSTEM_PROMPT as FAMILY
from prompts.scenarios.it_safety import SYSTEM_PROMPT as SAFETY
from prompts.scenarios.job_interview import SYSTEM_PROMPT as INTERVIEW
from prompts.scenarios.social_media import SYSTEM_PROMPT as MEDIA
from prompts.scenarios.sports import SYSTEM_PROMPT as SPORTS
from prompts.scenarios.teacher_conversation import SYSTEM_PROMPT as TEACHER
from prompts.scenarios.university import SYSTEM_PROMPT as UNIVERSITY


SCENARIOS = {
    "airport": AIRPORT,
    "hotel": HOTEL,
    "famous_person": CELEB, 
    "choosing_profession": PROFESSION,
    "buying_clothes": CLOTHES,
    "doctor_appointment": DOCTOR,
    "ecology_discussion": ECOLOGY,
    "final_exam": EXAM,
    "family_rules": FAMILY,
    "internet_safety": SAFETY,
    "job_interview": INTERVIEW,
    "social_media_discussion": MEDIA,
    "sports_discussion": SPORTS,
    "teacher_conversation": TEACHER,
    "university_open_day": UNIVERSITY,
}