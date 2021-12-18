use std::{
    cmp::{max, min},
    ops::RangeInclusive,
};

use itertools::Itertools;
use regex::Regex;

#[derive(Debug, Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Debug, Clone, Copy)]
struct Probe {
    xvel: i32,
    yvel: i32,
    pos: Point,
}

impl Probe {
    fn new(xvel: i32, yvel: i32) -> Self {
        Probe {
            xvel,
            yvel,
            pos: Point { x: 0, y: 0 },
        }
    }
}

#[derive(Debug, Clone)]
struct Target {
    x: RangeInclusive<i32>,
    y: RangeInclusive<i32>,
}

impl Target {
    fn new(x1: i32, x2: i32, y1: i32, y2: i32) -> Self {
        Target {
            x: min(x1, x2)..=max(x1, x2),
            y: min(y1, y2)..=max(y1, y2),
        }
    }
}

fn read_problem(line: &str) -> Target {
    let re = Regex::new(r".*x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)").unwrap();
    let m: Vec<i32> = re
        .captures(line)
        .unwrap()
        .iter()
        .skip(1)
        .map(|x| x.unwrap().as_str().parse().unwrap())
        .collect();
    Target::new(m[0], m[1], m[2], m[3])
}

fn step(p: Probe) -> Probe {
    Probe {
        xvel: max(p.xvel - 1, 0),
        yvel: p.yvel - 1,
        pos: Point {
            x: p.pos.x + p.xvel,
            y: p.pos.y + p.yvel,
        },
    }
}

fn simulate(mut p: Probe, t: &Target) -> Option<i32> {
    let mut max_ypos = 0;

    loop {
        if &p.pos.x > t.x.end() || &p.pos.y < t.y.start() {
            return None;
        }
        max_ypos = max(max_ypos, p.pos.y);
        if t.x.contains(&p.pos.x) && t.y.contains(&p.pos.y) {
            return Some(max_ypos);
        }
        p = step(p);
    }
}

fn solve(tgt: &Target) -> Vec<i32> {
    let &xmax = tgt.x.end();
    let &ymin = tgt.y.start();

    (0..=xmax)
        .cartesian_product(ymin..=-ymin)
        .filter_map(|(x, y)| simulate(Probe::new(x, y), &tgt))
        .collect()
}

fn part1(tgt: &Target) -> i32 {
    *solve(&tgt).iter().max().unwrap()
}

fn part2(tgt: &Target) -> usize {
    solve(&tgt).len()
}

fn main() {
    // let problem = read_problem("target area: x=20..30, y=-10..-5");
    let problem = read_problem("target area: x=60..94, y=-171..-136");
    println!("Part 1: {}", part1(&problem));
    println!("Part 2: {}", part2(&problem));
}
