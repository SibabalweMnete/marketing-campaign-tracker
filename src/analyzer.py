# src/analyzer.py - Performance analysis
class CampaignAnalyzer:
    """Analyzes campaign performance and generates insights"""
    
    def __init__(self, database):
        self.db = database
    
    def calculate_roi(self, campaign_id):
        """Calculate Return on Investment"""
        metrics = self.db.get_campaign_metrics(campaign_id)
        if not metrics:
            return 0
        
        total_spend = sum(m[6] for m in metrics)
        total_revenue = sum(m[7] for m in metrics)
        
        if total_spend == 0:
            return 0
        
        roi = ((total_revenue - total_spend) / total_spend) * 100
        return round(roi, 2)
    
    def calculate_ctr(self, campaign_id):
        """Calculate Click-Through Rate"""
        metrics = self.db.get_campaign_metrics(campaign_id)
        if not metrics:
            return 0
        
        total_impressions = sum(m[3] for m in metrics)
        total_clicks = sum(m[4] for m in metrics)
        
        if total_impressions == 0:
            return 0
        
        ctr = (total_clicks / total_impressions) * 100
        return round(ctr, 2)
    
    def calculate_conversion_rate(self, campaign_id):
        """Calculate Conversion Rate"""
        metrics = self.db.get_campaign_metrics(campaign_id)
        if not metrics:
            return 0
        
        total_clicks = sum(m[4] for m in metrics)
        total_conversions = sum(m[5] for m in metrics)
        
        if total_clicks == 0:
            return 0
        
        conversion_rate = (total_conversions / total_clicks) * 100
        return round(conversion_rate, 2)
    
    def get_campaign_summary(self, campaign_id):
        """Get complete performance summary"""
        metrics = self.db.get_campaign_metrics(campaign_id)
        
        if not metrics:
            return None
        
        total_spend = sum(m[6] for m in metrics)
        total_revenue = sum(m[7] for m in metrics)
        total_conversions = sum(m[5] for m in metrics)
        
        return {
            'roi': self.calculate_roi(campaign_id),
            'ctr': self.calculate_ctr(campaign_id),
            'conversion_rate': self.calculate_conversion_rate(campaign_id),
            'total_spend': total_spend,
            'total_revenue': total_revenue,
            'total_conversions': total_conversions
        }