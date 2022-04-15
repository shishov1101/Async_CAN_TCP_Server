# Asynchronous CAN TCP Server

Cross-platform asynchronous script for multi-user work with CAN bus via TCP protocol

## Server launch

The following environment variables are used for configuration:

`CAN_PORT` - CAN bus interface (`can0` by default for Linux, `PCAN_USBBUS1` by default for Windows);

`logs` - used to write CAN bus messages (`OFF` by default);

`port` - TCP port (`8020` by default);

To run a server on Linux:
Before launch you must run two commands in terminal:

1) `sudo ip link set can0 type can bitrate 500000`

2) `sudo ifconfig can0 up`

```cmd
python3 -m main -c can0 -l OFF -p 8020
```
To run a server on Windows:

```cmd
python -m main -c PCAN_USBBUS1 -l OFF -p 8020
```