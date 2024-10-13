use std::time::Duration;

use deku::{DekuContainerWrite, DekuRead, DekuWrite, DekuWriter};
use std::io::Write;

#[derive(Debug, DekuRead, DekuWrite)]
#[deku(id_type = "u8")]
#[repr(u8)]
enum Direction {
    Up = 'U' as u8,
    Down = 'D' as u8,
    Left = 'L' as u8,
    Right = 'R' as u8
}

#[derive(Debug, DekuRead, DekuWrite)]
struct Frame {
    dir: Direction,
    steps: u32
}

fn main() {
    let port = serialport::new("/dev/tty.usbmodem21201", 9_600)
    .timeout(Duration::from_millis(10))
    .open().expect("Failed to open port");

    let frame = Frame {
        dir: Direction::Down,
        steps: 10
    };

    let _ = frame.to_bytes()
}
