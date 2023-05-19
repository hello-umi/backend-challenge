"""
Strategy Registry to declare the valid options for Channels
"""

from proxy.strategies.message_email import EmailMessagingStrategy
from proxy.strategies.message_slack import SlackMessagingStrategy

CHANNEL_STRATEGY_REGISTRY = {
    "slack": SlackMessagingStrategy,
    "email": EmailMessagingStrategy,
}
