from typing import TypeVar

from beartype import beartype
from jinja2.sandbox import ImmutableSandboxedEnvironment
from jinja2schema import infer, to_json_schema
from jsonschema import validate

from ...activities.utils import ALLOWED_FUNCTIONS, constants, stdlib

__all__: list[str] = [
    "render_template",
]

# jinja environment
jinja_env: ImmutableSandboxedEnvironment = ImmutableSandboxedEnvironment(
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
    auto_reload=False,
    enable_async=True,
    loader=None,
)

# Add arrow to jinja

for k, v in (constants | stdlib | ALLOWED_FUNCTIONS).items():
    jinja_env.globals[k] = v


# Funcs
@beartype
async def render_template_string(
    template_string: str,
    variables: dict,
    check: bool = False,
) -> str:
    # Parse template
    template = jinja_env.from_string(template_string)

    # If check is required, get required vars from template and validate variables
    if check:
        schema = to_json_schema(infer(template_string))
        validate(instance=variables, schema=schema)

    # Render
    return await template.render_async(**variables)


# A render function that can render arbitrarily nested lists of dicts
# only render keys: content, text, image_url
# and only render values that are strings
T = TypeVar("T", str, dict, list[dict | list[dict]], None)


@beartype
async def render_template_nested(
    input: T,
    variables: dict,
    check: bool = False,
) -> T:
    match input:
        case str():
            return await render_template_string(input, variables, check)
        case dict():
            return {
                k: await render_template_nested(v, variables, check) for k, v in input.items()
            }
        case list():
            return [await render_template_nested(v, variables, check) for v in input]
        case _:
            return input


@beartype
async def render_template(
    input: str | list[dict],
    variables: dict,
    check: bool = False,
    skip_vars: list[str] | None = None,
) -> str | list[dict]:
    variables = {
        name: val
        for name, val in variables.items()
        if not (skip_vars is not None and isinstance(name, str) and name in skip_vars)
    }

    return await render_template_nested(input, variables, check)
