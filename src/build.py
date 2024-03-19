#!/usr/bin/env python3

import os

with open("src/template.html", "r") as file:
    template = file.read()


def build(path, titles):
    print(path)
    assert path.startswith("/") and path.endswith("/")

    src_path = f"src{path}"
    src_is_dir = os.path.exists(src_path)

    out_path = f"docs{path}"
    os.makedirs(out_path, exist_ok=True)

    content = []
    for depth, title in enumerate(titles, start=1):
        href = "../" * (len(titles) - depth)
        content.append(f'<ul><li><a href="{href}">{title}</a>')

    if src_is_dir:
        content.append("<ul>")

        with open(f"{src_path}_index.txt", "r") as file:
            lines = file.readlines()

        line_type = ""
        for line in lines:
            line = line.rstrip()
            parts = line.split("|")

            if not parts[0]:
                line_type = parts[1]
                continue

            if line_type == "raw":
                content.append(line)
                continue

            if line_type == "blog":
                date, note = parts
                content.append(
                    f'<li><a name="{date}" href="#{date}">{date}</a> - {note}</li>'
                )
                continue

            if line_type == "gif":
                name = parts[0]
                title = parts[-1]  # If `len(parts) == 1` then `title == name`.
                content.append(
                    f'<li><a name="{name}" href="#{name}">{title}</a><br />'
                    f'<img src="{name}.gif"></li>'
                )
                continue

            if line_type == "dir":
                name = parts[0]
                title = parts[-1]  # If `len(parts) == 1` then `title == name`.
                if title:
                    content.append(f'<li><a href="{name}/">{title}</a></li>')

                build(f"{path}{name}/", titles + [title or name])
                continue

            raise Exception(f'Unknown line type: "{line_type}"')

        content.append("</ul>")
    content.extend(["</li></ul>"] * len(titles))

    if src_is_dir:
        tail = f"{src_path}_tail.html"
        if os.path.exists(tail):
            with open(tail, "r") as file:
                content.append(file.read().rstrip())
    else:
        with open(f"{src_path[:-1]}.html", "r") as file:
            content.append(file.read().rstrip())

    text = template.replace("{CONTENT}", "\n".join(content))
    text = text.replace("{ROOT}", "../" * (len(titles) - 1))
    text = text.replace("{TITLE}", " - ".join(reversed(titles)))

    with open(f"{out_path}/index.html", "w") as file:
        file.write(text)


if __name__ == "__main__":
    build("/", ["Denis Ryzhkov"])
