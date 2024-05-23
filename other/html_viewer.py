import os
import webbrowser
from pathlib import Path

import clipboard

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        div {{
            font-family: 'Courier New', monospace;
            white-space: pre-wrap; /* Para mantener los espacios y saltos de línea */
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
        }}
    </style>
    <title>
        HTML VIEWER
    </title>
</head>
<body>
    <div>
        {body}
    </div>
</body>
</html>
"""

viewer_path = os.path.join(Path.home(), "html_viewer.html")


def main():
    body = clipboard.paste()
    html = HTML_TEMPLATE.format(body=body)
    with open(viewer_path, 'w') as f:
        f.write(html)

    webbrowser.open(viewer_path)


if __name__ == '__main__':
    """
    Is required to install xclip if linux is used
    >>> apt install xclip
    """
    main()
