use std::io::BufRead;

fn read_input() -> Vec<i32> {
    let stdin = std::io::stdin();

    stdin
        .lock()
        .lines()
        .into_iter()
        .map(|x| x.unwrap().parse().unwrap())
        .collect()
}

fn part1(lines: Vec<i32>) -> usize {
    lines.windows(2).filter(|p| p[0] < p[1]).count()
}

fn part2(lines: Vec<i32>) -> usize {
    let windows: Vec<i32> = lines.windows(3).map(|p| p.iter().sum()).collect();
    windows.windows(2).filter(|p| p[0] < p[1]).count()
}

fn main() {
    let lines = read_input();
    println!("Part 1: {}", part1(lines.clone()));
    println!("Part 2: {}", part2(lines.clone()));
}
