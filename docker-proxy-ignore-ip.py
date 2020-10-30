# docker-proxy: Mask -container-ip 172.17.x.x

class ProcessFormatterMixin(object):
    def adjust(self, process):
        super(ProcessFormatterMixin, self).adjust(process)

        if process.cmdline.startswith('/usr/bin/docker-proxy '):
            p = process.cmdline.split()
            try:
                container_ip_idx = p.index('-container-ip')
            except ValueError:
                pass
            else:
                if len(p) > container_ip_idx + 1:
                    p[container_ip_idx + 1] = 'x.x.x.x'
                    process.cmdline = ' '.join(p)
