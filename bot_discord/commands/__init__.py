from .help import help_command
from .join_channel import join_channel_command
from .leave_channel import leave_channel_command
from .play import play_command
from .stop_recording import stop_recording_command
from .schedule import schedule_command

def register_commands(bot):
    bot.add_application_command(help_command)
    bot.add_application_command(join_channel_command)
    bot.add_application_command(leave_channel_command)
    bot.add_application_command(play_command)
    bot.add_application_command(stop_recording_command)
    bot.add_application_command(schedule_command)