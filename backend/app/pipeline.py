import os
import json
import logging
from typing import Optional, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

from .build_system_prompt import build_scene_system_prompt
from .materials import get_material_table_str
from .scene_to_code import generate_script_from_scene

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SceneGeneratorPipeline:
    """
    Pipeline to generate PyElastica scene specifications (JSON) using Keywords AI.
    """

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.keywordsai.co/api/"):
        """
        Initialize the pipeline with Keywords AI credentials.

        Args:
            api_key: Keywords AI API Key. Defaults to KEYWORDSAI_API_KEY env var.
            base_url: Keywords AI API Base URL.
        """
        self.api_key = os.environ.get("KEYWORDSAI_API_KEY")
        if not self.api_key:
            logger.warning(
                "KEYWORDSAI_API_KEY not found in environment variables.")

        # Keywords AI is OpenAI-compatible
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=base_url
        )

        # Pre-build the system prompt with materials
        self.material_table = get_material_table_str()
        self.system_prompt = build_scene_system_prompt(self.material_table)

    def generate_scene(self, user_description: str, model: str = "gpt-4o-mini") -> Dict[str, Any]:
        """
        Generates a JSON scene specification from a natural language description.

        Args:
            user_description: The user's request (e.g., "A rubber rod falling under gravity")
            model: The model to use via Keywords AI (default: gpt-4o-mini)

        Returns:
            A dictionary containing the scene specification.
        """
        if not self.client.api_key:
            raise ValueError(
                "API Key is missing. Please set KEYWORDSAI_API_KEY.")

        logger.info(f"Generating scene for: {user_description}")

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_description}
        ]

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                # Enforce JSON mode if supported
                response_format={"type": "json_object"},
                temperature=0.2,  # Low temperature for consistent JSON
            )

            content = response.choices[0].message.content
            logger.debug(f"Raw response: {content}")

            # Parse JSON
            scene_data = json.loads(content)
            return scene_data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise
        except Exception as e:
            logger.error(f"Error communicating with Keywords AI: {e}")
            raise

    def generate_python_script(self, scene_data: Dict[str, Any]) -> str:
        """
        Converts a JSON scene specification into a PyElastica Python script.
        """
        return generate_script_from_scene(scene_data)
