use std::io::{stdin, Read};

fn read_problem() -> Vec<Vec<String>> {
    let mut content = String::new();
    stdin().read_to_string(&mut content).unwrap();

    content
        .split("inp w\n")
        .skip(1)
        .map(|seg| seg.trim().lines().map(str::to_string).collect())
        .collect()
}

fn solve(segments: Vec<Vec<String>>) -> (i64, i64) {
    let mut max = [0; 14];
    let mut min = [0; 14];
    let mut stack = Vec::new();

    for (i, block) in segments.into_iter().enumerate() {
        match block[3].as_str() {
            "div z 1" => {
                let val = block[14].split_whitespace().last().unwrap();
                stack.push((i, val.parse::<i64>().unwrap()));
            }
            "div z 26" => {
                let (j, x) = stack.pop().unwrap();
                let val = block[4].split_whitespace().last().unwrap();
                let y = x + val.parse::<i64>().unwrap();

                if y > 0 {
                    max[i] = 9;
                    max[j] = 9 - y;
                    min[i] = 1 + y;
                    min[j] = 1;
                } else {
                    max[i] = 9 + y;
                    max[j] = 9;
                    min[i] = 1;
                    min[j] = 1 - y;
                }
            }
            _ => {}
        }
    }

    (digits_to_int(&max), digits_to_int(&min))
}

fn digits_to_int(digits: &[i64]) -> i64 {
    digits.iter().fold(0, |acc, x| acc * 10 + x)
}

fn main() {
    let segments = read_problem();
    let (max, min) = solve(segments);
    println!("Part 1: {}", max);
    println!("Part 2: {}", min);
}
