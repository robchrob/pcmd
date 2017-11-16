import socket


def main(master_root):
    if not master_root.pidFile.running():
        master_root.logger.error(
            'pcmd master is not currently running'
        )
        return 1
    else:
        (pid, port) = master_root.pidFile.read()

    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        local_socket.connect(('127.0.0.1', port))
        local_socket.sendall(bytes('stop', 'utf-8'))
        response = local_socket.recv(4096)
    finally:
        local_socket.close()

    if response == b'ok':
        master_root.pidFile.remove()
        return 0
    else:
        master_root.logger.error(
            'stopping the master failed - err (%s)', response
        )
        return 1
