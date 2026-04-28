# listen-veth: Replace "p_raw:*vethacfdebf" interface with "p_raw:*:vethX"

class ProcessFormatterMixin(object):
    def adjust(self, process):
        super(ProcessFormatterMixin, self).adjust(process)

        # Replace these:
        # > lldpd: connected to some.switch.  {user=_lldpd, listen=(
        # >     p_raw:*:VRF1,
        # >     p_raw:*:VRF2,
        # >     p_raw:*:vethacfdebf)}  <-- these
        process._listens = set(
            ('p_raw:*:vethX' if lst.startswith('p_raw:*:veth') else lst)
            for lst in process._listens)
