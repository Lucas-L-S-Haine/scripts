use std::env;
use std::fs;
use comfy_table::Table;

const UTF8_SOLID_LINES: &'static str = "││──├─┼┤│    ┬┴┌┐└┘";

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];

    let mut content_str = fs::read_to_string(file_path)
        .expect("File can't be read");

    content_str = String::from(content_str.trim());

    let mut content_lines = vec![];
    for line in content_str.split("\n") {
        content_lines.push(line);
    }

    let mut table = Table::new();
    table.load_preset(UTF8_SOLID_LINES);
    for (line_index, line) in content_lines.into_iter().enumerate() {
        if line_index == 0 {
            table.set_header(line.split(","));
        } else {
            table.add_row(line.split(","));
        }
    }

    println!("{}", table);
}
