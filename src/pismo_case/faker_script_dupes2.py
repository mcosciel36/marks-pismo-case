import json
import random
import uuid

from faker import Faker

fake = Faker()

# Set the seed for both Faker and random for reproducibility
seed_value = 42  # You can choose any number here
Faker.seed(seed_value)
random.seed(seed_value)


def generate_event(event_id=None):
    # If event_id is None, generate a new event_id; otherwise, reuse
    # the passed event_id
    event_id = event_id if event_id else str(uuid.uuid4())
    timestamp = fake.date_time_this_decade().isoformat()
    domain = random.choice(["account", "transaction"])
    event_type = random.choice(["status-change", "created", "updated"])
    data = {
        "id": random.randint(100000, 999999),
        "old_status": random.choice(["SUSPENDED", "ACTIVE"]),
        "new_status": random.choice(["SUSPENDED", "ACTIVE"]),
        "reason": fake.sentence(),
    }
    return {
        "event_id": event_id,
        "timestamp": timestamp,
        "domain": domain,
        "event_type": event_type,
        "data": data,
    }


# Create some fake events with duplicates
def generate_events(num_events=10, duplicate_ratio=0.5):
    events = []
    unique_event_ids = []

    for _ in range(num_events):
        # Generate new event
        event = generate_event()
        events.append(event)
        unique_event_ids.append(event["event_id"])

    # Create duplicates by reusing some event_ids
    num_duplicates = int(duplicate_ratio * num_events)
    for _ in range(num_duplicates):
        # Pick a random event to duplicate
        random_event_id = random.choice(unique_event_ids)
        duplicate_event = generate_event(event_id=random_event_id)
        events.append(duplicate_event)

    return events


# Generate the events
events = generate_events(num_events=10, duplicate_ratio=0.5)

# Save the events to a file with newline-separated JSON rows
with open("events.json", "w") as f:
    for event in events:
        f.write(json.dumps(event) + "\n")
