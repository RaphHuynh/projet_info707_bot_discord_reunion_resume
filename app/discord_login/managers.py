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
        user_id = user["id"]
        discord_user = self.get(id=user_id)
        discord_user.global_name = user["global_name"]
        discord_user.avatar = user["avatar"]
        discord_user.public_flags = user["public_flags"]
        discord_user.flags = user["flags"]
        discord_user.locale = user["locale"]
        discord_user.mfa_enabled = user["mfa_enabled"]
        discord_user.save()
