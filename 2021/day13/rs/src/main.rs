use std::{
    collections::HashSet,
    io::{stdin, Read},
};

use regex::Regex;

type Grid = HashSet<(i32, i32)>;

#[derive(Clone, Debug)]
struct Problem {
    grid: Grid,
    folds: Vec<(String, i32)>,
}

fn read_problem() -> Problem {
    let mut input = String::new();
    stdin().read_to_string(&mut input).unwrap();

    let (coords_input, folds_input) = input.split_once("\n\n").unwrap();
    let grid: Grid = coords_input
        .lines()
        .map(|line| {
            let (x, y) = line.split_once(',').unwrap();
            (x.parse().unwrap(), y.parse().unwrap())
        })
        .collect();

    let re = Regex::new(r"fold along ([xy])=(\d+)").unwrap();
    let folds: Vec<(String, i32)> = re
        .captures_iter(folds_input)
        .map(|x| {
            (
                x.get(1).unwrap().as_str().into(),
                x.get(2).unwrap().as_str().parse().unwrap(),
            )
        })
        .collect();

    Problem { grid, folds }
}

fn print_grid(grid: &Grid) {
    let max_x = grid.iter().map(|p| p.0).max().unwrap();
    let max_y = grid.iter().map(|p| p.1).max().unwrap();

    for y in 0..=max_y {
        for x in 0..=max_x {
            let char = if grid.contains(&(x, y)) { "░" } else { " " };
            print!("{}", char);
        }
        println!();
    }
}

fn fold(grid: Grid, (dir, pos): (String, i32)) -> Grid {
    grid.into_iter()
        .map(|(x, y)| match dir.as_str() {
            "y" => {
                if y > pos {
                    (x, 2 * pos - y)
                } else {
                    (x, y)
                }
            }
            "x" => {
                if x > pos {
                    (2 * pos - x, y)
                } else {
                    (x, y)
                }
            }
            _ => unreachable!(),
        })
        .collect()
}

fn do_folds(problem: Problem, n: Option<usize>) -> Grid {
    let n = n.unwrap_or(problem.folds.len());
    problem.folds.into_iter().take(n).fold(problem.grid, fold)
}

fn part1(problem: Problem) -> usize {
    do_folds(problem, Some(1)).len()
}

fn part2(problem: Problem) {
    let grid = do_folds(problem, None);
    print_grid(&grid);
}

fn main() {
    let problem = read_problem();
    println!("Part 1: {}", part1(problem.clone()));
    println!("Part 2");
    part2(problem);
}
