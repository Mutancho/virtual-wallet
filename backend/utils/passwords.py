import asyncio
import bcrypt


async def hash_password(password: str) -> str | None:
    try:
        if not password:
            raise ValueError("Password cannot be empty")
        if not isinstance(password, str):
            raise TypeError("Password must be a string")

        salt = bcrypt.gensalt()
        hashed_password = await asyncio.to_thread(bcrypt.hashpw, password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    except (ValueError, TypeError) as e:
        print(f"Error hashing password: {e}")
        return None

    except Exception as e:
        print(f"Error hashing password: {e}")
        return None


async def verify_password(password: str, hashed_password: str) -> bool | str:
    try:
        if not password or not hashed_password:
            raise ValueError("Both password and hashed_password must be provided")
        if not isinstance(password, str) or not isinstance(hashed_password, str):
            raise TypeError("Password and hashed_password must be strings")

        result = await asyncio.to_thread(bcrypt.checkpw, password.encode("utf-8"), hashed_password.encode("utf-8"))
        return result

    except (ValueError, TypeError) as e:
        print(f"Error verifying password: {e}")
        return False

    except Exception as e:
        print(f"Error verifying password: {e}")
        return False
