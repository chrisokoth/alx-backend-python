import aiosqlite
import asyncio

# Async function to fetch all users
async def async_fetch_users(db_name):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All Users:")
            for row in results:
                print(row)

# Async function to fetch users older than 40
async def async_fetch_older_users(db_name):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            print("Users older than 40:")
            for row in results:
                print(row)

# Function to run both queries concurrently
async def fetch_concurrently():
    db_name = "users.db"
    await asyncio.gather(
        async_fetch_users(db_name),
        async_fetch_older_users(db_name)
    )

# Main entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
