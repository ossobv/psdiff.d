# Filter processes that are not indirect children of pid1.
# This is useful in LXC containers where main processes are children of
# (its) pid1, but externally spawned processes (through lxc-attach)
# have a different parent. We'll hide those latter processes.

class ProcessFormatterMixin(object):
    def grandparent(self, process):
        if process.parent is None or process.parent.pid == 0:
            return process.pid
        return self.grandparent(process.parent)

    def include(self, process):
        if self.grandparent(process) not in (0, 1):  # 0 is _our_ ROOT
            return False

        return super(ProcessFormatterMixin, self).include(process)
