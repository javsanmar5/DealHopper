from math import sqrt

from master.models import Smartphone


def recommend_similar_smartphones(smartphone_vector, n=5):
    all_smartphones = _get_all_smartphones()
    scores = [
        (_sim_distance_content(smartphone_vector, other_vector), other_id)
        for other_id, other_vector in all_smartphones.items()
        if other_vector != smartphone_vector
    ]
    scores.sort(reverse=True) 
    
    top_smartphone_ids = [other_id for _, other_id in scores][:n]
    recommended_smartphones = Smartphone.objects.filter(id__in=top_smartphone_ids).values_list('name', flat=True).distinct()
    return recommended_smartphones

def _sim_distance_content(item1, item2):
    return 1 / (1 + sqrt(sum((a - b) ** 2 for a, b in zip(item1, item2))))

def _get_all_smartphones():
    smartphones = Smartphone.objects.all()
    smartphone_vectors = {
        smartphone.id: [
            smartphone.ram or 0,
            smartphone.screen_size or 0,
            smartphone.storage or 0,
            smartphone.battery or 0,
        ]
        for smartphone in smartphones
    }
    return smartphone_vectors
