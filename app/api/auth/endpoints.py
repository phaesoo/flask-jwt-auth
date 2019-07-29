import logging

from app.api.restplus import api


logger = logging.getLogger(__name__)

ns = api.namespace("auth", description="Endpoints for user auth")