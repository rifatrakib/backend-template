import bcrypt
from passlib.context import CryptContext

from server.core.config import settings


class PasswordManager:
    def __init__(self):
        self.hash_context: CryptContext = CryptContext(
            schemes=[settings.PASSWORD_HASH_ALGORITHM],
            deprecated="auto",
            **settings.hash_round_settings,
        )

    def _combine_salt_and_password(self, salt: str, password: str) -> str:
        """A method to combine the salt and password together."""
        return salt + password

    def generate_hash_salt(self) -> str:
        """A method to generate a hashed salt for the user password."""
        return bcrypt.gensalt(rounds=settings.HASH_ROUNDS).decode()

    def generate_hashed_password(self, hash_salt: str, password: str) -> str:
        """A method to generate a hashed password for the user."""
        return self.hash_context.hash(secret=self._combine_salt_and_password(hash_salt, password))

    def verify_password(self, password: str, hash_salt: str, hashed_password: str) -> bool:
        """A method to verify the user's password."""
        return self.hash_context.verify(
            secret=self._combine_salt_and_password(hash_salt, password),
            hash=hashed_password,
        )


def get_password_manager() -> PasswordManager:
    return PasswordManager()


password_manager: PasswordManager = get_password_manager()
