import sqlite3
import datetime
import threading


class MemoryStore:

    def __init__(self, db_path="memory.db"):
        self.db_path = db_path
        self.lock = threading.Lock()
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._initialize_database()

    # =====================================
    # DATABASE INIT (UPGRADED)
    # =====================================

    def _initialize_database(self):

        cursor = self.conn.cursor()

        # Schema version
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        # Contacts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                name TEXT PRIMARY KEY,
                number TEXT NOT NULL,
                created_at TEXT
            )
        """)

        # Scheduled messages
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scheduled_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                number TEXT,
                message TEXT,
                scheduled_time TEXT,
                created_at TEXT
            )
        """)

        # Command usage tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS command_usage (
                command TEXT PRIMARY KEY,
                count INTEGER DEFAULT 0,
                last_used TEXT
            )
        """)

        # Conversation memory (NEW)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_text TEXT,
                assistant_text TEXT,
                timestamp TEXT
            )
        """)

        # Index for faster schedule lookup
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_scheduled_time
            ON scheduled_messages (scheduled_time)
        """)

        self.conn.commit()

    # =====================================
    # CONTACTS (SELF-LEARNING READY)
    # =====================================

    def add_contact(self, name, number):

        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO contacts (name, number, created_at)
                VALUES (?, ?, ?)
            """, (
                name.lower(),
                number,
                datetime.datetime.now().isoformat()
            ))
            self.conn.commit()

    def get_contact(self, name):

        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT number FROM contacts WHERE name = ?
            """, (name.lower(),))
            result = cursor.fetchone()
            return result[0] if result else None

    def get_all_contacts(self):

        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name, number FROM contacts")
            results = cursor.fetchall()
            return {name: number for name, number in results}

    # =====================================
    # SCHEDULED MESSAGES (PERSISTENT)
    # =====================================

    def add_scheduled_message(self, name, number, message, scheduled_time):

        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO scheduled_messages 
                (name, number, message, scheduled_time, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                name,
                number,
                message,
                scheduled_time.isoformat(),
                datetime.datetime.now().isoformat()
            ))
            self.conn.commit()

    def get_due_messages(self):

        with self.lock:
            cursor = self.conn.cursor()
            now = datetime.datetime.now().isoformat()
            cursor.execute("""
                SELECT id, name, number, message 
                FROM scheduled_messages
                WHERE scheduled_time <= ?
            """, (now,))
            return cursor.fetchall()

    def remove_scheduled_message(self, message_id):

        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM scheduled_messages WHERE id = ?
            """, (message_id,))
            self.conn.commit()

    # =====================================
    # COMMAND USAGE TRACKING (SMART LEARNING)
    # =====================================

    def track_command(self, command):

        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO command_usage (command, count, last_used)
                VALUES (?, 1, ?)
                ON CONFLICT(command)
                DO UPDATE SET 
                    count = count + 1,
                    last_used = excluded.last_used
            """, (
                command.lower(),
                datetime.datetime.now().isoformat()
            ))
            self.conn.commit()

    def get_top_commands(self, limit=5):

        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT command, count
                FROM command_usage
                ORDER BY count DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()

    # =====================================
    # CONVERSATION MEMORY (NEW)
    # =====================================

    def store_conversation(self, user_text, assistant_text):

        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO conversations (user_text, assistant_text, timestamp)
                VALUES (?, ?, ?)
            """, (
                user_text,
                assistant_text,
                datetime.datetime.now().isoformat()
            ))
            self.conn.commit()

    def get_recent_conversations(self, limit=10):

        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT user_text, assistant_text
                FROM conversations
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()

    # =====================================
    # CLEANUP (AUTO MAINTENANCE)
    # =====================================

    def cleanup_old_conversations(self, days=30):

        cutoff = (
            datetime.datetime.now() - datetime.timedelta(days=days)
        ).isoformat()

        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM conversations
                WHERE timestamp <= ?
            """, (cutoff,))
            self.conn.commit()

    # =====================================
    # CLOSE CONNECTION (SAFE SHUTDOWN)
    # =====================================

    def close(self):
        with self.lock:
            self.conn.close()