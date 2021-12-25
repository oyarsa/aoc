use memoize::memoize;

static FREQS: [(u64, u64); 7] = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)];

type Pair = [u64; 2];
#[derive(Clone, Debug, Hash, PartialEq, Eq)]
struct State {
    positions: Pair,
    scores: Pair,
}

impl State {
    fn new(positions: Pair, scores: Pair) -> Self {
        Self { positions, scores }
    }
}

fn vadd(a: Pair, b: Pair) -> Pair {
    [a[0] + b[0], a[1] + b[1]]
}

fn vmul(x: u64, b: Pair) -> Pair {
    [x * b[0], x * b[1]]
}

fn do_move(val: u64, p: usize, state: &State) -> State {
    let mut pos = state.positions;
    let mut sco = state.scores;
    pos[p] = (pos[p] + val - 1) % 10 + 1;
    sco[p] += pos[p];
    State::new(pos, sco)
}

fn part1(positions: Pair) -> u64 {
    let niter = 1000;
    let mut i = 0;
    let mut state = State::new(positions, [0, 0]);

    while state.scores[0] < niter && state.scores[1] < niter {
        let p = i % 2;
        let val = 3 * (3 * i + 1) + 3;
        state = do_move(val, p as usize, &state);
        i += 1;
    }

    let score = if state.scores[0] < niter {
        state.scores[0]
    } else {
        state.scores[1]
    };
    score * i * 3
}

#[memoize]
fn play(p: usize, state: State) -> Pair {
    if state.scores[0] >= 21 {
        return [1, 0];
    }
    if state.scores[1] >= 21 {
        return [0, 1];
    }
    let nextp = if p == 0 { 1 } else { 0 };
    let mut result = [0, 0];
    for &(val, freq) in FREQS.iter() {
        let played = play(nextp, do_move(val, p, &state));
        result = vadd(result, vmul(freq, played));
    }
    result
}

fn part2(positions: Pair) -> u64 {
    let [p1, p2] = play(0, State::new(positions, [0, 0]));
    u64::max(p1, p2)
}

fn main() {
    // let problem = [4, 8] // test
    let problem = [8, 4]; // input

    println!("Part 1: {}", part1(problem));
    println!("Part 2: {}", part2(problem));
}
