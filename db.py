import datetime
import os
from uuid import uuid4
from dotenv import load_dotenv
import libsql_client
load_dotenv()

db = libsql_client.create_client_sync(
    url=os.getenv("DB_URL"),
    auth_token=os.getenv("DB_TOKEN")
)


def close():
    db.close()


def create_goal(id: int, goal: str) -> bool:
    dt = datetime.datetime.now()
    res = db.execute("""
        insert into goals
        (id, user_id, goal, longest_streak_start, current_streak_start, created_at, prompt_at)
        values
        (?, ?, ?, ?, ?, ?, ?)
    """, [
        str(uuid4()),
        str(id),
        goal,
        dt,
        dt,
        dt,
        dt,
    ])

    return res.rows_affected == 1

def list_goals(id: int):
    res = db.execute("""
        select goal, longest_streak_start, longest_streak_end,
        current_streak_start, created_at, prompt_at
        from goals where user_id = ?
        order by created_at
    """, [str(id)])

    return res.rows, res.columns


def do_goal(id: int, goal_num: int) -> bool:
    # get goal_id from userid and goal_num
    goals = db.execute("select id from goals where user_id = ? order by created_at", [str(id)])
    if goal_num < 1 or goal_num > len(goals.rows):
        return False

    res = db.execute("""
        insert into completions (id, completed_at, goal_id) values (?, ?, ?)
    """,[str(uuid4()), datetime.datetime.now(), goals.rows[goal_num - 1][0]]
    )

    return res.rows_affected == 1
