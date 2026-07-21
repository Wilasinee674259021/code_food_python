"""
Food Schemas (Pydantic)
แทนที่ manual input validation ใน PHP FoodController
FastAPI ตรวจ schema อัตโนมัติและคืน 422 เมื่อ field ผิด
"""
from pydantic import BaseModel, Field


class FoodCreate(BaseModel):
    """Body สำหรับ POST /foods — เทียบเท่า PHP Food::init() + validation"""
    nameTh:   str = Field(..., min_length=1, description="ชื่ออาหารภาษาไทย")
    category: str = Field(..., min_length=1, description="หมวดหมู่อาหาร")

    model_config = {
        "json_schema_extra": {
            "example": {"nameTh": "ข้าวผัด", "category": "อาหารไทย"}
        }
    }


class FoodUpdate(BaseModel):
    """Body สำหรับ PUT /foods — ต้องมี id ด้วย"""
    id:       int = Field(..., gt=0, description="Food ID")
    nameTh:   str = Field(..., min_length=1, description="ชื่ออาหารภาษาไทย")
    category: str = Field(..., min_length=1, description="หมวดหมู่อาหาร")

    model_config = {
        "json_schema_extra": {
            "example": {"id": 1, "nameTh": "ข้าวผัดกุ้ง", "category": "อาหารไทย"}
        }
    }
