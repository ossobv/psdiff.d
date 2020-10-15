# mysqld: Ignore wsrep argument

class ProcessFormatterMixin(object):
    def adjust(self, process):
        super(ProcessFormatterMixin, self).adjust(process)

        if process.cmdline.startswith('/usr/sbin/mysqld ') and (
                '--wsrep_start_position=' in process.cmdline):
            process.cmdline = ' '.join(
                ('--wsrep_start_position=X'
                 if i.startswith('--wsrep_start_position=') else i)
                for i in process.cmdline.split(' '))
