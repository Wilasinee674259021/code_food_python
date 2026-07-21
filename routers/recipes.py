"""
Recipes Router — เทียบเท่า controllers/RecipeController.php + endpoints/recipes.php
"""
from fastapi import APIRouter, Depends, HTTPException
from psycopg2.extensions import connection as Connection

from config.database import get_db
from models.recipe import Recipe
from schemas.recipe_schema import RecipeCreate, RecipeUpdate

router = APIRouter()


# ---- GET /recipes?food_id=X ----
@router.get("/", summary="ดู Recipes ตาม food_id หรือ id")
def get_recipes(
    food_id: int | None = None,
    id: int | None = None,
    conn: Connection = Depends(get_db),
):
    """
    เทียบเท่า PHP case 'GET'
    ?food_id=X → ดู Recipes ทั้งหมดของ Food นั้น
    ?id=X      → ดู Recipe เดี่ยว
    """
    recipe = Recipe(conn)

    if food_id is not None:
        if food_id <= 0:
            raise HTTPException(status_code=422, detail="food_id must be positive")
        recipe.food_id = food_id
        return {"success": True, "data": recipe.get_all_by_food_id()}

    if id is not None:
        if id <= 0:
            raise HTTPException(status_code=422, detail="id must be positive")
        recipe.id = id
        row = recipe.get_one()
        if row is None:
            raise HTTPException(status_code=404, detail=f"Recipe id={id} not found")
        return {"success": True, "data": row}

    raise HTTPException(status_code=422, detail="Provide ?id or ?food_id")


# ---- POST /recipes ----
@router.post("/", status_code=201, summary="เพิ่ม Recipe เข้าสู่ Food")
def create_recipe(body: RecipeCreate, conn: Connection = Depends(get_db)):
    """
    เทียบเท่า PHP case 'POST' — Recipe::foodExists() + Recipe::create()
    Pydantic ตรวจ field ทั้งหมดอัตโนมัติ รวมถึง quantity > 0
    """
    recipe = Recipe(conn)
    recipe.food_id     = body.food_id
    recipe.recipe_name = body.recipeName.strip()
    recipe.quantity    = body.quantity
    recipe.unit_name   = body.unitName.strip()

    # ตรวจว่า Food มีอยู่จริง (referential integrity)
    if not recipe.food_exists():
        raise HTTPException(status_code=404, detail=f"Food id={body.food_id} not found")

    new_id = recipe.create()
    return {
        "success": True,
        "data": {
            "id":         new_id,
            "food_id":    body.food_id,
            "recipeName": body.recipeName,
            "quantity":   body.quantity,
            "unitName":   body.unitName,
            "message":    "Recipe added successfully",
        },
    }


# ---- PUT /recipes ----
@router.put("/", summary="แก้ไข Recipe")
def update_recipe(body: RecipeUpdate, conn: Connection = Depends(get_db)):
    """เทียบเท่า PHP case 'PUT' — ตรวจ getOne() ก่อน update()"""
    recipe = Recipe(conn)
    recipe.id          = body.id
    recipe.recipe_name = body.recipeName.strip()
    recipe.quantity    = body.quantity
    recipe.unit_name   = body.unitName.strip()

    # ดึง food_id เดิมจาก DB
    existing = recipe.get_one()
    if existing is None:
        raise HTTPException(status_code=404, detail=f"Recipe id={body.id} not found")
    recipe.food_id = existing["food_id"]

    updated = recipe.update()
    if not updated:
        raise HTTPException(status_code=422, detail="No changes were made")

    return {"success": True, "data": {"id": body.id, "message": "Recipe updated successfully"}}


# ---- DELETE /recipes/{recipe_id} ----
@router.delete("/{recipe_id}", summary="ลบ Recipe")
def delete_recipe(recipe_id: int, conn: Connection = Depends(get_db)):
    """เทียบเท่า PHP case 'DELETE'"""
    recipe = Recipe(conn)
    recipe.id = recipe_id

    if recipe.get_one() is None:
        raise HTTPException(status_code=404, detail=f"Recipe id={recipe_id} not found")

    recipe.delete()
    return {"success": True, "data": {"id": recipe_id, "message": "Recipe deleted successfully"}}
