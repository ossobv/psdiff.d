# gitlab Omnibus
import re

ADJUST_REGEXES = (
    (r'^ruby /opt/gitlab/embedded/service/gitaly-ruby/bin/gitaly-ruby [0-9]+ '
     r'/var/opt/gitlab/gitaly/internal_sockets/ruby.[0-9]+'),
    r'puma: cluster worker 0: [0-9]+ \[gitlab-puma-worker\]',
    r'puma: cluster worker 1: [0-9]+ \[gitlab-puma-worker\]',
    r'puma: cluster worker 2: [0-9]+ \[gitlab-puma-worker\]',
    r'puma: cluster worker 3: [0-9]+ \[gitlab-puma-worker\]',
)
ADJUST_CREGEXES = tuple(re.compile(i) for i in ADJUST_REGEXES)

NOCHILDREN_MATCHES = (
    r'/opt/gitlab/embedded/bin/postgres -D /var/opt/gitlab/postgresql/data',
    r'/bin/sh /opt/gitlab/embedded/bin/gitlab-logrotate-wrapper',
)

EXCLUDE_REGEXES = (
    (r'^/opt/gitlab/embedded/bin/git --git-dir [^ ]+ '
     r'cat-file --batch(-check)?$'),
)
EXCLUDE_CREGEXES = tuple(re.compile(i) for i in EXCLUDE_REGEXES)


class ProcessFormatterMixin(object):
    def adjust(self, process):
        super(ProcessFormatterMixin, self).adjust(process)

        for idx, regex in enumerate(ADJUST_CREGEXES):
            s = process.cmdline
            m = regex.search(s)
            if m:
                process.cmdline = (
                    s[:m.start()] +
                    ADJUST_REGEXES[idx].replace('\\', '') +
                    s[m.end():])
                break

    def include(self, process):
        ret = super(ProcessFormatterMixin, self).include(process)
        if not ret:
            return False

        if process.has_parent(
                include_self=False, cmdline__startswith=NOCHILDREN_MATCHES):
            return False

        for idx, regex in enumerate(EXCLUDE_CREGEXES):
            if regex.search(process.cmdline):
                return False

        return True
