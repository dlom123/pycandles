# build some data to work with
fields = ("open", "close", "high", "low")
data_day = [
    (9.38, 10.50, 10.77, 9.22),
    (11.02, 9.85, 12.47, 9.51),
    (10.65, 10.28, 10.87, 9.90),
    (10.16, 11.16, 11.40, 9.94)
]

days = [
    {f: v for f, v in zip(fields, data)}
    for data in data_day
]
