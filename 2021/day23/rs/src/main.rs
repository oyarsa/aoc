use std::{
    cmp::Ordering,
    collections::{BinaryHeap, HashMap, HashSet},
    hash::Hash,
    io::{stdin, Read},
};

use itertools::Itertools;

use once_cell::sync::Lazy;

static HALL: [usize; 7] = [0, 1, 5, 9, 13, 17, 18];
static DEST: [[usize; 4]; 4] = [
    [3, 4, 19, 20],   // 0 (A)
    [7, 8, 21, 22],   // 1 (B)
    [11, 12, 23, 24], // 2 (C)
    [15, 16, 25, 26], // 3 (D)
];
static NEIGHBOURS: Lazy<[Vec<usize>; 27]> = Lazy::new(|| {
    [
        vec![1],          // 0
        vec![0, 2],       // 1
        vec![1, 3, 5],    // 2
        vec![2, 4],       // 3
        vec![3, 19],      // 4
        vec![2, 6],       // 5
        vec![5, 7, 9],    // 6
        vec![6, 8],       // 7
        vec![7, 21],      // 8
        vec![6, 10],      // 9
        vec![9, 11, 13],  // 10
        vec![10, 12],     // 11
        vec![11, 23],     // 12
        vec![10, 14],     // 13
        vec![13, 15, 17], // 14
        vec![14, 16],     // 15
        vec![15, 25],     // 16
        vec![14, 18],     // 17
        vec![17],         // 18
        vec![4, 20],      // 19
        vec![19],         // 20
        vec![8, 22],      // 21
        vec![21],         // 22
        vec![12, 24],     // 23
        vec![23],         // 24
        vec![16, 26],     // 25
        vec![25],         // 26
    ]
});

type Index = usize;
type Cost = usize;
type Positions = [Amphi; 27];

#[derive(Clone, Copy, PartialEq, Eq, Hash)]
enum Amphi {
    A,
    B,
    C,
    D,
    O,
}

impl Amphi {
    fn weight(self) -> usize {
        match self {
            Amphi::A => 1,
            Amphi::B => 10,
            Amphi::C => 100,
            Amphi::D => 1000,
            Amphi::O => panic!("Called Amphi::weight on open position"),
        }
    }

    fn is_open(self) -> bool {
        matches!(self, Amphi::O)
    }
}

impl From<char> for Amphi {
    fn from(c: char) -> Self {
        match c {
            '.' => Amphi::O,
            'A' => Amphi::A,
            'B' => Amphi::B,
            'C' => Amphi::C,
            'D' => Amphi::D,
            c => panic!("Invalid character for Amphi: {}", c),
        }
    }
}

impl From<Amphi> for &str {
    fn from(a: Amphi) -> Self {
        match a {
            Amphi::A => "A",
            Amphi::B => "B",
            Amphi::C => "C",
            Amphi::D => "D",
            Amphi::O => ".",
        }
    }
}

#[derive(Clone, PartialEq, Eq, Hash)]
struct State {
    cost: Cost,
    positions: Positions,
}

impl State {
    fn new(cost: Cost, positions: Positions) -> Self {
        Self { cost, positions }
    }

    fn is_final(&self) -> bool {
        use Amphi::*;
        #[rustfmt::skip]
        let final_pos = [
            O, O, O, A, A, O, O, B, B, O, O, C, C, O, O, D, D, O, O,
            A, A, B, B, C, C, D, D,
        ];
        self.positions == final_pos
    }
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other.cost.cmp(&self.cost)
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn replace(pos: &Positions, old: Index, new: Index, amphi: Amphi) -> Positions {
    let mut new_pos = *pos;
    new_pos[old] = Amphi::O;
    new_pos[new] = amphi;
    new_pos
}

fn calc_cost(pos: &Positions, old: Index, new: Index, amphi: Amphi) -> Cost {
    let c = dfs(pos, old, new).unwrap();
    c * amphi.weight()
}

fn do_move(state: &State, old_pos: Index, new_pos: Index, amphi: Amphi) -> State {
    State::new(
        state.cost + calc_cost(&state.positions, old_pos, new_pos, amphi),
        replace(&state.positions, old_pos, new_pos, amphi),
    )
}

fn is_valid(pos: &Positions, i: Index, j: Index) -> bool {
    dfs(pos, i, j).is_some()
}

fn dfs_(seen: &mut HashSet<Index>, pos: &Positions, cur: Index, dst: Index) -> Option<Cost> {
    if cur == dst {
        return Some(0);
    }
    seen.insert(cur);
    for &nxt in &NEIGHBOURS[cur] {
        if !pos[nxt].is_open() || seen.contains(&nxt) {
            continue;
        }
        if let Some(x) = dfs_(seen, pos, nxt, dst) {
            return Some(1 + x);
        }
    }
    None
}

fn djikstra(start: State) -> Option<State> {
    let mut dist = HashMap::new();
    let mut pq = BinaryHeap::new();

    dist.insert(start.clone(), 0);
    pq.push(start);

    while let Some(s) = pq.pop() {
        if s.is_final() {
            return Some(s);
        }
        for v in possible_moves(&s) {
            if v.cost < *dist.get(&v).unwrap_or(&usize::MAX) {
                dist.insert(v.clone(), v.cost);
                pq.push(v);
            }
        }
    }
    None
}

fn possible_moves(state: &State) -> Vec<State> {
    let mut moves = Vec::new();
    let pos = &state.positions;

    for (i, &amphi) in pos.iter().enumerate() {
        if amphi.is_open() {
            continue;
        }
        let room = DEST[amphi as usize];
        let n = room.len();

        // If the current position is in a room and everyone below is the same type,
        // we don't want to move.
        if (0..n).any(|j| i == room[j] && (j + 1..n).all(|k| pos[room[k]] == amphi)) {
            continue;
        }

        // We won't move in the hall if we're already there.
        if !HALL.contains(&i) {
            for &h in &HALL {
                if pos[h].is_open() && is_valid(pos, i, h) {
                    moves.push(do_move(state, i, h, amphi));
                }
            }
        }

        // We'll only enter a room if the spot doesn't havy any amphis from other types.
        // We also won't leave empty spaces below us.
        for j in 0..n {
            if pos[room[j]].is_open()
                && (j + 1..n).all(|k| pos[room[k]] == amphi)
                && is_valid(pos, i, room[j])
            {
                moves.push(do_move(state, i, room[j], amphi));
            }
        }
    }
    moves
}

fn dfs(pos: &Positions, cur: Index, dst: Index) -> Option<Cost> {
    dfs_(&mut HashSet::new(), pos, cur, dst)
}

fn print_game(s: &State) {
    let h = |n| "#".repeat(n);
    #[allow(unstable_name_collisions)]
    let p = |idxs: &[usize], sep: &str| -> String {
        idxs.iter()
            .map(|&i| s.positions[i].into())
            .intersperse(sep)
            .collect()
    };

    println!("Cost: {}", s.cost);
    println!("{}", h(13));
    let hall: Vec<_> = HALL
        .iter()
        .copied()
        .chain([2, 6, 10, 14].into_iter())
        .sorted()
        .collect();
    println!("{}{}{}", h(1), p(&hall, ""), h(1));
    let top = [3, 7, 11, 15];
    println!("{}{}{}", h(3), p(&top, "#"), h(3));

    let bot_rows = [[4, 8, 12, 16], [19, 21, 23, 25], [20, 22, 24, 26]];
    for row in bot_rows {
        println!("  {}{}{}", h(1), p(&row, "#"), h(1));
    }
    println!("  {}\n", h(9));
}

fn read_problem() -> State {
    let mut buf = String::new();
    stdin().read_to_string(&mut buf).unwrap();

    let mut lines: Vec<_> = buf.lines().skip(2).collect();
    lines.pop();
    let rows = lines.into_iter().map(|l| l.trim().replace("#", ""));

    let mut positions = [Amphi::O; 27];
    for (j, line) in rows.enumerate() {
        for (i, x) in line.char_indices() {
            let pos = if j < 2 {
                3 + 4 * i + j
            } else {
                19 + 2 * i + j - 2
            };
            positions[pos] = x.into();
        }
    }
    State::new(0, positions)
}

fn main() {
    let p = read_problem();
    print_game(&p);
    let d = djikstra(p).unwrap();
    print_game(&d);
}
