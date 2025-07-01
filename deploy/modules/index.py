from viur.core import current, errors, exposed, Module, secret
from viur.core.decorators import access
from ai import query_anthropic
import logging


class Index(Module):

    @exposed
    def index(self, *args, **kwargs):
        """
        This is the final route where every request ends, which was not previously routed elsewhere.
        It normally should provide the landing page of a website, or redirect to a login method,
        depending on the project's use-case.
        """

        # The two lines below ensure that requesting a non-existent module or template throws
        # an error 404 instead of referring to index.
        if len(args) > 1 or kwargs:
            raise errors.NotFound()

        # Else, render index.html
        template = self.render.getEnv().get_template("index.html")
        return template.render()

    @exposed
    @access()
    def ai(
        self,
        prompt,
        provider: str = "anthropic",
        model: str = None,
        max_tokens: int = None,
        temperature: float = None,
        modules_to_include: list[
            str
        ] = None,  # musst be provided with multiple arguments
        enable_caching: bool = None,
        max_thinking_tokens: int = None,
        dry_run: bool = None,
    ):
        """
        Request a response from an AI provider based on the given prompt.

        This method interacts with the specified AI provider to generate a response based on the input prompt.
        It supports various configuration options, allowing users to customize their interaction with the provider.

        Parameters:
        - prompt (str): The input text for which the AI will generate a response.
        - provider (str): The AI provider to use for the request. Default is "anthropic".
        - model (str, optional): Specific model to use from the provider.
        - max_tokens (int, optional): The maximum number of tokens to generate in the response.
        - temperature (float, optional): Controls the randomness of the response. Higher values mean more randomness.
        - modules_to_include (list[str], optional): A list of modules to include in the request. Must be provided as multiple arguments.
        - enable_caching (bool, optional): Flag to enable caching of responses.
        - max_thinking_tokens (int, optional): Maximum tokens to use for thinking during the generation process.
        - dry_run (bool, optional): If True, the function will simulate the request without actually sending it. The Response in this case is null

        Returns:
        - The JSON response from the AI provider if successful or null

        Raises:
        - errors.NotAcceptable: If there is an error during the API request.
        - errors.BadRequest: If no valid provider is specified for the request.
        - errors.Unauthorized: If not logged in.
        """
        if provider == "anthropic":

            options = {
                n: locals()[n]
                for n in [
                    "model",
                    "max_tokens",
                    "temperature",
                    "modules_to_include",
                    "enable_caching",
                    "max_thinking_tokens",
                    "dry_run",
                ]
                if locals()[n]
            }

            try:
                params, response = query_anthropic(
                    prompt, **options, anthropic_api_key=secret.get("anthropic_api_key")
                )

                current.request.get().response.headers[
                    "Content-Type"
                ] = "application/json"

                if response:
                    return response.json()
                return "null"
            except Exception as e:
                logging.exception(e)
                raise errors.NotAcceptable(
                    "An error occurred while requesting the API."
                )

        raise errors.BadRequest("no matching provider found")
