from django.contrib.auth import models


class DiscordUserOAuth2Manager(models.UserManager):
    def create_new_discord_user(self, user):
        return self.create(
            id=user["id"],
            discord_tag=user["username"] + "#" + user["discriminator"],
            global_name=user["global_name"],
            avatar=user["avatar"],
            public_flags=user["public_flags"],
            flags=user["flags"],
            locale=user["locale"],
            mfa_enabled=user["mfa_enabled"],
        )

    def update_discord_user(self, user):
        return self.update(
            discord_tag=user["username"] + "#" + user["discriminator"],
            global_name=user["global_name"],
            avatar=user["avatar"],
            public_flags=user["public_flags"],
            flags=user["flags"],
            locale=user["locale"],
            mfa_enabled=user["mfa_enabled"],
        )
