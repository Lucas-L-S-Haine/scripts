use chrono::{Local,Timelike};

fn main() {
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
        _ => ' ',
    };

    println!("{}", clock_icon);
}
