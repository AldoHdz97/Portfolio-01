from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Dict, Any
from enum import Enum
import re

######################CAMPUS NORMALIZATION UTILS##########################

CAMPUS_MAPPING = {
    'MTY': 'Monterrey',
    'PUE': 'Puebla',
    'GDL': 'Guadalajara',
    'CDJ': 'Ciudad Juárez',
    'TOL': 'Toluca',
    'CCM': 'Ciudad de México',
    'CEM': 'Estado de México',
    'QRO': 'Querétaro',
    'CHI': 'Chihuahua',
    'SIN': 'Sinaloa',
    'AGS': 'Aguascalientes',
    'COB': 'Ciudad Obregón',
    'LEO': 'León',
    'LAG': 'Laguna',
    'SON': 'Sonora',
    'HGO': 'Hidalgo',
    'SLP': 'San Luis Potosí',
    'CVA': 'Cuernavaca',
    'CSF': 'Santa Fe',
    'SAL': 'Saltillo',
}

class CampusID(str, Enum):
    MTY = "MTY"
    PUE = "PUE"
    GDL = "GDL"
    CDJ = "CDJ"
    TOL = "TOL"
    CCM = "CCM"
    CEM = "CEM"
    QRO = "QRO"
    CHI = "CHI"
    SIN = "SIN"
    AGS = "AGS"
    COB = "COB"
    LEO = "LEO"
    LAG = "LAG"
    SON = "SON"
    HGO = "HGO"
    SLP = "SLP"
    CVA = "CVA"
    CSF = "CSF"
    SAL = "SAL"

# ============================================================================
# PUBLICATIONS DATA STRUCTURE
# ============================================================================

class Publication(BaseModel):

    platform: str = Field(
        ..., 
        description="Social media platform: Instagram or Facebook"
    )
    content: str = Field(
        ..., 
        description="The actual text/description of the post"
    )
    interacciones: int = Field(
        ..., 
        description="Total interactions (likes + comments + shares + reactions) for this post"
    )
    alcance: int = Field(
        ..., 
        description="Total reach - number of unique users who saw this post"
    )
    engagement_score: int = Field(
        ..., 
        description="Calculated engagement metric: (interacciones × 10) + alcance"
    )
    
    class Config:
        extra = 'ignore'

class CampusPublications(BaseModel):
    """Publications for one campus - up to 8 posts (4 Instagram + 4 Facebook)"""
    campus_id: CampusID = Field(
        ..., 
        description="Campus identifier - must be one of the 20 valid campus codes"
    )
    publications: List[Publication] = Field(
        ..., 
        description="List of top publications for this campus (max 8: 4 Instagram + 4 Facebook)"
    )

class CampusInsight(BaseModel):
    campus_id: CampusID = Field(description="Campus ID (e.g., MTY, GDL)")
    campus_name: str = Field(description="Campus full name")
    insight: str = Field(description="Complete insight paragraph in Spanish")
