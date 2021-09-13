# sshd: "sshd: /usr/sbin/sshd -D [listener] n of 10-100 startups"

class ProcessFormatterMixin(object):
    def adjust(self, process):
        super().adjust(process)

        if process.cmdline.startswith(
                'sshd: /usr/sbin/sshd -D [listener] '):
            if process.cmdline.endswith(' of 10-100 startups'):
                process.cmdline = (
                    'sshd: /usr/sbin/sshd -D [listener] n of 10-100 startups')
