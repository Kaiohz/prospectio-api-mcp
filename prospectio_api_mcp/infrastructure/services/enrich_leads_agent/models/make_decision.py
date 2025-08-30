from pydantic import BaseModel


class MakeDecisionResult(BaseModel):
    """
    Model representing the result of a decision.

    Attributes:
        result (bool): The outcome of the decision.
    """

    result: bool
