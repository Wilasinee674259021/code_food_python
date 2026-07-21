"""
Recipe Schemas (Pydantic)
แทนที่ manual input validation ใน PHP RecipeController
"""
from pydantic import BaseModel, Field


class RecipeCreate(BaseModel):
    """Body สำหรับ POST /recipes"""
    food_id:    int   = Field(..., gt=0,  description="Food ID ที่ Recipe นี้สังกัด")
    recipeName: str   = Field(..., min_length=1, description="ชื่อวัตถุดิบ/ขั้นตอน")
    quantity:   float = Field(..., gt=0,  description="ปริมาณ (ต้องมากกว่า 0)")
    unitName:   str   = Field(..., min_length=1, description="หน่วย เช่น กรัม, ช้อน")

    model_config = {
        "json_schema_extra": {
            "example": {
                "food_id": 1, "recipeName": "กระเทียม",
                "quantity": 5, "unitName": "กลีบ"
            }
        }
    }


class RecipeUpdate(BaseModel):
    """Body สำหรับ PUT /recipes — ต้องมี id ด้วย"""
    id:         int   = Field(..., gt=0, description="Recipe ID")
    recipeName: str   = Field(..., min_length=1)
    quantity:   float = Field(..., gt=0)
    unitName:   str   = Field(..., min_length=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1, "recipeName": "กระเทียมสับ",
                "quantity": 8, "unitName": "กลีบ"
            }
        }
    }
