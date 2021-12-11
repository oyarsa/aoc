use std::io::{stdin, BufRead};

#[derive(Debug, Clone)]
enum Direction {
    Forward(i32),
    UpDown(i32),
}

#[derive(Debug)]
struct Submarine1 {
    horizontal: i32,
    depth: i32,
}

impl Submarine1 {
    fn new() -> Self {
        Self {
            horizontal: 0,
            depth: 0,
        }
    }
    fn update(self, dir: Direction) -> Self {
        match dir {
            Direction::Forward(x) => Self {
                horizontal: self.horizontal + x,
                ..self
            },
            Direction::UpDown(x) => Self {
                depth: self.depth + x,
                ..self
            },
        }
    }
}

#[derive(Debug)]
struct Submarine2 {
    horizontal: i32,
    depth: i32,
    aim: i32,
}

impl Submarine2 {
    fn new() -> Self {
        Self {
            horizontal: 0,
            depth: 0,
            aim: 0,
        }
    }
    fn update(self, dir: Direction) -> Self {
        match dir {
            Direction::Forward(x) => Self {
                horizontal: self.horizontal + x,
                depth: self.depth + x * self.aim,
                ..self
            },
            Direction::UpDown(x) => Self {
                aim: self.aim + x,
                ..self
            },
        }
    }
}

fn read_input() -> Vec<Direction> {
    let stdin = stdin();

    stdin
        .lock()
        .lines()
        .map(|l| {
            let l = l.expect("Couldn't read line");
            let (dir, val) = l.split_once(' ').expect("Invalid line");
            let val = val.parse().expect("Invalid value");
            match dir.as_ref() {
                "forward" => Direction::Forward(val),
                "down" => Direction::UpDown(val),
                "up" => Direction::UpDown(-val),
                _ => unreachable!(),
            }
        })
        .collect()
}

fn part1(dirs: Vec<Direction>) -> i32 {
    let end = dirs
        .into_iter()
        .fold(Submarine1::new(), |sub, dir| sub.update(dir));
    end.depth * end.horizontal
}

fn part2(dirs: Vec<Direction>) -> i32 {
    let end = dirs
        .into_iter()
        .fold(Submarine2::new(), |sub, dir| sub.update(dir));
    end.depth * end.horizontal
}

fn main() {
    let problem = read_input();
    println!("Part 1 {}", part1(problem.clone()));
    println!("Part 2 {}", part2(problem));
}
