use std::{
    collections::HashMap,
    io::{stdin, BufRead},
};

static D: [(isize, isize); 8] = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 1),
    (-1, -1),
    (1, -1),
    (-1, 1),
];
type Problem = HashMap<(isize, isize), u32>;

fn read_problem() -> Problem {
    let mut map = HashMap::new();
    for (i, line) in stdin().lock().lines().flatten().enumerate() {
        for (j, c) in line.char_indices() {
            map.insert((i as isize, j as isize), c.to_digit(10).unwrap());
        }
    }
    map
}

fn do_step(problem: &mut Problem) -> usize {
    let mut next: Vec<_> = problem.keys().copied().collect();
    while let Some((x, y)) = next.pop() {
        if let Some(o) = problem.get_mut(&(x, y)) {
            *o += 1;
            if *o == 10 {
                next.extend(D.iter().map(|(dx, dy)| (x + dx, y + dy)));
            }
        };
    }

    problem.values_mut().fold(0, |flashes, item| {
        if *item >= 10 {
            *item = 0;
            flashes + 1
        } else {
            flashes
        }
    })
}

fn part1(mut problem: Problem, steps: usize) -> usize {
    (0..steps).map(|_| do_step(&mut problem)).sum()
}

fn part2(mut problem: Problem) -> usize {
    (1..)
        .find(|_| do_step(&mut problem) == problem.len())
        .unwrap()
}

fn main() {
    let problem = read_problem();
    println!("Part 1: {}", part1(problem.clone(), 100));
    println!("Part 2: {}", part2(problem));
}
