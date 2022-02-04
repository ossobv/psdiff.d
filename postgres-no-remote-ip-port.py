# postgres: postgres postgres 172.28.0.12(56114) idle


class ProcessFormatterMixin(object):
    def adjust(self, process):
        super(ProcessFormatterMixin, self).adjust(process)

        if process.cmdline.startswith('postgres: '):
            p = process.cmdline.split()
            for idx, arg in enumerate(p):
                if arg.endswith(')') and '(' in arg:
                    p[idx] = 'x.x.x.x(xxx)'
                    process.cmdline = ' '.join(p)
