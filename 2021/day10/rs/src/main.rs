use std::io::{stdin, BufRead};

use itertools::Itertools;
use maplit::hashmap;

fn part1_score(line: &str) -> usize {
    let matches = hashmap! { '('=> ')', '<'=> '>', '{'=> '}', '['=> ']' };
    let scores = hashmap! { ')' => 3, ']' => 57, '}' => 1197, '>' => 25137 };
    let mut stack = vec![];
    for char in line.chars() {
        if "([{<".contains(char) {
            stack.push(char);
        } else if char != matches[&stack.pop().unwrap()] {
            return scores[&char];
        }
    }
    0
}

fn part1(problem: &[String]) -> usize {
    problem.iter().map(|s| part1_score(s)).sum()
}

fn part2_score(line: &str) -> usize {
    let scores = hashmap! { '(' => 1, '[' => 2, '{' => 3, '<' => 4 };
    let mut stack = vec![];
    for char in line.chars() {
        if "([{<".contains(char) {
            stack.push(char);
        } else {
            stack.pop();
        }
    }
    stack
        .iter()
        .rev()
        .fold(0, |score, char| 5 * score + scores[char])
}

fn part2(problem: &[String]) -> usize {
    let scores: Vec<_> = problem
        .iter()
        .filter(|l| part1_score(l) == 0)
        .map(|l| part2_score(l))
        .sorted()
        .collect();
    scores[scores.len() / 2]
}

fn main() {
    let problem: Vec<_> = stdin().lock().lines().flatten().collect();
    println!("Part 1: {}", part1(&problem));
    println!("Part 2: {}", part2(&problem));
}
