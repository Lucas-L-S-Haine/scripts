use std::env::args;

fn main() {
    let mut argv: Vec<String> = vec![];

    for argument in args() {
        argv.push(argument);
    }

    println!("{:?}", argv);
}
