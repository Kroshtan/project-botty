from pathlib import Path

from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).parent


class _Config(BaseSettings):
    version: str = "0.1.0"
    project_root: Path = PROJECT_ROOT
    resource_folder: Path = project_root.parent / "resources"

    @property
    def avatar_image_path(self):
        return self.resource_folder / "portrait.jpg"

    @property
    def embed_service_url(self):
        return "http://embed_service:8080/embed"

    @property
    def self_assignable_roles(self):
        return {
            "⭐": "VIP",
            "🌞": "Caregiver",
            "❤️": "Partner",
            "💚": "Family Member",
            "📖": "Professional",
            "💗": "Biological Mother",
        }

    @property
    def chatgpt_roles(self):
        return {"Admin"}

    @property
    def content_search_admin_roles(self):
        return {"Admin"}

    @property
    def introduction_channels(self):
        return [
            1215812458531262544,
            1222655667488296960,
        ]

    @property
    def welcome_channels(self):
        # This handles, for example, 2 intro channels, for English and Dutch
        return [
            {"channel_id": 1222655567705669693, "message_id": 1224098100021432410},
            {"channel_id": 1217567159576821800, "message_id": 1224088412055933008},
        ]

    @property
    def admin_channel_id(self):
        return 1222295125229834440


CONFIG = _Config()
