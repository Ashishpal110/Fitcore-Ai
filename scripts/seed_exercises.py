"""FitCore Exercise Taxonomy & Catalog Seeding CLI Script."""

import asyncio
import os
import sys

# Ensure backend package is in python search path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend"))

from app.core.database import AsyncSessionLocal
from app.seeds.exercise_seeder import seed_exercises


async def main() -> None:
    print("==================================================")
    print("FitCore Database Seeder: Exercise Taxonomy & Catalog")
    print("==================================================")
    async with AsyncSessionLocal() as session:
        try:
            results = await seed_exercises(session)
            print(f"Taxonomy Categories: {results['taxonomy']['categories']}")
            print(f"Training Modalities: {results['taxonomy']['modalities']}")
            print(f"Equipment Items:     {results['taxonomy']['equipment']}")
            print(f"Muscles:             {results['taxonomy']['muscles']}")
            print(f"Exercise Locations:  {results['taxonomy']['locations']}")
            print("--------------------------------------------------")
            print(f"Exercises Created:   {results['created_exercises']}")
            print(f"Exercises Updated:   {results['updated_exercises']}")
            print(f"Total Database Items:{results['total_exercises']}")
            print("==================================================")
            print("Seeding completed successfully!")
        except Exception as e:
            print(f"Error during seeding: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
