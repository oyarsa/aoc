use std::{
    collections::HashMap,
    io::{stdin, BufRead},
};

#[derive(Clone, PartialEq)]
struct Map {
    grid: HashMap<(usize, usize), char>,
    n: usize,
    m: usize,
}

fn read_problem() -> Map {
    let mut grid = HashMap::new();
    for (i, line) in stdin().lock().lines().flatten().enumerate() {
        for (j, c) in line.char_indices() {
            grid.insert((i, j), c);
        }
    }
    let n = grid.keys().map(|(i, _)| i).max().unwrap() + 1;
    let m = grid.keys().map(|(_, j)| j).max().unwrap() + 1;
    Map { grid, n, m }
}

fn step_east(map: Map) -> Map {
    let mut new_grid = map.grid.clone();
    for (&(i, j), &c) in map.grid.iter() {
        if c != '>' {
            continue;
        }
        let next_j = (j + 1) % map.m;
        if map.grid[&(i, next_j)] == '.' {
            new_grid.insert((i, next_j), '>');
            new_grid.insert((i, j), '.');
        }
    }
    Map {
        grid: new_grid,
        n: map.n,
        m: map.m,
    }
}

fn step_south(map: Map) -> Map {
    let mut new_grid = map.grid.clone();
    for (&(i, j), &c) in map.grid.iter() {
        if c != 'v' {
            continue;
        }
        let next_i = (i + 1) % map.n;
        if map.grid[&(next_i, j)] == '.' {
            new_grid.insert((next_i, j), 'v');
            new_grid.insert((i, j), '.');
        }
    }
    Map {
        grid: new_grid,
        n: map.n,
        m: map.m,
    }
}

fn step(mut m: Map) -> Map {
    m = step_east(m);
    m = step_south(m);
    m
}

fn solve(m: Map) -> usize {
    let mut old = m;
    let mut i = 0;
    loop {
        i += 1;
        let new = step(old.clone());
        if new == old {
            break i;
        }
        old = new;
    }
}

fn main() {
    let p = read_problem();
    println!("Part 1: {}", solve(p));
}
