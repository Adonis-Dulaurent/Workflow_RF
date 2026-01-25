import pandas as pd


def suppr(df):
    mask = df["radio"] == "FranceInfo"

    before = df.loc[mask, "emission"].copy()

    df.loc[mask, "emission"] = (
        df.loc[mask, "emission"]
        .str.replace(r"^(.*)\s+avec.*$", r"\1", regex=True, case=False)
        .str.strip()
    )

    count = (before != df.loc[mask, "emission"]).sum()
    print(f"{count} lignes nettoyées")

    return df


if __name__ == "__main__":
    df = pd.read_csv("rf.csv")
    df = suppr(df)
    print(df)
