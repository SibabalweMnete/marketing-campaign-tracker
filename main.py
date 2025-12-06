# main.py - Main application entry point
import argparse
from datetime import datetime
from src.database import CampaignDatabase
from src.data_collector import DataCollector
from src.analyzer import CampaignAnalyzer
from src.report_generator import ReportGenerator
from src.dashboard import Dashboard
from src.comparator import CampaignComparator

def main():
    parser = argparse.ArgumentParser(description='Marketing Campaign Tracker')
    parser.add_argument('--init', action='store_true', help='Initialize database')
    parser.add_argument('--collect', action='store_true', help='Collect campaign data')
    parser.add_argument('--report', action='store_true', help='Generate performance report')
    parser.add_argument('--dashboard', action='store_true', help='Display live dashboard')
    parser.add_argument('--summary', action='store_true', help='Display portfolio summary')
    parser.add_argument('--insights', action='store_true', help='Generate insights and recommendations')
    parser.add_argument('--compare', nargs='*', help='Compare specific campaigns')
    parser.add_argument('--channels', action='store_true', help='Compare performance by channel')
    parser.add_argument('--efficiency', action='store_true', help='Show efficiency metrics')
    parser.add_argument('--auto', action='store_true', help='Run full automated workflow')
    
    args = parser.parse_args()
    
    # Initialize database
    db = CampaignDatabase()
    
    if args.init:
        print("🚀 Initializing Marketing Campaign Tracker...")
        db.init_database()
        return
    
    if args.collect or args.auto:
        print("📥 Collecting campaign data from all channels...\n")
        collector = DataCollector()
        campaigns = collector.collect_all_campaigns()
        
        # Store in database
        for campaign in campaigns:
            db.insert_campaign(campaign)
            db.insert_metrics({
                'campaign_id': campaign['campaign_id'],
                'date': datetime.now().date(),
                **campaign['metrics']
            })
        
        print("✅ All campaign data stored in database\n")
    
    if args.report or args.auto:
        analyzer = CampaignAnalyzer(db)
        report_gen = ReportGenerator(db, analyzer)
        
        # Generate daily summary
        report_gen.generate_daily_report()
        
        # Generate intelligent insights
        report_gen.generate_insights()
        
        # Export for stakeholders
        report_gen.export_to_csv('reports/campaign_performance.csv')
        report_gen.export_to_json('reports/campaign_data.json')
        
        print("\n🎉 Full reporting suite generated successfully!")
    
    if args.dashboard:
        analyzer = CampaignAnalyzer(db)
        dashboard = Dashboard(db, analyzer)
        try:
            dashboard.live_dashboard(refresh_interval=3, duration=60)
        except KeyboardInterrupt:
            print("\n\n✋ Dashboard stopped by user.\n")
    
    if args.summary:
        analyzer = CampaignAnalyzer(db)
        dashboard = Dashboard(db, analyzer)
        dashboard.summary_view()
    
    if args.insights:
        analyzer = CampaignAnalyzer(db)
        report_gen = ReportGenerator(db, analyzer)
        report_gen.generate_insights()
    
    if args.compare is not None:
        analyzer = CampaignAnalyzer(db)
        comparator = CampaignComparator(db, analyzer)
        
        if args.compare:  # Specific campaign IDs provided
            comparator.compare_campaigns(args.compare)
        else:  # No specific IDs, compare all
            all_campaigns = db.get_all_campaigns()
            campaign_ids = [c[0] for c in all_campaigns]
            comparator.compare_campaigns(campaign_ids)
    
    if args.channels:
        analyzer = CampaignAnalyzer(db)
        comparator = CampaignComparator(db, analyzer)
        comparator.compare_by_channel()
    
    if args.efficiency:
        analyzer = CampaignAnalyzer(db)
        comparator = CampaignComparator(db, analyzer)
        comparator.efficiency_report()

if __name__ == "__main__":
    main()