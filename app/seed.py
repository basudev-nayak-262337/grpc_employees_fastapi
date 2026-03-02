from app.database import SessionLocal, engine
from app.models import Base, Employee

# Create tables
Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()

    employees = [
        Employee(name="Basudev Nayak", email="basu@gmail.com", department="Engineering"),
        Employee(name="Rohit Sharma", email="rohit@gmail.com", department="HR"),
        Employee(name="Anjali Singh", email="anjali@gmail.com", department="Finance"),
        Employee(name="Priya Das", email="priya@gmail.com", department="Marketing"),
    ]

    db.add_all(employees)
    db.commit()

    print("Sample employees inserted successfully!")

    db.close()

if __name__ == "__main__":
    seed()