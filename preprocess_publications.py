import json
import re
from collections import defaultdict

def filter_publications(input_file, output_file):
    """Filter top 4 Instagram + top 4 Facebook posts per campus"""
    
    # Read all publications
    publications_data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                publications_data.append(json.loads(line))
    
    # Group by campus and platform
    campus_platform_posts = defaultdict(lambda: defaultdict(list))
    
    for pub in publications_data:
        account = pub.get('ACCOUNT', '')
        social_network = pub.get('SOCIAL_NETWORK', '').lower()
        
        # Extract campus ID
        match = re.search(r'Campus\s+(\w+)\s+\[', account, re.IGNORECASE)
        
        if match:
            campus_id = match.group(1).upper()
            interactions = pub.get('INTERACCIONES_GENERAL__SUM', 0) or 0
            alcance = pub.get('ALCANCE_GENERAL__SUM', 0) or 0
            engagement_score = (interactions * 10) + alcance
            
            # Only Instagram and Facebook
            if 'instagram' in social_network:
                platform = 'Instagram'
            elif 'facebook' in social_network:
                platform = 'Facebook'
            else:
                continue
            
            filtered_pub = {
                'platform': platform,
                'content': pub.get('OUTBOUND_POST', ''),
                'interacciones': interactions,
                'alcance': alcance,
                'engagement_score': engagement_score
            }
            
            campus_platform_posts[campus_id][platform.lower()].append(filtered_pub)
    
    # Get top 4 per platform per campus
    campus_grouped_output = []
    
    for campus_id, platforms in campus_platform_posts.items():
        campus_posts = []
        
        for platform, posts in platforms.items():
            sorted_posts = sorted(posts, key=lambda x: x['engagement_score'], reverse=True)
            campus_posts.extend(sorted_posts[:4])
        
        campus_grouped_output.append({
            'campus_id': campus_id,
            'publications': campus_posts
        })
    
    # Create proper JSON structure
    output = {
        'publications_by_campus': campus_grouped_output
    }
    
    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Processed {len(campus_grouped_output)} campuses")
    print(f"💾 Saved to: {output_file}")


if __name__ == "__main__":
    filter_publications(
        input_file='Todas_las_publicaciones_con_sus_metricas_1_SDMxRegion.json',
        output_file='publicaciones_estructurado.json'
    )