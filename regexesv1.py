# custom regexes
import re

REPLACE_REGEXES = (
    # Replace this match with itself (but without backslash escaped characters)
    
    # elasticsearch: -Djava.io.tmpdir=/tmp/elasticsearch-+
    r'/tmp/elasticsearch-\d+\b',
)


def without_backslash_stuff(s):
    return without_backslash_re.sub('', s)


without_backslash_re = re.compile(r'\\.')

REPLACE_CREGEXES = tuple(re.compile(i) for i in REPLACE_REGEXES)
REPLACE_RESULTS = tuple(without_backslash_stuff(i) for i in REPLACE_REGEXES)


class ProcessFormatterMixin(object):
    def adjust(self, process):
        super(ProcessFormatterMixin, self).adjust(process)

        for idx, regex in enumerate(REPLACE_CREGEXES):
            s = process.cmdline
            m = regex.search(s)
            if m:
                process.cmdline = REPLACE_CREGEXES[idx].sub(
                    REPLACE_RESULTS[idx], s)
                break
