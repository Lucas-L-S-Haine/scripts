use std::collections::HashMap;
use clap::{Arg, Command};
use chrono::{Local,Timelike};

fn print_clock_icon() -> char {
    let minute: f32 = Local::now().minute() as f32;
    let (_is_pm, hour12) = Local::now().hour12();

    let hour: f32 = (hour12 as f32) + minute / 60.0;

    let clock_icon: char = match hour {
        hour if 00.00 <= hour && hour < 00.30 => '🕛',
        hour if 00.30 <= hour && hour < 01.00 => '🕧',
        hour if 01.00 <= hour && hour < 01.30 => '🕐',
        hour if 01.30 <= hour && hour < 02.00 => '🕜',
        hour if 02.00 <= hour && hour < 02.30 => '🕑',
        hour if 02.30 <= hour && hour < 03.00 => '🕝',
        hour if 03.00 <= hour && hour < 03.30 => '🕒',
        hour if 03.30 <= hour && hour < 04.00 => '🕞',
        hour if 04.00 <= hour && hour < 04.30 => '🕓',
        hour if 04.30 <= hour && hour < 05.00 => '🕟',
        hour if 05.00 <= hour && hour < 05.30 => '🕔',
        hour if 05.30 <= hour && hour < 06.00 => '🕠',
        hour if 06.00 <= hour && hour < 06.30 => '🕕',
        hour if 06.30 <= hour && hour < 07.00 => '🕡',
        hour if 07.00 <= hour && hour < 07.30 => '🕖',
        hour if 07.30 <= hour && hour < 08.00 => '🕢',
        hour if 08.00 <= hour && hour < 08.30 => '🕗',
        hour if 08.30 <= hour && hour < 09.00 => '🕣',
        hour if 09.00 <= hour && hour < 09.30 => '🕘',
        hour if 09.30 <= hour && hour < 10.00 => '🕤',
        hour if 10.00 <= hour && hour < 10.30 => '🕙',
        hour if 10.30 <= hour && hour < 11.00 => '🕥',
        hour if 11.00 <= hour && hour < 11.30 => '🕚',
        hour if 11.30 <= hour && hour < 00.00 => '🕦',
        _ => panic!("Cannot print clock icon"),
    };

    return clock_icon;
}

fn apply_color(color: &str) -> &str {
    let mut color_table: HashMap<&str, &str> = HashMap::new();

    color_table.insert("black", "\x1b[1;30m");
    color_table.insert("red", "\x1b[1;31m");
    color_table.insert("green", "\x1b[1;32m");
    color_table.insert("yellow", "\x1b[1;33m");
    color_table.insert("blue", "\x1b[1;34m");
    color_table.insert("magenta", "\x1b[1;35m");
    color_table.insert("cyan", "\x1b[1;36m");
    color_table.insert("white", "\x1b[1;37m");
    color_table.insert("reset", "\x1b[00m");

    return match color_table.get(color) {
        Some(color) => color,
        None => "\x1b[00m",
    };
}

fn main() {
    let matches = Command::new("print")
        .subcommand_required(false)
        .arg_required_else_help(false)
        .arg(
            Arg::new("color")
                .short('c')
                .long("color")
        );

    let arg_list = matches.get_matches();

    match arg_list.get_raw("color") {
        Some(color) => for raw_value in color {
            match raw_value.to_str() {
                Some(value) => {
                    print!("{}", apply_color(value));
                    print!("{}", print_clock_icon());
                    print!("{}", apply_color("reset"));
                },
                None => (),
            }
        },
        None => print!("{}", print_clock_icon()),
    };
}
