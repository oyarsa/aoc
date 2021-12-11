use std::io::{stdin, BufRead};

fn read() -> Vec<Vec<char>> {
    let stdin = stdin();
    stdin
        .lock()
        .lines()
        .flat_map(|r| r.map(|l| l.chars().collect()))
        .collect()
}

fn transpose(v: Vec<Vec<char>>) -> Vec<Vec<char>> {
    let m = v[0].len();
    let n = v.len();
    let mut t: Vec<Vec<char>> = vec![vec![]; m];

    for j in 0..m {
        t[j] = vec![' '; n];
        for i in 0..n {
            t[j][i] = v[i][j];
        }
    }

    return t;
}

fn most_least_common(v: &[char]) -> (char, char) {
    let mut count = [0, 0];
    for c in v {
        match c {
            '0' => count[0] += 1,
            '1' => count[1] += 1,
            _ => unreachable!(),
        }
    }
    if count[0] > count[1] {
        ('0', '1')
    } else {
        ('1', '0')
    }
}

fn charvec_to_bin(v: &[char]) -> usize {
    let s: String = v.iter().collect();
    usize::from_str_radix(&s, 2).unwrap()
}

fn filter_numbers(numbers: Vec<Vec<char>>, pos: usize, bin: char) -> Vec<Vec<char>> {
    let mut out = vec![];
    for row in numbers {
        if row[pos] == bin {
            out.push(row);
        }
    }
    out
}

fn oxygen_rating(mut data: Vec<Vec<char>>) -> usize {
    for j in 0..data.len() {
        let cols = transpose(data.clone());
        let (most, _) = most_least_common(&cols[j]);
        data = filter_numbers(data, j, most);
        if data.len() == 1 {
            return charvec_to_bin(&data[0]);
        }
    }
    unreachable!()
}

fn scrubber_rating(mut data: Vec<Vec<char>>) -> usize {
    for j in 0..data.len() {
        let cols = transpose(data.clone());
        let (_, least) = most_least_common(&cols[j]);
        data = filter_numbers(data, j, least);
        if data.len() == 1 {
            return charvec_to_bin(&data[0]);
        }
    }
    unreachable!()
}

fn part1(data: &Vec<Vec<char>>) {
    let data = data.clone();
    let data = transpose(data);
    let mut gamma = vec![];
    let mut epsilon = vec![];

    for r in data {
        let (most, least) = most_least_common(&r);
        gamma.push(most);
        epsilon.push(least);
    }

    let gamma = charvec_to_bin(&gamma);
    let epsilon = charvec_to_bin(&epsilon);
    println!("Part 1: {}", gamma * epsilon);
}

fn part2(data: &Vec<Vec<char>>) {
    let data = data.clone();
    let oxy = oxygen_rating(data.clone());
    let scr = scrubber_rating(data);
    println!("Part 2: {}", oxy * scr);
}

fn main() {
    let data = read();
    part1(&data);
    part2(&data);
}
