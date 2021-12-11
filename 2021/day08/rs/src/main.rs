use std::{
    collections::{HashMap, HashSet},
    io::{stdin, BufRead},
};

use itertools::Itertools;

struct Problem {
    input: Vec<String>,
    output: Vec<String>,
}

fn read_problem() -> Vec<Problem> {
    stdin()
        .lock()
        .lines()
        .flatten()
        .map(|line| {
            let (input, output) = line.split_once(" | ").unwrap();
            Problem {
                input: input.split_whitespace().map(str::to_string).collect(),
                output: output.split_whitespace().map(str::to_string).collect(),
            }
        })
        .collect()
}

fn part1(problems: &[Problem]) -> usize {
    problems
        .iter()
        .map(|p| {
            p.output
                .iter()
                .filter(|o| [2, 4, 3, 7].contains(&o.len()))
                .count()
        })
        .sum()
}

fn decode_dictionary(input: &[String]) -> HashMap<String, char> {
    let mut digits = HashMap::new();
    let (mut five_len, mut six_len) = (vec![], vec![]);

    let digit_to_charset = |digit: &str| digit.chars().collect();
    for digit in input.iter() {
        if digit.len() == 2 {
            digits.insert('1', digit_to_charset(digit));
        } else if digit.len() == 4 {
            digits.insert('4', digit_to_charset(digit));
        } else if digit.len() == 3 {
            digits.insert('7', digit_to_charset(digit));
        } else if digit.len() == 7 {
            digits.insert('8', digit_to_charset(digit));
        } else if digit.len() == 5 {
            five_len.push(digit_to_charset(digit));
        } else if digit.len() == 6 {
            six_len.push(digit_to_charset(digit));
        }
    }

    let ncommon = |a: &HashSet<char>, b: &HashSet<char>| a.intersection(b).count();
    for digit in five_len.into_iter() {
        if ncommon(&digit, &digits[&'1']) == 1 && ncommon(&digit, &digits[&'4']) == 2 {
            digits.insert('2', digit);
        } else if ncommon(&digit, &digits[&'7']) == 3 {
            digits.insert('3', digit);
        } else if ncommon(&digit, &digits[&'1']) == 1 && ncommon(&digit, &digits[&'4']) == 3 {
            digits.insert('5', digit);
        }
    }

    for digit in six_len.into_iter() {
        if ncommon(&digit, &digits[&'1']) == 1 {
            digits.insert('6', digit);
        } else if ncommon(&digit, &digits[&'4']) == 4 {
            digits.insert('9', digit);
        } else if ncommon(&digit, &digits[&'4']) == 3 {
            digits.insert('0', digit);
        }
    }

    digits
        .into_iter()
        .map(|(k, v)| (v.into_iter().sorted().collect(), k))
        .collect()
}

fn part2(problem: Vec<Problem>) -> usize {
    problem
        .into_iter()
        .flat_map(|p| {
            let decoded = decode_dictionary(&p.input);
            p.output
                .into_iter()
                .map(|digit| decoded[&digit.chars().sorted().collect::<String>()])
                .collect::<String>()
                .parse::<usize>()
        })
        .sum()
}

fn main() {
    let problems = read_problem();
    println!("Part 1: {}", part1(&problems));
    println!("Part 2: {}", part2(problems));
}
