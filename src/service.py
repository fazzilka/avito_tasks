from sqlalchemy.ext.asyncio import AsyncSession

from src.database.crud import add_slug_to_database, get_long_url_by_slug_from_database
from src.exception import NoLongUrlFoundError, SlugAlreadyExistsError
from src.shortener import generate_random_slug


async def generate_short_url(long_url: str, session: AsyncSession) -> str:
    async def _generate_slug_and_add_to_db() -> str:
        slug = generate_random_slug()
        await add_slug_to_database(slug, long_url, session)
        return slug

    for attempt in range(5):
        try:
            return await _generate_slug_and_add_to_db()
        except SlugAlreadyExistsError:
            if attempt == 4:
                raise SlugAlreadyExistsError
            continue


async def get_url_by_slug(slug: str, session: AsyncSession) -> str:
    long_url = await get_long_url_by_slug_from_database(slug, session)
    if long_url is None:
        raise NoLongUrlFoundError(slug)
    return long_url
