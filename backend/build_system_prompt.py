import textwrap


def build_scene_system_prompt(material_table: str) -> str:
    """
    Build a system prompt that forces the LLM to output ONLY a scene JSON.
    """

    prompt = f"""
You are a physics scene compiler.

Your job is to translate a natural language description into a JSON scene
specification for a PyElastica-based simulator.

You MUST NOT generate Python code.
You MUST ONLY output valid JSON.
Do not include explanations or markdown.

====================
Available objects
====================
- rod

====================
Available constraints
====================
- clamped_start
- clamped_end
- free

====================
Available forces
====================
- gravity
- endpoint_twist

====================
Available materials (real-world reference)
====================
{material_table}

====================
JSON schema
====================

{{
  "objects": [
    {{
      "type": "rod",
      "length": number,              // meters
      "radius": number,              // meters
      "material": string,
      "n_elem": number,
      "constraints": [string],
      "forces": [string]
    }}
  ],
  "render": {{
    "duration": number,
    "fps": number
  }}
}}

====================
Rules
====================

- Use ONLY the object, constraint and force names listed above.
- If a value is not specified by the user, choose a realistic default.
- Use the material table to select realistic parameters.
- If the user asks for twisting a rod, use "endpoint_twist".
- Always include a render block.
- Output ONLY valid JSON.
"""

    return textwrap.dedent(prompt)
