# haproxy: Remove -x/-sf arguments which may fluctuate

class ProcessFormatterMixin(object):
    def adjust(self, process):
        super(ProcessFormatterMixin, self).adjust(process)

        # /usr/sbin/haproxy ... [-x ...sock] [-sf 12345 4444]
        if process.cmdline.startswith('/usr/sbin/haproxy '):
            p = process.cmdline.split()
            if len(p) > 2 and p[-2] == '-x' and p[-1].endswith('.sock'):
                process.cmdline = ' '.join(p[0:-2])
                p = process.cmdline.split()

            try:
                idx = p.index('-sf')
            except ValueError:
                pass
            else:
                idx += 1
                while len(p) > idx and p[idx].isdigit():
                    p.pop(idx)
                p.pop(idx - 1)
                process.cmdline = ' '.join(p)
                p = process.cmdline.split()
