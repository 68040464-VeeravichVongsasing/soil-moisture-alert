import sqlite3
import os

# กำหนดที่เก็บไฟล์ฐานข้อมูล
DB_PATH = "data/app.db"

def get_conn():
    """ฟังก์ชันสำหรับเชื่อมต่อฐานข้อมูล"""
    # สร้างโฟลเดอร์ data ถ้ายังไม่มี
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    """สร้างตารางฐานข้อมูล 3 ตารางหลักหากยังไม่มี"""
    with get_conn() as conn:
        cursor = conn.cursor()
        
        # 1. ตารางข้อมูลความชื้น
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                moisture_level REAL NOT NULL
            )
        """)
        
        # 2. ตารางประวัติการรดน้ำ
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS watering_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                status TEXT NOT NULL,
                mode TEXT NOT NULL
            )
        """)
        
        # 3. ตารางการแจ้งเตือน
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                message TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)
        conn.commit()