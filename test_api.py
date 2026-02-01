import requests
import time
import sys

BASE_URL = "http://localhost:8000"


def test_pipeline():
    prompt = "a red snake slithering on the ground"
    print(f"Sending prompt: {prompt}")

    try:
        response = requests.post(
            f"{BASE_URL}/generate", json={"prompt": prompt})
        response.raise_for_status()
        data = response.json()
        print(f"Response: {data}")

        task_id = data["id"]
        print(f"Task ID: {task_id}")

        while True:
            status_res = requests.get(f"{BASE_URL}/status/{task_id}")
            status_res.raise_for_status()
            status_data = status_res.json()

            print(f"Status: {status_data}")

            if status_data["status"] == "completed":
                print("Simulation completed successfully!")
                print(f"GIF URL: {BASE_URL}/gif/{task_id}")
                print(f"Code URL: {BASE_URL}/code/{task_id}")
                break

            if status_data["status"] == "failed":
                print(f"Simulation failed: {status_data.get('error')}")
                break

            time.sleep(2)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_pipeline()
