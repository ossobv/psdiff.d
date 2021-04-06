# Add @VRF to the process name if not in default.
# Use this on hosts where you have VRFs as l3mdev cgroups
# (like on Cumulus switches).
import os

try:
    # If you have a l3mdev cgroup ...
    os.stat('/sys/fs/cgroup/l3mdev')
except OSError as e:
    if e.args[0] == 2:  # ENOENT
        pass
    else:
        raise
else:
    # ... then add an adjust class to add "@VRF" to processes outside of
    # default VRFs.

    class ProcessFormatterMixin(object):
        def adjust(self, process):
            super(ProcessFormatterMixin, self).adjust(process)

            try:
                with open('/proc/{}/cgroup'.format(process.pid)) as fp:
                    groups = fp.read()
            except IOError:
                pass
            else:
                l3mdev = [
                    i for i in groups.split('\n') if ':l3mdev:' in groups]
                if l3mdev:
                    l3mdev = l3mdev[0].split(':', 2)
                    assert len(l3mdev) == 3, l3mdev
                    assert l3mdev[2].startswith('/'), l3mdev
                    vrf = l3mdev[2][1:]
                    if vrf:
                        try:
                            name, rest = process.cmdline.split(' ', 1)
                        except ValueError:
                            process.cmdline = '{}@{}'.format(
                                process.cmdline, vrf)
                        else:
                            process.cmdline = '{}@{} {}'.format(
                                name, vrf, rest)
