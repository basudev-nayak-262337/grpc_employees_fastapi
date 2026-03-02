import asyncio
import grpc
from grpc import aio

from app.proto import employee_pb2
from app.proto import employee_pb2_grpc
from app.database import AsyncSessionLocal
from app.models import Employee
from sqlalchemy import select

class EmployeeService(employee_pb2_grpc.EmployeeServiceServicer):

    async def GetAllEmployees(self, request, context):
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(Employee))
            employees = result.scalars().all()

            response_list = [
                employee_pb2.EmployeeResponse(
                    id=e.id,
                    name=e.name,
                    email=e.email,
                    department=e.department,
                )
                for e in employees
            ]

            return employee_pb2.EmployeeList(employees=response_list)

async def serve():
    server = aio.server()
    employee_pb2_grpc.add_EmployeeServiceServicer_to_server(
        EmployeeService(), server
    )

    server.add_insecure_port("[::]:50051")
    await server.start()
    print("🚀 Async gRPC Server running on port 50051")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())