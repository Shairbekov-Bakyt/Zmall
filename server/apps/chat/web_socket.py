from decouple import config

import pusher


pusher_client = pusher.Pusher(
    app_id=config("PUSHER_APP_ID"),
    key=config("PUSHER_KEY"),
    secret=config("PUSHER_SECRET"),
    cluster="ap2",
    ssl=True,
)
