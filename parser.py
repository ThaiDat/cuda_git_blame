from datetime import datetime


def __split_by_first_space(txt):
    '''
    Helper function to split bytes by first space occurence
    txt: bytes to split
    return tuple (txt before first space, txt after first space)
    '''
    first_space_idx = txt.find(b' ')
    return txt[:first_space_idx], txt[first_space_idx+1:]


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
    lines = msg_bytes.split(b'\n')
    _, committer = __split_by_first_space(lines[5])
    _, committer_mail = __split_by_first_space(lines[6])
    _, committer_time = __split_by_first_space(lines[7])
    _, committer_tz = __split_by_first_space(lines[8])
    _, summary = __split_by_first_space(lines[9])

    # process datetime
    committer_time = datetime.fromtimestamp(int(committer_time))
    datediff = datetime.now() - committer_time

    return [
        'committer     : ' + committer.decode('utf-8'),
        'committer-mail: ' + committer_mail.decode('utf-8'),
        'committer-time: ' + committer_time.strftime('%m/%d/%Y') + committer_tz.decode('utf-8') + ' (' + str(datediff.days) + ' days)',
        'summary       : ' + summary.decode('utf-8')
    ]


def parse_blame_analysis(error, msg_bytes):
    '''
    Parse message when call blame on multiple lines
    error: error code. 0 mean success
    msg_bytes: return message in bytes
    return list of messages
    '''
    if error != 0:
        return [line.decode('utf-8') for line in msg_bytes.split(b'\n')]
    # error == 0
    # number of section per line = 12 or 13(run git blame --line-porcelain for more detail)
    lines = msg_bytes.split(b'\n')
    i = 0
    # construct analysis on the go
    count_analysis = dict()
    oldest_commit = 999_999_999_999
    newest_commit = -999_999_999_999
    total_cnt = 0

    while i + 11 < len(lines):
        _, committer = __split_by_first_space(lines[i+5])
        _, committer_mail = __split_by_first_space(lines[i+6])
        _, committer_time = __split_by_first_space(lines[i+7])
        _, committer_tz = __split_by_first_space(lines[i+8])
        _, summary = __split_by_first_space(lines[i+9])
        # count analysis
        total_cnt += 1
        committer = committer.decode('utf-8')
        committer_mail = committer_mail.decode('utf-8');
        if (committer, committer_mail) in count_analysis:
            count_analysis[(committer, committer_mail)] += 1
        else:
            count_analysis[(committer, committer_mail)] = 1
        # time anlysis
        committer_time = int(committer_time)
        if committer_time < oldest_commit:
            oldest_commit = committer_time
        if committer_time > newest_commit:
            newest_commit = committer_time
        # next
        i += 13 if lines[i+10].startswith(b'previous ') else 12
    # post process
    count_analysis = sorted(count_analysis.items(), key=lambda x: x[1], reverse=True)
    oldest_commit = datetime.fromtimestamp(oldest_commit)
    oldest_diff = datetime.now() - oldest_commit
    newest_commit = datetime.fromtimestamp(newest_commit)
    newest_diff = datetime.now() - newest_commit
    # construct result
    result = list()
    result.append('On total {total_cnt} lines'.format(total_cnt=total_cnt))
    for (name, email), cnt in count_analysis:
        result.append('- {} {}: {} ({:.2f}%)'.format(name, email, cnt, cnt/total_cnt * 100))
    result.extend([
        'Oldest commit: {oldest:%m/%d/%Y} ({days_to_oldest} days)'.format(oldest=oldest_commit, days_to_oldest=oldest_diff.days),
        'Oldest commit: {newest:%m/%d/%Y} ({days_to_newest} days)'.format(newest=newest_commit, days_to_newest=newest_diff.days)
    ])
    return result