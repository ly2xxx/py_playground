"""
Generate synthetic customer support ticket data
"""
import pandas as pd
import random
from datetime import datetime, timedelta

# Ticket templates with realistic patterns
TICKET_TEMPLATES = {
    "Login Issues": [
        "Cannot log into my account. Getting 'invalid credentials' error.",
        "Password reset not working. Link expired.",
        "Two-factor authentication code never arrives.",
        "Account locked after multiple login attempts.",
        "Login button not responding on mobile app.",
    ],
    "Payment Problems": [
        "Payment failed with error code 402. Card was charged twice.",
        "Cannot add new payment method. System keeps rejecting my card.",
        "Subscription renewal failed. Account suspended.",
        "Refund not received after 5 business days.",
        "Payment processing stuck at 'pending' for 24 hours.",
    ],
    "Feature Requests": [
        "Would like dark mode option in the app.",
        "Can you add export to Excel functionality?",
        "Requesting batch upload feature for multiple files.",
        "Need API access for integration with our CRM.",
        "Please add support for SSO with Google Workspace.",
    ],
    "Bug Reports": [
        "Dashboard crashes when filtering by date range.",
        "Export function generates corrupted PDF files.",
        "Mobile app freezes on Android 13.",
        "Search results showing wrong data after last update.",
        "Notification emails contain broken links.",
    ],
    "Account Management": [
        "Need to upgrade my plan to Enterprise.",
        "How do I cancel my subscription?",
        "Want to transfer account ownership to another user.",
        "Can I get a refund for unused months?",
        "Need invoice for last 3 months for accounting.",
    ],
    "Performance Issues": [
        "Website extremely slow during peak hours.",
        "File upload takes forever for large files.",
        "Reports taking 10+ minutes to generate.",
        "Dashboard not loading - timeout error.",
        "API response time increased by 300% this week.",
    ],
    "Data Issues": [
        "Missing data from yesterday's import.",
        "Duplicate records appearing in my dashboard.",
        "Cannot delete old records - getting permission error.",
        "Data export incomplete - only showing 50% of records.",
        "Sync with third-party service stopped working.",
    ],
}

def generate_tickets(num_tickets=100, num_days=5):
    """Generate synthetic support tickets"""
    
    tickets = []
    start_date = datetime.now() - timedelta(days=num_days)
    
    # Weight topics to create realistic distribution
    topics = list(TICKET_TEMPLATES.keys())
    weights = [0.25, 0.20, 0.10, 0.15, 0.12, 0.10, 0.08]  # Login & Payment most common
    
    priorities = ["Low", "Medium", "High", "Critical"]
    priority_weights = [0.3, 0.4, 0.25, 0.05]
    
    statuses = ["Open", "In Progress", "Resolved", "Closed"]
    status_weights = [0.15, 0.25, 0.40, 0.20]
    
    for i in range(num_tickets):
        # Random day within the 5-day period
        day_offset = random.randint(0, num_days - 1)
        ticket_date = start_date + timedelta(days=day_offset)
        
        # Business hours: 9am-6pm
        hour = random.randint(9, 17)
        minute = random.randint(0, 59)
        ticket_datetime = ticket_date.replace(hour=hour, minute=minute)
        
        # Select topic and template
        topic = random.choices(topics, weights=weights)[0]
        conversation = random.choice(TICKET_TEMPLATES[topic])
        
        # Add some variation to conversations
        if random.random() < 0.3:
            follow_ups = [
                " Urgent - this is blocking our business operations.",
                " This has been happening for 3 days now.",
                " Please escalate to senior support.",
                " Tried all troubleshooting steps already.",
                " Multiple users affected by this issue.",
            ]
            conversation += random.choice(follow_ups)
        
        priority = random.choices(priorities, weights=priority_weights)[0]
        status = random.choices(statuses, weights=status_weights)[0]
        
        # Resolution time (in hours) - varies by priority
        if status in ["Resolved", "Closed"]:
            if priority == "Critical":
                resolution_time = random.uniform(0.5, 4)
            elif priority == "High":
                resolution_time = random.uniform(2, 12)
            elif priority == "Medium":
                resolution_time = random.uniform(12, 48)
            else:
                resolution_time = random.uniform(24, 120)
        else:
            resolution_time = None
        
        # Customer satisfaction (for resolved/closed tickets)
        satisfaction = None
        if status in ["Resolved", "Closed"] and random.random() < 0.8:
            # Satisfaction correlates with resolution time
            if resolution_time and resolution_time < 24:
                satisfaction = random.randint(4, 5)
            else:
                satisfaction = random.randint(2, 4)
        
        tickets.append({
            "ticket_id": f"TKT-{1000 + i}",
            "created_at": ticket_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "topic": topic,
            "priority": priority,
            "status": status,
            "conversation": conversation,
            "resolution_time_hours": resolution_time,
            "customer_satisfaction": satisfaction,
        })
    
    return pd.DataFrame(tickets)

if __name__ == "__main__":
    df = generate_tickets(100, 5)
    df.to_csv("support_tickets.csv", index=False)
    print(f"[OK] Generated {len(df)} tickets")
    print(f"\n[STATS] Topic Distribution:")
    print(df['topic'].value_counts())
    print(f"\n[STATS] Priority Distribution:")
    print(df['priority'].value_counts())
    print(f"\n[STATS] Status Distribution:")
    print(df['status'].value_counts())
