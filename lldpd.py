# lldpd: Do not list all lldpd neighbours/changes

class ProcessFormatterMixin(object):
    def adjust(self, process):
        super(ProcessFormatterMixin, self).adjust(process)

        if (process.has_parent(cmdline__startswith=('lldpd: ',)) and
                process.cmdline.startswith('lldpd: ')):
            process.cmdline = 'lldpd: (zero or more neighbors)'
