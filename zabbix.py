# zabbix-proxy/zabbix-server: Remove "started" from zabbix daemon children

class ProcessFormatterMixin(object):
    def adjust(self, process):
        super(ProcessFormatterMixin, self).adjust(process)

        if (process.cmdline.startswith((
                '/usr/sbin/zabbix_proxy: ', '/usr/sbin/zabbix_server: '))
                and process.cmdline.endswith(' started')):
            process.cmdline = process.cmdline[0:-8]
