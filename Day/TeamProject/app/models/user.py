from enum import Enum

class UserRole(str,Enum):
    CUSTOMER = "customer"
    SUPPORT_AGENT = "support_agent"
    SUPPORT_TEAM_LEAD = "support_team_lead"
    ADMIN = "admin"