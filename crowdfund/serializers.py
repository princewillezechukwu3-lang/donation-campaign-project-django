from rest_framework import serializers
from .models import Campaign, Donation

class CampaignSerializer(serializers.ModelSerializer):
    total_raised = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    donor_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Campaign
        fields = ['id', 'title', 'description', 'goal_amount', 'minimum_donation', 'is_active', 'end_date', 'total_raised', 'donor_count']


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id', 'campaign', 'amount', 'donor_name', 'donor_email', 'created_at']