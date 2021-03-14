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


def main():
    # set up the window
    window_ = turtle.Screen()
    window_.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
    # create a turtle for drawing candles
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()

    candles = [Candle(*day.values()) for day in days]
    for i, candle in enumerate(candles):
        draw_candle(t, candle)
        # prepare for next candle
        t.forward(PADDING)

    turtle.done()


def draw_candle(
                t: turtle.Turtle,
                candle: Candle,
                with_wicks: bool = True
                ) -> None:
    draw_real_body(t, candle)
    if with_wicks:
        draw_wicks(t, candle)
    else:
        # send turtle to the bottom-right of the real body,
        # pointing right to begin the next candle
        t.setheading(EAST)
        t.forward(candle.width)


def draw_real_body(t: turtle.Turtle, candle: Candle) -> None:
    """
    Draws the real body of a candle from the bottom-left, counter-clockwise.
    """
    t.fillcolor(candle.color)
    t.begin_fill()
    t.forward(candle.width)
    t.setheading(NORTH)
    t.forward(candle.height)
    t.setheading(WEST)
    t.forward(candle.width)
    t.setheading(SOUTH)
    t.forward(candle.height)
    t.end_fill()


def draw_wicks(t: turtle.Turtle, candle: Candle) -> None:
    """
    Draws the wicks of a candle, top then bottom.
    Finishes at the bottom-right of the real body, pointing right.
    """
    # draw top wick
    t.penup()
    x, y = t.pos()
    # go to the top-center of the candle
    t.goto(x + (candle.width // 2), y + candle.height)
    # point upwards
    t.setheading(NORTH)
    t.pendown()
    t.forward(candle.wick_top_height)

    # draw bottom wick
    t.penup()
    x, y = t.pos()
    # go to the bottom-center of the candle
    t.goto(x, y - candle.wick_top_height - candle.height)
    # point downwards
    t.setheading(SOUTH)
    t.pendown()
    t.forward(candle.wick_bottom_height)
    t.penup()
    # go back up the bottom wick to the bottom of the real body and
    # end at the bottom-right of the real body, pointing to the right
    t.setheading(NORTH)
    t.forward(candle.wick_bottom_height)
    t.setheading(EAST)
    t.forward(candle.width // 2)



if __name__ == '__main__':
    main()
