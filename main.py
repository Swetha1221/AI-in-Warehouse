from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()

FILE = "expenses.json"

class Expense(BaseModel):
    id: int
    title: str
    amount: float
    category: str

def load_expenses():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

def save_expenses(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# ➕ Add expense
@app.post("/expenses")
def add_expense(expense: Expense):
    expenses = load_expenses()
    
    for exp in expenses:
        if exp["id"] == expense.id:
            raise HTTPException(status_code=400, detail="ID already exists")

    expenses.append(expense.dict())
    save_expenses(expenses)
    return {"message": "Expense added", "data": expense}

# 📄 Get all expenses
@app.get("/expenses", response_model=List[Expense])
def get_all():
    return load_expenses()

@app.get("/expenses/filter")
def filter_expenses(min_amount: float):
    return load_expenses()

# ✏ Update
@app.put("/expenses/{expense_id}")
def update(expense_id: int, updated: Expense):
    expenses = load_expenses()
    for i, exp in enumerate(expenses):
        if exp["id"] == expense_id:
            expenses[i] = updated.dict()
            save_expenses(expenses)
            return {"message": "Updated"}
    raise HTTPException(status_code=404, detail="Not found")

# ❌ Delete
@app.delete("/expenses/{expense_id}")
def delete(expense_id: int):
    expenses = load_expenses()
    for exp in expenses:
        if exp["id"] == expense_id:
            expenses.remove(exp)
            save_expenses(expenses)
            return {"message": "Deleted"}
    raise HTTPException(status_code=404, detail="Not found")

@app.get("/expenses/filter")
def filter_expenses(min_amount: float):
    expenses = load_expenses()
    filtered = [exp for exp in expenses if exp["amount"] >= min_amount]
    return filtered
