from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import SensorData, engine
from datetime import datetime, timezone

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Dummy data example
dummy_data = SensorData(
    timestamp=datetime.now(timezone.utc),
    temperature=45,  # Example temperature value
    soil_moisture=25  # Example soil moisture value
)

# Add data to session and commit to database
db.add(dummy_data)
db.commit()

# Close the session
db.close()
