from fastapi import Request, HTTPException


def get_database(request: Request):
    """
    دریافت اتصال دیتابیس Cloudflare D1
    """

    env = request.scope.get("env")

    if env is None:
        raise HTTPException(
            status_code=503,
            detail="Worker environment is unavailable"
        )

    db = getattr(env, "DB", None)

    if db is None:
        raise HTTPException(
            status_code=503,
            detail="Database is not configured"
        )

    return db


async def execute_query(request: Request, query: str, *params):
    """
    اجرای دستورات SQL
    """

    db = get_database(request)

    statement = db.prepare(query)

    if params:
        statement = statement.bind(*params)

    return await statement.run()


async def fetch_all(request: Request, query: str, *params):
    """
    دریافت چند رکورد
    """

    result = await execute_query(
        request,
        query,
        *params
    )

    data = result.to_py()

    return data.get("results", [])


async def fetch_one(request: Request, query: str, *params):
    """
    دریافت یک رکورد
    """

    rows = await fetch_all(
        request,
        query,
        *params
    )

    return rows[0] if rows else None
