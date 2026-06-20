"""
image_analyzer.py — Module C: Per-Image VLM Probe.

Analyzes a single image independently using a Vision-Language Model (VLM).
Extracts raw visual observations (object, part, damage type, image quality)
without making final adjudication decisions.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

@dataclass
class ImageObservation:
    """Structured raw visual observations from a single image."""
    image_path: str
    visible_object: str
    object_part: str
    issue_type: str
    quality_issues: List[str] = field(default_factory=list)
    is_original: bool = True
    text_overlay_present: bool = False
    raw_severity_observation: str = "unknown"


class ImageAnalyzer:
    """Probes a single image to extract visual evidence."""

    def __init__(self, model_client=None):
        """
        Initializes the image analyzer.
        
        Args:
            model_client: The initialized VLM client (e.g., OpenAI, Anthropic, Gemini).
                          If None, operates in mock/stub mode for testing.
        """
        self.model_client = model_client

    def _build_prompt(self, claim_context: dict) -> str:
        """Constructs the structured prompt for the VLM."""
        return f"""
        Analyze this image for a damage claim review.
        Context: The user claims {claim_context.get('issue_hint', 'damage')} on a {claim_context.get('claim_object', 'object')} ({claim_context.get('claimed_parts', 'unknown part')}).
        
        Please identify the following fields in JSON format:
        - "visible_object": What object is clearly visible?
        - "object_part": What specific part is visible?
        - "issue_type": Is there visible damage? If so, what type? You MUST choose EXACTLY ONE value from: ["dent", "scratch", "crack", "glass_shatter", "broken_part", "missing_part", "torn_packaging", "crushed_packaging", "water_damage", "stain", "none", "unknown"]. Do not use any other value.
        - "quality_issues": List of any image quality issues (e.g., blurry_image, damage_not_visible, cropped_or_obstructed, wrong_angle)
        - "is_original": Boolean, does the image appear to be an original photo?
        - "text_overlay_present": Boolean, is there any instruction text overlaying the image?
        - "raw_severity_observation": What is the severity of the visible damage? You MUST choose EXACTLY ONE value from: ["none", "low", "medium", "high", "unknown"]. Do not use any other value.

        Return ONLY a raw JSON object, no markdown blocks.
        """

    def analyze(self, image_path: str, claim_context: dict = None) -> ImageObservation:
        """
        Analyze a single image and return structured visual observations.
        
        Note: This module strictly observes the visual evidence present in the 
        image and does not cross-reference or adjudicate the claim status.
        """
        if not Path(image_path).exists():
            logger.error(f"Image not found at: {image_path}")
            return ImageObservation(
                image_path=image_path,
                visible_object="unknown",
                object_part="unknown",
                issue_type="unknown",
                quality_issues=["file_not_found"]
            )

        claim_context = claim_context or {}
        logger.debug(f"Analyzing image: {image_path}")

        if self.model_client is None:
            # Fallback/Mock mode for local testing without API keys
            logger.warning("No VLM client provided. Using mock visual observation.")
            return self._mock_analysis(image_path, claim_context)

        try:
            import json
            import PIL.Image
            import time
            import google.api_core.exceptions
            
            # Enforce rate limit for API key
            logger.info(f"Rate limiting: sleeping for 2 seconds before calling Gemini...")
            time.sleep(2)
            
            img = PIL.Image.open(image_path)
            prompt = self._build_prompt(claim_context)
            
            response = self.model_client.generate_content(
                [prompt, img],
                generation_config={"response_mime_type": "application/json"}
            )
            
            parsed = json.loads(response.text)
            
            return ImageObservation(
                image_path=image_path,
                visible_object=parsed.get("visible_object", "unknown"),
                object_part=parsed.get("object_part", "unknown"),
                issue_type=parsed.get("issue_type", "unknown"),
                quality_issues=parsed.get("quality_issues", []),
                is_original=parsed.get("is_original", True),
                text_overlay_present=parsed.get("text_overlay_present", False),
                raw_severity_observation=parsed.get("raw_severity_observation", "unknown")
            )
        except Exception as e:
            logger.error(f"Error calling VLM for image {image_path}: {e}")
            return self._mock_analysis(image_path, claim_context)

    def _mock_analysis(self, image_path: str, claim_context: dict) -> ImageObservation:
        """Mock analysis for pipeline testing."""
        # Simple heuristics for testing purposes based on file path or context
        issue = claim_context.get("issue_hint", "unknown")
        
        quality = []
        if "blurry" in image_path:
            quality.append("blurry_image")
            
        return ImageObservation(
            image_path=image_path,
            visible_object=claim_context.get("claim_object", "unknown"),
            object_part=claim_context.get("claimed_parts", ["unknown"])[0],
            issue_type=issue,
            quality_issues=quality,
            is_original=True,
            text_overlay_present=False,
            raw_severity_observation="medium"
        )
