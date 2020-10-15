# salt-minion: Don't include any children of children of salt-minion.
# This way we can psdiff (write) through the salt master.
# (Drawback is that we don't see runaway salt-minion children.)

class ProcessFormatterMixin(object):
    def has_salt_minion_parent(self, process):
        "Including self"
        if not process.parent or not process.parent.parent:
            return False

        if process.parent and process.parent.parent and all(
                cmdline == '/usr/bin/python3 /usr/bin/salt-minion'
                for cmdline in (
                    process.cmdline,
                    process.parent.cmdline,
                    process.parent.parent.cmdline)):
            return True

        return self.has_salt_minion_parent(process.parent)

    def include(self, process):
        inc = super(ProcessFormatterMixin, self).include(process)
        if not inc:
            return inc

        if self.has_salt_minion_parent(process):
            return False

        return True
