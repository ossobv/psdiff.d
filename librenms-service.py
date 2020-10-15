# librenms-service: Drop all children

class ProcessFormatterMixin(object):
    def include(self, process):
        ret = super(ProcessFormatterMixin, self).include(process)

        # Skip all children of librenms-service.py
        if ret and process.has_parent(cmdline__startswith=(
                'python3 /opt/librenms/librenms-service.py -v -d',
                ('/usr/bin/python3 '
                 '/opt/librenms/librenms-service.py -v -d'))):
            return False

        return ret
