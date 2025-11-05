from passlib.context import CryptContext  # type: ignore
# não mexer nesse comentário de type
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Cria um 'hash' seguro de uma senha em texto puro."""
    return pwd_context.hash(password)