from pydantic import BaseModel, Field, field_validator
from typing import Optional
from .GenderOptions import GenderOptions
from .DietaryFrequency import DietaryFrequency

class FormData(BaseModel):
  # Section 1: General User Data
  age: int = Field(..., gt=0, le=120, example=30)
  sex: GenderOptions
  weight_kg: float = Field(..., gt=0, le=300, example=70.5)
  height_cm: int = Field(..., gt=50, le=250, example=175)
  state: str = Field(default="", max_length=2, pattern=r"^[A-z]{2,25}$")
  city: str = Field(default="", max_length=30)
  family_medical_history: str = Field(default="", max_length=100)

  # Section 2: Dietary Habits
  fruits: DietaryFrequency
  vegetables: DietaryFrequency
  grains: DietaryFrequency
  animal_proteins: DietaryFrequency
  plant_proteins: DietaryFrequency
  dairy: DietaryFrequency
  ultra_processed_foods: DietaryFrequency
  sweets: DietaryFrequency
  water_intake_liters: float = Field(..., ge=0, le=20, example=2.5)
  special_dietary_practices: str = Field(default="", max_length=100)
  breakfast_time: str = Field(default="", max_length=5, pattern=r"^\d{1,2}:\d{2}$")
  lunch_time: str = Field(default="", max_length=5, pattern=r"^\d{1,2}:\d{2}$")
  dinner_time: str = Field(default="", max_length=5, pattern=r"^\d{1,2}:\d{2}$")
  snack_time: str = Field(default="", max_length=5, pattern=r"^\d{1,2}:\d{2}$")

  # Section 3: Symptoms
  fatigue: bool
  hair_loss: bool
  dry_skin: bool
  vision_problems: bool
  brittle_nails: bool
  appetite_changes: bool
  muscle_pain: bool
  tingling_extremities: bool
  difficulty_concentrating: bool
  other_symptoms: str = Field(default="", max_length=500)

  # Section 4: Medication
  regular_medication_use: bool
  medications_list: str = Field(default="", max_length=500)
  taking_supplements: bool
  supplements_list: str = Field(default="", max_length=500)
  frequency_dosage: str = Field(default="", max_length=100)

  # Section 5: Lifestyle
  physical_activity_frequency: str = Field(..., max_length=50)
  sleep_hours_per_night: int = Field(..., ge=0, le=24)
  perceived_stress_level: str = Field(..., max_length=50)

  # Section 6: Preferences
  favorite_foods: str = Field(default="", max_length=500)
  avoided_foods: str = Field(default="", max_length=500)
  dietary_restrictions: str = Field(default="", max_length=500)

  # Sections 7-9
  nutritional_goal: str = Field(default="", max_length=500)
  consent_given: bool
  additional_notes: str = Field(default="", max_length=1000)

  @field_validator("medications_list")
  def validate_medications(cls, v, info):
    if info.data.get("regular_medication_use") and not v.strip():
      raise ValueError("Medication list required when using regular medication")
    return v.strip()

  @field_validator("supplements_list")
  def validate_supplements(cls, v, info):
    if info.data.get("taking_supplements") and not v.strip():
      raise ValueError("Supplements list required when taking supplements")
    return v.strip()

  @field_validator("*", mode="before")
  def strip_strings(cls, v):
    if isinstance(v, str):
      return v.strip()
    return v
