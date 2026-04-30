from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AuthenticationResetToken(PasswordResetTokenGenerator):
    """
    Custom token generator for account activation.
    The token will change if the user's active status changes.
    """
    def _make_hash_value(self, user, timestamp):
        # Using six is no longer necessary in modern Django
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )

account_activation_token = AuthenticationResetToken()