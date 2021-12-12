use std::{
    collections::{HashMap, HashSet},
    io::{stdin, BufRead},
};

struct Graph {
    adj_list: HashMap<String, Vec<String>>,
}

impl Graph {
    fn new() -> Self {
        Self {
            adj_list: HashMap::new(),
        }
    }

    fn add_edge(&mut self, src: &str, dst: &str) {
        self.adj_list
            .entry(src.to_string())
            .or_insert_with(Vec::new)
            .push(dst.to_string());
    }

    fn add(&mut self, b: &str, a: &str) {
        self.add_edge(a, b);
        self.add_edge(b, a);
    }

    fn adj(&self, node: &str) -> impl Iterator<Item = &String> {
        self.adj_list[node].iter()
    }
}

fn recur_walk<'a>(graph: &Graph, node: &'a str, mut seen: HashSet<&'a str>) -> usize {
    if seen.contains(&node) {
        return 0;
    }
    if node == "end" {
        return 1;
    }
    if node == node.to_lowercase() {
        seen.insert(node);
    }

    graph
        .adj(node)
        .map(|node| recur_walk(graph, node, seen.clone()))
        .sum()
}

fn recur_walk2<'a>(
    graph: &Graph,
    node: &'a str,
    mut seen: HashSet<&'a str>,
    mut double: bool,
) -> usize {
    if seen.contains(&node) {
        if double {
            return 0;
        } else {
            double = true;
        }
    }
    if node == "end" {
        return 1;
    }
    if node.chars().all(char::is_lowercase) {
        seen.insert(node);
    }

    graph
        .adj(node)
        .filter(|&node| node != "start")
        .map(|node| recur_walk2(graph, node, seen.clone(), double))
        .sum()
}

fn part1(graph: &Graph) -> usize {
    recur_walk(graph, "start", HashSet::new())
}

fn part2(graph: &Graph) -> usize {
    recur_walk2(graph, "start", HashSet::new(), false)
}

fn main() {
    let mut graph = Graph::new();
    for line in stdin().lock().lines().flatten() {
        let (src, dst) = line.split_once('-').unwrap();
        graph.add(src, dst);
    }
    println!("Part 1: {}", part1(&graph));
    println!("Part 2: {}", part2(&graph));
}
