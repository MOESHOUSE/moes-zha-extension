"""Config flow for MOES ZHA Extension."""

from homeassistant import config_entries

from .const import DOMAIN


class MoesZhaConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a config flow for MOES ZHA Extension."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step."""

        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(
                title="MOES ZHA Extension",
                data={},
            )

        return self.async_show_form(
            step_id="user",
        )
