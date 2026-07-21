"""
main.py — FastAPI Application Entry Point
เทียบเท่า endpoints/foods.php + endpoints/recipes.php (ส่วน CORS + entry)
รัน: uvicorn main:app --reload
Docs: http://localhost:8000/docs
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from routers import foods, recipes

# ---- App Instance ----
app = FastAPI(
    title="Food Recipe API",
    description="REST API สำหรับ Food & Recipe Management System\n\n"
                "เทียบเท่า PHP PDO API ที่เขียนด้วย **FastAPI + PyMySQL**",
    version="1.0.0",
)

# ---- CORS Middleware ----
# เทียบเท่า header("Access-Control-Allow-Origin: *") ใน PHP endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,
)

# ---- Exception Handlers ----

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    แปลง Pydantic validation error → { success: false, error: "..." }
    เทียบเท่า Response::error(..., 422) ใน PHP FoodController
    """
    errors = exc.errors()
    msg = errors[0]["msg"] if errors else "Validation error"
    return JSONResponse(
        status_code=422,
        content={"success": False, "error": msg},
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """จับ ValueError จาก Model._validate()"""
    return JSONResponse(
        status_code=422,
        content={"success": False, "error": str(exc)},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """จับ error ที่ไม่คาดคิด — ซ่อน detail ใน production"""
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"},
    )

# ---- Include Routers ----
# เทียบเท่า require_once '../controllers/FoodController.php' ใน PHP endpoints

app.include_router(
    foods.router,
    prefix="/foods",
    tags=["Foods"],
)

app.include_router(
    recipes.router,
    prefix="/recipes",
    tags=["Recipes"],
)

# ---- Health Check ----
@app.get("/", tags=["Health"])
def root():
    return {"message": "Food Recipe API is running", "docs": "/docs"}
