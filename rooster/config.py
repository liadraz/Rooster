from datetime import time

SEARCH_PARAMS = {
    "sites": [
        "boards.greenhouse.io",
        "jobs.lever.co",
        "comeet.com",
        "workday.com",
        # "app.comeet.co",
        # "myworkdayjobs.com",
    ],
    "titles": ["junior", "entry level", "mid", "intermediate", "backend", "software engineer", "software developer"],
    "keywords": ["backend", "api", "server side"],
    "locations": ["Tel Aviv", "תל אביב", "Haifa", "חיפה", "Herzliya", "הרצליה", "Israel", "ישראל"],
    "exclude": ["senior", "lead", "manager", "director"],
    "after_date": "2025-10-01",
}

QUERY_BUCKETS = [
    {"name":"Backend",
     "keywords":["backend","api","server side"],
     "titles":["junior","entry level","mid","intermediate","backend","software engineer"]},
    {"name":"Full-Stack",
     "keywords":["React","Angular","Vue","frontend","backend"],
     "titles":["junior","entry level","mid","intermediate","full stack","software developer"]},
    {"name":"Python",
     "keywords":["python","flask","fastapi","django","automation","backend"],
     "titles":["junior","entry level","mid","intermediate","python","software engineer"]},
    { "name":".NET",
     "keywords":[".net","c#","asp.net","entity framework","backend","api"],
     "titles":["junior","entry level","mid","intermediate",".net","c#","software developer"]},
]

SCHEDULE_LOCAL_TIMES = {"morning": "09:00", "afternoon": "16:00"}
TIMEZONE = "Asia/Jerusalem"
