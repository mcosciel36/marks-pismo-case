from src.pismo_case.faker_script_dupes2 import generate_event, generate_events


def test_generate_event_structure():
    event = generate_event()
    assert "event_id" in event
    assert "timestamp" in event
    assert "domain" in event
    assert "event_type" in event
    assert "data" in event
    assert "id" in event["data"]


def test_generate_events_with_duplicates():
    events = generate_events(num_events=100, duplicate_ratio=0.1)
    event_ids = [event["event_id"] for event in events]
    duplicates = [
        event_id for event_id in set(event_ids)
        if event_ids.count(event_id) > 1
    ]
    assert len(duplicates) > 0
