import fetch
import wifi

URL = "https://catfact.ninja/fact"
# Set to True to automatically update the fact every 5 minutes
UPDATE_AUTOMATICALLY = False
SLEEP_MINUTES = 5

# define some screen areas for drawing the header and body text
header = rect(0, 0, screen.width, 35)
body = rect(10, 35, screen.width - 20, screen.height - 35)

# connecting to Wi-Fi takes a moment, so show a message while we wait
screen.pen = color.white
screen.clear()
screen.pen = color.black
screen.font = font.sins
screen.text(
    "Connecting to Wi-Fi...", header, font_size=2, align=(image.CENTER, image.MIDDLE)
)
badge.update()

while not wifi.connect():
    pass

# start fetching the cat fact
fact_request = fetch.url(URL)


def update():
    if fact_request:
        fact = fact_request.json()["fact"]

        screen.pen = color.white
        screen.clear()

        # solid header bar with inverted (white-on-black) title text
        screen.pen = color.black
        screen.rectangle(header)

        screen.pen = color.white
        screen.font = font.awesome

        screen.text(
            "Cat Fact!", header, font_size=2, align=(image.CENTER, image.MIDDLE)
        )
        screen.pen = color.black
        screen.font = font.sins

        # shorter facts get drawn bigger since there's less text to fit
        if len(fact) < 45:
            fact_size = 3
        elif len(fact) < 100:
            fact_size = 2
        else:
            fact_size = 1

        # draw the fact text, with ellipses if it doesn't fit
        screen.text(
            fact,
            body,
            font_size=fact_size,
            align=(image.LEFT, image.MIDDLE),
            overflow=image.ELLIPSES,
        )

        badge.update()

        # if the user wants to automatically update the fact, set an alarm to wake up in 5 minutes
        if UPDATE_AUTOMATICALLY:
            rtc.set_alarm(minutes=SLEEP_MINUTES)
        # go to sleep until the user presses a button
        wifi.disconnect()
        badge.sleep()


run(update)
