# custom regexes; similar to regexesv1.py
from re import compile as re_compile


class ProcessFormatterMixin(object):
    REPLACEMENTS = [(re_compile(re_str), re_str) for re_str in (
        (r'/usr/lib/passenger/support-binaries/PassengerAgent'
         r' temp-dir-toucher /tmp/passenger-standalone.\w+'
         r' --cleanup --daemonize --pid-file'
         r' /tmp/passenger-standalone.\w+/temp_dir_toucher.pid'
         r' --log-file /webapps/Paldi_ReportManager/passenger.\d+.log'
         r' --nginx-pid \d+'),
        (r'nginx: master process'
         r' /usr/lib/passenger/support-binaries/nginx-1.26.1'
         r' -c /tmp/passenger-standalone.\w+/nginx.conf'
         r' -p /tmp/passenger-standalone.\w+'),
    )]

    def adjust(self, process):
        super(ProcessFormatterMixin, self).adjust(process)

        for cre, re in self.REPLACEMENTS:
            m = cre.match(process.cmdline)
            if m and m.start() == 0 and m.end() == len(process.cmdline):
                process.cmdline = re
                break
