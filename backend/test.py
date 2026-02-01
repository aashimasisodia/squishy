import os
import json
from backend.pipeline import SceneGeneratorPipeline

# 🌸 Set this in your environment:
# export KEYWORDSAI_API_KEY="your-keywordsai-api-key"

def test_pipeline():
    print("Initializing pipeline...")
    pipeline = SceneGeneratorPipeline()
    
    prompt = "A copper rod fixed at both ends, 2 meters long, with radius 5cm."
    print(f"Testing with prompt: '{prompt}'")
    
    try:
        scene = pipeline.generate_scene(prompt)
        print("\n✅ Success! Generated Scene JSON:")
        print(json.dumps(scene, indent=2))
        
        # Validation checks
        assert "objects" in scene
        assert len(scene["objects"]) > 0
        assert scene["objects"][0]["material"] == "copper"
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_pipeline()
