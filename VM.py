import subprocess

def create_vm():
    # Define the QEMU command to create a VM
    qemu_cmd = [
        'qemu-system-x86_64',
        '-name', 'my_vm',
        '-memory', '1G',
        '-cpu', 'host',
        '-drive', 'file=/path/to/your/disk.qcow2,format=qcow2',
        '-boot', 'c',
        '-net', 'nic,model=virtio',
        '-net', 'user',
    ]

    # Execute the QEMU command
    try:
        subprocess.run(qemu_cmd, check=True)
        print('Virtual machine created successfully')
    except subprocess.CalledProcessError as e:
        print(f'Failed to create virtual machine. Error: {e}')

if __name__ == '__main__':
    create_vm()
