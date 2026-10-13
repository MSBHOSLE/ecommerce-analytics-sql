import sqlite3
import unittest


class TestECommerceSQL(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE orders (
                order_id TEXT PRIMARY KEY,
                customer_id TEXT,
                order_date TEXT,
                amount REAL
            )
        """)
        # Populate test data
        cur.executemany("""
            INSERT INTO orders VALUES (?, ?, ?, ?)
        """, [
            ("O1", "C1", "2026-01-01", 100.0),
            ("O2", "C1", "2026-02-01", 150.0),
            ("O3", "C2", "2025-10-01", 50.0),
            ("O4", "C3", "2026-02-15", 300.0),
        ])
        self.conn.commit()

    def test_running_total_window_function(self):
        cur = self.conn.cursor()
        query = """
            SELECT
                order_id,
                amount,
                SUM(amount) OVER (ORDER BY order_date ASC) as running_revenue
            FROM orders
            ORDER BY order_date ASC
        """
        cur.execute(query)
        rows = cur.fetchall()
        self.assertEqual(len(rows), 4)
        # Final running total should equal 50 + 100 + 150 + 300 = 600.0
        self.assertEqual(rows[-1][2], 600.0)


if __name__ == "__main__":
    unittest.main()
