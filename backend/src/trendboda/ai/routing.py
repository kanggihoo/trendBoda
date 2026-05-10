from dataclasses import dataclass

from trendboda.ai.types import AIFeature, AIModel

OPENROUTER_MODEL_IDS: dict[AIModel, str] = {
    AIModel.OPENAI_GPT_4_1_NANO: "openai/gpt-4.1-nano",
    AIModel.GOOGLE_GEMINI_2_5_FLASH_LITE: "google/gemini-2.5-flash-lite",
}


@dataclass(frozen=True)
class AIRoute:
    feature: AIFeature
    models: list[AIModel]

    @property
    def openrouter_models(self) -> list[str]:
        return [OPENROUTER_MODEL_IDS[model] for model in self.models]


def default_ai_routes() -> dict[AIFeature, AIRoute]:
    return {
        AIFeature.GEEKNEWS_SUMMARY: AIRoute(
            feature=AIFeature.GEEKNEWS_SUMMARY,
            models=[
                AIModel.OPENAI_GPT_4_1_NANO,
                AIModel.GOOGLE_GEMINI_2_5_FLASH_LITE,
            ],
        )
    }
