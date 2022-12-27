use std::env::args;
use std::process::Command;
use std::collections::VecDeque;
use comfy_table::Table;
use regex::Regex;

const UTF8_SOLID_LINES: &'static str = "││──├─┼┤│    ┬┴┌┐└┘";

fn has_format(argument: &String) -> bool {
    let re = Regex::new(r"^--format").unwrap();
    return re.is_match(argument.as_str());
}

fn main() {
    let mut argv = VecDeque::new();

    let mut has_format_argument: bool = false;

    for argument in args() {
        if has_format(&argument) {
            has_format_argument = true;
        }
        if argument != "ps" {
            argv.push_back(argument);
        }
    }

    argv.pop_front();
    if !has_format_argument {
        argv.push_back("--format".to_string());
        argv.push_back("table{{.ID}};;{{.Names}};;{{.Image}};;{{.Status}}"
            .to_string());
    }

    let docker_command = Command::new("docker")
        .arg("ps")
        .args(argv)
        .output()
        .expect("failed to execute process");

    let stdout = String::from_utf8(docker_command.stdout);

    let mut command_output = match stdout {
        Ok(output) => output,
        Err(error) => panic!("{:?}", error),
    };

    command_output.pop();

    let mut output_lines: Vec<&str> = vec![];
    let lines: Vec<&str> = command_output.split("\n").collect();
    for line in &lines {
        output_lines.push(line);
    }

    let mut result: Vec<Vec<&str>> = vec![];
    for line in &output_lines {
        result.push(line.split(";;").collect());
    }

    let mut table = Table::new();
    table.load_preset(UTF8_SOLID_LINES);
    for (line_index, line) in result.iter().enumerate() {
        if line_index == 0 {
            table.set_header(line);
        } else {
            table.add_row(line);
        }
    }

    println!("{}", table);
}
