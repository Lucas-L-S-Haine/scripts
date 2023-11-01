import os
import sys
import tempfile as tmp
import subprocess as sp
import io


args = sys.argv[1:]
script_name = args[0]

tmp_html_name = os.path.basename(tmp.NamedTemporaryFile(suffix=".html").name)
tmp_script_name = os.path.basename(tmp.NamedTemporaryFile(suffix=".js").name)

html_file       = io.BytesIO()
js_file         = io.BytesIO()
tmp_html_file   = io.BytesIO()
tmp_script_file = io.BytesIO()


try:
    html_file = open("log.html", mode="rt")
    title_element = f"<title>Netscript - {script_name}</title>"
    script_element = f'<script src="{tmp_script_name}"></script>'
    html = (html_file
            .read()
            .replace("TITLE_ELEMENT", title_element)
            .replace("SCRIPT_ELEMENT", script_element)
            .encode())

    js_file = open(script_name, mode="rb")
    script = js_file.read()

    tmp_html_file = open(tmp_html_name, mode="wb")
    tmp_html_file.write(html)
    tmp_html_file.seek(0)

    tmp_script_file = open(tmp_script_name, mode="wb")
    tmp_script_file.write(script)
    tmp_script_file.seek(0)

    sp.run(["brave", tmp_html_name])

finally:
    html_file.close()
    js_file.close()
    tmp_html_file.close()
    tmp_script_file.close()

    os.unlink(tmp_html_name)
    os.unlink(tmp_script_name)
