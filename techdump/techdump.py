#!/usr/bin/env python3

import configparser
import json
from os import mkdir
from subprocess import call
from time import strftime

config = configparser.ConfigParser(allow_no_value=True)
config.read('config.ini')


def run(cmd, outdir):
    filename = cmd.replace(' ', '_')
    filename = filename.replace('/', '_')
    shellcommand = '%s 2>%s/%s.stderr >%s/%s.stdout' % (cmd, outdir, filename,
                                                        outdir, filename)
    print('Running: %s' % cmd)
    return call(shellcommand, shell=True)


def main():
    resultsdir = strftime('%Y-%m-%d_%H:%M_UTC%z')
    mkdir(resultsdir)
    summary = []
    for cmd in config['Commands']:
        cmdsummary = {'command': cmd}
        cmdsummary['starttime'] = strftime('%Y-%m-%d_%H:%M:%S_UTC%z')
        result = run(cmd, resultsdir)
        cmdsummary['endtime'] = strftime('%Y-%m-%d_%H:%M:%S_UTC%z')
        cmdsummary['resultcode'] = result
        if result > 0:
            print('%s returned non-zero exit code %d' % (cmd, result))
        summary.append(cmdsummary)
    with open('%s/summary.json' % resultsdir, 'w') as f:
        f.write(json.dumps(summary))


if __name__ == '__main__':
    main()
