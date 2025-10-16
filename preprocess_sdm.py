import csv
import json
from typing import Optional

def categorize_score(score: Optional[int]) -> Optional[str]:
    """Categorize score: deficiente, regular, satisfactorio, sobresaliente, excepcional"""
    if score is None:
        return None
    
    if score <= 75:
        return "deficiente"
    elif score <= 100:
        return "regular"
    elif score <= 120:
        return "satisfactorio"
    elif score <= 140:
        return "sobresaliente"
    else:
        return "excepcional"


def map_campus_name_to_id(campus_name: str) -> str:
    """Map campus full name to campus_id"""
    
    CAMPUS_MAPPING = {
        'Monterrey': 'MTY',
        'Puebla': 'PUE',
        'Guadalajara': 'GDL',
        'Ciudad Juárez': 'CDJ',
        'Toluca': 'TOL',
        'Ciudad de México': 'CCM',
        'Estado de México': 'CEM',
        'Querétaro': 'QRO',
        'Chihuahua': 'CHI',
        'Sinaloa': 'SIN',
        'Aguascalientes': 'AGS',
        'Ciudad Obregón': 'COB',
        'León': 'LEO',
        'Laguna': 'LAG',
        'Sonora': 'SON',
        'Hidalgo': 'HGO',
        'San Luis Potosí': 'SLP',
        'Cuernavaca': 'CVA',
        'Santa Fe': 'CSF',
        'Saltillo': 'SAL',
    }
    
    for full_name, code in CAMPUS_MAPPING.items():
        if full_name.lower() in campus_name.lower():
            return code
    
    return campus_name[:3].upper()


def normalize_score_name(score_name: str) -> str:
    """Normalize score field names"""
    mapping = {
        'visibilidad': 'visibilidad',
        'resonancia': 'resonancia',
        'permanencia': 'permanencia',
        'sentimiento': 'sentimiento',
        'salud de marca': 'salud_de_marca'
    }
    return mapping.get(score_name.lower(), score_name)


def parse_score(value: str) -> Optional[int]:
    """Parse score value, handle empty values"""
    if not value or value.lower() == 'calificaciones':
        return None
    
    try:
        return int(value.replace(',', ''))
    except ValueError:
        return None


def parse_campus_scores_csv(csv_file: str, json_file: str):
    """Parse campus performance scores from CSV to structured JSON"""
    
    campuses = []
    current_campus = None
    current_platform = None
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        for row in reader:
            if len(row) < 2:
                continue
            
            left_col = row[0].strip().lower()
            right_col = row[1].strip()
            
            # Detect campus name
            if left_col == 'campus':
                if current_campus:
                    campuses.append(current_campus)
                
                campus_name = right_col
                campus_id = map_campus_name_to_id(campus_name)
                
                current_campus = {
                    'campus_id': campus_id,
                    'campus_name': campus_name,
                    'facebook': {},
                    'twitter': {},
                    'instagram': {},
                    'totales': {}
                }
                current_platform = None
            
            # Detect platform
            elif left_col in ['facebook', 'twitter', 'instagram', 'totales']:
                current_platform = left_col
            
            # Detect score type
            elif left_col in ['visibilidad', 'resonancia', 'permanencia', 'sentimiento', 'salud de marca']:
                score_type = normalize_score_name(left_col)
                score_value = parse_score(right_col)
                category = categorize_score(score_value)
                
                if current_platform and current_campus:
                    current_campus[current_platform][score_type] = score_value
                    current_campus[current_platform][f"{score_type}_categoria"] = category
        
        if current_campus:
            campuses.append(current_campus)
    
    # Create output structure
    output = {
        'campuses': campuses
    }
    
    # Save to JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Processed {len(campuses)} campuses with categorization")
    print(f"💾 Saved to: {json_file}")
    
    return output


if __name__ == "__main__":
    parse_campus_scores_csv(
        csv_file='Regiones Unificadas - Valores.csv',
        json_file='sdm_estructurado.json'
    )