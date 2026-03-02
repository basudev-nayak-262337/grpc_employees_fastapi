import grpc
from app.proto import employee_pb2
from app.proto import employee_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")
stub = employee_pb2_grpc.EmployeeServiceStub(channel)

def create_employee(data):
    request = employee_pb2.EmployeeRequest(**data)
    return stub.CreateEmployee(request)

def get_employee(emp_id: int):
    request = employee_pb2.EmployeeId(id=emp_id)
    return stub.GetEmployee(request)
def update_employee(data):
    request = employee_pb2.UpdateEmployeeRequest(**data)
    return stub.UpdateEmployee(request)

def delete_employee(emp_id: int):
    request = employee_pb2.EmployeeId(id=emp_id)
    return stub.DeleteEmployee(request)
async def get_all_employees():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = employee_pb2_grpc.EmployeeServiceStub(channel)
        response = await stub.GetAllEmployees(employee_pb2.Empty())
        return response