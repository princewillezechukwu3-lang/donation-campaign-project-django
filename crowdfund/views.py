from django.db.models import Sum, Count
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Campaign, Donation
from .serializers import CampaignSerializer, DonationSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer

    def get_queryset(self):
        # Dynamically aggregate total_raised and donor_count using optimized database joins
        return Campaign.objects.annotate(
            total_raised=Sum('donations__amount'),
            donor_count=Count('donations')
        ).order_by('id')


class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

    def create(self, request, *args, **kwargs):
        # Capture incoming data payload
        campaign_id = request.data.get('campaign')
        amount_input = request.data.get('amount')

        # 1. Fetch the targeted campaign
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except (Campaign.DoesNotExist, ValueError):
            return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)

        # 2. Robust numeric validation on incoming amount
        try:
            donation_amount = float(amount_input)
            if donation_amount <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return Response({"error": "Donation amount must be a valid positive number"}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Validation Wall: Enforce threshold minimums
        if donation_amount < campaign.minimum_donation:
            return Response(
                {"error": f"Minimum donation amount for this campaign is ₦{campaign.minimum_donation}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. Validation Wall: Block closed/expired campaigns
        if not campaign.is_active or campaign.end_date < timezone.now():
            return Response({"error": "Campaign has ended or is inactive"}, status=status.HTTP_400_BAD_REQUEST)

        # Everything passes perfectly -> Execute database insertion
        return super().create(request, *args, **kwargs)