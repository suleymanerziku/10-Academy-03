import pytest


def test_trend_fetcher_contract():
    """
    This test asserts that the trend fetcher returns
    data matching the defined API contract.
    """

    # hypothetical import (does not exist yet)
    from skills.skill_fetch_trends import fetch_trends

    result = fetch_trends(
        platform="tiktok",
        region="ET",
        limit=5
    )

    assert isinstance(result, dict)
    assert "trends" in result
    assert isinstance(result["trends"], list)

    trend = result["trends"][0]
    assert "topic" in trend
    assert "confidence" in trend
    assert isinstance(trend["confidence"], float)

    assert "source" in result
    assert "retrieved_at" in result
