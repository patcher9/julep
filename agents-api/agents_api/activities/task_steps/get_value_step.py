from beartype import beartype
from temporalio import activity

from ...common.protocol.tasks import StepContext, StepOutcome
from ...env import testing


# TODO: We should use this step to query the parent workflow and get the value from the workflow context
# SCRUM-1
@beartype
async def get_value_step(
    context: StepContext,
) -> StepOutcome:
    try:
        assert hasattr(context.current_step, 'get'), "current_step does not have 'get' attribute"
        key: str = context.current_step.get
        raise NotImplementedError("Not implemented yet")
    except AttributeError:
        activity.logger.error("current_step does not have 'get' attribute")
        return StepOutcome(error="Invalid step type: missing 'get' attribute.")


# Note: This is here just for clarity. We could have just imported get_value_step directly
# They do the same thing, so we dont need to mock the get_value_step function
mock_get_value_step = get_value_step

get_value_step = activity.defn(name="get_value_step")(
    get_value_step if not testing else mock_get_value_step
)
