# src/data_collector.py - Simulates API data collection
import json
from datetime import datetime, timedelta
import random

class DataCollector:
    """Collects campaign data from marketing platforms"""
    
    def __init__(self):
        self.today = datetime.now().date()
    
    def fetch_facebook_campaigns(self):
        """Simulate Facebook Ads API call"""
        print("📱 Fetching Facebook campaign data...")
        
        campaigns = [
            {
                'campaign_id': 'FB_001',
                'name': 'Summer Sale 2024',
                'channel': 'Facebook',
                'start_date': '2024-06-01',
                'end_date': '2024-12-31',
                'budget': 10000.00,
                'status': 'active',
                'metrics': {
                    'impressions': 125000,
                    'clicks': 3200,
                    'conversions': 180,
                    'spend': 8500.00,
                    'revenue': 27200.00
                }
            },
            {
                'campaign_id': 'FB_002',
                'name': 'Brand Awareness',
                'channel': 'Facebook',
                'start_date': '2024-05-15',
                'end_date': '2024-12-31',
                'budget': 5000.00,
                'status': 'active',
                'metrics': {
                    'impressions': 89000,
                    'clicks': 1800,
                    'conversions': 95,
                    'spend': 4200.00,
                    'revenue': 12350.00
                }
            }
        ]
        
        print(f"✅ Collected {len(campaigns)} Facebook campaigns")
        return campaigns
    
    def fetch_google_campaigns(self):
        """Simulate Google Ads API call"""
        print("🔍 Fetching Google Ads campaign data...")
        
        campaigns = [
            {
                'campaign_id': 'GOOGLE_001',
                'name': 'Product Launch',
                'channel': 'Google Ads',
                'start_date': '2024-07-01',
                'end_date': '2024-12-31',
                'budget': 15000.00,
                'status': 'active',
                'metrics': {
                    'impressions': 210000,
                    'clicks': 5600,
                    'conversions': 340,
                    'spend': 12300.00,
                    'revenue': 30135.00
                }
            }
        ]
        
        print(f"✅ Collected {len(campaigns)} Google campaigns")
        return campaigns
    
    def fetch_email_campaigns(self):
        """Simulate Email Marketing API call"""
        print("📧 Fetching Email campaign data...")
        
        campaigns = [
            {
                'campaign_id': 'EMAIL_001',
                'name': 'Newsletter Campaign',
                'channel': 'Email',
                'start_date': '2024-01-01',
                'end_date': '2024-12-31',
                'budget': 2000.00,
                'status': 'active',
                'metrics': {
                    'impressions': 45000,
                    'clicks': 2800,
                    'conversions': 220,
                    'spend': 1800.00,
                    'revenue': 8900.00
                }
            }
        ]
        
        print(f"✅ Collected {len(campaigns)} Email campaigns")
        return campaigns
    
    def collect_all_campaigns(self):
        """Collect from all channels"""
        all_campaigns = []
        all_campaigns.extend(self.fetch_facebook_campaigns())
        all_campaigns.extend(self.fetch_google_campaigns())
        all_campaigns.extend(self.fetch_email_campaigns())
        
        print(f"\n📊 Total campaigns collected: {len(all_campaigns)}")
        return all_campaigns