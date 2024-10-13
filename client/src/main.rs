fn main() {
    let port = serialport::new("/dev/tty.usbmodem21201", 9_600)
    .timeout(Duration::from_millis(10))
    .open().expect("Failed to open port");
}
