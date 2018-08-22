import pandas as pd


def load_and_clean(fp):
    return (
        pd.read_excel(fp).drop([
            "link",
            "storage_type",
            "screen_size",
            "age",
            "RAM_speed",
            "graphics_memory"
        ], axis=1)
        .assign(
            price=lambda x: x["price"].astype("str").str.strip().astype("int"),
            processor=lambda x: x["processor"].str.extract("(\d)"),
            processor_clockspeed=lambda x: x["processor_clockspeed"].str.extract(
                "(\d[\.\,]\d)").pipe(lambda x: x.iloc[:, 0].str.replace(",", ".")),
            weight=lambda x: x["weight"].str.extract(
                "(\d+[\.\,]?\d*)").pipe(lambda x: x.iloc[:, 0].str.replace(",", ".")),
            RAM_size=lambda x: x["RAM_size"].str.extract("(\d+)"),
            storage_size=lambda x: x["storage_size"].str.extract(
                "(\d+)").iloc[:, 0].astype("int").apply(lambda x: x if x < 10 else x / 1000),
            battery_life=lambda x: x["battery_ life"].str.extract("(\d+)"),
            screen_resolution=lambda x: x["screen_resolution"].str.split("x").apply(
                lambda x: [int(i.strip()) for i in x]).apply(lambda x: x[0] * x[1])
        )
        .drop("battery_ life", axis=1)
        .rename(columns={"processor": "processor_modifier", "battery_life": "battery.life", "graphics_card": "graphics_brand"})
    )
