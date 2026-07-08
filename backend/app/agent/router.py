TEAM_ROUTING = {
    "Billing": "Billing Support Team",
    "Technical": "Technical Support Team",
    "Account": "Account Support Team",
    "Product": "Product Support Team",
    "Security": "Security Team",
    "General": "Customer Support Team",
}


def route_ticket(category: str) -> str:
    return TEAM_ROUTING.get(category, "Customer Support Team")