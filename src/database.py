# src/database.py - Database operations
import sqlite3
from datetime import datetime

class CampaignDatabase:
    """Manages campaign data storage and retrieval"""
    
    def __init__(self, db_path='data/campaigns.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create campaigns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaigns (
                campaign_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                channel TEXT NOT NULL,
                start_date DATE,
                end_date DATE,
                budget REAL,
                status TEXT
            )
        ''')
        
        # Create metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id TEXT,
                date DATE,
                impressions INTEGER,
                clicks INTEGER,
                conversions INTEGER,
                spend REAL,
                revenue REAL,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")
    
    def insert_campaign(self, campaign_data):
        """Insert new campaign into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO campaigns 
            (campaign_id, name, channel, start_date, end_date, budget, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            campaign_data['campaign_id'],
            campaign_data['name'],
            campaign_data['channel'],
            campaign_data['start_date'],
            campaign_data['end_date'],
            campaign_data['budget'],
            campaign_data['status']
        ))
        
        conn.commit()
        conn.close()
    
    def insert_metrics(self, metrics_data):
        """Insert performance metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO metrics 
            (campaign_id, date, impressions, clicks, conversions, spend, revenue)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            metrics_data['campaign_id'],
            metrics_data['date'],
            metrics_data['impressions'],
            metrics_data['clicks'],
            metrics_data['conversions'],
            metrics_data['spend'],
            metrics_data['revenue']
        ))
        
        conn.commit()
        conn.close()
    
    def get_all_campaigns(self):
        """Retrieve all campaigns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM campaigns')
        campaigns = cursor.fetchall()
        
        conn.close()
        return campaigns
    
    def get_campaign_metrics(self, campaign_id):
        """Get metrics for specific campaign"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM metrics 
            WHERE campaign_id = ? 
            ORDER BY date DESC
        ''', (campaign_id,))
        
        metrics = cursor.fetchall()
        conn.close()
        return metrics