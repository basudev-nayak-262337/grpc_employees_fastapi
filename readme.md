Client (REST API)
        ↓
FastAPI (Async REST Gateway)
        ↓
Async gRPC Client
        ↓
Async gRPC Server
        ↓
Async SQLAlchemy 2.0
        ↓
Database (SQLite / PostgreSQL)
-------------------------------------------------------------------------------------------------------------

gRPC_Employee/
│
├── app/
│   ├── main.py
│   ├── grpc_client.py
│   ├── database.py
│   ├── models.py
│   └── proto/
│       ├── employee_pb2.py
│       ├── employee_pb2_grpc.py
│
├── grpc_server/
│   └── server.py
│
├── proto/
│   └── employee.proto
│
├── Dockerfile.fastapi
├── Dockerfile.grpc
├── docker-compose.yml
└── README.md
-------------------------------------------------------------------------------------------------------------

| Layer                 | Technology           |
| --------------------- | -------------------- |
| API Gateway           | FastAPI (Async)      |
| Service Communication | gRPC (grpc.aio)      |
| ORM                   | SQLAlchemy 2.0 Async |
| Database              | SQLite (default)     |
| Containerization      | Docker               |
| Orchestration         | Docker Compose       |


1️⃣ Create Virtual Environment

python -m venv .venv
.venv\Scripts\activate   # Windows

2️⃣ Install Dependencies

pip install fastapi uvicorn grpcio grpcio-tools sqlalchemy aiosqlite

3️⃣ Generate gRPC Code

python -m grpc_tools.protoc \
-I=proto \
--python_out=app/proto \
--grpc_python_out=app/proto \
proto/employee.proto


⚠ After generation, update:

app/proto/employee_pb2_grpc.py

import employee_pb2 as employee__pb2
from . import employee_pb2 as employee__pb2
