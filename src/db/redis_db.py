import redis.asyncio as aioredis
from src.config import config_obj

JTI_EXPIRY = 3600

# create a blocklist in redis
token_blocklist = aioredis.from_url(
    config_obj.REDIS_URL,
    decode_responses=True
)


# function to add jti to blocklist in redis
async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value=1, ex=JTI_EXPIRY)

# check whether jti exists in redis blocklist
async def check_jti_in_blocklist(jti: str) -> bool:
    return await token_blocklist.exists(jti) > 0