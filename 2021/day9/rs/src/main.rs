mod pad;
use std::io::{stdin, BufRead};

use itertools::Itertools;
use ndarray::Array2;
use pad::pad_2d;

type Problem = Array2<u32>;

static D: [(isize, isize); 4] = [(1, 0), (0, -1), (-1, 0), (0, 1)];

fn main() {
    let stdin = stdin();
    let arr: Vec<Vec<u32>> = stdin
        .lock()
        .lines()
        .flatten()
        .map(|l| l.chars().flat_map(|c| c.to_digit(10)).collect())
        .collect();
    let shape = (arr.len(), arr[0].len());
    let arr: Vec<u32> = arr.into_iter().flatten().collect();
    let arr = Array2::from_shape_vec(shape, arr).unwrap();
    let arr = pad_2d(&arr, 1, 9);

    println!("Part 1: {}", part1(arr.clone()));
    println!("Part 2: {}", part2(arr));
}

fn find_lowest_points(problem: &Problem) -> Vec<(usize, usize)> {
    let (n, m) = problem.dim();
    (1..n - 1)
        .cartesian_product(1..m - 1)
        .filter(|&(i, j)| {
            let min = D
                .iter()
                .map(|&(dx, dy)| problem[[d(i, dy), d(j, dx)]])
                .min()
                .unwrap();
            problem[[i, j]] < min
        })
        .collect()
}

fn part1(problem: Problem) -> u32 {
    find_lowest_points(&problem)
        .into_iter()
        .map(|(i, j)| problem[[i, j]] + 1)
        .sum()
}

fn search(problem: &mut Problem, i: usize, j: usize) -> usize {
    if problem[[i, j]] == 9 {
        0
    } else {
        problem[[i, j]] = 9;
        1 + D
            .iter()
            .map(|&(dx, dy)| search(problem, d(i, dy), d(j, dx)))
            .sum::<usize>()
    }
}

fn part2(mut problem: Problem) -> usize {
    find_lowest_points(&problem)
        .into_iter()
        .map(|(i, j)| search(&mut problem, i, j))
        .sorted()
        .rev()
        .take(3)
        .product()
}

fn d(a: usize, b: isize) -> usize {
    (a as isize - b) as usize
}
