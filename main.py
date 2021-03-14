import argparse
import sys
import turtle
from candle import Candle
import requests

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
NORTH = 90
SOUTH = 270
EAST = 0
WEST = 180
PAD_X = 5  # number of pixels space separating each candle
PAD_Y = 0.1  # percentage of space above/below highest/lowest candles
YAHOO_BASE_URL = "https://query1.finance.yahoo.com"

current_market_price = 11.16


def main():
    parser = create_parser()
    args = parser.parse_args()

    # get market data
    url = f"{YAHOO_BASE_URL}/v8/finance/chart/{args.ticker}"
    params = {
        "range": args.range.lower(),
        "interval": args.interval.lower(),
        "includePrePost": args.no_pre_post
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        print("Error")
        sys.exit(1)
    data = r.json()['chart']['result'][0]
    quotes = data['indicators']['quote'][0]
    timestamps = data['timestamp']
    fields = ("timestamp", "open", "close", "high", "low", "volume")
    data = list(zip(
        timestamps,
        quotes["open"],
        quotes["close"],
        quotes["high"],
        quotes["low"],
        quotes["volume"]
    ))
    candle_data = [
        {f: round(v, 2) for f, v in zip(fields, item)}
        for item in data
    ]
    # create candle objects and find price boundaries
    candles = []
    price_highest = 0
    price_lowest = 0
    for i, candle_ in enumerate(candle_data):
        candle = Candle(*candle_.values())
        if i == 0 or candle.high > price_highest:
            price_highest = candle.high
        if i == 0 or candle.low < price_lowest:
            price_lowest = candle.low
        candles.append(candle)

    # compute padded boundaries for window height
    high_low_diff = price_highest - price_lowest
    pad_amount = high_low_diff * PAD_Y
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
        t.setx((candle.width * i) + (PAD_X * i))
        draw_candle(t, candle, not args.no_wicks)

    turtle.done()


def create_parser():
    parser = argparse.ArgumentParser(
        description="Candlestick chart generator for stocks")
    parser.add_argument("ticker", help="stock ticker symbol")
    parser.add_argument(
        "-r", "--range",
        help="chart time range (e.g., 1d, 5d, 1mo, 1y)",
        default="1d")
    parser.add_argument(
        "-i", "--interval",
        help="candle time interval (e.g., 1m, 1h, 1d)",
        default="1h")
    parser.add_argument(
        "--no-pre-post",
        action="store_false",
        help="hide pre-market and post-market data")
    parser.add_argument(
        "--no-volume",
        action="store_true",
        help="hide volume bars")
    parser.add_argument(
        "--no-wicks",
        action="store_true",
        help="hide wicks")
    return parser


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
