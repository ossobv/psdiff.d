# docker: Ignore dockerd/containerd children

class ProcessFormatterMixin(object):
    def include(self, process):
        ret = super(ProcessFormatterMixin, self).include(process)

        if ret and process.has_parent(cmdline__startswith=(
                '/usr/bin/containerd',
                '/usr/bin/dockerd ')):
            return False

        if ret and process.has_parent(cmdline__startswith=(
                '/usr/bin/containerd-shim-runc-v2 ',), include_self=True):
            return False

        return ret
