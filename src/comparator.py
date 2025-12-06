# src/comparator.py - Campaign Comparison & Benchmarking
from datetime import datetime

class CampaignComparator:
    """Compare and benchmark campaigns against each other"""
    
    def __init__(self, database, analyzer):
        self.db = database
        self.analyzer = analyzer
    
    def compare_campaigns(self, campaign_ids):
        """Compare specific campaigns side-by-side"""
        print("\n" + "="*80)
        print("⚖️  CAMPAIGN COMPARISON ANALYSIS")
        print("="*80)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        campaigns = {campaign[0]: campaign for campaign in self.db.get_all_campaigns()}
        summaries = {}
        
        for camp_id in campaign_ids:
            if camp_id in campaigns:
                summary = self.analyzer.get_campaign_summary(camp_id)
                if summary:
                    summaries[camp_id] = (campaigns[camp_id], summary)
        
        if not summaries:
            print("No valid campaigns to compare.\n")
            return
        
        # Print comparison table
        print(f"{'Campaign':<25} {'Channel':<15} {'ROI':<12} {'CTR':<12} {'Conv Rate':<12} {'Spend':<15}")
        print("-" * 91)
        
        sorted_campaigns = sorted(summaries.items(), 
                                 key=lambda x: x[1][1]['roi'], 
                                 reverse=True)
        
        best_roi = sorted_campaigns[0][1][1]['roi']
        
        for camp_id, (campaign, summary) in sorted_campaigns:
            name = campaign[1][:22]
            channel = campaign[2]
            roi = f"{summary['roi']:.1f}%"
            ctr = f"{summary['ctr']:.2f}%"
            conv_rate = f"{summary['conversion_rate']:.2f}%"
            spend = f"R{summary['total_spend']:,.0f}"
            
            # Highlight best performer
            prefix = "🥇 " if summary['roi'] == best_roi else "   "
            print(f"{prefix}{name:<21} {channel:<15} {roi:<12} {ctr:<12} {conv_rate:<12} {spend:<15}")
        
        print("-" * 91)
        
        # Analysis
        print("\n📊 DETAILED COMPARISON:\n")
        
        for camp_id, (campaign, summary) in sorted_campaigns:
            print(f"🎯 {campaign[1]}")
            print(f"   Channel: {campaign[2]}")
            print(f"   ROI: {summary['roi']:.1f}% | CTR: {summary['ctr']:.2f}% | Conv: {summary['conversion_rate']:.2f}%")
            print(f"   Spend: R{summary['total_spend']:,.2f} → Revenue: R{summary['total_revenue']:,.2f}")
            print(f"   Conversions: {summary['total_conversions']:.0f}\n")
        
        # Efficiency metrics
        print("💡 EFFICIENCY INSIGHTS:\n")
        
        for camp_id, (campaign, summary) in sorted_campaigns:
            cost_per_conversion = (summary['total_spend'] / summary['total_conversions'] 
                                  if summary['total_conversions'] > 0 else 0)
            revenue_per_click = (summary['total_revenue'] / 
                               (summary['total_spend'] / summary['ctr'] * 100)
                               if summary['ctr'] > 0 else 0)
            
            print(f"📌 {campaign[1]}")
            print(f"   Cost per Conversion: R{cost_per_conversion:,.2f}")
            print(f"   Revenue per Ad Spend: R{1 + (summary['roi']/100):.2f}")
            print()
        
        print("="*80 + "\n")
    
    def compare_by_channel(self):
        """Compare performance across different channels"""
        print("\n" + "="*80)
        print("📡 CHANNEL PERFORMANCE COMPARISON")
        print("="*80)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        campaigns = self.db.get_all_campaigns()
        channels = {}
        
        for campaign in campaigns:
            campaign_id = campaign[0]
            channel = campaign[2]
            summary = self.analyzer.get_campaign_summary(campaign_id)
            
            if summary:
                if channel not in channels:
                    channels[channel] = {
                        'campaigns': [],
                        'total_roi': 0,
                        'total_spend': 0,
                        'total_revenue': 0,
                        'total_conversions': 0,
                        'total_clicks': 0,
                        'total_impressions': 0
                    }
                
                channels[channel]['campaigns'].append(campaign[1])
                channels[channel]['total_roi'] += summary['roi']
                channels[channel]['total_spend'] += summary['total_spend']
                channels[channel]['total_revenue'] += summary['total_revenue']
                channels[channel]['total_conversions'] += summary['total_conversions']
        
        # Sort by average ROI
        sorted_channels = sorted(channels.items(), 
                               key=lambda x: x[1]['total_roi']/len(x[1]['campaigns']), 
                               reverse=True)
        
        print(f"{'Channel':<15} {'Campaigns':<12} {'Avg ROI':<12} {'Total Spend':<18} {'Total Revenue':<18}")
        print("-" * 75)
        
        for channel, data in sorted_channels:
            avg_roi = data['total_roi'] / len(data['campaigns'])
            print(f"{channel:<15} {len(data['campaigns']):<12} {avg_roi:.1f}%{'':<6} R{data['total_spend']:>13,.0f}   R{data['total_revenue']:>13,.0f}")
        
        print("-" * 75 + "\n")
        
        # Recommendations
        print("🎯 CHANNEL RECOMMENDATIONS:\n")
        
        top_channel = sorted_channels[0]
        print(f"🏆 Best Performer: {top_channel[0]}")
        print(f"   Average ROI: {top_channel[1]['total_roi']/len(top_channel[1]['campaigns']):.1f}%")
        print(f"   Active Campaigns: {', '.join(top_channel[1]['campaigns'])}\n")
        
        if len(sorted_channels) > 1:
            bottom_channel = sorted_channels[-1]
            print(f"⚠️  Needs Attention: {bottom_channel[0]}")
            print(f"   Average ROI: {bottom_channel[1]['total_roi']/len(bottom_channel[1]['campaigns']):.1f}%")
            print(f"   Active Campaigns: {', '.join(bottom_channel[1]['campaigns'])}\n")
        
        print("="*80 + "\n")
    
    def efficiency_report(self):
        """Generate efficiency metrics across campaigns"""
        print("\n" + "="*80)
        print("⚡ CAMPAIGN EFFICIENCY REPORT")
        print("="*80)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        campaigns = self.db.get_all_campaigns()
        efficiencies = []
        
        for campaign in campaigns:
            campaign_id = campaign[0]
            summary = self.analyzer.get_campaign_summary(campaign_id)
            
            if summary and summary['total_conversions'] > 0:
                cost_per_conv = summary['total_spend'] / summary['total_conversions']
                rev_per_spend = summary['total_revenue'] / summary['total_spend']
                
                efficiencies.append({
                    'name': campaign[1],
                    'channel': campaign[2],
                    'cost_per_conv': cost_per_conv,
                    'rev_per_spend': rev_per_spend,
                    'conversions': summary['total_conversions'],
                    'roi': summary['roi']
                })
        
        # Sort by cost per conversion (lower is better)
        efficiencies.sort(key=lambda x: x['cost_per_conv'])
        
        print("Most Efficient Campaigns (Lowest Cost per Conversion):\n")
        print(f"{'Campaign':<25} {'Cost/Conv':<12} {'Revenue/Spend':<15} {'Total Conv':<12}")
        print("-" * 64)
        
        for eff in efficiencies[:5]:
            print(f"{eff['name'][:24]:<25} R{eff['cost_per_conv']:>8,.2f}   {eff['rev_per_spend']:>6.2f}x{'':<6} {int(eff['conversions']):>8}")
        
        print("\n" + "="*80 + "\n")
