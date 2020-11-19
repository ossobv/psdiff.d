# gitlab Omnibus
import re


ADJUST_REGEXES = (
    '^ruby /opt/gitlab/embedded/service/gitaly-ruby/bin/gitaly-ruby [0-9]+ /tmp/gitaly-ruby[0-9]+/socket',
)
ADJUST_CREGEXES = tuple(re.compile(i) for i in ADJUST_REGEXES)

NOCHILDREN_MATCHES = (
    '/opt/gitlab/embedded/bin/postgres -D /var/opt/gitlab/postgresql/data',
    '/bin/sh /opt/gitlab/embedded/bin/gitlab-logrotate-wrapper',
)

EXCLUDE_REGEXES = (
    '^/opt/gitlab/embedded/bin/git --git-dir [^ ]+ cat-file --batch(-check)?$',
)
EXCLUDE_CREGEXES = tuple(re.compile(i) for i in EXCLUDE_REGEXES)

class ProcessFormatterMixin(object):
    def adjust(self, process):
        super(ProcessFormatterMixin, self).adjust(process)

        for idx, regex in enumerate(ADJUST_CREGEXES):
            s = process.cmdline
            m = regex.search(s)
            if m:
                process.cmdline = s[:m.start()] + ADJUST_REGEXES[idx] + s[m.end():]
                break

    def include(self, process):
        ret = super(ProcessFormatterMixin, self).include(process)
        if not ret:
            return False

        if process.has_parent(include_self=False, cmdline__startswith=NOCHILDREN_MATCHES):
            return False

        for idx, regex in enumerate(EXCLUDE_CREGEXES):
            if regex.search(process.cmdline):
                return False

        return True
