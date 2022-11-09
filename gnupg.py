# gnupg: Ignore gnupg gpg-agent+dirmngr

class ProcessFormatterMixin(object):
    def include(self, process):
        ret = super(ProcessFormatterMixin, self).include(process)

        if ret and process.cmdline.startswith((
                'dirmngr --daemon --homedir ',
                'gpg-agent --homedir ')):
            return False

        return ret
