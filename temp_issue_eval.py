import os
import csv
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location("image_analyzer", "code/pipeline/image_analyzer.py")
image_analyzer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(image_analyzer)
ImageAnalyzer = image_analyzer.ImageAnalyzer

import google.generativeai as genai
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
analyzer = ImageAnalyzer()
analyzer.model_client = genai.GenerativeModel('gemini-1.5-pro')

truth = {r['user_id']: r for r in csv.DictReader(open('dataset/sample_claims.csv', encoding='utf-8'))}
errors = ['user_002', 'user_007', 'user_005', 'user_006', 'user_008', 'user_018', 'user_020', 'user_031', 'user_032', 'user_033', 'user_034']

print("Starting evaluation...")
for uid in errors:
    t = truth[uid]
    case_dir = uid.replace('user_', 'case_')
    images = list(Path(f'dataset/images/sample/{case_dir}').glob('*.jpg'))
    if not images: continue
    
    ctx = {'issue_hint': 'unknown', 'claim_object': t['object_part']}
    try:
        import time
        time.sleep(4)
        obs = analyzer.analyze(str(images[0]), ctx)
        print(f'{uid}: expected={t["issue_type"]}, predicted={obs.issue_type}')
    except Exception as e:
        print(f'{uid}: Error: {e}')
