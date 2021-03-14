class Candle:
    """
        TODO: add an init parameter for the candle's time range
        TODO: should currently-rounded values be truncated instead?
        TODO: determine doji range (neither bullish nor bearish)
    """
    def __init__(self, price_open, price_close, price_high, price_low):
        self.open = price_open
        self.close = price_close
        self.high = price_high
        self.low = price_low

        self.is_bullish = self.close - self.open >= 0
        self.color = "green" if self.is_bullish else "red"
        # set top/bottom prices based on bullish/bearish
        self.real_body_top, self.real_body_bottom = (
            self.close, self.open
            ) if self.is_bullish else (
                self.open, self.close
            )
        self.real_body_range = round(abs(self.close - self.open), 2)
        self.wick_top_range = round(self.high - self.real_body_top, 2)
        self.wick_bottom_range = round(
            abs(self.low - self.real_body_bottom), 2
        )
        self.width = 30
        # turn real body and wick dollar amounts into cents
        self.height = self.real_body_range * 100
        self.wick_top_height = self.wick_top_range * 100
        self.wick_bottom_height = self.wick_bottom_range * 100

    def __repr__(self):
        return (
            f"{'Bullish' if self.is_bullish else 'Bearish'}\n"
            f"{'-' * 30}\n"
            "Ends\n"
            f"{'Wick top':>18}: {self.high}\n"
            f"{'Real body top':>18}: {self.real_body_top}\n"
            f"{'Real body bottom':>18}: {self.real_body_bottom}\n"
            f"{'Wick bottom':>18}: {self.low}\n"
            "Ranges:\n"
            f"{'Real body range':>18}: {self.real_body_range}\n"
            f"{'Wick top range':>18}: {self.wick_top_range}\n"
            f"{'Wick bottom range':>18}: {self.wick_bottom_range}\n"
            f"{'-' * 30}"
        )
