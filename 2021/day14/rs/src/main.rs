use std::{
    collections::HashMap,
    io::{stdin, Read},
};

#[derive(Debug, Clone)]
struct Problem {
    template: String,
    rules: HashMap<(u8, u8), u8>,
}

fn read_problem() -> Problem {
    let mut input = String::new();
    stdin().read_to_string(&mut input).unwrap();

    let (template, rules) = input.split_once("\n\n").unwrap();
    let rules = rules
        .lines()
        .map(|rule| {
            let (ab, c) = rule.split_once(" -> ").unwrap();
            let ab = ab.as_bytes();
            ((ab[0], ab[1]), c.as_bytes()[0])
        })
        .collect();
    Problem {
        template: template.into(),
        rules,
    }
}

fn solve(p: Problem, steps: usize) -> usize {
    let mut total_counts = HashMap::new();
    p.template
        .as_bytes()
        .iter()
        .for_each(|c| *total_counts.entry(c).or_insert(0) += 1);

    let mut pair_counts = HashMap::new();
    p.template
        .as_bytes()
        .windows(2)
        .for_each(|ab| *pair_counts.entry((ab[0], ab[1])).or_insert(0) += 1);

    for _ in 0..steps {
        let mut new_pairs = pair_counts.clone();
        for (&(a, b), count) in pair_counts.iter() {
            let c = p.rules.get(&(a, b)).unwrap();
            *new_pairs.entry((a, *c)).or_insert(0) += count;
            *new_pairs.entry((*c, b)).or_insert(0) += count;
            *new_pairs.entry((a, b)).or_insert(0) -= count;
            *total_counts.entry(c).or_insert(0) += count;
        }
        pair_counts = new_pairs;
    }
    let min = total_counts.values().min().unwrap();
    let max = total_counts.values().max().unwrap();

    max - min
}

fn main() {
    let problem = read_problem();
    println!("Part 1: {}", solve(problem.clone(), 10));
    println!("Part 2: {}", solve(problem, 40));
}
