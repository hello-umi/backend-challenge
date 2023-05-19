class MessagingStrategy:
    """Base class for Messaging Strategies. Subclass it to declare new methods"""

    def send_message(self, message):
        raise NotImplementedError()
