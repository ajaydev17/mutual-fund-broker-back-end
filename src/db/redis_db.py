import redis.asyncio as aioredis
from src.config import config_obj

JTI_EXPIRY = 3600

token_blocklist = aioredis.from_url(
    config_obj.REDIS_URL,
    decode_responses=True
)


async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value=1, ex=JTI_EXPIRY)


async def check_jti_in_blocklist(jti: str) -> bool:
    return await token_blocklist.exists(jti) > 0
