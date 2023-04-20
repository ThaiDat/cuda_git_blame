from datetime import datetime


def parse_blame_one_line(error, msg_bytes):
    '''
    Parse message when call blame on one line
    error: error code. 0 mean success
    msg_bytes: return message in bytes
    return list of messages
    '''
    if error != 0:
        return [line.decode('utf-8') for line in msg_bytes.split(b'\n')]
    # error == 0 
    sections = dict()
    for line in msg_bytes.split(b'\n'):
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
        'committer-time: ' + sections['committer-time'].strftime('%m/%d/%Y') + sections['committer-tz'] + ' (' + str(datediff.days) + ' days)',
        'summary       : ' + sections['summary']
    ]