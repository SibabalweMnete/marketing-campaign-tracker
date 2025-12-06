# Unit tests for the Marketing Campaign Tracker
import unittest
import os
import json
from datetime import datetime
from src.database import CampaignDatabase
from src.analyzer import CampaignAnalyzer
from src.report_generator import ReportGenerator

class TestCampaignDatabase(unittest.TestCase):
    """Test database operations"""
    
    def setUp(self):
        """Create a test database"""
        self.db = CampaignDatabase('test_campaigns.db')
    
    def tearDown(self):
        """Clean up test database"""
        if os.path.exists('test_campaigns.db'):
            os.remove('test_campaigns.db')
    
    def test_database_initialization(self):
        """Test that database initializes correctly"""
        self.assertTrue(os.path.exists('test_campaigns.db'))
    
    def test_insert_campaign(self):
        """Test inserting a campaign"""
        campaign = {
            'campaign_id': 'TEST_001',
            'name': 'Test Campaign',
            'channel': 'Test',
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'budget': 1000.0,
            'status': 'active'
        }
        self.db.insert_campaign(campaign)
        
        campaigns = self.db.get_all_campaigns()
        self.assertEqual(len(campaigns), 1)
        self.assertEqual(campaigns[0][1], 'Test Campaign')
    
    def test_insert_metrics(self):
        """Test inserting metrics"""
        campaign = {
            'campaign_id': 'TEST_002',
            'name': 'Test Campaign 2',
            'channel': 'Test',
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'budget': 1000.0,
            'status': 'active'
        }
        self.db.insert_campaign(campaign)
        
        metrics = {
            'campaign_id': 'TEST_002',
            'date': datetime.now().date(),
            'impressions': 1000,
            'clicks': 100,
            'conversions': 10,
            'spend': 500.0,
            'revenue': 1000.0
        }
        self.db.insert_metrics(metrics)
        
        retrieved_metrics = self.db.get_campaign_metrics('TEST_002')
        self.assertEqual(len(retrieved_metrics), 1)
        self.assertEqual(retrieved_metrics[0][3], 1000)  # impressions


class TestCampaignAnalyzer(unittest.TestCase):
    """Test analytics calculations"""
    
    def setUp(self):
        """Set up test data"""
        self.db = CampaignDatabase('test_analyzer.db')
        self.analyzer = CampaignAnalyzer(self.db)
        
        # Insert test campaign
        campaign = {
            'campaign_id': 'TEST_003',
            'name': 'Analysis Test',
            'channel': 'Test',
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'budget': 1000.0,
            'status': 'active'
        }
        self.db.insert_campaign(campaign)
        
        # Insert test metrics
        metrics = {
            'campaign_id': 'TEST_003',
            'date': datetime.now().date(),
            'impressions': 10000,
            'clicks': 500,
            'conversions': 50,
            'spend': 1000.0,
            'revenue': 3000.0
        }
        self.db.insert_metrics(metrics)
    
    def tearDown(self):
        """Clean up"""
        if os.path.exists('test_analyzer.db'):
            os.remove('test_analyzer.db')
    
    def test_calculate_roi(self):
        """Test ROI calculation"""
        roi = self.analyzer.calculate_roi('TEST_003')
        # ROI = (3000 - 1000) / 1000 * 100 = 200%
        self.assertEqual(roi, 200.0)
    
    def test_calculate_ctr(self):
        """Test CTR calculation"""
        ctr = self.analyzer.calculate_ctr('TEST_003')
        # CTR = 500 / 10000 * 100 = 5%
        self.assertEqual(ctr, 5.0)
    
    def test_calculate_conversion_rate(self):
        """Test conversion rate calculation"""
        conv_rate = self.analyzer.calculate_conversion_rate('TEST_003')
        # Conversion Rate = 50 / 500 * 100 = 10%
        self.assertEqual(conv_rate, 10.0)
    
    def test_get_campaign_summary(self):
        """Test getting full campaign summary"""
        summary = self.analyzer.get_campaign_summary('TEST_003')
        
        self.assertIsNotNone(summary)
        self.assertEqual(summary['roi'], 200.0)
        self.assertEqual(summary['ctr'], 5.0)
        self.assertEqual(summary['conversion_rate'], 10.0)
        self.assertEqual(summary['total_spend'], 1000.0)
        self.assertEqual(summary['total_revenue'], 3000.0)
        self.assertEqual(summary['total_conversions'], 50)


class TestReportGenerator(unittest.TestCase):
    """Test report generation"""
    
    def setUp(self):
        """Set up test data"""
        self.db = CampaignDatabase('test_reports.db')
        self.analyzer = CampaignAnalyzer(self.db)
        self.report_gen = ReportGenerator(self.db, self.analyzer)
        
        # Insert test campaign
        campaign = {
            'campaign_id': 'TEST_004',
            'name': 'Report Test',
            'channel': 'Test',
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'budget': 1000.0,
            'status': 'active'
        }
        self.db.insert_campaign(campaign)
        
        metrics = {
            'campaign_id': 'TEST_004',
            'date': datetime.now().date(),
            'impressions': 5000,
            'clicks': 250,
            'conversions': 25,
            'spend': 500.0,
            'revenue': 2000.0
        }
        self.db.insert_metrics(metrics)
    
    def tearDown(self):
        """Clean up"""
        if os.path.exists('test_reports.db'):
            os.remove('test_reports.db')
        if os.path.exists('test_report.csv'):
            os.remove('test_report.csv')
        if os.path.exists('test_report.json'):
            os.remove('test_report.json')
    
    def test_csv_export(self):
        """Test CSV export"""
        self.report_gen.export_to_csv('test_report.csv')
        self.assertTrue(os.path.exists('test_report.csv'))
        
        with open('test_report.csv', 'r') as f:
            content = f.read()
            self.assertIn('Report Test', content)
            self.assertIn('Test', content)
    
    def test_json_export(self):
        """Test JSON export"""
        self.report_gen.export_to_json('test_report.json')
        self.assertTrue(os.path.exists('test_report.json'))
        
        with open('test_report.json', 'r') as f:
            data = json.load(f)
            self.assertIn('generated_at', data)
            self.assertIn('campaigns', data)
            self.assertEqual(len(data['campaigns']), 1)


class TestDataTypes(unittest.TestCase):
    """Test data type handling"""
    
    def test_roi_is_float(self):
        """Test that ROI is returned as float"""
        db = CampaignDatabase('test_types.db')
        analyzer = CampaignAnalyzer(db)
        
        campaign = {
            'campaign_id': 'TEST_005',
            'name': 'Type Test',
            'channel': 'Test',
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'budget': 1000.0,
            'status': 'active'
        }
        db.insert_campaign(campaign)
        
        metrics = {
            'campaign_id': 'TEST_005',
            'date': datetime.now().date(),
            'impressions': 1000,
            'clicks': 100,
            'conversions': 10,
            'spend': 100.0,
            'revenue': 300.0
        }
        db.insert_metrics(metrics)
        
        roi = analyzer.calculate_roi('TEST_005')
        self.assertIsInstance(roi, (int, float))
        
        if os.path.exists('test_types.db'):
            os.remove('test_types.db')


if __name__ == '__main__':
    unittest.main()
