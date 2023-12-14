import re


def clean_html_text(text: str):
    text = text.replace("\n", " ").replace("\t", " ").strip()
    text = re.sub(
        r" +",
        " ",
        text,
    )
    return text
