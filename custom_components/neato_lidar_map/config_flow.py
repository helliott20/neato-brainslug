"""Config flow for Neato LIDAR Map integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import selector

from .const import (
    CONF_IMAGE_SIZE,
    CONF_LIDAR_ENTITY,
    CONF_MAX_RANGE,
    CONF_POS_X_ENTITY,
    CONF_POS_Y_ENTITY,
    CONF_POS_HEADING_ENTITY,
    DEFAULT_IMAGE_SIZE,
    DEFAULT_MAX_RANGE,
    DOMAIN,
)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_LIDAR_ENTITY): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor"),
        ),
        vol.Optional(CONF_POS_X_ENTITY): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor"),
        ),
        vol.Optional(CONF_POS_Y_ENTITY): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor"),
        ),
        vol.Optional(CONF_POS_HEADING_ENTITY): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor"),
        ),
        vol.Optional(CONF_IMAGE_SIZE, default=DEFAULT_IMAGE_SIZE): vol.All(
            vol.Coerce(int), vol.Range(min=200, max=1200)
        ),
        vol.Optional(CONF_MAX_RANGE, default=DEFAULT_MAX_RANGE): vol.All(
            vol.Coerce(int), vol.Range(min=1000, max=10000)
        ),
    }
)


class NeatoLidarMapConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Neato LIDAR Map."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(
                title="Neato LIDAR Map",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
        )
