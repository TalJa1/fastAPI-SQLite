from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from database import SessionLocal, AsyncSession, get_db
from models.Employee import Employee, EmployeeCreate, EmployeeRead, EmployeeUpdate

router = APIRouter()


@router.get("/employees/", status_code=200, response_model=dict)
async def get_employees(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Employee))
        employees = result.scalars().all()

        # Convert SQLAlchemy model instances to Pydantic model instances
        employees_data = [
            EmployeeRead.model_validate(employee) for employee in employees
        ]

        return {
            "message": "Employees retrieved successfully",
            "data": employees_data,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving employees: {str(e)}"
        )


@router.get("/employees/{employee_id}", status_code=200, response_model=dict)
async def get_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Employee).where(Employee.employee_id == employee_id)
    )
    employee = result.scalars().first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee_data = EmployeeRead.model_validate(employee)

    return {
        "message": "Employee retrieved successfully",
        "data": employee_data,
    }


@router.post("/employees/", status_code=201, response_model=dict)
async def create_employee(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Create a new Employee instance using the data from the EmployeeCreate Pydantic model
        new_employee = Employee(
            first_name=employee.first_name,
            last_name=employee.last_name,
            position=employee.position,
            hire_date=employee.hire_date,
            salary=employee.salary,
        )

        # Add the new employee to the database session
        db.add(new_employee)
        await db.commit()
        await db.refresh(new_employee)

        # Convert the new employee to a Pydantic model instance
        employee_data = EmployeeRead.model_validate(new_employee)

        return {
            "message": "Employee created successfully",
            "data": employee_data,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating employee: {str(e)}"
        )


@router.put("/employees/{employee_id}", status_code=200, response_model=dict)
async def update_employee(
    employee_id: int, employee: EmployeeUpdate, db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(Employee).where(Employee.employee_id == employee_id)
        )
        existing_employee = result.scalars().first()

        if not existing_employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        # Update the existing employee with the new data
        existing_employee.first_name = employee.first_name
        existing_employee.last_name = employee.last_name
        existing_employee.position = employee.position
        existing_employee.hire_date = employee.hire_date
        existing_employee.salary = employee.salary

        await db.commit()
        await db.refresh(existing_employee)

        # Convert the updated employee to a Pydantic model instance
        employee_data = EmployeeRead.model_validate(existing_employee)

        return {
            "message": "Employee updated successfully",
            "data": employee_data,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating employee: {str(e)}"
        )


@router.delete("/employees/{employee_id}", status_code=200, response_model=dict)
async def remove_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Employee).where(Employee.employee_id == employee_id)
    )
    employee = result.scalars().first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    await db.delete(employee)
    await db.commit()

    # Verify if the employee was successfully removed
    result = await db.execute(
        select(Employee).where(Employee.employee_id == employee_id)
    )
    removed_employee = result.scalars().first()

    if removed_employee:
        return {"message": f"Failed to remove employee with employee id {employee_id}"}

    return {"message": f"Employee removed successfully with employee id {employee_id}"}
