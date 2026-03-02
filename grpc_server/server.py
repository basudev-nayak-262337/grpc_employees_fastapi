



# python -m grpc_tools.protoc -I=proto --python_out=. --grpc_python_out=. proto/employee.proto
# important  --python_out should be in app folder so give proper path also

import grpc
from concurrent import futures
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.proto import employee_pb2
from app.proto import employee_pb2_grpc
from app.database import  engine
from app.database import AsyncSessionLocal
import asyncio
from grpc import aio
from app.models import Base, Employee
from sqlalchemy import select
from app.database import engine

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)






class EmployeeService(employee_pb2_grpc.EmployeeServiceServicer):

    async def CreateEmployee(self, request, context):
        async with AsyncSessionLocal() as db:
            employee = Employee(
                name=request.name,
                email=request.email,
                department=request.department,
            )

            db.add(employee)
            await db.commit()
            await db.refresh(employee)

            return employee_pb2.EmployeeResponse(
                id=employee.id,
                name=employee.name,
                email=employee.email,
                department=employee.department,
            )

    def GetEmployee(self, request, context):
        db = SessionLocal()
        employee = db.query(Employee).filter(Employee.id == request.id).first()

        if not employee:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Employee not found")
            return employee_pb2.EmployeeResponse()

        return employee_pb2.EmployeeResponse(
            id=employee.id,
            name=employee.name,
            email=employee.email,
            department=employee.department
        )
    def UpdateEmployee(self, request, context):
        db = SessionLocal()
        employee = db.query(Employee).filter(Employee.id == request.id).first()

        if not employee:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Employee not found")
            return employee_pb2.EmployeeResponse()

        employee.name = request.name
        employee.email = request.email
        employee.department = request.department

        db.commit()
        db.refresh(employee)

        return employee_pb2.EmployeeResponse(
            id=employee.id,
            name=employee.name,
            email=employee.email,
            department=employee.department,
        )
    def DeleteEmployee(self, request, context):
        db = SessionLocal()
        employee = db.query(Employee).filter(Employee.id == request.id).first()

        if not employee:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Employee not found")
            return employee_pb2.DeleteResponse()

        db.delete(employee)
        db.commit()

        return employee_pb2.DeleteResponse(message="Employee deleted successfully")
    
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
    await create_tables()   # 👈 ADD THIS

    server = grpc.aio.server()
    employee_pb2_grpc.add_EmployeeServiceServicer_to_server(
        EmployeeService(), server
    )

    server.add_insecure_port("[::]:50051")
    await server.start()
    print("🚀 Async gRPC Server running on port 50051")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
