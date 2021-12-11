use std::{
    cmp::{max, min},
    io::{stdin, BufRead},
    ops::AddAssign,
};

use ndarray::{s, Array, Array2};
use regex::Regex;

type Coord = (isize, isize);
type Line = (Coord, Coord);
type Matrix = Array2<u8>;

fn read_problem() -> Vec<Line> {
    let stdin = stdin();
    stdin
        .lock()
        .lines()
        .flatten()
        .map(|line| {
            let re = Regex::new(r"(\d+),(\d+) -> (\d+),(\d+)").unwrap();
            let xs: Vec<_> = re
                .captures(&line)
                .unwrap()
                .iter()
                .flat_map(|x| x.unwrap().as_str().parse())
                .collect();
            ((xs[0], xs[1]), (xs[2], xs[3]))
        })
        .collect()
}

fn fill_lines(mut m: Matrix, line: &Line, diagonal: bool) -> Matrix {
    let ((x1, y1), (x2, y2)) = (min(line.0, line.1), max(line.0, line.1));

    if x1 == x2 {
        let (y1, y2) = (min(y1, y2), max(y1, y2));
        m.slice_mut(s![y1..=y2, x1]).add_assign(1);
    } else if y1 == y2 {
        let (x1, x2) = (min(x1, x2), max(x1, x2));
        m.slice_mut(s![y1, x1..=x2]).add_assign(1);
    } else if diagonal {
        let step = (y2 - y1).signum();
        for i in 0..(y1 - y2).abs() {
            let y = y1 + i * step;
            let x = x1 + i;
            m[[y as usize, x as usize]] += 1
        }
    }

    m
}

fn get_dim(lines: &[Line]) -> usize {
    *lines
        .iter()
        .flat_map(|((x1, _), (x2, _))| vec![x1, x2])
        .max()
        .unwrap() as usize
        + 1
}

fn solve(lines: &[Line], part: u8) -> usize {
    let dim = get_dim(lines);
    lines
        .iter()
        .fold(Array::zeros((dim, dim)), |m, l| fill_lines(m, l, part == 2))
        .mapv(|x| (x >= 2) as usize)
        .sum()
}

fn main() {
    let lines = read_problem();
    println!("Part 1: {}", solve(&lines, 1));
    println!("Part 2: {}", solve(&lines, 2));
}
