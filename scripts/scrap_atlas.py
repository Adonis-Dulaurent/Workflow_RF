import re
import time

import pandas as pd
import requests
from lxml import html


def build_slugs(df):
    """
    add the 'slug' colone from'Invités' colone
    """
    df = df.copy()

    slugs = []
    for invite in df["Invités"].dropna():
        slug = invite.lower()
        slug = re.sub(r"\s+", "-", invite.lower())
        slugs.append(slug)

    df.loc[df["Invités"].notna(), "slug"] = slugs
    return df


def scrap_data(df):
    """
    Checks the existence of Radio France pages based on slugs
    """
    base_url = "https://www.radiofrance.fr/personnes/"

    results = []

    for _, row in df.dropna(subset=["slug"]).iterrows():
        invite = row["Invités"]
        slug = row["slug"]

        url = base_url + slug
        r = requests.get(url, timeout=10)

        exists = False

        if r.status_code == 200:
            tree = html.fromstring(r.content)
            title = tree.xpath("//h1/text()")
            exists = not (title and "Zut !" in title[0])

        results.append(
            {"Invités": invite, "slug": slug, "radio_france": exists, "url": url}
        )

    return pd.DataFrame(results)


if __name__ == "__main__":
    df = build_slugs(df)
    df_rf = scrap_data(df)
    df_rf
