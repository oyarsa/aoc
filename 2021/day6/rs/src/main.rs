use std::io::stdin;

fn read_problem() -> Vec<usize> {
    let mut line = String::new();
    stdin().read_line(&mut line).unwrap();
    line.trim().split(',').flat_map(|x| x.parse()).collect()
}

fn solve<'a>(problem: impl Iterator<Item = &'a usize>, ndays: usize) -> usize {
    let mut cur = [0; 9];
    problem.for_each(|&i| cur[i] += 1);

    for _ in 0..ndays {
        cur.rotate_left(1);
        cur[6] += cur[8];
    }

    cur.iter().sum()
}

fn main() {
    let problem = read_problem();
    println!("Part 1: {}", solve(problem.iter(), 80));
    println!("Part 2: {}", solve(problem.iter(), 256));
}
