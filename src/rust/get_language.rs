use std::fs;
use std::str;

fn main() {
    let dir_content = fs::read_dir(".")
        .expect("Cannot read directory content");

    for entry in dir_content {
        match entry {
            Ok(file) => {
                let file_name: String = match file.file_name().to_str() {
                    Some(name) => str::replace(name, "\"", ""),
                    None => String::from(""),
                };

                print!("{} ", file_name);
            },
            Err(_) => panic!("Error reading file"),
        }
    }

    println!();
}
