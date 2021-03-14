from data import days
from candle import Candle
import turtle

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
NORTH = 90
SOUTH = 270
EAST = 0
WEST = 180
PADDING = 5

price_highest: int
price_lowest: int
current_market_price = 11.16


def main():
    # create candle objects and find price boundaries
    candles = []
    global price_highest, price_lowest
    for i, day in enumerate(days):
        candle = Candle(*day.values())
        if i == 0 or candle.high > price_highest:
            price_highest = candle.high
        if i == 0 or candle.low < price_lowest:
            price_lowest = candle.low
        candles.append(candle)

    high_low_diff = price_highest - price_lowest
    pad_percentage = 0.1
    pad_amount = high_low_diff * pad_percentage
    bounds_top = round(price_highest + pad_amount, 1)
    bounds_bottom = round(price_lowest - pad_amount, 1)

    # set up the window
    window_ = turtle.Screen()
    window_.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
    window_.setworldcoordinates(0, bounds_bottom, WINDOW_WIDTH, bounds_top)
    # create a turtle for drawing candles
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.penup()

    # draw candles
    for i, candle in enumerate(candles):
        t.setx((candle.width * i) + (PADDING * i))
        draw_candle(t, candle)

    turtle.done()


def draw_candle(
                t: turtle.Turtle,
                candle: Candle,
                with_wicks: bool = True
                ) -> None:
    draw_real_body(t, candle)
    if with_wicks:
        draw_wicks(t, candle)


def draw_real_body(t: turtle.Turtle, candle: Candle) -> None:
    """
    Draws the real body of a candle from the bottom-left, counter-clockwise.
    """
    t.penup()
    t.sety(candle.real_body_bottom)
    t.fillcolor(candle.color)
    t.begin_fill()
    t.setheading(EAST)
    t.forward(candle.width)
    t.setheading(NORTH)
    t.sety(candle.real_body_top)
    t.setheading(WEST)
    t.forward(candle.width)
    t.setheading(SOUTH)
    t.sety(candle.real_body_bottom)
    t.end_fill()
    t.pendown()


def draw_wicks(t: turtle.Turtle, candle: Candle) -> None:
    """
    Draws the wicks of a candle, top then bottom.
    Finishes at the bottom-right of the real body, pointing right.
    """
    # draw top wick
    t.penup()
    x, y = t.pos()
    # go to the top-center of the candle
    t.goto(x + (candle.width // 2), candle.real_body_top)
    # point upwards
    t.setheading(NORTH)
    t.pendown()
    t.sety(candle.high)

    # draw bottom wick
    t.penup()
    x, y = t.pos()
    # go to the bottom-center of the candle
    t.goto(x, candle.real_body_bottom)
    # point downwards
    t.setheading(SOUTH)
    t.pendown()
    t.sety(candle.low)
    t.penup()


if __name__ == '__main__':
    main()
