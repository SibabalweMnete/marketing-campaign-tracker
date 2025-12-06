# src/dashboard.py - Real-time performance dashboard
import os
from datetime import datetime
import time

class Dashboard:
    """Interactive real-time campaign dashboard"""
    
    def __init__(self, database, analyzer):
        self.db = database
        self.analyzer = analyzer
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def render_progress_bar(self, current, total, width=30):
        """Render a nice progress bar"""
        percentage = current / total if total > 0 else 0
        filled = int(width * percentage)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{bar}] {percentage*100:.0f}%"
    
    def display_campaign_card(self, campaign, summary):
        """Display individual campaign as a card"""
        name = campaign[1]
        channel = campaign[2]
        roi = summary['roi']
        conversion_rate = summary['conversion_rate']
        total_spend = summary['total_spend']
        total_revenue = summary['total_revenue']
        
        # Color coding based on performance
        status_icon = "🟢" if roi > 100 else "🟡" if roi > 50 else "🔴"
        
        print(f"\n{status_icon} {name}")
        print(f"   Channel: {channel}")
        print(f"   Spend: R{total_spend:,.2f} → Revenue: R{total_revenue:,.2f}")
        print(f"   ROI: {roi:.1f}% | Conversion Rate: {conversion_rate:.2f}%")
        print(f"   Performance: {self.render_progress_bar(max(0, roi), 200)}")
    
    def live_dashboard(self, refresh_interval=5, duration=30):
        """Display live updating dashboard"""
        print("\n🚀 LAUNCHING LIVE DASHBOARD...")
        time.sleep(1)
        
        start_time = time.time()
        iteration = 0
        
        while time.time() - start_time < duration:
            self.clear_screen()
            
            print("="*70)
            print("📊 LIVE MARKETING CAMPAIGN DASHBOARD")
            print("="*70)
            print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Refresh Rate: Every {refresh_interval} seconds | Duration: {duration}s")
            print("="*70)
            
            campaigns = self.db.get_all_campaigns()
            total_spend = 0
            total_revenue = 0
            active_count = 0
            
            for campaign in campaigns:
                campaign_id = campaign[0]
                status = campaign[6]
                summary = self.analyzer.get_campaign_summary(campaign_id)
                
                if status == 'active':
                    active_count += 1
                
                if summary:
                    total_spend += summary['total_spend']
                    total_revenue += summary['total_revenue']
                    self.display_campaign_card(campaign, summary)
            
            # Summary metrics
            print("\n" + "="*70)
            print("📈 PORTFOLIO SUMMARY")
            print("="*70)
            print(f"Total Campaigns: {len(campaigns)} | Active: {active_count}")
            print(f"Total Spend: R{total_spend:,.2f}")
            print(f"Total Revenue: R{total_revenue:,.2f}")
            
            overall_roi = ((total_revenue - total_spend) / total_spend * 100) if total_spend > 0 else 0
            print(f"Overall ROI: {overall_roi:.1f}%")
            print(f"Net Profit: R{total_revenue - total_spend:,.2f}")
            print(f"\nPortfolio Health: {self.render_progress_bar(max(0, overall_roi), 200)}")
            
            iteration += 1
            remaining = duration - (time.time() - start_time)
            
            if remaining > 0:
                print(f"\n⏱️  Next refresh in {int(remaining)}s (Press Ctrl+C to exit)...")
                time.sleep(min(refresh_interval, remaining))
            else:
                break
        
        print("\n✅ Dashboard session ended.\n")
    
    def summary_view(self):
        """Quick summary view without live updates"""
        self.clear_screen()
        
        print("\n" + "="*70)
        print("📊 CAMPAIGN PORTFOLIO SUMMARY")
        print("="*70)
        print(f"Snapshot: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        campaigns = self.db.get_all_campaigns()
        
        if not campaigns:
            print("No campaigns found in database.\n")
            return
        
        # Summary stats
        total_spend = 0
        total_revenue = 0
        total_conversions = 0
        
        for campaign in campaigns:
            campaign_id = campaign[0]
            summary = self.analyzer.get_campaign_summary(campaign_id)
            
            if summary:
                total_spend += summary['total_spend']
                total_revenue += summary['total_revenue']
                total_conversions += summary['total_conversions']
                self.display_campaign_card(campaign, summary)
        
        overall_roi = ((total_revenue - total_spend) / total_spend * 100) if total_spend > 0 else 0
        
        print("\n" + "="*70)
        print(f"💰 Total Spend: R{total_spend:,.2f}")
        print(f"💵 Total Revenue: R{total_revenue:,.2f}")
        print(f"📊 Total Conversions: {total_conversions:,.0f}")
        print(f"🎯 Overall ROI: {overall_roi:.1f}%")
        print(f"📈 Net Profit: R{total_revenue - total_spend:,.2f}")
        print("="*70 + "\n")
