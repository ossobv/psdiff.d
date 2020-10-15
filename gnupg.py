# dirmngr: Ignore gnupg dirmngr

class ProcessFormatterMixin(object):
    def include(self, process):
        ret = super(ProcessFormatterMixin, self).include(process)

        if ret and process.cmdline.startswith('dirmngr --daemon --homedir '):
            return False

        return ret
