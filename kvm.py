# kvm: Trim kvm/qemu command line parameters

class ProcessFormatterMixin(object):
    def adjust(self, process):
        super(ProcessFormatterMixin, self).adjust(process)

        # For kvm, show only "/usr/bin/kvm -id X -name Y".
        if process.cmdline.startswith('/usr/bin/kvm '):
            p = process.cmdline.split()
            new = [p[0]]
            [new.extend(p[i:i+2])
             for i, j in enumerate(p)
             if j.startswith(('-id', '-name'))]
            process.cmdline = ' '.join(new)
