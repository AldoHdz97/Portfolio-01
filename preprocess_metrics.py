import json
import re
from typing import Optional

def extract_campus_from_region(region: str) -> tuple[str, str]:
    """Extract campus ID and name from REGION field"""
    
    CAMPUS_MAPPING = {
        'MTY': 'Monterrey',
        'PUE': 'Puebla',
        'GDL': 'Guadalajara',
        'CDJ': 'Cd. Juárez',
        'TOL': 'Toluca',
        'CCM': 'Ciudad de México',
        'CEM': 'Estado de México',
        'QRO': 'Querétaro',
        'CHI': 'Chihuahua',
        'SIN': 'Sinaloa',
        'AGS': 'Aguascalientes',
        'COB': 'Cd. Obregón',
        'LEO': 'León',
        'LAG': 'Laguna',
        'SON': 'Sonora',
        'HGO': 'Hidalgo',
        'SLP': 'San Luis Potosí',
        'CVA': 'Cuernavaca',
        'CSF': 'Santa Fe',
        'SAL': 'Saltillo',
    }
    
    # Try to extract from parentheses
    match = re.search(r'\((\w+)\)', region)
    if match:
        campus_id = match.group(1).upper()
        campus_name = CAMPUS_MAPPING.get(campus_id, campus_id)
        return campus_id, campus_name
    
    # Look for campus ID codes
    region_upper = region.upper()
    for code in CAMPUS_MAPPING.keys():
        if code in region_upper:
            return code, CAMPUS_MAPPING[code]
    
    # Look for campus full names
    for code, name in CAMPUS_MAPPING.items():
        if name.lower() in region.lower():
            return code, name
    
    # Fallback
    campus_id = region[:3].upper() if len(region) >= 3 else "UNK"
    return campus_id, region


def calculate_percentage_change(current: float, previous: float) -> Optional[str]:
    """Calculate percentage change with + or - sign"""
    if previous == 0 or previous is None or current is None:
        return None
    
    change = ((current - previous) / previous) * 100
    sign = "+" if change >= 0 else ""
    return f"{sign}{change:.2f}%"


def process_metrics(current_file: str, previous_file: str, output_file: str):
    """Merge current and previous year metrics with percentage changes"""
    
    # Load current month metrics
    current_data = []
    with open(current_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                current_data.append(json.loads(line))
    
    # Load previous year metrics
    previous_data = []
    with open(previous_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                previous_data.append(json.loads(line))
    
    # Create lookup dictionary
    previous_lookup = {item['REGION']: item for item in previous_data}
    
    # Process and merge
    campuses = []
    
    for current in current_data:
        region_str = current.get('REGION', '')
        campus_id, campus_name = extract_campus_from_region(region_str)
        previous = previous_lookup.get(region_str, None)
        
        # Current metrics
        curr_comentarios = current.get('POST_COMMENTS__SUM', 0)
        curr_alcance = current.get('ALCANCE_TOTAL', 0.0)
        curr_publicaciones = current.get('VOLUMEN_DE_PUBLICACIONES', 0)
        curr_interacciones = current.get('INTERACCIONES_TOTALES', 0)
        
        # Previous metrics
        if previous:
            prev_comentarios = previous.get('POST_COMMENTS__SUM', 0)
            prev_alcance = previous.get('ALCANCE_TOTAL', 0.0)
            prev_publicaciones = previous.get('VOLUMEN_DE_PUBLICACIONES', 0)
            prev_interacciones = previous.get('INTERACCIONES_TOTALES', 0)
        else:
            prev_comentarios = 0
            prev_alcance = 0.0
            prev_publicaciones = 0
            prev_interacciones = 0
        
        # Calculate percentage changes
        cambios = {
            'comentarios': calculate_percentage_change(curr_comentarios, prev_comentarios),
            'alcance': calculate_percentage_change(curr_alcance, prev_alcance),
            'publicaciones': calculate_percentage_change(curr_publicaciones, prev_publicaciones),
            'interacciones': calculate_percentage_change(curr_interacciones, prev_interacciones)
        }
        
        # Create campus object
        campus = {
            'campus_id': campus_id,
            'campus_name': campus_name,
            'current_month': {
                'POST_COMMENTS__SUM': curr_comentarios,
                'ALCANCE_TOTAL': curr_alcance,
                'VOLUMEN_DE_PUBLICACIONES': curr_publicaciones,
                'INTERACCIONES_TOTALES': curr_interacciones
            },
            'previous_year_month': {
                'POST_COMMENTS__SUM': prev_comentarios,
                'ALCANCE_TOTAL': prev_alcance,
                'VOLUMEN_DE_PUBLICACIONES': prev_publicaciones,
                'INTERACCIONES_TOTALES': prev_interacciones
            },
            'cambios_porcentuales': cambios
        }
        
        campuses.append(campus)
    
    # Create output structure
    output = {
        'campuses': campuses
    }
    
    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Processed {len(campuses)} campuses with percentage changes")
    print(f"💾 Saved to: {output_file}")
    
    return output


if __name__ == "__main__":
    process_metrics(
        current_file='Mes_Actual_2_SDMxRegion.json',
        previous_file='Mes_del_A_o_anterior_3_SDMxRegion.json',
        output_file='metrics_estructurado.json'
    )

    