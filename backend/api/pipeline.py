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

        # System prompt for the prompt polisher
        self.polisher_system_prompt = """
        You are an expert Physics Simulation Engineer specializing in PyElastica (Cosserat Rod theory).
        Your goal is to refine and "polish" user prompts into clear, behavioral, and physical descriptions that can be understood by a downstream simulation generator.
        
        CRITICAL INSTRUCTION: Do NOT invent specific numerical values (e.g., "Length: 1.0m", "Young's Modulus: 5000 Pa") unless the user explicitly provides them.
        Instead, focus on describing the *behavior*, *regime*, and *mechanisms* accurately.
        
        Refine the user's input to clarify:
        1. **Locomotion/Behavior**: Describe HOW the object moves (e.g., "undulatory swimming via traveling sinusoidal waves", "tumbling under gravity").
        2. **Physical Regime**: Describe the material properties qualitatively (e.g., "highly flexible soft biological tissue", "stiff elastic rod").
           - Explicitly mention that the material must be soft enough to be actuated by internal muscles if applicable.
        3. **Environmental Constraints**: Describe the environment (e.g., "anisotropic frictional ground to enable propulsion", "fluid-like drag").
        4. **Actuation Mechanism**: Describe the forces (e.g., "internal muscle torques propagating from head to tail", "external endpoint force").
        5. **Stability Requirements**: Mention that the simulation requires a small time step (dt) and appropriate damping (nu) to remain stable.
        
        Example Output:
        "A soft, flexible Cosserat rod simulating a snake. It performs undulatory locomotion on a frictional surface using a traveling sinusoidal wave of internal torque. The material should be soft (biological tissue range) to allow significant bending. The environment requires anisotropic friction to convert lateral motion into forward thrust. Ensure the time step is small enough to handle the high-frequency muscle actuation without instability."
        
        Output ONLY the polished prompt text. Do not add conversational filler.
        """

    def polish_prompt(self, raw_prompt: str, model: str = "gpt-4o-mini") -> str:
        """
        Refines the user's raw prompt into a technical description.
        """
        logger.info(f"Polishing prompt: {raw_prompt}")

        messages = [
            {"role": "system", "content": self.polisher_system_prompt},
            {"role": "user", "content": raw_prompt}
        ]

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3,
            )
            polished = response.choices[0].message.content.strip()
            logger.info(f"Polished prompt: {polished}")
            return polished
        except Exception as e:
            logger.error(f"Error polishing prompt: {e}")
            # Fallback to original prompt if polishing fails
            return raw_prompt

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

        # Step 1: Polish the prompt
        polished_description = self.polish_prompt(
            user_description, model=model)

        logger.info(f"Generating scene for: {polished_description}")

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": polished_description}
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
