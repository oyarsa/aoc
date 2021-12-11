use std::io::stdin;

use itertools::Itertools;

fn read_problem() -> Vec<isize> {
    let mut line = String::new();
    stdin().read_line(&mut line).unwrap();
    line.trim().split(',').flat_map(|x| x.parse()).collect()
}

fn median(mut s: Vec<isize>) -> isize {
    s.sort();
    s[s.len() / 2]
}

fn gauss(x1: isize, x2: isize) -> isize {
    let n = (x2 - x1).abs() + 1;
    (n * (n - 1)) / 2
}

fn part2(problem: &[isize]) -> isize {
    let (&min, &max) = problem.iter().minmax().into_option().unwrap();
    (min..=max)
        .map(|x| problem.iter().map(|&y| gauss(x, y)).sum())
        .min()
        .unwrap()
}

fn part1(problem: &[isize]) -> isize {
    let point = median(problem.to_owned());
    problem.iter().map(|x| (x - point).abs()).sum()
}

fn main() {
    let problem = read_problem();
    println!("Part 1: {}", part1(&problem));
    println!("Part 2: {}", part2(&problem));
}
