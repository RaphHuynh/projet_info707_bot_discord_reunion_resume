from .on_ready import on_ready_event
from .recording import handle_finished_recording

def register_events(bot):
    bot.event(on_ready_event)