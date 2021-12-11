use std::{
    collections::HashSet,
    fmt::Display,
    io::{stdin, BufRead},
};

use ndarray::{iter::Lanes, Array, Array2, Dim};

#[derive(Clone)]
struct Problem {
    draw: Vec<usize>,
    boards: Vec<Board>,
}

#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
enum Piece {
    Marked(usize),
    Unmarked(usize),
}

impl Piece {
    fn new(i: usize) -> Self {
        Piece::Unmarked(i)
    }
    fn mark_eq(self, piece: usize) -> Self {
        match self {
            Piece::Unmarked(s) if s == piece => Piece::Marked(s),
            _ => self,
        }
    }
    fn is_marked(&self) -> bool {
        matches!(self, Piece::Marked(_))
    }
    fn value(&self) -> usize {
        match self {
            Piece::Marked(_) => 0,
            Piece::Unmarked(s) => *s,
        }
    }
}

impl Display for Piece {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Piece::Marked(s) => write!(f, "*{:>2}*", s),
            Piece::Unmarked(s) => write!(f, " {:>2} ", s),
        }
    }
}

impl Display for Board {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for row in self.0.rows() {
            writeln!(f, "{}", join(row.as_slice().unwrap(), " "))?;
        }
        Ok(())
    }
}

fn join(v: &[impl Display], sep: &str) -> String {
    v.iter()
        .map(|x| x.to_string())
        .collect::<Vec<_>>()
        .join(sep)
}

impl Display for Problem {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "{}", join(&self.draw, ","))?;
        writeln!(f, "{}", join(&self.boards, "\n"))?;
        Ok(())
    }
}

#[derive(Clone)]
struct Board(Array2<Piece>);

impl Board {
    fn mark_piece(&self, piece: usize) -> Self {
        Board(self.0.mapv(|p| p.mark_eq(piece)))
    }
}

fn read_board(lines: &mut impl Iterator<Item = String>) -> Board {
    let board = lines.take(5).flat_map(|row| {
        row.split_whitespace()
            .map(|x| Piece::new(x.parse().unwrap()))
            .collect::<Vec<_>>()
    });
    Board(Array::from_iter(board).into_shape((5, 5)).unwrap())
}

fn read() -> Problem {
    let stdin = stdin();

    let mut lines = stdin.lock().lines().flatten();
    let draw: Vec<usize> = lines
        .next()
        .unwrap()
        .split(',')
        .map(|x| x.parse().unwrap())
        .collect();

    let mut boards = vec![];
    while let Some(_) = lines.next() {
        boards.push(read_board(&mut lines));
    }

    Problem { draw, boards }
}

fn is_winner(b: &Board) -> bool {
    let check = |lane: Lanes<Piece, Dim<[usize; 1]>>| {
        lane.into_iter().any(|i| i.iter().all(|x| x.is_marked()))
    };
    check(b.0.rows()) || check(b.0.columns())
}

fn sum_of_unmarked(b: &Board) -> usize {
    b.0.iter().map(|x| x.value()).sum()
}

fn part1(problem: Problem) {
    let mut boards = problem.boards;
    for piece in problem.draw {
        for b in &mut boards {
            *b = b.mark_piece(piece);
            if is_winner(b) {
                println!("Part 1: {}", sum_of_unmarked(b) * piece);
                return;
            }
        }
    }
}

fn part2(problem: Problem) {
    let mut boards = problem.boards;
    let nboards = boards.len();
    let mut won = HashSet::new();
    for piece in problem.draw {
        for (i, b) in boards.iter_mut().enumerate() {
            *b = b.mark_piece(piece);
            if won.contains(&i) || !is_winner(b) {
                continue;
            }
            won.insert(i);
            if won.len() == nboards {
                println!("Part 2: {}", sum_of_unmarked(b) * piece);
                return;
            }
        }
    }
}

fn main() {
    let p = read();
    part1(p.clone());
    part2(p);
}
