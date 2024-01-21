"""Pydantic models definition.

This package contains the Pydantic model defintiions used for recommendations.

"""

from pydantic import BaseModel
from .module import Module


class Recommendation(BaseModel):
    """Model for recommendations

    This is a Pydantic model for the modules recommendations of users.

    Attributes:
      cf_recommendations:
        The list of modules recommended through collaborative filtering.
      cbf_recommendations:
        The list of modules recommended through content-based filtering.
    """

    cf_recommendations: list[Module] = []
    cbf_recommendations: list[Module] = []
