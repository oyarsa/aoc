use std::{
    cmp::Ordering,
    collections::{BinaryHeap, HashMap},
    io::{stdin, BufRead},
};

type Pair = (i32, i32);
type Graph = HashMap<Pair, i32>;

fn neighbours((y, x): Pair) -> impl Iterator<Item = Pair> {
    let directions = [(1, 0), (0, 1), (-1, 0), (0, -1)];
    directions.into_iter().map(move |(dy, dx)| (y + dy, x + dx))
}

fn get_n_m(graph: &Graph) -> Pair {
    let n = graph.keys().map(|(y, _)| y).max().unwrap() + 1;
    let m = graph.keys().map(|(_, x)| x).max().unwrap() + 1;
    (n, m)
}

#[derive(Copy, Clone, Eq, PartialEq)]
struct Item {
    cost: i32,
    point: Pair,
}

impl Ord for Item {
    fn cmp(&self, other: &Self) -> Ordering {
        other
            .cost
            .cmp(&self.cost)
            .then_with(|| self.point.cmp(&other.point))
    }
}

impl PartialOrd for Item {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Item {
    fn new(point: Pair, cost: i32) -> Self {
        Self { cost, point }
    }
}

fn djikstra(graph: &Graph, start: Pair, end: Pair) -> HashMap<Pair, i32> {
    let mut dist: HashMap<Pair, i32> = graph.keys().map(|&k| (k, i32::MAX)).collect();
    let mut pq = BinaryHeap::new();

    dist.insert(start, 0);
    pq.push(Item::new(start, 0));

    while let Some(Item { cost, point: u }) = pq.pop() {
        if u == end {
            return dist;
        }
        if cost > dist[&u] {
            continue;
        }
        for v in neighbours(u).filter(|v| graph.contains_key(v)) {
            let alt = dist[&u] + graph[&v];
            if alt < dist[&v] {
                dist.insert(v, alt);
                pq.push(Item::new(v, alt));
            }
        }
    }

    dist
}

fn read_problem() -> Graph {
    stdin()
        .lock()
        .lines()
        .flatten()
        .enumerate()
        .flat_map(|(i, line)| {
            line.chars()
                .enumerate()
                .map(|(j, val)| ((i as i32, j as i32), val.to_digit(10).unwrap() as i32))
                .collect::<Vec<_>>()
        })
        .collect()
}

fn replicate_map(mut graph: Graph) -> Graph {
    let (n, m) = get_n_m(&graph);
    for ix in 0..5 {
        for jx in 0..5 {
            for i in 0..n {
                for j in 0..m {
                    let key = (ix * n + i, jx * m + j);
                    let val = (ix + jx + graph[&(i, j)] - 1) % 9 + 1;
                    graph.insert(key, val);
                }
            }
        }
    }
    graph
}

fn solve(problem: &Graph) -> i32 {
    let (n, m) = get_n_m(problem);
    let (start, end) = ((0, 0), (n - 1, m - 1));
    let dist = djikstra(problem, start, end);
    dist[&end]
}

fn main() {
    let problem = read_problem();
    println!("Part 1: {}", solve(&problem));
    println!("Part 2: {}", solve(&replicate_map(problem)));
}
