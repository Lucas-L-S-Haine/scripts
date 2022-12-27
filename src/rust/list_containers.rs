use std::env::args;
use std::process::Command;
use std::collections::VecDeque;
use comfy_table::Table;

const UTF8_SOLID_LINES: &'static str = "││──├─┼┤│    ┬┴┌┐└┘";

fn main() {
    let mut argv = VecDeque::new();

    for argument in args() {
        if argument != "ps" {
            argv.push_back(argument);
        }
    }

    argv.pop_front();

    let docker_command = Command::new("docker")
        .arg("ps")
        .args(argv)
        .args(["--format",
               "table{{.ID}};;{{.Names}};;{{.Image}};;{{.Status}}"])
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
