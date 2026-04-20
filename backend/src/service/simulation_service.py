import asyncio
import random

from faker import Faker

from backend.src.model.plant import Plant
from backend.src.model.plant_category import PlantCategory
from backend.src.model.plant_location import PlantLocation
from backend.src.repository.plant_repository import plant_repository

fake = Faker()

class SimulationService:
    def __init__(self):
        self.running = False
        self._task = None
        self._connections: set = set()

    def register(self, ws):
        self._connections.add(ws)

    def unregister(self, ws):
        self._connections.discard(ws)

    async def _broadcast(self, message: str):
        dead = set()
        for ws in self._connections:
            try:
                await ws.send_text(message)
            except Exception:
                dead.add(ws)
        self._connections -= dead

    async def run_loop(self):
        while self.running:
            print(f"[sim] loop tick, running={self.running}")
            try:
                date_planted = fake.date_between(start_date='-30y', end_date='today')
                new_plant = Plant(
                    id=0,
                    name=fake.first_name() + ' ' + random.choice(['Fern', 'Magnolia', 'Oak', 'Maple', 'Bloom', 'Vine']),
                    latin_name=fake.last_name().lower() + "us " + fake.last_name().lower() + "is",
                    category=random.choice([t for t in list(PlantCategory) if t != PlantCategory.ALL ]),
                    location=random.choice(list(PlantLocation)),
                    date_planted = date_planted,
                    watering_schedule=random.randint(1,14),
                    photos=[],
                    last_watered=fake.date_between(start_date=date_planted, end_date='today'),
                    notes=fake.text(),
                )
                saved = plant_repository.save(new_plant)
                print(f"[sim] added plant #{saved.id}: {saved.name}")
                await self._broadcast(f'{{"event":"plant_added", "id":{saved.id}}}')
            except Exception as e:
                print(f"[sim] ERROR: {e}")
            await asyncio.sleep(1)

    def start(self):
        if not self.running:
            self.running = True
            self._task = asyncio.create_task(self.run_loop())
            print("[sim] simulation started")
    def stop(self):
        self.running = False
        if self._task:
            self._task.cancel()
            self._task = None
        print("[sim] simulation stopped")

simulation_service = SimulationService()