import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql@123", # <--- Enter your actual MySQL password here
        database="alumni_nexus"
    )

def check_user_status(reg_no):
    """Checks if the user exists and returns their data."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE reg_no = %s", (reg_no,))
    user = cursor.fetchone()
    conn.close()
    return user

def save_user_data(reg_no, name, branch, password, is_new, linkedin="", intro="", email="", is_mentor=0):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if is_new:
            query = """INSERT INTO users (reg_no, full_name, branch, password, linkedin_id, intro, email, is_mentor) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (reg_no, name, branch, password, linkedin, intro, email, is_mentor))
        else:
            query = """UPDATE users SET full_name=%s, branch=%s, password=%s, 
                       linkedin_id=%s, intro=%s, email=%s, is_mentor=%s WHERE reg_no=%s"""
            cursor.execute(query, (name, branch, password, linkedin, intro, email, is_mentor, reg_no))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Save Error: {e}")
        return False

def get_all_alumni():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT reg_no, full_name, branch, linkedin_id, email, is_mentor FROM users WHERE password IS NOT NULL")
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        return []

def post_job(title, company, description, posted_by, link):
    """Saves a job referral."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO jobs (title, company, description, posted_by, link) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (title, company, description, posted_by, link))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def get_all_jobs():
    """Fetches all job referrals."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
        jobs = cursor.fetchall()
        conn.close()
        return jobs
    except Exception as e:
        return []
def get_total_alumni_count():#show number of alumni in the dashboard, we will only count those who have set their password, as that indicates they have completed their profile setup and are active users of the platform.
    """Sirf un users ko count karega jinhone password set kar liya hai"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE password IS NOT NULL")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"Error: {e}")
        return 0