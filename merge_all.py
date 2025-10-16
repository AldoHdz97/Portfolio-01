import json

def merge_all_data(metrics_file: str, publications_file: str, sdm_file: str, output_file: str):
    """Merge all preprocessed data into unified campus insights structure"""
    
    # Load all files
    with open(metrics_file, 'r', encoding='utf-8') as f:
        metrics_data = json.load(f)
    
    with open(publications_file, 'r', encoding='utf-8') as f:
        publications_data = json.load(f)
    
    with open(sdm_file, 'r', encoding='utf-8') as f:
        sdm_data = json.load(f)
    
    # Create lookup dictionaries by campus_id
    publications_lookup = {
        item['campus_id']: item['publications'] 
        for item in publications_data['publications_by_campus']
    }
    
    sdm_lookup = {
        item['campus_id']: {
            'facebook': item['facebook'],
            'twitter': item['twitter'],
            'instagram': item['instagram'],
            'totales': item['totales']
        }
        for item in sdm_data['campuses']
    }
    
    # Merge all data by campus
    campus_insights = []
    
    for campus in metrics_data['campuses']:
        campus_id = campus['campus_id']
        
        # Build unified campus object
        campus_unified = {
            'campus_id': campus_id,
            'campus_name': campus['campus_name'],
            'metrics': {
                'current_month': campus['current_month'],
                'previous_year_month': campus['previous_year_month'],
                'cambios_porcentuales': campus['cambios_porcentuales']
            },
            'publications': publications_lookup.get(campus_id, []),
            'scores': sdm_lookup.get(campus_id, {
                'facebook': {},
                'twitter': {},
                'instagram': {},
                'totales': {}
            })
        }
        
        campus_insights.append(campus_unified)
    
    # Create final output
    output = {
        'campus_insights': campus_insights
    }
    
    # Save unified JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Unified data for {len(campus_insights)} campuses")
    print(f"💾 Saved to: {output_file}")
    
    return output


if __name__ == "__main__":
    merge_all_data(
        metrics_file='metrics_estructurado.json',
        publications_file='publicaciones_estructurado.json',
        sdm_file='sdm_estructurado.json',
        output_file='unified_campus_data.json'
    )