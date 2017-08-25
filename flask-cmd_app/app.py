#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from flask import Flask, Response

app = Flask(__name__)


def stream_template(template_name, **context):
    # http://flask.pocoo.org/docs/patterns/streaming/#streaming-from-templates
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    # uncomment if you don't need immediate reaction
    rv.enable_buffering(5)
    return rv


def get_lines(cmd):
    '''
    :param cmd: str 実行するコマンド.
    :rtype: generator
    :return: 標準出力 (行毎).
    '''
    proc = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        line = proc.stdout.readline()
        if line:
            yield line

        if not line and proc.poll() is not None:
            break


@app.route("/")
def streaming():
    def generate():
        for line in get_lines(cmd='df -h'):
            yield line.decode('utf-8')
    return Response(stream_template('index.html', data=generate()))


if __name__ == "__main__":
    app.run()

# vim fileencoding=utf-8
