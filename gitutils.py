import os
import subprocess
from datetime import datetime


def git_blame(path, line):
    '''
    Call the git blame command on specified file-line and return result
    path: file to blame
    line: line to blame
    return list of result/error string messages
    '''
    # startupinfo to prevent external console window appear
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    #path = path.replace('\\', '/')
    result = subprocess.run(['git', 'blame', os.path.basename(path), '-L', f'{line},{line}', '-p'], 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, cwd=os.path.dirname(path))
    # escape if error
    if result.returncode != 0:
        return [result.stderr.decode('utf-8')]
    # command successfully executed
    sections = dict()
    for line in result.stdout.split(b'\n'):
        first_space_idx = line.find(b' ')
        section = line[:first_space_idx]
        if section in {b'committer', b'committer-mail', b'committer-time', b'committer-tz', b'summary'}:
            sections[section.decode('utf-8')] = line[first_space_idx+1:].decode('utf-8')
    # process datetime
    sections['committer-time'] = datetime.fromtimestamp(int(sections['committer-time']))
    datediff = datetime.now() - sections['committer-time']
 
    return [
        'committer     : ' + sections['committer'],
        'committer-mail: ' + sections['committer-mail'],
        'committer-time: ' + sections['committer-time'].strftime('%m/%d/%Y') + sections['committer-tz'] + '(' + str(datediff.days) + ' days)',
        'summary       : ' + sections['summary']
    ]