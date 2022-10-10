from stocks_v1.models import StockTracker
from channels.layers import channel_layers


class Notification:
    """Sends notification to all subscribers when their quote price condition is met. The user must be authenticated and active to receive the push notification"""

    @classmethod
    def check_match(cls, stock):
        """Compares each updated stock's price with the tracked prices"""
        

    @classmethod
    def update_tracker(cls, stock):
        """Upates the statuses of a tracked stock when the price condition is met"""

    @classmethod
    def send_notification(cls, notification):
        """Sends notification to all connected tracking clients when their tracked price condition is met"""

    @classmethod
    def add_to_queue(cls, notification):
        """Adds the notification to a pending queue for all the unconnected clients. Upon connection, they'll receive the notification in bulk"""
