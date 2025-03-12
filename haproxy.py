# haproxy: Remove -x/-sf arguments which may fluctuate

class ProcessFormatterMixin(object):
    def include(self, process):
        # Ignore one or more haproxy children, but only if they're not
        # listening to anything.
        if process.has_parent(cmdline__startswith='/usr/sbin/haproxy '):
            listens = getattr(process, '_listens', [])
            if not listens:
                return False

        return super(ProcessFormatterMixin, self).include(process)

    def adjust(self, process):
        super(ProcessFormatterMixin, self).adjust(process)

        # /usr/sbin/haproxy ... [-x ...sock] [-sf 12345 4444]
        if process.cmdline.startswith('/usr/sbin/haproxy '):
            p = process.cmdline.split()
            idx = 0
            new_p = []
            arg1 = None

            try:
                while idx < len(p):
                    arg1 = p[idx]
                    # [-x ...sock]
                    if arg1 == '-x' and p[idx + 1].endswith('.sock'):
                        idx += 2
                    # [-sf PID1 PID2 PID3...]
                    elif arg1 == '-sf':
                        arg1 = None
                        idx += 1
                        while p[idx].isdigit():
                            idx += 1
                    else:
                        new_p.append(arg1)
                        idx += 1
            except IndexError:
                if arg1 is not None:
                    new_p.append(arg1)

            process.cmdline = ' '.join(new_p)
