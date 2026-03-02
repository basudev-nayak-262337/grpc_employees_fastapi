from fastapi import FastAPI, HTTPException
from .grpc_client import create_employee, get_employee, update_employee,delete_employee,get_all_employees
import grpc
app = FastAPI()

@app.get("/employees/{emp_id}")
def get_emp(emp_id: int):
    try:
        response = get_employee(emp_id)
        return {
            "id": response.id,
            "name": response.name,
            "email": response.email,
            "department": response.department,
        }
    except grpc.RpcError:
        raise HTTPException(status_code=404, detail="Employee not found")

@app.post("/employees/")
def create_emp(emp: dict):
    response = create_employee(emp)
    return {
        "id": response.id,
        "name": response.name,
        "email": response.email,
        "department": response.department,
    }
@app.put("/employees/{emp_id}")
def update_emp(emp_id: int, emp: dict):
    try:
        emp["id"] = emp_id
        response = update_employee(emp)

        return {
            "id": response.id,
            "name": response.name,
            "email": response.email,
            "department": response.department,
        }
    except grpc.RpcError:
        raise HTTPException(status_code=404, detail="Employee not found")
@app.delete("/employees/{emp_id}")
def delete_emp(emp_id: int):
    try:
        response = delete_employee(emp_id)
        return {"message": response.message}
    except grpc.RpcError:
        raise HTTPException(status_code=404, detail="Employee not found")
@app.get("/employees/")
async def get_all():
    response = await get_all_employees()
    return [
        {
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "department": emp.department,
        }
        for emp in response.employees
    ]