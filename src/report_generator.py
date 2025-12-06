# src/report_generator.py - Automated report creation
from datetime import datetime
import json
import csv
from pathlib import Path

class ReportGenerator:
    """Generates automated performance reports"""
    
    def __init__(self, database, analyzer):
        self.db = database
        self.analyzer = analyzer
    
    def generate_daily_report(self):
        """Generate daily performance report"""
        print("\n" + "="*60)
        print("📊 DAILY CAMPAIGN PERFORMANCE REPORT")
        print("="*60)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        campaigns = self.db.get_all_campaigns()
        
        total_spend = 0
        total_revenue = 0
        active_count = 0
        
        top_performers = []
        
        for campaign in campaigns:
            campaign_id = campaign[0]
            name = campaign[1]
            channel = campaign[2]
            status = campaign[6]
            
            if status == 'active':
                active_count += 1
            
            summary = self.analyzer.get_campaign_summary(campaign_id)
            
            if summary:
                total_spend += summary['total_spend']
                total_revenue += summary['total_revenue']
                
                top_performers.append({
                    'name': name,
                    'channel': channel,
                    'roi': summary['roi'],
                    'spend': summary['total_spend'],
                    'revenue': summary['total_revenue']
                })
        
        # Overall performance
        overall_roi = ((total_revenue - total_spend) / total_spend * 100) if total_spend > 0 else 0
        
        print(f"📈 Overall Performance:")
        print(f"Total Campaigns: {len(campaigns)}")
        print(f"Active Campaigns: {active_count}")
        print(f"Total Spend: R{total_spend:,.2f}")
        print(f"Total Revenue: R{total_revenue:,.2f}")
        print(f"Overall ROI: {overall_roi:.0f}%\n")
        
        # Top performers
        top_performers.sort(key=lambda x: x['roi'], reverse=True)
        
        print("🔥 Top Performing Campaigns:")
        for i, campaign in enumerate(top_performers[:3], 1):
            print(f"{i}. \"{campaign['name']}\" ({campaign['channel']})")
            print(f"   - ROI: {campaign['roi']:.0f}% | Spend: R{campaign['spend']:,.2f} | Revenue: R{campaign['revenue']:,.2f}")
            status_icon = "✅" if campaign['roi'] > 100 else "⚠️"
            print(f"   - Status: {status_icon} {'Exceeding targets' if campaign['roi'] > 100 else 'Needs attention'}\n")
        
        print("="*60)
        print("✅ Report Generation Complete!\n")
    
    def export_to_csv(self, filepath):
        """Export campaign performance data to CSV"""
        campaigns = self.db.get_all_campaigns()
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = ['campaign_id', 'name', 'channel', 'status', 'roi', 'ctr', 
                         'conversion_rate', 'total_spend', 'total_revenue', 'total_conversions']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for campaign in campaigns:
                campaign_id = campaign[0]
                summary = self.analyzer.get_campaign_summary(campaign_id)
                
                if summary:
                    writer.writerow({
                        'campaign_id': campaign_id,
                        'name': campaign[1],
                        'channel': campaign[2],
                        'status': campaign[6],
                        'roi': f"{summary['roi']:.2f}%",
                        'ctr': f"{summary['ctr']:.2f}%",
                        'conversion_rate': f"{summary['conversion_rate']:.2f}%",
                        'total_spend': f"R{summary['total_spend']:,.2f}",
                        'total_revenue': f"R{summary['total_revenue']:,.2f}",
                        'total_conversions': summary['total_conversions']
                    })
        
        print(f"✅ CSV report exported to: {filepath}")
    
    def export_to_json(self, filepath):
        """Export campaign performance data to JSON"""
        campaigns = self.db.get_all_campaigns()
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'total_campaigns': len(campaigns),
            'campaigns': []
        }
        
        total_spend = 0
        total_revenue = 0
        
        for campaign in campaigns:
            campaign_id = campaign[0]
            summary = self.analyzer.get_campaign_summary(campaign_id)
            
            if summary:
                total_spend += summary['total_spend']
                total_revenue += summary['total_revenue']
                
                report_data['campaigns'].append({
                    'campaign_id': campaign_id,
                    'name': campaign[1],
                    'channel': campaign[2],
                    'start_date': campaign[3],
                    'end_date': campaign[4],
                    'budget': campaign[5],
                    'status': campaign[6],
                    'metrics': {
                        'roi_percent': round(summary['roi'], 2),
                        'ctr_percent': round(summary['ctr'], 2),
                        'conversion_rate_percent': round(summary['conversion_rate'], 2),
                        'total_spend_rand': round(summary['total_spend'], 2),
                        'total_revenue_rand': round(summary['total_revenue'], 2),
                        'total_conversions': summary['total_conversions']
                    }
                })
        
        report_data['summary'] = {
            'total_spend_rand': round(total_spend, 2),
            'total_revenue_rand': round(total_revenue, 2),
            'overall_roi_percent': round(((total_revenue - total_spend) / total_spend * 100) if total_spend > 0 else 0, 2)
        }
        
        with open(filepath, 'w') as jsonfile:
            json.dump(report_data, jsonfile, indent=2)
        
        print(f"✅ JSON report exported to: {filepath}")
    
    def generate_insights(self):
        """Generate AI-like insights and recommendations"""
        campaigns = self.db.get_all_campaigns()
        
        print("\n" + "🧠 INTELLIGENT INSIGHTS & RECOMMENDATIONS")
        print("="*60 + "\n")
        
        # Find best and worst performers
        top_roi = None
        lowest_roi = None
        top_roi_value = -float('inf')
        lowest_roi_value = float('inf')
        
        high_performers = []
        underperformers = []
        
        for campaign in campaigns:
            campaign_id = campaign[0]
            summary = self.analyzer.get_campaign_summary(campaign_id)
            
            if summary:
                if summary['roi'] > top_roi_value:
                    top_roi = campaign
                    top_roi_value = summary['roi']
                
                if summary['roi'] < lowest_roi_value:
                    lowest_roi = campaign
                    lowest_roi_value = summary['roi']
                
                if summary['roi'] > 150:
                    high_performers.append((campaign, summary))
                elif summary['roi'] < 50:
                    underperformers.append((campaign, summary))
        
        # Recommendations
        if high_performers:
            print("💡 Scaling Opportunity:")
            for campaign, summary in high_performers[:2]:
                print(f"   • \"{campaign[1]}\" is outperforming (ROI: {summary['roi']:.0f}%)")
                print(f"     → Consider increasing budget allocation\n")
        
        if underperformers:
            print("⚠️  Optimization Needed:")
            for campaign, summary in underperformers[:2]:
                print(f"   • \"{campaign[1]}\" needs attention (ROI: {summary['roi']:.0f}%)")
                print(f"     → Review targeting, creative, or pause if ROI < 0\n")
        
        # Channel analysis
        print("📊 Channel Performance:")
        channels = {}
        for campaign in campaigns:
            campaign_id = campaign[0]
            channel = campaign[2]
            summary = self.analyzer.get_campaign_summary(campaign_id)
            
            if summary:
                if channel not in channels:
                    channels[channel] = {'count': 0, 'total_roi': 0}
                channels[channel]['count'] += 1
                channels[channel]['total_roi'] += summary['roi']
        
        for channel, data in sorted(channels.items(), key=lambda x: x[1]['total_roi']/x[1]['count'], reverse=True):
            avg_roi = data['total_roi'] / data['count']
            print(f"   • {channel}: Average ROI {avg_roi:.0f}% ({data['count']} campaigns)")
        
        print("\n" + "="*60)