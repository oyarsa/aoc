use std::{
    collections::{HashMap, HashSet},
    io::{stdin, Read},
};

use itertools::{iproduct, Itertools};
use ndarray::Array;
use ndarray_linalg::Determinant;
use once_cell::sync::Lazy;

type Matrix = ndarray::Array2<i32>;
type Vector = ndarray::Array1<i32>;

fn gen_rotation_matrices() -> Vec<Matrix> {
    let mut matrices = Vec::new();
    for t in [0, 1, 2].iter().permutations(3) {
        let (&x, &y, &z) = (t[0], t[1], t[2]);
        for (&sx, &sy, &sz) in iproduct!([-1, 1].iter(), [-1, 1].iter(), [-1, 1].iter()) {
            let mut m = Array::zeros((3, 3));
            m[[0, x]] = sx as f32;
            m[[1, y]] = sy as f32;
            m[[2, z]] = sz as f32;
            match m.det() {
                Ok(x) if x == 1.0 => matrices.push(m.mapv(|x| x as i32)),
                _ => {}
            }
        }
    }
    matrices
}

static ROTATIONS: Lazy<Vec<Matrix>> = Lazy::new(gen_rotation_matrices);

fn common(a: &[Vector], b: &[Vector]) -> Option<(Vec<Vector>, Vector)> {
    let set_a: HashSet<Vector> = a.iter().cloned().collect();

    for rot in ROTATIONS.iter() {
        let b_rot: Vec<_> = b.iter().map(|v| rot.dot(v)).collect();
        for point_a in a {
            for point_b in &b_rot {
                let delta = point_a - point_b;
                let new_b: Vec<_> = b_rot.iter().map(|pb| pb + &delta).collect();
                let set_b: HashSet<_> = new_b.iter().cloned().collect();
                if set_a.intersection(&set_b).count() >= 12 {
                    return Some((new_b, delta));
                }
            }
        }
    }
    None
}

#[allow(clippy::needless_range_loop)]
fn solve(scanners: Vec<Vec<Vector>>) -> (HashSet<Vector>, Vec<Vector>) {
    let n = scanners.len();
    let mut normalised = HashMap::from([(0, scanners[0].clone())]);
    let mut deltas = vec![Vector::zeros(3)];
    let mut left: HashSet<_> = (0..n).collect();

    while !left.is_empty() {
        for i in 0..n {
            if !normalised.contains_key(&i) || !left.contains(&i) {
                continue;
            }
            for j in 0..n {
                if i == j || normalised.contains_key(&j) {
                    continue;
                }
                if let Some((norm_beacons, delta)) = common(&normalised[&i], &scanners[j]) {
                    normalised.insert(j, norm_beacons);
                    deltas.push(delta);
                }
            }
            left.remove(&i);
        }
    }

    let beacons: HashSet<Vector> = normalised.into_values().flatten().collect();
    (beacons, deltas)
}

fn read_problem() -> Vec<Vec<Vector>> {
    let mut input = String::new();
    stdin().read_to_string(&mut input).unwrap();

    input
        .split("\n\n")
        .map(|scanner| {
            scanner
                .lines()
                .skip(1) // scanner name
                .map(|line| line.split(',').map(|x| x.parse().unwrap()).collect())
                .collect()
        })
        .collect()
}

fn main() {
    let problem = read_problem();

    let (beacons, deltas) = solve(problem);
    println!("Part 1: {}", beacons.len());
    let maxd = deltas
        .iter()
        .cartesian_product(deltas.iter())
        .map(|(a, b)| (a - b).mapv(|x| x.abs()).sum())
        .max()
        .unwrap();
    println!("Part 2: {}", maxd);
}
