from json import dumps

from aiohttp import ClientSession, FormData

from .models import AIStyle, AIModel, GenerateResponse, StatusGenerationResponse, FusionBrainError


class HttpFusionBrain:
    def __init__(self, api_key: str, secret_key: str) -> None:
        self.BASE_URL = "https://api-key.fusionbrain.ai/"

        self._api_key = api_key
        self._secret_key = secret_key

        self.__AUTH_HEADERS = {
            "X-Key": f"Key {api_key}",
            "X-Secret": f"Secret {secret_key}"
        }

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def secret_key(self) -> str:
        return self._secret_key

    async def _create_request(
        self,
        method: str,
        end_point: str,
        params: dict | None = None,
        kwargs: dict | None = None
    ):
        params = params or {}
        kwargs = kwargs or {}

        async with ClientSession(
            headers=self.__AUTH_HEADERS
        ) as session:
            response = await session.request(
                method=method,
                url=end_point,
                params=params,
                **kwargs
            )
            response_json = await response.json()

            if not response.ok:
                raise FusionBrainError(response.status, response_json)

            return response_json

    async def get_styles(self) -> list[AIStyle]:
        """
        https://fusionbrain.ai/docs/doc/api-dokumentaciya/
        """
        # https://cdn.fusionbrain.ai/static/styles/key
        response = await self._create_request(
            "GET",
            "https://cdn.fusionbrain.ai/static/styles/web"
        )

        return [AIStyle(**data) for data in response]

    async def get_models(self) -> list[AIModel]:
        """
        https://fusionbrain.ai/docs/doc/api-dokumentaciya/
        """
        response = await self._create_request(
            "GET",
            "https://api-key.fusionbrain.ai/key/api/v1/models"
        )

        return [AIModel(**data) for data in response]

    async def generate(
        self,
        prompt: str,
        model_id: int,
        negative_prompt: str | None = None,
        style: str = "DEFAULT",
        width: int = 1024,
        height: int = 1024,
        num_images = 1
    ) -> GenerateResponse:
        """
        https://fusionbrain.ai/docs/doc/api-dokumentaciya/
        """
        params = {
            "type": "GENERATE",
            "style": style,
            "width": width,
            "height": height,
            "num_images": num_images,
            "generateParams": {
                "query": prompt
            }
        }

        if negative_prompt:
            params.update(
                {
                    "negativePromptUnclip": negative_prompt
                }
            )

        form_data = FormData()
        form_data.add_field('params', dumps(params), content_type='application/json')
        form_data.add_field('model_id', str(model_id))

        response = await self._create_request(
            "POST",
            "https://api-key.fusionbrain.ai/key/api/v1/text2image/run",
            kwargs={
                "data": form_data
            }
        )

        return GenerateResponse(**response)

    async def check_generation(self, generation_uuid: str) -> StatusGenerationResponse:
        response = await self._create_request(
            "GET",
            "https://api-key.fusionbrain.ai/key/api/v1/text2image/status/" + generation_uuid
        )

        return StatusGenerationResponse(**response)
