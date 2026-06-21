"""Server-rendered frontend pages for the donation campaign site.

These views render HTML templates. List/detail pages read campaign data from
the database (using the same aggregation the API uses), while the donate form
submits to the existing REST endpoint (POST /api/donations/) via fetch(), so the
backend stays the single source of truth for validation.
"""
from decimal import Decimal

from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Campaign


def _campaigns_with_stats():
    """Campaigns annotated with total_raised and donor_count (mirrors the API)."""
    return Campaign.objects.annotate(
        total_raised=Sum("donations__amount"),
        donor_count=Count("donations"),
    ).order_by("id")


def _decorate(campaign, now):
    """Attach display helpers (raised, progress %, remaining, ended) to a campaign."""
    raised = campaign.total_raised or Decimal("0")
    goal = campaign.goal_amount or Decimal("0")
    campaign.raised = raised
    campaign.progress = min(100, int((raised / goal) * 100)) if goal else 0
    campaign.remaining = max(Decimal("0"), goal - raised)
    campaign.ended = (not campaign.is_active) or (campaign.end_date < now)
    return campaign


def campaign_list(request):
    now = timezone.now()
    campaigns = [_decorate(c, now) for c in _campaigns_with_stats()]
    return render(request, "crowdfund/campaign_list.html", {"campaigns": campaigns})


def campaign_detail(request, pk):
    now = timezone.now()
    campaign = _decorate(get_object_or_404(_campaigns_with_stats(), pk=pk), now)
    return render(request, "crowdfund/campaign_detail.html", {"campaign": campaign})


def donate(request, pk):
    now = timezone.now()
    campaign = _decorate(get_object_or_404(_campaigns_with_stats(), pk=pk), now)
    return render(request, "crowdfund/donate.html", {"campaign": campaign})
