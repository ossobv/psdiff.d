# docker-proxy + erlang: Remove fluctuating args

class ProcessFormatterMixin(object):
    def adjust(self, process):
        super(ProcessFormatterMixin, self).adjust(process)

        # For docker-proxy, mask the IP which can switch after restart.
        # /usr/bin/docker-proxy -proto tcp ... -container-ip 172.17.0.2 ...
        if process.cmdline.startswith('/usr/bin/docker-proxy '):
            p = process.cmdline.split()
            new = [p[0]]
            [new.extend(p[(i * 2 + 1):(i * 2 + 3)])
             for i, j in enumerate(p[1::2])
             if not j.startswith(('-container-ip',))]
            process.cmdline = ' '.join(new)

        # For rabbit/erlang, drop the code/cookie from rabbit@CODE.
        # /usr/lib/erlang/erts-8.2/bin/beam.smp ... -sname rabbit@c450cb080cc5 ...
        if process.cmdline.startswith('/usr/lib/erlang/'):
            p = process.cmdline.split()
            if p[0].endswith('/bin/beam.smp'):
                to_replace = [i for i in p if i.startswith('rabbit@')]
                if to_replace:
                    to_replace = to_replace[0]
                    new = [i.replace(to_replace, 'rabbit@CRC') for i in p]
                    process.cmdline = ' '.join(new)
