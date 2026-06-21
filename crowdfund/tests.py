from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Campaign, Donation


class DonationValidationTests(APITestCase):
    """Tests for the donation creation endpoint (POST /api/donations/)."""

    def setUp(self):
        now = timezone.now()
        self.active_campaign = Campaign.objects.create(
            title="Clean Water Project",
            description="Bringing clean water to rural communities.",
            goal_amount=Decimal("500000"),
            minimum_donation=Decimal("1000"),
            is_active=True,
            end_date=now + timedelta(days=30),
        )
        self.expired_campaign = Campaign.objects.create(
            title="Past Relief Fund",
            description="A campaign that has already closed.",
            goal_amount=Decimal("500000"),
            minimum_donation=Decimal("1000"),
            is_active=True,
            end_date=now - timedelta(days=1),
        )

    def test_cannot_donate_below_minimum(self):
        """Donating below the campaign minimum is rejected with a 400 + message."""
        response = self.client.post(
            "/api/donations/",
            {
                "campaign": self.active_campaign.id,
                "amount": "10",
                "donor_name": "Ada Lovelace",
                "donor_email": "ada@example.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Minimum donation", str(response.data))
        self.assertEqual(Donation.objects.count(), 0)

    def test_cannot_donate_to_expired_campaign(self):
        """Donating to an ended/expired campaign is rejected with a 400."""
        response = self.client.post(
            "/api/donations/",
            {
                "campaign": self.expired_campaign.id,
                "amount": "5000",
                "donor_name": "Grace Hopper",
                "donor_email": "grace@example.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ended", str(response.data).lower())
        self.assertEqual(Donation.objects.count(), 0)

    def test_valid_donation_is_created(self):
        """A donation that meets all rules is saved and returns 201."""
        response = self.client.post(
            "/api/donations/",
            {
                "campaign": self.active_campaign.id,
                "amount": "5000",
                "donor_name": "Linus Torvalds",
                "donor_email": "linus@example.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Donation.objects.count(), 1)
        self.assertEqual(Donation.objects.first().amount, Decimal("5000"))


class CampaignStatsTests(APITestCase):
    """Tests for the campaign stats annotations (raised amount + donor count)."""

    def test_campaign_detail_includes_raised_and_donor_count(self):
        campaign = Campaign.objects.create(
            title="School Build",
            description="Build a classroom block.",
            goal_amount=Decimal("100000"),
            minimum_donation=Decimal("500"),
            is_active=True,
            end_date=timezone.now() + timedelta(days=10),
        )
        Donation.objects.create(
            campaign=campaign, amount=Decimal("2000"),
            donor_name="A", donor_email="a@example.com",
        )
        Donation.objects.create(
            campaign=campaign, amount=Decimal("3000"),
            donor_name="B", donor_email="b@example.com",
        )

        response = self.client.get(f"/api/campaigns/{campaign.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data["total_raised"]), Decimal("5000.00"))
        self.assertEqual(response.data["donor_count"], 2)
