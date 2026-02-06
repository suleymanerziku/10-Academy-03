import inspect


def test_generate_video_metadata_signature():
    """
    Validate skill_generate_video_metadata input interface.
    """

    from skills.skill_generate_video_metadata import generate_video_metadata

    sig = inspect.signature(generate_video_metadata)

    expected_params = {
        "objective",
        "platform",
        "trend_context",
        "constraints"
    }

    assert set(sig.parameters.keys()) == expected_params
