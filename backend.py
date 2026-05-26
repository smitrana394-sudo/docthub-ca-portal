
LEADERBOARD = [
    {"rank":1,"name":"Aarav Shah","college":"AIIMS Delhi","points":5800},
    {"rank":2,"name":"Riya Mehta","college":"CMC Vellore","points":5200},
    {"rank":3,"name":"Smit Rana","college":"AIIMS Kalyani","points":2450},
]

TASKS = [
    {"task":"Instagram Promotion","desc":"Promote DOCTHUB on Instagram","pts":100,"status":"Completed","deadline":"Done"},
    {"task":"College Webinar","desc":"Organize webinar in campus","pts":200,"status":"Pending","deadline":"Jun 10"},
]

REWARDS = [
    {"name":"Amazon Voucher","pts":1000,"icon":"🎁","desc":"₹500 Amazon voucher"},
]

ACTIVITIES = [
    {"text":"Completed Instagram Campaign","time":"2h ago","color":"#1565C0"},
]

POINTS_HISTORY = {
    "months":["Jan","Feb","Mar","Apr","May"],
    "points":[100,500,1200,1800,2450]
}

PERFORMANCE_STATS = {
    "categories":["Referrals","Events","Social","Tasks","Leadership"],
    "values":[80,70,90,75,60]
}

BADGES = [
    {"label":"Top Performer","bg":"#DBEAFE","color":"#1D4ED8","border":"#93C5FD"}
]

TIMELINE = [
    ("May 2026","Joined DOCTHUB CA Program","#1565C0"),
]

def get_task_summary(tasks):
    completed = sum(1 for t in tasks if t["status"]=="Completed")
    pending = sum(1 for t in tasks if t["status"]=="Pending")
    new = sum(1 for t in tasks if t["status"]=="New")
    return {"completed":completed,"pending":pending,"new":new}

def get_pending_tasks(tasks):
    return [t for t in tasks if t["status"]!="Completed"]

def can_redeem(points, required):
    return points >= required

def progress_pct(points, required):
    return min(int((points/required)*100),100)
