from telegrambotapi2 import getUpdates, sendMessage
import time

if __name__ == "__main__":
    token = ""
    counter = 0
    offset = -2
    while counter < 20:
        print(counter)
        # as the first offset will be -1, bellow a get the value
        # and increase it + 1 too
        updates = getUpdates(
            f"https://api.telegram.org/bot{token}/getUpdates?offset={offset + 1}"
        )
        if updates["result"]:
            offset = updates["result"][0]["update_id"]
            chat_id = updates["result"][0]["message"]["from"]["id"]
            sendMessage(chat_id, "Hello!", token)
        # get query to server for getUpdates each 2 second
        time.sleep(2)
        counter += 1
