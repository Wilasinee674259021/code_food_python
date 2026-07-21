"""
Foods Router — เทียบเท่า controllers/FoodController.php + endpoints/foods.php
FastAPI APIRouter แทนที่ switch($method) ใน PHP
HTTPException แทน Response::notFound() / Response::error()
"""
from fastapi import APIRouter, Depends, HTTPException
from psycopg2.extensions import connection as Connection

from config.database import get_db
from models.food import Food
from schemas.food_schema import FoodCreate, FoodUpdate

router = APIRouter()


# ---- GET /foods ----
@router.get("/", summary="ดู Food ทั้งหมด")
def get_all_foods(conn: Connection = Depends(get_db)):
    """เทียบเท่า PHP case 'GET' ไม่มี ?id — Food::getAll()"""
    food = Food(conn)
    return {"success": True, "data": food.get_all()}


# ---- GET /foods/{food_id} ----
@router.get("/{food_id}", summary="ดู Food พร้อม recipeList")
def get_food(food_id: int, conn: Connection = Depends(get_db)):
    """
    เทียบเท่า PHP case 'GET' มี ?id — Food::display()
    คืน Food พร้อม recipeList ทั้งหมด (LEFT JOIN)
    """
    food = Food(conn)
    food.id = food_id
    result = food.display()
    if result is None:
        raise HTTPException(status_code=404, detail=f"Food id={food_id} not found")
    return {"success": True, "data": result}


# ---- POST /foods ----
@router.post("/", status_code=201, summary="สร้าง Food ใหม่")
def create_food(body: FoodCreate, conn: Connection = Depends(get_db)):
    """
    เทียบเท่า PHP case 'POST' — Food::init() + Food::create()
    Pydantic ตรวจ nameTh/category อัตโนมัติ (แทน manual validation ใน PHP)
    """
    food = Food(conn)
    food.init(body.nameTh, body.category)
    new_id = food.create()
    return {
        "success": True,
        "data": {
            "id":       new_id,
            "nameTh":   body.nameTh,
            "category": body.category,
            "message":  "Food created successfully",
        },
    }


# ---- PUT /foods ----
@router.put("/", summary="แก้ไข Food")
def update_food(body: FoodUpdate, conn: Connection = Depends(get_db)):
    """เทียบเท่า PHP case 'PUT' — ตรวจ exists() ก่อน update()"""
    food = Food(conn)
    food.id       = body.id
    food.name_th  = body.nameTh
    food.category = body.category

    if not food.exists():
        raise HTTPException(status_code=404, detail=f"Food id={body.id} not found")

    updated = food.update()
    if not updated:
        raise HTTPException(status_code=422, detail="No changes were made")

    return {"success": True, "data": {"id": body.id, "message": "Food updated successfully"}}


# ---- DELETE /foods/{food_id} ----
@router.delete("/{food_id}", summary="ลบ Food (CASCADE ลบ Recipes ด้วย)")
def delete_food(food_id: int, conn: Connection = Depends(get_db)):
    """เทียบเท่า PHP case 'DELETE' — ตรวจ exists() ก่อน delete()"""
    food = Food(conn)
    food.id = food_id

    if not food.exists():
        raise HTTPException(status_code=404, detail=f"Food id={food_id} not found")

    food.delete()
    return {"success": True, "data": {"id": food_id, "message": "Food deleted successfully"}}
