def get(master_root):
    if (
            master_root.conf.get('local_hostname') in
            ("127.0.0.1", "localhost") or
            master_root.local
    ):
        if not master_root.pidFile.running():
            raise NotCurrentlyRunning
        else:
            (_, port) = master_root.pidFile.read()
    else:
        if master_root.conf.get('local_port') == "random":
            raise PortNotValid
        else:
            port = int(master_root.conf.get('local_port'))

    return master_root.conf.get('local_hostname'), port


class NotCurrentlyRunning(Exception):
    pass


class PortNotValid(Exception):
    pass
